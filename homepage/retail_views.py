from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from .models import Retail_Crop_Sales, Retail_Egg_Sales, Retail_Milk_Sales, Retail_Machinery_Renting # type: ignore
from .retail_forms import RetailCropSalesForm, RetailEggSalesForm, RetailMilkSalesForm, RetailMachineryRentingForm # type: ignore

from datetime import date
from django.db.models import Sum

def retail_dashboard(request):
    context = {}
    if request.user.is_superuser or request.user.is_staff:
        today = date.today()
        
        todays_sales = sum([
            Retail_Crop_Sales.objects.filter(Date=today).aggregate(Sum('Total_Amount'))['Total_Amount__sum'] or 0,
            Retail_Egg_Sales.objects.filter(Date=today).aggregate(Sum('Total_Amount'))['Total_Amount__sum'] or 0,
            Retail_Milk_Sales.objects.filter(Date=today).aggregate(Sum('Total_Amount'))['Total_Amount__sum'] or 0,
            Retail_Machinery_Renting.objects.filter(Date=today).aggregate(Sum('Total_Amount'))['Total_Amount__sum'] or 0,
        ])
        
        from .models import Crops
        active_crops = Crops.objects.filter(Is_harvested=False).count()
        ready_for_harvest = Crops.objects.filter(Is_harvested=False, Harvesting_date__lte=today).count()
        
        new_orders = sum([
            Retail_Crop_Sales.objects.filter(Date=today).count(),
            Retail_Egg_Sales.objects.filter(Date=today).count(),
            Retail_Milk_Sales.objects.filter(Date=today).count(),
            Retail_Machinery_Renting.objects.filter(Date=today).count(),
        ])
        
        recent_orders = []
        for s in Retail_Crop_Sales.objects.all().order_by('-Date')[:5]:
            recent_orders.append({'id': f"#CROP-{s.id}", 'buyer': s.Customer_Name, 'phone': 'N/A', 'amount': s.Total_Amount, 'status': 'Paid', 'date': s.Date})
        for s in Retail_Egg_Sales.objects.all().order_by('-Date')[:5]:
            recent_orders.append({'id': f"#EGG-{s.id}", 'buyer': s.Customer_Name, 'phone': 'N/A', 'amount': s.Total_Amount, 'status': 'Paid', 'date': s.Date})
        for s in Retail_Milk_Sales.objects.all().order_by('-Date')[:5]:
            recent_orders.append({'id': f"#MILK-{s.id}", 'buyer': s.Customer_Name, 'phone': 'N/A', 'amount': s.Total_Amount, 'status': 'Paid', 'date': s.Date})
        for s in Retail_Milk_Sales.objects.all().order_by('-Date')[:5]:
            recent_orders.append({'id': f"#MILK-{s.id}", 'buyer': s.Customer_Name, 'phone': 'N/A', 'amount': s.Total_Amount, 'status': 'Paid', 'date': s.Date})
            
        recent_orders.sort(key=lambda x: x['date'], reverse=True)
        recent_orders = recent_orders[:6]
        
        context = {
            'todays_sales': todays_sales,
            'active_crops': active_crops,
            'ready_for_harvest': ready_for_harvest,
            'new_orders': new_orders,
            'recent_orders': recent_orders,
        }
        
    return render(request, "homepage/retail_dashboard.html", context)

# --- Retail Crop Sales ---
def show_retail_crop_sales(request):
    sales = Retail_Crop_Sales.objects.all().order_by('-Date')
    return render(request, "homepage/show_retail_crop_sales.html", {'sales': sales})

def add_retail_crop_sale(request):
    if request.method == "POST":
        form = RetailCropSalesForm(request.POST, request.FILES)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
                sale.Customer_Name = request.user.username
            else:
                sale.Customer_Name = ""
            sale.save()
            
            # --- CUSTOMER BUYS -> FARMER SEES (SYNC) ---
            if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
                seller_id = request.POST.get('seller_id')
                from .models import Crops, Crop_sales
                # Try to find the crop by name to attach the sale to a real farmer's Crop record.
                if seller_id:
                    crop = Crops.objects.filter(Crop_name__iexact=sale.Crop_Name, user_id=seller_id).first()
                else:
                    crop = Crops.objects.filter(Crop_name__iexact=sale.Crop_Name).first()
                
                if crop:
                    Crop_sales.objects.create(
                        crops=crop,
                        Sale_date=sale.Date,
                        Quantity_sold=str(sale.Quantity_Sold),
                        Unit_price=sale.Unit_Price,
                        Buyer_information=sale.Customer_Name,
                        Payment_method=sale.Payment_Method,
                        Payment_status='received',
                        Invoice_number=f"RET-{sale.id}",
                        Additional_notes="Auto-synced from Retail Marketplace purchase"
                    )

            return redirect("homepage:show-retail-crop-sales")
    else:
        initial_data = {}
        if request.GET.get('crop_name'):
            initial_data['Crop_Name'] = request.GET.get('crop_name')
        if request.GET.get('unit_price'):
            initial_data['Unit_Price'] = request.GET.get('unit_price')
        form = RetailCropSalesForm(initial=initial_data)
        
    seller_id = request.GET.get('seller_id', '')

    if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
        form.fields['Crop_Name'].widget.attrs['readonly'] = True
        form.fields['Unit_Price'].widget.attrs['readonly'] = True
        form.fields['Quantity_Sold'].label = "Quantity to Buy"
        
    return render(request, "homepage/add_retail_crop_sale.html", {'form': form, 'seller_id': seller_id})

