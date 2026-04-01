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


from .utils.weather_api import get_dashboard_weather, _fetch_weather_from_coords  # type: ignore
from .utils.crop_recommender import recommend_crop  # type: ignore
from .utils.market_api import get_daily_market_prices, get_historical_prices  # type: ignore
import requests  # type: ignore
from django.http import JsonResponse  # type: ignore
from django.views.decorators.csrf import csrf_exempt  # type: ignore

# Create your views here.
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import FarmExpense

def Mainpage(request):
    weather_info = get_dashboard_weather()
    
    # Calculate expense data for chart (last 6 months)
    today = datetime.now().date()
    six_months_ago = today - timedelta(days=180)
    
    import json
    
    # Group by month
    if request.user.is_authenticated:
        expenses_query = FarmExpense.objects.filter(
            user=request.user, 
            Expense_date__gte=six_months_ago
        ).annotate(
            month=TruncMonth('Expense_date')
        ).values('month').annotate(
            total_sales=Sum('Crop_sale'),
            total_investment=Sum('Total_investment')
        ).order_by('month')
    else:
        expenses_query = []

    # Prepare data arrays for the chart
    expense_labels = []
    crop_sales_data = []
    expenses_data = []
    
    # Fill in grouped data
    for entry in expenses_query:
        if entry['month']:
            month_label = entry['month'].strftime('%b %Y') # 'Jan 2026'
            expense_labels.append(month_label)
            crop_sales_data.append(float(entry['total_sales'] or 0))
            expenses_data.append(float(entry['total_investment'] or 0))
        
    # If no data, provide fallbacks
    if not expense_labels:
        expense_labels = ['No Data']
        crop_sales_data = [0]
        expenses_data = [0]

    context = {
        "weather": weather_info,
        "expense_labels": json.dumps(expense_labels),
        "crop_sales_data": json.dumps(crop_sales_data),
        "expenses_data": json.dumps(expenses_data),
    }

    return render(request, "homepage/home.html", context)

def api_weather(request):
    """API endpoint to fetch weather for specific lat/lon from frontend Geolocation."""
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if lat and lon:
        try:
            # Try to reverse geocode the coordinates to get the city name
            city_name = "Your Location"
            geo_url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en"
            geo_res = requests.get(geo_url, timeout=5)
            if geo_res.status_code == 200:
                geo_data = geo_res.json()
                # Prefer locality, then city, then principal subdivision (state)
                city_name = geo_data.get('locality') or geo_data.get('city') or geo_data.get('principalSubdivision') or "Your Location"
            
            weather = _fetch_weather_from_coords(lat, lon, city_name)
            if weather:
                return JsonResponse({'success': True, 'weather': weather})
        except Exception as e:
            print(f"Error in api_weather view: {e}")
            
    return JsonResponse({'success': False, 'error': 'Could not fetch weather data'})

# --- New Modules --- #

@csrf_exempt
def crop_recommendation(request):
    """View for the Crop Recommendation Module."""
    recommendations = None
    if request.method == "POST":
        soil = request.POST.get("soil")
        season = request.POST.get("season")
        water = request.POST.get("water")
        
        if soil and season and water:
            recommendations = recommend_crop(soil, season, water)
            
    return render(request, "homepage/crop_recommendation.html", {
        "recommendations": recommendations,
        "submitted": request.method == "POST"
    })

def market_prices(request):
    """View for the Market Price Analysis Dashboard."""
    prices = get_daily_market_prices()
    
    # Check differences to assign trends
    for p in prices:
        diff = float(p.get("difference", 0))
        p["is_increase"] = diff > 0
        p["is_neutral"] = diff == 0
        
    return render(request, "homepage/market_prices.html", {"prices": prices})

def api_historical_prices(request):
    """API Endpoint to fetch 7-day historical price data for Chart.js."""
    crop = request.GET.get("crop")
    if crop:
        data = get_historical_prices(crop)
        return JsonResponse({"success": True, "data": data})
    return JsonResponse({"success": False, "error": "No crop provided"})


from .utils.weather_api import get_realtime_weather, get_realtime_weather_for_district, INDIA_REGIONS  # type: ignore

