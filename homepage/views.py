from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from io import BytesIO  # type: ignore
import base64  # type: ignore
try:
    import matplotlib  # type: ignore
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt  # type: ignore
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

import json
import requests  # type: ignore
from datetime import datetime, timedelta
from django.http import JsonResponse  # type: ignore
from django.views.decorators.csrf import csrf_exempt  # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models.functions import TruncMonth  # type: ignore
from django.db.models import Sum  # type: ignore

from .models import FarmExpense  # type: ignore
from .utils.weather_api import (
    get_dashboard_weather, 
    _fetch_weather_from_coords, 
    get_realtime_weather, 
    get_realtime_weather_for_district, 
    get_7_day_weather_forecast, 
    WORLD_REGIONS
) # type: ignore
from .utils.crop_recommender import recommend_crop  # type: ignore
from .utils.market_api import get_daily_market_prices, get_historical_prices  # type: ignore
from .utils.disease_model import DISEASE_DB, compute_features, classify_plant_and_disease, HAS_ML_DEPS  # type: ignore

# --- DASHBOARD VIEWS ---

def Mainpage(request):    
    weather_info = get_dashboard_weather()
            
    # Calculate expense data for chart (last 6 months)
    today = datetime.now().date()
    six_months_ago = today - timedelta(days=180)
    
    # Group by month
    if request.user.is_authenticated:
        if request.user.is_superuser:
            expenses_query = FarmExpense.objects.filter(Expense_date__gte=six_months_ago)
        else:
            expenses_query = FarmExpense.objects.filter(user=request.user, Expense_date__gte=six_months_ago)
            
        expenses_query = expenses_query.annotate(month=TruncMonth('Expense_date')).values('month').annotate(
            total_sales=Sum('Crop_sale'),
            total_investment=Sum('Total_investment')
        ).order_by('month')
    else:
        expenses_query = []

    expense_labels, crop_sales_data, expenses_data = [], [], []
    for entry in expenses_query:
        if entry['month']:
            expense_labels.append(entry['month'].strftime('%b %Y'))
            crop_sales_data.append(float(entry['total_sales'] or 0))
            expenses_data.append(float(entry['total_investment'] or 0))
        
    if not expense_labels:
        expense_labels, crop_sales_data, expenses_data = ['No Data'], [0], [0]
    
    # Pie Chart Data
    seed_total, fert_total, labor_total, other_total = 0, 0, 0, 0
    if expenses_query:
        f_query = FarmExpense.objects.filter(Expense_date__gte=six_months_ago)
        if not request.user.is_superuser:
            f_query = f_query.filter(user=request.user)
        totals = f_query.aggregate(s=Sum('Seed_cost'), f=Sum('Fertilizer_cost'), l=Sum('Labor_cost'), o=Sum('Other_costs'))
        seed_total, fert_total, labor_total, other_total = float(totals['s'] or 0), float(totals['f'] or 0), float(totals['l'] or 0), float(totals['o'] or 0)

    # Bar Chart Data
    from .models import Retail_Crop_Sales, Retail_Egg_Sales, Retail_Milk_Sales, Retail_Machinery_Renting
    if request.user.is_superuser:
        r_crop = Retail_Crop_Sales.objects.aggregate(t=Sum('Total_Amount'))['t'] or 0
        r_egg = Retail_Egg_Sales.objects.aggregate(t=Sum('Total_Amount'))['t'] or 0
        r_milk = Retail_Milk_Sales.objects.aggregate(t=Sum('Total_Amount'))['t'] or 0
        r_mach = Retail_Machinery_Renting.objects.aggregate(t=Sum('Total_Amount'))['t'] or 0
    else:
        r_crop = Retail_Crop_Sales.objects.filter(user=request.user).aggregate(t=Sum('Total_Amount'))['t'] or 0
        r_egg = Retail_Egg_Sales.objects.filter(user=request.user).aggregate(t=Sum('Total_Amount'))['t'] or 0
        r_milk = Retail_Milk_Sales.objects.filter(user=request.user).aggregate(t=Sum('Total_Amount'))['t'] or 0
        r_mach = Retail_Machinery_Renting.objects.filter(user=request.user).aggregate(t=Sum('Total_Amount'))['t'] or 0

    # Payment Methods
    cash_t, card_t, upi_t, other_t = 0, 0, 0, 0
    for model in [Retail_Crop_Sales, Retail_Egg_Sales, Retail_Milk_Sales, Retail_Machinery_Renting]:
        qs = model.objects.all() if request.user.is_superuser else model.objects.filter(user=request.user)
        cash_t += qs.filter(Payment_Method='Cash').count()
        card_t += qs.filter(Payment_Method='Card').count()
        upi_t += qs.filter(Payment_Method='UPI').count()
        other_t += qs.filter(Payment_Method='Other').count()

    context = {
        "weather": weather_info,
        "expense_labels": json.dumps(expense_labels),
        "crop_sales_data": json.dumps(crop_sales_data),
        "expenses_data": json.dumps(expenses_data),
        "pie_chart_data": json.dumps([seed_total, fert_total, labor_total, other_total]),
        "bar_chart_data": json.dumps([float(r_crop), float(r_milk), float(r_egg), float(r_mach)]),
        "payment_chart_data": json.dumps([cash_t, card_t, upi_t, other_t]),
    }
    return render(request, "homepage/home.html", context)

