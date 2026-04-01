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

def calculate_irrigation_time(crop, area_acres, flow_rate_lpm):
    """
    Calculates estimated minutes required for ONE irrigation session.
    Assuming one session requires ~2% of the total seasonal water.
    """
    total_seasonal_need = CROP_WATER_NEEDS_LPA.get(crop, 2000000) * float(area_acres)
    session_need_liters = total_seasonal_need * 0.02 # 2% per session
    
    if float(flow_rate_lpm) <= 0:
        return 0
        
    minutes_required = session_need_liters / float(flow_rate_lpm)
    return int(minutes_required)