def daily_climate(request):
    """
    Renders the Daily Climate Tracker dashboard.
    Shows search UI if Country/State/District not selected, else shows real-time weather data.
    """
    country = request.GET.get('country')
    state = request.GET.get('state')
    district = request.GET.get('district')
    
    states_list = sorted(list(INDIA_REGIONS.keys()))
    districts_list = []
    
    if state and state in INDIA_REGIONS:
        districts_list = sorted(list(INDIA_REGIONS[state].keys()))
    
    if country == 'India' and state in INDIA_REGIONS and district in districts_list:
        weather_info = get_realtime_weather_for_district(state, district)
        return render(request, 'homepage/daily_climate.html', {
            'weather_data': weather_info,
            'country': country,
            'state': state,
            'district': district,
            'states_list': states_list,
            'districts_list': districts_list,
            'show_results': True
        })
    else:
        return render(request, 'homepage/daily_climate.html', {
            'country': country,
            'state': state,
            'district': district,
            'states_list': states_list,
            'districts_list': districts_list,
            'show_results': False
        })


# views for the employees
from .employees_form import EmployeesForm  # type: ignore
from .models import Employees  # type: ignore


def Show_employees(request):
    employees = Employees.objects.filter(user=request.user)

    return render(request, "homepage/showemployees.html", {"employees": employees})


def Add_employees(request):
    if request.method == "POST":
        form = EmployeesForm(request.POST)
        if form.is_valid():
            employees = form.save(commit=False)
            employees.user = request.user

            form.save()

            return redirect("homepage:show-employees")

    else:
        form = EmployeesForm()
    return render(request, "homepage/addemployees.html", {"form": form})


def Delete_employees(request, Eid):
    employees = Employees.objects.get(Eid=Eid)
    if request.method == "POST":
        employees.delete()
        return redirect("homepage:show-employees")

    return render(request, "homepage/deleteemployees.html", {"employees": employees})


def Update_employees(request, Eid):
    employees = Employees.objects.get(Eid=Eid)
    if request.method == 'POST':
        form = EmployeesForm(request.POST, instance=employees)
        if form.is_valid():
            form.save()
            return redirect("homepage:show-employees")
    else:
        form = EmployeesForm(instance=employees)
    return render(request, "homepage/updateemployees.html", {"form": form, "employees": employees})


# views for crops
from .models import Crops,Crop_expenses,Crop_sales,Crop_operations  # type: ignore
from .crops_form import CropsForm,Crop_expensesForm,Crop_salesForm,Crop_operationsForm  # type: ignore


def Show_crops(request):
    crops = Crops.objects.filter(user=request.user)

    return render(request, "homepage/showcrops.html", {"crops": crops})


def Add_crops(request):
    if request.method == "POST":
        form = CropsForm(request.POST)
        if form.is_valid():
            crops = form.save(commit=False)
            crops.user = request.user
            form.save()

            return redirect("homepage:show-crops")
    else:
        form = CropsForm()

    return render(request, "homepage/addcrops.html", {"form": form})


def Update_crops(request, Cid):
    crops = Crops.objects.get(Cid=Cid)
    if request.method == 'POST':
        form = CropsForm(request.POST, instance=crops)
        if form.is_valid():
            form.save()
            return redirect("homepage:show-crops")
    else:
        form = CropsForm(instance=crops)
    return render(request, "homepage/updatecrops.html", {"form": form, "crops": crops})

def Delete_crops (request,Cid):
    crops=Crops.objects.get(Cid=Cid)
    if request.method =="POST":
        crops.delete()
        return redirect("homepage:show-crops")
    
    return render(request,'homepage/deletecrops.html', {'crops':crops})

def Show_crop_expenses(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)
    expenses=Crop_expenses.objects.filter(crops=crops)

    return render(request,'homepage/showcropexpenses.html',{'crops':crops,'expenses':expenses})

def Add_crop_expenses(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)

    if request.method=='POST':
        form=Crop_expensesForm(request.POST)
        if form.is_valid():
            crop_expense=form.save(commit=False)
            crop_expense.crops=crops
            crop_expense.save()
            return redirect('homepage:show-cropexpenses', Cid=crops.Cid)
        
    else:
        form = Crop_expensesForm()
        return render(request,'homepage/addcropexpenses.html',{'form':form, 'crops':crops})
    