def api_weather(request):
    lat, lon = request.GET.get('lat'), request.GET.get('lon')
    if lat and lon:
        try:
            city_name = "Your Location"
            geo_res = requests.get(f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en", timeout=5)
            if geo_res.status_code == 200:
                geo_data = geo_res.json()
                city_name = geo_data.get('locality') or geo_data.get('city') or geo_data.get('principalSubdivision') or "Your Location"
            weather = _fetch_weather_from_coords(lat, lon, city_name)
            if weather: return JsonResponse({'success': True, 'weather': weather})
        except Exception as e: print(f"Weather error: {e}")
    return JsonResponse({'success': False, 'error': 'Failed to fetch weather'})

@csrf_exempt
def crop_recommendation(request):
    recommendations = None
    if request.method == "POST":
        soil, season, water = request.POST.get("soil"), request.POST.get("season"), request.POST.get("water")
        if soil and season and water: recommendations = recommend_crop(soil, season, water)
    return render(request, "homepage/crop_recommendation.html", {"recommendations": recommendations, "submitted": request.method == "POST"})

def market_prices(request):
    prices = get_daily_market_prices()
    for p in prices:
        diff = float(p.get("difference", 0))
        p["is_increase"], p["is_neutral"] = diff > 0, diff == 0
    return render(request, "homepage/market_prices.html", {"prices": prices})

def api_historical_prices(request):
    crop = request.GET.get("crop")
    if crop: return JsonResponse({"success": True, "data": get_historical_prices(crop)})
    return JsonResponse({"success": False, "error": "No crop provided"})

@csrf_exempt
def analysis_dashboard(request): return render(request, 'homepage/analysis_dashboard.html')
@csrf_exempt
def production_dashboard(request): return render(request, 'homepage/production_dashboard.html')
@csrf_exempt
def reports_dashboard(request): return render(request, 'homepage/reports_dashboard.html')

@csrf_exempt
def crop_disease_analysis(request):
    result, error = None, None
    if request.method == "POST":
        if "image" not in request.FILES: error = "No image uploaded"
        else:
            f = request.FILES["image"]
            try:
                if not HAS_ML_DEPS: raise Exception("ML dependencies missing.")
                import numpy as np; import cv2; from PIL import Image
                file_bytes = np.frombuffer(f.read(), dtype=np.uint8)
                bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                if bgr is None:
                    f.seek(0); pil = Image.open(f).convert("RGB"); rgb = np.array(pil)
                else: rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                features = compute_features(rgb)
                plant, disease, confidence = classify_plant_and_disease(features, request.POST.get("plant_type"))
                info = DISEASE_DB.get(disease, {"curable":"Unknown","pesticide":"Unknown","prevention":"No data available."})
                result = {"plant": plant, "disease": disease.replace("_", " "), "confidence": confidence, "curable": info.get("curable"), "pesticide": info.get("pesticide"), "prevention": info.get("prevention"), "features": features}
            except Exception as e: error = f"Failed: {e}"
    return render(request, "homepage/crop_disease_analysis.html", {"result": result, "error": error})

def daily_climate(request):
    c, s, d = request.GET.get('country'), request.GET.get('state'), request.GET.get('district')
    if c and d:
        w = get_7_day_weather_forecast(c, s or "", d)
        if w: return render(request, 'homepage/daily_climate.html', {'weather_data': w, 'country': c, 'state': s, 'district': d, 'show_results': True})
    return render(request, 'homepage/daily_climate.html', {'country': c, 'state': s, 'district': d, 'show_results': False})

def settings_page(request): return render(request, 'homepage/settings.html')
def Help(request): return render(request, 'homepage/help.html')
@login_required
def profile_view(request): return render(request, 'homepage/profile.html')

# --- EMPLOYEES ---
from .employees_form import EmployeesForm, EmployeesCreationForm, EmployeesUpdateForm  # type: ignore
from .models import Employees  # type: ignore

def Show_employees(request):
    employees = Employees.objects.all() if request.user.is_superuser else Employees.objects.filter(user=request.user)
    return render(request, "homepage/showemployees.html", {"employees": employees})

def Add_employees(request):
    from django.contrib.auth.models import User
    if request.method == "POST":
        form = EmployeesCreationForm(request.POST)
        if form.is_valid():
            u, p = form.cleaned_data.get("employee_username"), form.cleaned_data.get("employee_password")
            if User.objects.filter(username=u).exists():
                form.add_error("employee_username", "Exists."); return render(request, "homepage/addemployees.html", {"form": form})
            new_u = User.objects.create_user(username=u, password=p); new_u.is_staff = True; new_u.save()
            emp = form.save(commit=False); emp.user = new_u; form.save()
            return redirect("homepage:show-employees")
    else: form = EmployeesCreationForm()
    return render(request, "homepage/addemployees.html", {"form": form})

def Delete_employees(request, Eid):
    emp = Employees.objects.get(Eid=Eid)
    if request.method == "POST": emp.delete(); return redirect("homepage:show-employees")
    return render(request, "homepage/deleteemployees.html", {"employees": emp})

def Update_employees(request, Eid):
    from django.contrib.auth.models import User
    emp = Employees.objects.get(Eid=Eid); u_obj = emp.user
    if request.method == 'POST':
        form = EmployeesUpdateForm(request.POST, instance=emp)
        if form.is_valid():
            u, p = form.cleaned_data.get("employee_username"), form.cleaned_data.get("employee_password")
            if u != u_obj.username and User.objects.filter(username=u).exists():
                form.add_error("username", "Exists"); return render(request, "homepage/updateemployees.html", {"form": form, "employees": emp})
            u_obj.username = u; 
            if p: u_obj.set_password(p)
            u_obj.save(); form.save()
            return redirect("homepage:show-employees")
    else: form = EmployeesUpdateForm(instance=emp, initial={'employee_username': u_obj.username})
    return render(request, "homepage/updateemployees.html", {"form": form, "employees": emp})

# --- CROPS ---
from .models import Crops, Crop_expenses, Crop_sales  # type: ignore
from .crops_form import CropsForm, Crop_expensesForm, Crop_salesForm  # type: ignore

def Show_crops(request):
    crops = Crops.objects.all() if request.user.is_superuser else Crops.objects.filter(user=request.user)
    return render(request, "homepage/showcrops.html", {"crops": crops})

def Add_crops(request):
    if request.method == "POST":
        form = CropsForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False); c.user = request.user; form.save(); return redirect("homepage:show-crops")
    else: form = CropsForm()
    return render(request, "homepage/addcrops.html", {"form": form})

