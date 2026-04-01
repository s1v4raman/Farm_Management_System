# Water calculation utilities based on crop type
# Values are approximations for overall seasonal water need (Liters per Acre)
# To find a practical short-term irrigation length, we calculate per irrigation session
# Assuming an average irrigation session provides a fraction of total need.

CROP_WATER_NEEDS_LPA = {
    'Rice': 5000000,      # High water need
    'Wheat': 2000000,     # Medium water need
    'Cotton': 3000000,    # Medium-High
    'Maize': 2500000,
    'Sugarcane': 8000000, # Very high
    'Vegetables': 1500000,
    'Fruits': 3000000,
    'Pulses': 1200000,
    'Other': 2000000
}

CROP_CHOICES = [(k, k) for k in CROP_WATER_NEEDS_LPA.keys()]

def calculate_irrigation_time(crop, area_acres, water_level, flow_rate_lpm):
    """
    Calculates estimated minutes required for ONE irrigation session.
    Adjusted by current water_level.
    """
    total_seasonal_need = CROP_WATER_NEEDS_LPA.get(crop, 2000000) * float(area_acres)
    
    if water_level == 'High':
        session_percent = 0.005 # 0.5%
    elif water_level == 'Medium':
        session_percent = 0.015 # 1.5%
    elif water_level == 'Low':
        session_percent = 0.025 # 2.5%
    elif water_level == 'Dry':
        session_percent = 0.040 # 4.0%
    else:
        session_percent = 0.020 # Default

    session_need_liters = total_seasonal_need * session_percent
    
    if float(flow_rate_lpm) <= 0:
        return 0
        
    minutes_required = session_need_liters / float(flow_rate_lpm)
    return max(1, int(minutes_required)) if session_need_liters > 0 else 0