def Update_crop_expenses(request,Cid,Expense_date):
    crops=get_object_or_404(Crops,Cid=Cid)
    crop_expenses=get_object_or_404(Crop_expenses,crops__Cid=Cid,Expense_date=Expense_date)
    if request.method == 'POST':
        form=Crop_expensesForm(request.POST,instance=crop_expenses)
        if form.is_valid():
            form.save()
            return redirect('homepage:show-cropexpenses',Cid=crop_expenses.crops.Cid)
    else:
        form=Crop_expensesForm(instance=crop_expenses)
    return render(request,'homepage/updatecropexpenses.html',{'form':form,'crops':crops,'crop_expenses':crop_expenses})

def Delete_crop_expenses(request,Cid,Expense_date):
    crop_expenses=get_object_or_404(Crop_expenses, crops__Cid=Cid,Expense_date=Expense_date)
    if request.method=="POST":
        Crop_expenses.delete()
        return redirect('homepage:show-cropexpenses ',Cid=crop_expenses.crops.Cid)
    
    return render(request,'homepage/deletecropexpenses.html',{'crop_expenses':crop_expenses})
    

def Show_crop_sales(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)
    sales=Crop_sales.objects.filter(crops=crops)

    return render(request,"homepage/showcropsales.html",{'crops':crops,'sales':sales})

def Add_crop_sales(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)

    if request.method =='POST':
        form=Crop_salesForm(request.POST)
        if form.is_valid():
            crop_sale=form.save(commit=False)
            crop_sale.crops=crops
            crop_sale.save()
            return redirect('homepage:show-cropsales', Cid=crops.Cid)
        
    else:
        form=Crop_salesForm()
    return render(request,'homepage/addcropsales.html', {'form':form, 'crops':crops})
    

def Delete_crop_sales(request,Cid,Sale_date):
    crop_sales=get_object_or_404(Crop_sales,crops__Cid=Cid,Sale_date=Sale_date)

    if request.method=='POST':
        crop_sales.delete()
        return redirect('homepage:show-cropsales', Cid=crop_sales.crops.Cid)
    return render(request,'homepage/deletecropsales.html',{'crop_sales':crop_sales})

def Update_crop_sales(request,Cid,Sale_date):
    crops= get_object_or_404(Crops,Cid=Cid)
    crop_sales=get_object_or_404(Crop_sales,crops__Cid=Cid,Sale_date=Sale_date)
    if request.method == 'POST':
        form=Crop_salesForm(request.POST,instance=crop_sales)
        if form.is_valid():
            form.save()
            return redirect('homepage:show-cropsales', Cid=crop_sales.crops.Cid)
    else:
        form=Crop_salesForm(instance=crop_sales)
    return render(request,'homepage/updatecropsales.html',{'form':form,'crops':crops,'crop_sales':crop_sales})

def Show_crop_operations(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)
    operations=Crop_operations.objects.filter(crops=crops)

    return render(request,'homepage/showcropoperations.html',{'crops':crops, 'operations':operations})

def Add_crop_operations(request,Cid):
    crops=get_object_or_404(Crops,Cid=Cid)

    if request.method=='POST':
        form=Crop_operationsForm(request.POST)
        if form.is_valid():
            crop_operation=form.save(commit=False)
            crop_operation.crops=crops
            crop_operation.save()
            return redirect('homepage:show-cropoperations',Cid=crops.Cid)
    else:
        form=Crop_operationsForm()
        return render(request, 'homepage/addcropoperations.html',{'form':form,'crops':crops})

def Delete_crop_operations(request,Cid,Operation_date):
    crop_operations=get_object_or_404(Crop_operations,crops__Cid=Cid,Operation_date=Operation_date)
    if request.method=='POST':
        crop_operations.delete()
        return redirect('homepage:show-cropoperations',Cid=crop_operations.crops.Cid)
    
    return render(request, 'homepage/deletecropoperations.html',{'crop_operations':crop_operations})


def Update_crop_operations(request,Cid,Operation_date):
    crops= get_object_or_404(Crops,Cid=Cid)
    crop_operations=get_object_or_404(Crop_operations,crops__Cid=Cid,Operation_date=Operation_date)
    if request.method == 'POST':
        form = Crop_operationsForm(request.POST,instance=crop_operations)
        if form.is_valid():
            form.save()
            return redirect('homepage:show-cropoperations',Cid=crop_operations.crops.Cid)
    else:
        form = Crop_operationsForm(instance=crop_operations)
    return render(request,'homepage/updatecropoperations.html',{'form':form,'crops':crops,'crop_operations':crop_operations})
    
    
    

#views for the Machinery