def Update_crops(request, Cid):
    c = Crops.objects.get(Cid=Cid)
    if request.method == 'POST':
        form = CropsForm(request.POST, instance=c)
        if form.is_valid(): form.save(); return redirect("homepage:show-crops")
    else: form = CropsForm(instance=c)
    return render(request, "homepage/updatecrops.html", {"form": form, "crops": c})

def Delete_crops(request, Cid):
    c = Crops.objects.get(Cid=Cid)
    if request.method == "POST": c.delete(); return redirect("homepage:show-crops")
    return render(request, 'homepage/deletecrops.html', {'crops': c})

def Show_crop_expenses(request, Cid):
    c = get_object_or_404(Crops, Cid=Cid); exps = Crop_expenses.objects.filter(crops=c)
    return render(request, 'homepage/showcropexpenses.html', {'crops': c, 'expenses': exps})

def Add_crop_expenses(request, Cid):
    c = get_object_or_404(Crops, Cid=Cid)
    if request.method == 'POST':
        form = Crop_expensesForm(request.POST)
        if form.is_valid():
            ce = form.save(commit=False); ce.crops = c; ce.save(); return redirect('homepage:show-cropexpenses', Cid=c.Cid)
    else: form = Crop_expensesForm(); return render(request, 'homepage/addcropexpenses.html', {'form': form, 'crops': c})

