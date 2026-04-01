from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from django.contrib import messages  # type: ignore
from django.utils import timezone  # type: ignore
from datetime import timedelta
from .models import WaterSchedule  # type: ignore
from .water_form import WaterScheduleForm  # type: ignore
from .utils.water_calc import calculate_irrigation_time  # type: ignore
from .utils.sms_sender import send_water_alert_sms  # type: ignore

def water_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("authentication:login")
        
    if request.user.is_superuser:
        schedules = WaterSchedule.objects.all().order_by('-id')
    else:
        schedules = WaterSchedule.objects.filter(user=request.user).order_by('-id')
    
    # Auto-update status for flowing schedules that have passed end_time
    # Normally done with Celery, but we can do a lazy catch-up on view load
    now = timezone.now()
    for sch in schedules:
        if sch.status == 'Flowing' and sch.end_time and now >= sch.end_time:
            sch.status = 'Completed'
            sch.save()
            
    return render(request, "homepage/water_dashboard.html", {"schedules": schedules})

from django.views.decorators.csrf import csrf_exempt  # type: ignore

@csrf_exempt
def add_water_schedule(request):
    if not request.user.is_authenticated:
        return redirect("authentication:login")
    
    if request.method == "POST":
        form = WaterScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            
            # Auto-calculate the required minutes
            calc_minutes = calculate_irrigation_time(
                schedule.crop, 
                schedule.field_area, 
                schedule.water_level,
                schedule.water_source_flow_rate
            )
            schedule.calculated_time_minutes = calc_minutes
            schedule.save()
            return redirect("homepage:water-dashboard")
    else:
        form = WaterScheduleForm()
        
    return render(request, "homepage/add_water_schedule.html", {"form": form})

def start_watering(request, id):
    if request.user.is_superuser:
        schedule = get_object_or_404(WaterSchedule, id=id)
    else:
        schedule = get_object_or_404(WaterSchedule, id=id, user=request.user)
    if schedule.status == 'Pending':
        schedule.status = 'Flowing'
        schedule.start_time = timezone.now()
        schedule.end_time = schedule.start_time + timedelta(minutes=schedule.calculated_time_minutes)
        schedule.save()
    return redirect("homepage:water-dashboard")

def mark_completed(request, id):
    if request.user.is_superuser:
        schedule = get_object_or_404(WaterSchedule, id=id)
    else:
        schedule = get_object_or_404(WaterSchedule, id=id, user=request.user)
    
    # Check if transitioning from Flowing to trigger SMS exactly once
    if schedule.status == 'Flowing':
        schedule.status = 'Completed'
        schedule.save()
        
        # Send Real SMS Alert
        if schedule.mobile_number:
            message = f"FARM ALERT: Water flow for your {schedule.field_area} Acre {schedule.crop} field is mathematically COMPLETE. Please turn off your pump."
            result = send_water_alert_sms(schedule.mobile_number, message)
            if result.get('success'):
                messages.success(request, f"SMS alert sent successfully to {schedule.mobile_number}")
            else:
                err_msg = result.get('error', 'Unknown Error')
                messages.error(request, f"Could not send SMS to {schedule.mobile_number}: {err_msg}")
            
    elif schedule.status != 'Completed':
        schedule.status = 'Completed'
        schedule.save()
        
    return redirect("homepage:water-dashboard")

def delete_water_schedule(request, id):
    if request.user.is_superuser:
        schedule = get_object_or_404(WaterSchedule, id=id)
    else:
        schedule = get_object_or_404(WaterSchedule, id=id, user=request.user)
    schedule.delete()
    return redirect("homepage:water-dashboard")