from .models import Machinery,Machinery_activities,Machinery_maintenance  # type: ignore
from .machinery_form import MachineryForm,Machinery_activitesForm,Machinery_maintenanceForm  # type: ignore

def Show_machinery(request):
    machinery = Machinery.objects.filter(user=request.user)

    return render(request, "homepage/showmachinery.html", {'machinery':machinery})


def Add_machinery(request):
    if request.method=='POST':
        form = MachineryForm(request.POST)
        if form.is_valid():
            machinery= form.save(commit=False)
            machinery.user =request.user
            form.save()
            return redirect("homepage:show-machinery")
        
    else:
        form = MachineryForm()

        return render(request,"homepage/addmachinery.html", {"form":form})


def Delete_machinery(request,Number_plate):
    machinery=Machinery.objects.get(Number_plate=Number_plate)
    if request.method=="POST":
        machinery.delete()
        return redirect("homepage:show-machinery")
        
    return render(request,"homepage/deletemachinery.html", {"machinery":machinery})


def Update_machinery(request,Number_plate):
    machinery=Machinery.objects.get(Number_plate=Number_plate)
    if request.method == 'POST':
        form = MachineryForm(request.POST, instance=machinery)
        if form.is_valid():
            form.save()
            return redirect("homepage:show-machinery")
    else:
        form = MachineryForm(instance=machinery)
    return render(request, "homepage/updatemachinery.html", {'form':form,'machinery':machinery})


def Show_machinery_activities(request,Number_plate):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)
    activities=Machinery_activities.objects.filter(machinery=machinery)
    return render(request, 'homepage/showmachineryactivities.html',{'machinery':machinery,'activities':activities})

def Add_machinery_activities(request,Number_plate):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)

    if request.method=='POST':
        form=Machinery_activitesForm(request.POST)
        if form.is_valid():
            machinery_activity=form.save(commit=False)
            machinery_activity.machinery=machinery
            machinery_activity.save()
            return redirect('homepage:show-machineryactivities', Number_plate=machinery.Number_plate)
        

    else:
        form=Machinery_activitesForm()
    return render(request, 'homepage/addmachineryactivities.html',{'machinery':machinery,'form':form})

def Delete_machinery_activity(request,Number_plate,Activity_date):
    machinery_activities=get_object_or_404(Machinery_activities,machinery__Number_plate=Number_plate,Activity_date=Activity_date)
    if request.method=='POST':
        machinery_activities.delete()
        return redirect('homepage:show-machineryactivities',Number_plate=machinery_activities.machinery.Number_plate)
    
    return render(request,'homepage/deletemachineryactivities.html',{'machinery_activities':machinery_activities})


def Update_machinery_activities(request,Number_plate,Activity_date):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)
    machinery_activities=get_object_or_404(Machinery_activities,machinery__Number_plate=Number_plate,Activity_date=Activity_date)
    if request.method == 'POST':
        form=Machinery_activitesForm(request.POST,instance=machinery_activities)
        if form.is_valid():
            form.save()
            return redirect('homepage:show-machineryactivities',Number_plate=machinery_activities.machinery.Number_plate)
    else:
        form=Machinery_activitesForm(instance=machinery_activities)
    return render(request,'homepage/updatemachineryactivities.html',{'form':form,'machinery':machinery,'machinery_activities':machinery_activities})

def Show_machinery_maintenance(request,Number_plate):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)
    maintenance=Machinery_maintenance.objects.filter(machinery=machinery)
    return render(request,'homepage/showmachinerymaintenance.html',{'machinery':machinery,'maintenance':maintenance})

def Add_machinery_maintenance(request,Number_plate):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)

    if request.method=='POST':
        form=Machinery_maintenanceForm(request.POST)
        if form.is_valid():
            machinery_maintenance=form.save(commit=False)
            machinery_maintenance.machinery=machinery
            machinery_maintenance.save()
            return redirect('homepage:show-machinerymaintenance',Number_plate=machinery.Number_plate)
        
    else:
        form=Machinery_maintenanceForm()
    return render(request, 'homepage/addmachinerymaintenance.html',{'machinery':machinery,'form':form})

def Delete_machinery_maintenance(request,Number_plate,Date):
    machinery_maintenance=get_object_or_404(Machinery_maintenance,machinery__Number_plate=Number_plate,Date=Date)
    if request.method=='POST':
        machinery_maintenance.delete()
        return redirect('homepage:show-machinerymaintenance',Number_plate=machinery_maintenance.machinery.Number_plate)
    
    return render(request,'homepage/deletemachinerymaintenance.html',{'machinery_maintenance':machinery_maintenance})