def Update_crop_expenses(request, Cid, Expense_date):
    c = get_object_or_404(Crops, Cid=Cid); ce = get_object_or_404(Crop_expenses, crops__Cid=Cid, Expense_date=Expense_date)
    if request.method == 'POST':
        form = Crop_expensesForm(request.POST, instance=ce)
        if form.is_valid(): form.save(); return redirect('homepage:show-cropexpenses', Cid=ce.crops.Cid)
    else: form = Crop_expensesForm(instance=ce)
    return render(request, 'homepage/updatecropexpenses.html', {'form': form, 'crops': c, 'crop_expenses': ce})

def Delete_crop_expenses(request, Cid, Expense_date):
    ce = get_object_or_404(Crop_expenses, crops__Cid=Cid, Expense_date=Expense_date)
    if request.method == "POST": ce.delete(); return redirect('homepage:show-cropexpenses', Cid=ce.crops.Cid)
    return render(request, 'homepage/deletecropexpenses.html', {'crop_expenses': ce})

def Show_crop_sales(request, Cid):
    c = get_object_or_404(Crops, Cid=Cid); sales = Crop_sales.objects.filter(crops=c)
    return render(request, "homepage/showcropsales.html", {'crops': c, 'sales': sales})

def Add_crop_sales(request, Cid):
    c = get_object_or_404(Crops, Cid=Cid)
    if request.method == 'POST':
        form = Crop_salesForm(request.POST)
        if form.is_valid():
            cs = form.save(commit=False); cs.crops = c; cs.save()
            from .models import Retail_Crop_Sales; from decimal import Decimal; import re
            try:
                nums = re.findall(r"[-+]?\d*\.\d+|\d+", str(cs.Quantity_sold))
                qty = Decimal(nums[0]) if nums else Decimal('0.0')
            except: qty = Decimal('0.0')
            Retail_Crop_Sales.objects.create(user=c.user, Date=cs.Sale_date, Crop_Name=c.Crop_name, Quantity_Sold=qty, Unit_Price=cs.Unit_price, Customer_Name=cs.Buyer_information, Payment_Method=cs.Payment_method if cs.Payment_method in ['Cash', 'Card', 'UPI', 'Other'] else 'Cash')
            return redirect('homepage:show-cropsales', Cid=c.Cid)
    else: form = Crop_salesForm()
    return render(request, 'homepage/addcropsales.html', {'form': form, 'crops': c})

def Delete_crop_sales(request, Cid, Sale_date):
    cs = get_object_or_404(Crop_sales, crops__Cid=Cid, Sale_date=Sale_date)
    if request.method == 'POST': cs.delete(); return redirect('homepage:show-cropsales', Cid=cs.crops.Cid)
    return render(request, 'homepage/deletecropsales.html', {'crop_sales': cs})

def Update_crop_sales(request, Cid, Sale_date):
    c = get_object_or_404(Crops, Cid=Cid); cs = get_object_or_404(Crop_sales, crops__Cid=Cid, Sale_date=Sale_date)
    if request.method == 'POST':
        form = Crop_salesForm(request.POST, instance=cs)
        if form.is_valid(): form.save(); return redirect('homepage:show-cropsales', Cid=cs.crops.Cid)
    else: form = Crop_salesForm(instance=cs)
    return render(request, 'homepage/updatecropsales.html', {'form': form, 'crops': c, 'crop_sales': cs})