def update_retail_crop_sale(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("homepage:show-retail-crop-sales")
    sale = get_object_or_404(Retail_Crop_Sales, id=id)
    if request.method == "POST":
        form = RetailCropSalesForm(request.POST, request.FILES, instance=sale)
        if form.is_valid():
            form.save()
            return redirect("homepage:show-retail-crop-sales")
    else:
        form = RetailCropSalesForm(instance=sale)
    return render(request, "homepage/update_retail_crop_sale.html", {'form': form, 'sale': sale})

def delete_retail_crop_sale(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("homepage:show-retail-crop-sales")
    sale = get_object_or_404(Retail_Crop_Sales, id=id)
    if request.method == "POST":
        sale.delete()
        return redirect("homepage:show-retail-crop-sales")
    return render(request, "homepage/delete_retail_crop_sale.html", {'sale': sale})

# --- Retail Egg Sales ---
def show_retail_egg_sales(request):
    sales = Retail_Egg_Sales.objects.all().order_by('-Date')
    return render(request, "homepage/show_retail_egg_sales.html", {'sales': sales})

def add_retail_egg_sale(request):
    if request.method == "POST":
        form = RetailEggSalesForm(request.POST, request.FILES)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
                sale.Customer_Name = request.user.username
            else:
                sale.Customer_Name = ""
            sale.save()
            return redirect("homepage:show-retail-egg-sales")
    else:
        initial_data = {}
        if request.GET.get('price_per_tray'):
            initial_data['Price_Per_Tray'] = request.GET.get('price_per_tray')
        if request.GET.get('price_per_egg'):
            initial_data['Price_Per_Egg'] = request.GET.get('price_per_egg')
        form = RetailEggSalesForm(initial=initial_data)
        
    if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
        form.fields['Price_Per_Tray'].widget.attrs['readonly'] = True
        form.fields['Price_Per_Egg'].widget.attrs['readonly'] = True
        form.fields['Tray_Count'].label = "Trays to Buy"
        form.fields['Egg_Count'].label = "Individual Eggs to Buy"
        
    return render(request, "homepage/add_retail_egg_sale.html", {'form': form})

def update_retail_egg_sale(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("homepage:show-retail-egg-sales")
    sale = get_object_or_404(Retail_Egg_Sales, id=id)
    if request.method == "POST":
        form = RetailEggSalesForm(request.POST, request.FILES, instance=sale)
        if form.is_valid():
            form.save()
            return redirect("homepage:show-retail-egg-sales")
    else:
        form = RetailEggSalesForm(instance=sale)
    return render(request, "homepage/update_retail_egg_sale.html", {'form': form, 'sale': sale})

def delete_retail_egg_sale(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("homepage:show-retail-egg-sales")
    sale = get_object_or_404(Retail_Egg_Sales, id=id)
    if request.method == "POST":
        sale.delete()
        return redirect("homepage:show-retail-egg-sales")
    return render(request, "homepage/delete_retail_egg_sale.html", {'sale': sale})

# --- Retail Milk Sales ---
def show_retail_milk_sales(request):
    sales = Retail_Milk_Sales.objects.all().order_by('-Date')
    return render(request, "homepage/show_retail_milk_sales.html", {'sales': sales})

def add_retail_milk_sale(request):
    if request.method == "POST":
        form = RetailMilkSalesForm(request.POST, request.FILES)
        if form.is_valid():
            sale = form.save(commit=False)
            sale.user = request.user
            if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
                sale.Customer_Name = request.user.username
            else:
                sale.Customer_Name = ""
            sale.save()
            return redirect("homepage:show-retail-milk-sales")
    else:
        initial_data = {}
        if request.GET.get('price_per_liter'):
            initial_data['Price_Per_Liter'] = request.GET.get('price_per_liter')
        form = RetailMilkSalesForm(initial=initial_data)
        
    if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
        form.fields['Price_Per_Liter'].widget.attrs['readonly'] = True
        form.fields['Quantity_Liters'].label = "Liters to Buy"
        
    return render(request, "homepage/add_retail_milk_sale.html", {'form': form})

def update_retail_milk_sale(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("homepage:show-retail-milk-sales")
    sale = get_object_or_404(Retail_Milk_Sales, id=id)
    if request.method == "POST":
        form = RetailMilkSalesForm(request.POST, request.FILES, instance=sale)
        if form.is_valid():
            form.save()
            return redirect("homepage:show-retail-milk-sales")
    else:
        form = RetailMilkSalesForm(instance=sale)
    return render(request, "homepage/update_retail_milk_sale.html", {'form': form, 'sale': sale})

def delete_retail_milk_sale(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("homepage:show-retail-milk-sales")
    sale = get_object_or_404(Retail_Milk_Sales, id=id)
    if request.method == "POST":
        sale.delete()
        return redirect("homepage:show-retail-milk-sales")
    return render(request, "homepage/delete_retail_milk_sale.html", {'sale': sale})

# --- Retail Machinery Renting ---
def show_retail_machinery_renting(request):
    rentings = Retail_Machinery_Renting.objects.all().order_by('-Date')
    return render(request, "homepage/show_retail_machinery_renting.html", {'rentings': rentings})

def add_retail_machinery_renting(request):
    if request.method == "POST":
        form = RetailMachineryRentingForm(request.POST, request.FILES)
        if form.is_valid():
            renting = form.save(commit=False)
            renting.user = request.user
            if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
                renting.Customer_Name = request.user.username
            else:
                renting.Customer_Name = ""
            renting.save()
            
            # --- CUSTOMER RENTS -> FARMER SEES (SYNC) ---
            if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
                seller_id = request.POST.get('seller_id')
                from .models import Machinery, Machinery_activities
                # Find machinery by equipment name
                if seller_id:
                    machinery = Machinery.objects.filter(Equipment_name__iexact=renting.Machinery_Used, user_id=seller_id).first()
                else:
                    machinery = Machinery.objects.filter(Equipment_name__iexact=renting.Machinery_Used).first()
                
                if machinery:
                    Machinery_activities.objects.create(
                        machinery=machinery,
                        Activity_date=renting.Date,
                        Activity_type="Rented Out",
                        Activity_cost=int(renting.Total_Amount),
                        Description=f"Rented to {renting.Customer_Name} for {renting.Hours_Rented} hours"
                    )

            return redirect("homepage:show-retail-machinery-renting")
    else:
        initial_data = {}
        if request.GET.get('machinery_used'):
            initial_data['Machinery_Used'] = request.GET.get('machinery_used')
        if request.GET.get('rate_per_hour'):
            initial_data['Rate_Per_Hour'] = request.GET.get('rate_per_hour')
        if request.GET.get('service_provided'):
            initial_data['Service_Provided'] = request.GET.get('service_provided')
        form = RetailMachineryRentingForm(initial=initial_data)
        
    seller_id = request.GET.get('seller_id', '')

    if request.user.is_authenticated and not request.user.is_superuser and not request.user.is_staff:
        form.fields['Machinery_Used'].widget.attrs['readonly'] = True
        form.fields['Service_Provided'].widget.attrs['readonly'] = True
        form.fields['Rate_Per_Hour'].widget.attrs['readonly'] = True
        form.fields['Hours_Rented'].label = "Hours to Rent"
        
    return render(request, "homepage/add_retail_machinery_renting.html", {'form': form, 'seller_id': seller_id})

def update_retail_machinery_renting(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("homepage:show-retail-machinery-renting")
    renting = get_object_or_404(Retail_Machinery_Renting, id=id)
    if request.method == "POST":
        form = RetailMachineryRentingForm(request.POST, request.FILES, instance=renting)
        if form.is_valid():
            form.save()
            return redirect("homepage:show-retail-machinery-renting")
    else:
        form = RetailMachineryRentingForm(instance=renting)
    return render(request, "homepage/update_retail_machinery_renting.html", {'form': form, 'renting': renting})

def delete_retail_machinery_renting(request, id):
    if not (request.user.is_superuser or request.user.is_staff):
        return redirect("homepage:show-retail-machinery-renting")
    renting = get_object_or_404(Retail_Machinery_Renting, id=id)
    if request.method == "POST":
        renting.delete()
        return redirect("homepage:show-retail-machinery-renting")
    return render(request, "homepage/delete_retail_machinery_renting.html", {'renting': renting})

# ================= RETAIL LIVESTOCK SALES =================

# Livestock Sales Removed