def Update_machinery_maintenance(request,Number_plate,Date):
    machinery=get_object_or_404(Machinery,Number_plate=Number_plate)
    machinery_maintenance=get_object_or_404(Machinery_maintenance,machinery__Number_plate=Number_plate,Date=Date)
    if request.method == 'POST':
        form=Machinery_maintenanceForm(request.POST,instance=machinery_maintenance)
        if form.is_valid():
            form.save()
            return redirect('homepage:show-machinerymaintenance',Number_plate=machinery_maintenance.machinery.Number_plate)
    else:
        form=Machinery_maintenanceForm(instance=machinery_maintenance)
    return render(request,'homepage/updatemachinerymaintenance.html',{'form':form,'machinery':machinery,'machinery_maintenance':machinery_maintenance})
    


#view function of the livestock section
from .livestock_form import LivestockForm,Livestock_productionForm,Milk_productionForm,Egg_productionForm  # type: ignore
from .models import Livestock,Livestock_production,Milk_production,Eggs_production  # type: ignore
from django.shortcuts import render, get_object_or_404  # type: ignore

def Show_livestock(request):
    livestock = Livestock.objects.filter(user=request.user)

    return render(request,"homepage/showlivestock.html", {'livestock':livestock})


def Add_livestock(request):
    if request.method=="POST":
        form=LivestockForm(request.POST)
        if form.is_valid():
            livestock=form.save(commit=False)
            livestock.user = request.user

            form.save()

            return redirect("homepage:show-livestock")
        
    else:
        form = LivestockForm()
        return render(request,"homepage/addlivestock.html", {'form':form})
    

def Update_livestock(request,Tag_number):
    livestock=Livestock.objects.get(Tag_number=Tag_number)
    if request.method == 'POST':
        form = LivestockForm(request.POST,instance=livestock)
        if form.is_valid():
            form.save()
            return redirect("homepage:show-livestock")
    else:
        form = LivestockForm(instance=livestock)
    return render(request,"homepage/updatelivestock.html",{'form':form,'livestock':livestock})

def Delete_livestock(request,Tag_number):
    livestock=Livestock.objects.get(Tag_number=Tag_number)
    if request.method=="POST":
        livestock.delete()
        return redirect("homepage:show-livestock")
    
    return render(request, "homepage/deletelivestock.html", {'livestock':livestock})

def Show_livestock_production(request, Tag_number):
    livestock = get_object_or_404(Livestock, Tag_number=Tag_number)
    productions = Livestock_production.objects.filter(livestock=livestock)

    return render(request, 'homepage/showlivestockproduction.html', {'livestock': livestock, 'productions': productions})


def Add_livestock_production(request, Tag_number):
    livestock = get_object_or_404(Livestock, Tag_number=Tag_number)

    if request.method == 'POST':
        form = Livestock_productionForm(request.POST)
        if form.is_valid():
            livestock_production = form.save(commit=False)
            livestock_production.livestock = livestock
            livestock_production.save()
            return redirect('homepage:show-livestockproduction', Tag_number=livestock.Tag_number)
    else:
        form = Livestock_productionForm()

        return render(request, 'homepage/addlivestockproduction.html', {'form': form, 'livestock': livestock})
    

def Delete_livestock_production(request,Tag_number,Production_date):
    livestock_production = get_object_or_404(Livestock_production,livestock__Tag_number=Tag_number,Production_date=Production_date)
    if request.method=="POST":
        livestock_production.delete()
        return redirect("homepage:show-livestockproduction",  Tag_number=livestock_production.livestock.Tag_number)
    
    return render(request, 'homepage/deletelivestockproduction.html',{'livestock_production':livestock_production})

def Update_livestock_production(request,Tag_number,Production_date):
    livestock=get_object_or_404(Livestock,Tag_number=Tag_number)
    livestock_production=get_object_or_404(Livestock_production,livestock__Tag_number=Tag_number,Production_date=Production_date)
    if request.method == 'POST':
        form=Livestock_productionForm(request.POST,instance=livestock_production)
        if form.is_valid():
            form.save()
            return redirect('homepage:show-livestockproduction', Tag_number=livestock_production.livestock.Tag_number)
    else:
        form=Livestock_productionForm(instance=livestock_production)
    return render(request,'homepage/updatelivestockproduction.html',{'form':form,'livestock':livestock, 'livestock_production':livestock_production})