# --- MACHINERY ---
from .models import Machinery, Machinery_activities, Machinery_maintenance  # type: ignore
from .machinery_form import MachineryForm, Machinery_activitesForm, Machinery_maintenanceForm  # type: ignore

def Show_machinery(request):
    m = Machinery.objects.all() if request.user.is_superuser else Machinery.objects.filter(user=request.user)
    return render(request, "homepage/showmachinery.html", {'machinery': m})

def Add_machinery(request):
    if request.method == 'POST':
        form = MachineryForm(request.POST)
        if form.is_valid(): form.save(commit=False).user = request.user; form.save(); return redirect("homepage:show-machinery")
    else: form = MachineryForm()
    return render(request, "homepage/addmachinery.html", {"form": form})

def Delete_machinery(request, Number_plate):
    m = Machinery.objects.get(Number_plate=Number_plate)
    if request.method == "POST": m.delete(); return redirect("homepage:show-machinery")
    return render(request, "homepage/deletemachinery.html", {"machinery": m})

def Update_machinery(request, Number_plate):
    m = Machinery.objects.get(Number_plate=Number_plate)
    if request.method == 'POST':
        form = MachineryForm(request.POST, instance=m)
        if form.is_valid(): form.save(); return redirect("homepage:show-machinery")
    else: form = MachineryForm(instance=m)
    return render(request, "homepage/updatemachinery.html", {'form': form, 'machinery': m})

def Show_machinery_activities(request, Number_plate):
    m = get_object_or_404(Machinery, Number_plate=Number_plate); acts = Machinery_activities.objects.filter(machinery=m)
    return render(request, 'homepage/showmachineryactivities.html', {'machinery': m, 'activities': acts})

def Add_machinery_activities(request, Number_plate):
    m = get_object_or_404(Machinery, Number_plate=Number_plate)
    if request.method == 'POST':
        form = Machinery_activitesForm(request.POST)
        if form.is_valid():
            ma = form.save(commit=False); ma.machinery = m; ma.save()
            if ma.Activity_type.lower() in ["rent", "rented", "lease"]:
                from .models import Retail_Machinery_Renting; from decimal import Decimal
                Retail_Machinery_Renting.objects.create(user=m.user, Date=ma.Activity_date, Machinery_Used=m.Equipment_name, Service_Provided=ma.Description or "Rental", Hours_Rented=Decimal('1.0'), Rate_Per_Hour=Decimal(ma.Activity_cost or 0), Customer_Name="Farmer Sync")
            return redirect('homepage:show-machineryactivities', Number_plate=m.Number_plate)
    else: form = Machinery_activitesForm(); return render(request, 'homepage/addmachineryactivities.html', {'machinery': m, 'form': form})

def Delete_machinery_activity(request, Number_plate, Activity_date):
    ma = get_object_or_404(Machinery_activities, machinery__Number_plate=Number_plate, Activity_date=Activity_date)
    if request.method == 'POST': ma.delete(); return redirect('homepage:show-machineryactivities', Number_plate=ma.machinery.Number_plate)
    return render(request, 'homepage/deletemachineryactivities.html', {'machinery_activities': ma})

def Update_machinery_activities(request, Number_plate, Activity_date):
    m = get_object_or_404(Machinery, Number_plate=Number_plate); ma = get_object_or_404(Machinery_activities, machinery__Number_plate=Number_plate, Activity_date=Activity_date)
    if request.method == 'POST':
        form = Machinery_activitesForm(request.POST, instance=ma)
        if form.is_valid(): form.save(); return redirect('homepage:show-machineryactivities', Number_plate=ma.machinery.Number_plate)
    else: form = Machinery_activitesForm(instance=ma)
    return render(request, 'homepage/updatemachineryactivities.html', {'form': form, 'machinery': m, 'machinery_activities': ma})

def Show_machinery_maintenance(request, Number_plate):
    m = get_object_or_404(Machinery, Number_plate=Number_plate); maint = Machinery_maintenance.objects.filter(machinery=m)
    return render(request, 'homepage/showmachinerymaintenance.html', {'machinery': m, 'maintenance': maint})

