from django.utils import timezone
from homepage.models import (
    WaterSchedule, Crops, ContactDetail, 
    Retail_Crop_Sales, Retail_Egg_Sales, Retail_Milk_Sales, 
    Retail_Machinery_Renting
)

def global_contact_info(request):
    contact = ContactDetail.objects.first()
    if not contact:
        contact = ContactDetail.objects.create()
    return {'contact_info': contact}

def global_notifications(request):
    if not request.user.is_authenticated:
        return {'notifications': [], 'notif_count': 0}

    notifications = []
    today = timezone.now().date()
    
    # 1. Farmer/Admin Alerts (only for staff/superusers)
    if request.user.is_superuser or request.user.is_staff:
        # Water schedules
        if hasattr(WaterSchedule, 'objects'):
            pending_water = WaterSchedule.objects.filter(user=request.user, status='Pending')
            for pw in pending_water:
                notifications.append({
                    'icon': 'bx-water',
                    'color': '#0ea5e9',
                    'text': f"Pending water schedule for {pw.crop}",
                    'url': '/water-dashboard/'
                })
                
            flowing_water = WaterSchedule.objects.filter(user=request.user, status='Flowing')
            for fw in flowing_water:
                notifications.append({
                    'icon': 'bx-loader bx-spin',
                    'color': '#10b981',
                    'text': f"Pump is ON for {fw.crop} ({fw.field_area} Ac)",
                    'url': '/water-dashboard/'
                })

        # Overdue Crops
        if hasattr(Crops, 'objects'):
            overdue_crops = Crops.objects.filter(user=request.user, Is_harvested=False, Harvesting_date__lte=today)
            for oc in overdue_crops:
                notifications.append({
                    'icon': 'bx-error-circle',
                    'color': '#e11d48',
                    'text': f"Harvest overdue: {oc.Crop_name}",
                    'url': '/show_crops/'
                })

    # 2. Customer Notifications (Today's Retail Arrivals)
    # This shows to everyone (customers see new deals, farmers see their own listings)
    
    # Crop Arrivals
    crops_today = Retail_Crop_Sales.objects.filter(Date=today).order_by('-id')[:2]
    for sale in crops_today:
        notifications.append({
            'icon': 'bx-leaf',
            'color': '#00cc00',
            'text': f"Fresh {sale.Crop_Name} just listed!",
            'url': '/show-retail-crop-sales/'
        })

    # Milk Arrivals
    milk_today = Retail_Milk_Sales.objects.filter(Date=today).order_by('-id')[:1]
    for sale in milk_today:
        notifications.append({
            'icon': 'bx-droplet',
            'color': '#3b82f6',
            'text': f"Fresh {sale.Quantity_Liters}L Milk available",
            'url': '/show-retail-milk-sales/'
        })

    # Egg Arrivals
    eggs_today = Retail_Egg_Sales.objects.filter(Date=today).order_by('-id')[:1]
    for sale in eggs_today:
        notifications.append({
            'icon': 'bx-circle',
            'color': '#eab308',
            'text': f"Fresh Eggs: {sale.Tray_Count} trays in stock",
            'url': '/show-retail-egg-sales/'
        })

    # Machinery Rentals
    mach_today = Retail_Machinery_Renting.objects.filter(Date=today).order_by('-id')[:1]
    for sale in mach_today:
        notifications.append({
            'icon': 'bx-wrench',
            'color': '#22c55e',
            'text': f"{sale.Machinery_Used} for rent today",
            'url': '/show-retail-machinery-renting/'
        })

    # Livestock Section Removed

    notif_count = len(notifications)
    
    return {
        'notifications': notifications[:10], # Show up to 10 recent notifications
        'notif_count': notif_count
    }