# the milk production section in the dashboard

def Select_year_month(request):
    if request.method=='POST':
        selected_year=request.POST.get('Year')
        selected_month=request.POST.get('Month')
        return redirect('homepage:milk-productionbymonth',selected_year=selected_year,selected_month=selected_month)
    return render(request,'homepage/selectyearmonth.html')

# views.py
# Matplotlib rendering handled at top of file

def Milk_production_by_month(request, selected_year, selected_month):
    # Fetching milk production by the year and month selected
    milk_production_records = Milk_production.objects.filter(Year=selected_year, Month=selected_month)

    # Prepare data for the bar graph of total consumption vs day
    days = [record.Day  for record in milk_production_records]
    total_consumption = [record.Total_consumption for record in milk_production_records]

    # Create a bar graph for Total Consumption vs Day
    if HAS_MATPLOTLIB:
        plt.figure(figsize=(12, 6))
        plt.bar(days, total_consumption, color='green')
        plt.title('Total Consumption vs Day')
        plt.xlabel('Day')
        plt.ylabel('Total Consumption')
    
    # Save the plot to a BytesIO object
    image_stream_consumption = BytesIO()
    if HAS_MATPLOTLIB:
        plt.savefig(image_stream_consumption, format='png')
    image_stream_consumption.seek(0)
    image_base64_consumption = base64.b64encode(image_stream_consumption.read()).decode('utf-8')

    # Close the plot to free up resources
    if HAS_MATPLOTLIB:
        plt.close()

    # Prepare data for the bar graph of milk production vs day
    total_production = [record.Total_production for record in milk_production_records]

    # Create a bar graph for Milk Production vs Day
    if HAS_MATPLOTLIB:
        plt.figure(figsize=(12, 6))
        plt.bar(days, total_production, color='blue')
        plt.title('Milk Production vs Day')
        plt.xlabel('Day')
        plt.ylabel('Milk Production')

    # Save the plot to a BytesIO object
    image_stream_production = BytesIO()
    if HAS_MATPLOTLIB:
        plt.savefig(image_stream_production, format='png')
    image_stream_production.seek(0)
    image_base64_production = base64.b64encode(image_stream_production.read()).decode('utf-8')

    # Close the plot to free up resources
    if HAS_MATPLOTLIB:
        plt.close('all')

    # Pass both base64-encoded images to the template
    return render(request, 'homepage/milkproductionbymonth.html', {
        'selected_year': selected_year,
        'selected_month': selected_month,
        'image_base64_consumption': image_base64_consumption,
        'image_base64_production': image_base64_production,
        'milk_production_records': milk_production_records,
    })


def Add_milk_production_by_month(request,selected_year,selected_month):
    if request.method=='POST':
        form=Milk_productionForm(request.POST)
        if form.is_valid():
            production=form.save(commit=False)
            production.Year=selected_year
            production.Month=selected_month
            production.save()
            return redirect('homepage:milk-productionbymonth',selected_year=selected_year,selected_month=selected_month)

    else:
        form=Milk_productionForm()

    return render(request,'homepage/addmilkproduction.html',{'form':form,'selected_year':selected_year,'selected_month':selected_month})



def Delete_milk_production_by_month(request,selected_year,selected_month,Day):
    milk_production_records=get_object_or_404(Milk_production,Day=Day)
    if request.method=='POST':
        milk_production_records.delete()
        return redirect('homepage:milk-productionbymonth', selected_year=selected_year,selected_month=selected_month)
    
    return render(request, 'homepage/deletemilkproduction.html', {'milk_production_records':milk_production_records,'selected_year':selected_year,'selected_month':selected_month})

def Update_milk_production_by_month(request,selected_year,selected_month,Day):
    milk_production_record=get_object_or_404(Milk_production,Day=Day,Year=selected_year,Month=selected_month)
    if request.method == 'POST':
        form=Milk_productionForm(request.POST,instance=milk_production_record)
        if form.is_valid():
            form.save()
            return redirect('homepage:milk-productionbymonth', selected_year=selected_year,selected_month=selected_month)
    else:
        form=Milk_productionForm(instance=milk_production_record)
    return render(request,'homepage/updatemilkproduction.html',{'form':form,'milk_production_record':milk_production_record, 'selected_year':selected_year,'selected_month':selected_month})