def Add_machinery_maintenance(request, Number_plate):
    m = get_object_or_404(Machinery, Number_plate=Number_plate)
    if request.method == 'POST':
        form = Machinery_maintenanceForm(request.POST)
        if form.is_valid():
            mm = form.save(commit=False); mm.machinery = m; mm.save(); return redirect('homepage:show-machinerymaintenance', Number_plate=m.Number_plate)
    else: form = Machinery_maintenanceForm(); return render(request, 'homepage/addmachinerymaintenance.html', {'machinery': m, 'form': form})

def Delete_machinery_maintenance(request, Number_plate, Date):
    mm = get_object_or_404(Machinery_maintenance, machinery__Number_plate=Number_plate, Date=Date)
    if request.method == 'POST': mm.delete(); return redirect('homepage:show-machinerymaintenance', Number_plate=mm.machinery.Number_plate)
    return render(request, 'homepage/deletemachinerymaintenance.html', {'machinery_maintenance': mm})

def Update_machinery_maintenance(request, Number_plate, Date):
    m = get_object_or_404(Machinery, Number_plate=Number_plate); mm = get_object_or_404(Machinery_maintenance, machinery__Number_plate=Number_plate, Date=Date)
    if request.method == 'POST':
        form = Machinery_maintenanceForm(request.POST, instance=mm)
        if form.is_valid(): form.save(); return redirect('homepage:show-machinerymaintenance', Number_plate=mm.machinery.Number_plate)
    else: form = Machinery_maintenanceForm(instance=mm)
    return render(request, 'homepage/updatemachinerymaintenance.html', {'form': form, 'machinery': m, 'machinery_maintenance': mm})

# Livestock Views Removed

# --- MILK & EGGS ---
from .models import Milk_production, Eggs_production  # type: ignore
from .livestock_form import Milk_productionForm, Egg_productionForm  # type: ignore

def Select_year_month(request):
    if request.method == 'POST':
        vt, y, m = request.POST.get('view_type'), request.POST.get('Yearly_Year'), request.POST.get('Month')
        if vt == 'yearly': return redirect('homepage:milk-productionbyyear', selected_year=y)
        return redirect('homepage:milk-productionbymonth', selected_year=request.POST.get('Year'), selected_month=m)
    return render(request, 'homepage/selectyearmonth.html')

def Milk_production_today(request):
    t = datetime.now(); rs = Milk_production.objects.filter(Year=t.year, Month=t.month, Day=t.day)
    return render(request, 'homepage/milkproductiontoday.html', {'selected_year': t.year, 'selected_month': t.month, 'selected_day': t.day, 'milk_production_records': rs})

def Milk_production_by_year(request, selected_year):
    md = Milk_production.objects.filter(Year=selected_year).values('Month').annotate(tp=Sum('Total_production'), tc=Sum('Total_consumption')).order_by('Month')
    ms, tp, tc = [d['Month'] for d in md], [float(d['tp'] or 0) for d in md], [float(d['tc'] or 0) for d in md]
    img_c, img_p = "", ""
    if HAS_MATPLOTLIB and ms:
        plt.figure(figsize=(10, 4)); plt.bar(ms, tc, color='green'); plt.title('Consumption'); plt.xticks(ms)
        buf = BytesIO(); plt.savefig(buf, format='png'); buf.seek(0); img_c = base64.b64encode(buf.read()).decode('utf-8'); plt.close()
        plt.figure(figsize=(10, 4)); plt.bar(ms, tp, color='blue'); plt.title('Production'); plt.xticks(ms)
        buf = BytesIO(); plt.savefig(buf, format='png'); buf.seek(0); img_p = base64.b64encode(buf.read()).decode('utf-8'); plt.close('all')
    return render(request, 'homepage/milkproductionbyyear.html', {'selected_year': selected_year, 'monthly_data': md, 'image_base64_consumption': img_c, 'image_base64_production': img_p})