#Eggs production
def Select_year_month_egg(request):
    if request.method=='POST':
        selected_year=request.POST.get('Year')
        selected_month=request.POST.get('Month')

        return redirect('homepage:egg-productionrecord', selected_year=selected_year, selected_month=selected_month)
        
    return render(request,'homepage/selectingyearandmonth.html' )


def Egg_production_record(request,selected_year, selected_month):
    egg_production_records=Eggs_production.objects.filter(Year=selected_year,Month=selected_month)

    return render(request,'homepage/showeggproduction.html', {'egg_production_records':egg_production_records, 'selected_year':selected_year, 'selected_month':selected_month})

def Add_egg_production_by_month(request,selected_year,selected_month):
    if request.method=='POST':
        form=Egg_productionForm(request.POST)
        if form.is_valid():
            production=form.save(commit=False)
            production.Year=selected_year
            production.Month=selected_month
            production.save()
            return redirect('homepage:egg-productionrecord', selected_year=selected_year,selected_month=selected_month)
    else:
        form=Egg_productionForm()
    return render(request, 'homepage/addeggproduction.html', {'form':form,'selected_year':selected_year,'selected_month':selected_month})

def Delete_egg_production_by_month(request,selected_year,selected_month,Day):
    egg_production_records=get_object_or_404(Eggs_production,Day=Day)
    if request.method=='POST':
        egg_production_records.delete()
        return redirect('homepage:egg-productionrecord', selected_year=selected_year,selected_month=selected_month)
    return render(request, 'homepage/deleteeggproduction.html', {'egg_production_records':egg_production_records,'selected_year':selected_year,'selected_month':selected_month})

def Update_egg_production_by_month(request,selected_year,selected_month,Day):
    egg_production_record=get_object_or_404(Eggs_production,Day=Day,Year=selected_year,Month=selected_month)
    if request.method == 'POST':
        form=Egg_productionForm(request.POST,instance=egg_production_record)
        if form.is_valid():
            form.save()
            return redirect('homepage:egg-productionrecord',selected_year=selected_year,selected_month=selected_month)
    else:
        form=Egg_productionForm(instance=egg_production_record)
    return render(request,'homepage/updateeggproduction.html',{'form':form,'egg_production_record':egg_production_record,'selected_year':selected_year,'selected_month':selected_month})



def Help(request):
    return render(request, 'homepage/help.html')

# Crop Disease Analysis View
from .utils.disease_model import DISEASE_DB, compute_features, classify_plant_and_disease, HAS_ML_DEPS  # type: ignore

@csrf_exempt
def crop_disease_analysis(request):
    result = None
    error = None
    if request.method == "POST":
        if "image" not in request.FILES:
            error = "No image uploaded"
        else:
            f = request.FILES["image"]
            try:
                if not HAS_ML_DEPS:
                    raise Exception("Machine learning dependencies (opencv-python, numpy, Pillow) are missing. Please downgrade to Python 3.12 or install C++ Build Tools and run `pip install -r requirements.txt` to enable this feature.")
                    
                import numpy as np  # type: ignore
                import cv2  # type: ignore
                from PIL import Image  # type: ignore
                
                # Read image directly from memory
                file_bytes = np.frombuffer(f.read(), dtype=np.uint8)
                bgr = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                
                if bgr is None:
                    # PIL fallback
                    f.seek(0)
                    pil = Image.open(f).convert("RGB")
                    rgb = np.array(pil)
                else:
                    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
                    
                plant_type = request.POST.get("plant_type")
                
                features = compute_features(rgb)
                plant, disease, confidence = classify_plant_and_disease(features, plant_type)
                info = DISEASE_DB.get(disease, {"curable":"Unknown","pesticide":"Unknown","prevention":"No data available."})
                
                result = {
                    "plant": plant,
                    "disease": disease.replace("_", " "),
                    "confidence": confidence,
                    "curable": info.get("curable","Unknown"),
                    "pesticide": info.get("pesticide","Unknown"),
                    "prevention": info.get("prevention","No data available."),
                    "features": features
                }
            except Exception as e:
                error = f"Processing failed: {e}"
                
    return render(request, "homepage/crop_disease_analysis.html", {"result": result, "error": error})