def Milk_production_by_month(request, selected_year, selected_month):
    rs = Milk_production.objects.filter(Year=selected_year, Month=selected_month); ds = [r.Day for r in rs]; tc = [r.Total_consumption for r in rs]; tp = [r.Total_production for r in rs]
    img_c, img_p = "", ""
    if HAS_MATPLOTLIB and ds:
        plt.figure(figsize=(10, 4)); plt.bar(ds, tc, color='green'); plt.title('Consumption'); buf = BytesIO(); plt.savefig(buf, format='png'); buf.seek(0); img_c = base64.b64encode(buf.read()).decode('utf-8'); plt.close()
        plt.figure(figsize=(10, 4)); plt.bar(ds, tp, color='blue'); plt.title('Production'); buf = BytesIO(); plt.savefig(buf, format='png'); buf.seek(0); img_p = base64.b64encode(buf.read()).decode('utf-8'); plt.close('all')
    return render(request, 'homepage/milkproductionbymonth.html', {'selected_year': selected_year, 'selected_month': selected_month, 'image_base64_consumption': img_c, 'image_base64_production': img_p, 'milk_production_records': rs})

def Add_milk_production_by_month(request, selected_year, selected_month):
    if request.method == 'POST':
        form = Milk_productionForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False); rd = form.cleaned_data.get('Record_date')
            if rd: p.Year, p.Month, p.Day = rd.year, rd.month, rd.day
            else: p.Year, p.Month, p.Day = selected_year, selected_month, 1
            p.save(); return redirect('homepage:milk-productionbymonth', selected_year=p.Year, selected_month=p.Month)
    else: form = Milk_productionForm()
    return render(request, 'homepage/addmilkproduction.html', {'form': form, 'selected_year': selected_year, 'selected_month': selected_month})

def Delete_milk_production_by_month(request, selected_year, selected_month, Day):
    r = get_object_or_404(Milk_production, Day=Day, Year=selected_year, Month=selected_month)
    if request.method == 'POST': r.delete(); return redirect('homepage:milk-productionbymonth', selected_year=selected_year, selected_month=selected_month)
    return render(request, 'homepage/deletemilkproduction.html', {'milk_production_records': r, 'selected_year': selected_year, 'selected_month': selected_month})

def Update_milk_production_by_month(request, selected_year, selected_month, Day):
    r = get_object_or_404(Milk_production, Day=Day, Year=selected_year, Month=selected_month)
    if request.method == 'POST':
        form = Milk_productionForm(request.POST, instance=r)
        if form.is_valid():
            rd = form.cleaned_data.get('Record_date')
            if rd: r.Year, r.Month, r.Day = rd.year, rd.month, rd.day
            r.save(); return redirect('homepage:milk-productionbymonth', selected_year=r.Year, selected_month=r.Month)
    else: form = Milk_productionForm(instance=r)
    return render(request, 'homepage/updatemilkproduction.html', {'form': form, 'milk_production_record': r, 'selected_year': selected_year, 'selected_month': selected_month})

def Select_year_month_egg(request):
    if request.method == 'POST':
        vt, y, m = request.POST.get('view_type'), request.POST.get('Yearly_Year'), request.POST.get('Month')
        if vt == 'yearly': return redirect('homepage:egg-productionbyyear', selected_year=y)
        return redirect('homepage:egg-productionrecord', selected_year=request.POST.get('Year'), selected_month=m)
    return render(request, 'homepage/selectingyearandmonth.html')

def Egg_production_today(request):
    t = datetime.now(); rs = Eggs_production.objects.filter(Year=t.year, Month=t.month, Day=t.day)
    return render(request, 'homepage/eggproductiontoday.html', {'selected_year': t.year, 'selected_month': t.month, 'selected_day': t.day, 'egg_production_records': rs})

def Egg_production_by_year(request, selected_year):
    md = Eggs_production.objects.filter(Year=selected_year).values('Month').annotate(tp=Sum('Total_egg_collection'), tc=Sum('Total_feeds')).order_by('Month')
    ms, tp, tc = [d['Month'] for d in md], [float(d['tp'] or 0) for d in md], [float(d['tc'] or 0) for d in md]
    img_c, img_p = "", ""
    if HAS_MATPLOTLIB and ms:
        plt.figure(figsize=(10, 4)); plt.bar(ms, tc, color='green'); plt.title('Feeds'); buf = BytesIO(); plt.savefig(buf, format='png'); buf.seek(0); img_c = base64.b64encode(buf.read()).decode('utf-8'); plt.close()
        plt.figure(figsize=(10, 4)); plt.bar(ms, tp, color='blue'); plt.title('Eggs'); buf = BytesIO(); plt.savefig(buf, format='png'); buf.seek(0); img_p = base64.b64encode(buf.read()).decode('utf-8'); plt.close('all')
    return render(request, 'homepage/eggproductionbyyear.html', {'selected_year': selected_year, 'monthly_data': md, 'image_base64_consumption': img_c, 'image_base64_production': img_p})

def Egg_production_record(request, selected_year, selected_month):
    rs = Eggs_production.objects.filter(Year=selected_year, Month=selected_month)
    return render(request, 'homepage/showeggproduction.html', {'egg_production_records': rs, 'selected_year': selected_year, 'selected_month': selected_month})

def Add_egg_production_by_month(request, selected_year, selected_month):
    if request.method == 'POST':
        form = Egg_productionForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False); rd = form.cleaned_data.get('Record_date')
            if rd: p.Year, p.Month, p.Day = rd.year, rd.month, rd.day
            else: p.Year, p.Month, p.Day = selected_year, selected_month, 1
            p.save(); return redirect('homepage:egg-productionrecord', selected_year=p.Year, selected_month=p.Month)
    else: form = Egg_productionForm()
    return render(request, 'homepage/addeggproduction.html', {'form': form, 'selected_year': selected_year, 'selected_month': selected_month})

def Delete_egg_production_by_month(request, selected_year, selected_month, Day):
    r = get_object_or_404(Eggs_production, Day=Day, Year=selected_year, Month=selected_month)
    if request.method == 'POST': r.delete(); return redirect('homepage:egg-productionrecord', selected_year=selected_year, selected_month=selected_month)
    return render(request, 'homepage/deleteeggproduction.html', {'egg_production_records': r, 'selected_year': selected_year, 'selected_month': selected_month})

def Update_egg_production_by_month(request, selected_year, selected_month, Day):
    r = get_object_or_404(Eggs_production, Day=Day, Year=selected_year, Month=selected_month)
    if request.method == 'POST':
        form = Egg_productionForm(request.POST, instance=r)
        if form.is_valid():
            rd = form.cleaned_data.get('Record_date')
            if rd: r.Year, r.Month, r.Day = rd.year, rd.month, rd.day
            r.save(); return redirect('homepage:egg-productionrecord', selected_year=r.Year, selected_month=r.Month)
    else: form = Egg_productionForm(instance=r)
    return render(request, 'homepage/updateeggproduction.html', {'form': form, 'egg_production_record': r, 'selected_year': selected_year, 'selected_month': selected_month})

# --- OTHERS ---
@csrf_exempt
def climate_analysis(request):
    c, s, d = request.GET.get('country'), request.GET.get('state'), request.GET.get('district')
    cl_data, show = None, False
    
    # Lists for dropdown population
    states_list = []
    districts_list = []
    
    if c:
        states_list = list(WORLD_REGIONS.get(c, {}).keys())
    if c and s:
        districts_list = list(WORLD_REGIONS.get(c, {}).get(s, {}).keys())
        
    if c and d:
        cl_data = get_7_day_weather_forecast(c, s or "", d)
        if cl_data: show = True
        
    return render(request, "homepage/climate_analysis.html", {
        "climate_data": cl_data, 
        "show_climate_results": show, 
        "country": c, 
        "state": s, 
        "district": d, 
        "WORLD_REGIONS": WORLD_REGIONS,
        "states_list": states_list,
        "districts_list": districts_list
    })

@login_required
def manage_contact(request):
    if not (request.user.is_superuser or request.user.is_staff): return redirect('homepage:mainpage')
    from homepage.models import ContactDetail
    contact = ContactDetail.objects.first() or ContactDetail.objects.create()
    if request.method == 'POST':
        contact.phone, contact.email, contact.address = request.POST.get('phone'), request.POST.get('email'), request.POST.get('address')
        contact.save(); from django.contrib import messages; messages.success(request, "Contact updated."); return redirect('homepage:mainpage')
    return render(request, 'homepage/manage_contact.html', {'contact': contact})
