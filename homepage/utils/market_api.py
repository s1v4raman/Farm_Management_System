# Utils for Market Price Analysis Module
import random
import datetime

# Realistic baseline prices for major crops in INR per Kg
BASE_PRICES = {
    "Rice (Paddy)": 40.0,
    "Wheat": 30.0,
    "Corn (Maize)": 24.0,
    "Cotton": 65.0,
    "Sugarcane": 3.5, # Per kg
    "Soybean": 48.0,
    "Groundnut": 70.0,
    "Mustard": 55.0,
    "Turmeric": 140.0,
    "Tomato": 20.0,
    "Onion": 25.0,
    "Potato": 18.0
}

def get_daily_market_prices():
    """
    Simulates highly realistic daily market prices (Mandi rates).
    Calculates Today, Yesterday, and the difference.
    Use a seed based on the current date so prices are consistent for a given day.
    """
    today = datetime.date.today()
    random.seed(today.toordinal())
    
    market_data = []
    
    for crop, base in BASE_PRICES.items():
        # Simulate yesterday's price
        # Organic fluctuation of +/- 5%
        yesterday_fluctuation = random.uniform(-0.05, 0.05)
        yesterday_price = round(base * (1 + yesterday_fluctuation), 1)  # type: ignore
        
        # Simulate today's price movement from yesterday
        # Market usually moves by -3% to +3% daily
        today_fluctuation = random.uniform(-0.03, 0.03)
        today_price = round(yesterday_price * (1 + today_fluctuation), 1)
        
        difference = round(today_price - yesterday_price, 1)
        
        market_data.append({
            "crop": crop,
            "yesterday_price": yesterday_price,
            "today_price": today_price,
            "difference": difference,
            "is_increase": difference > 0,
            "is_neutral": difference == 0
        })
        
    # Sort with highest value crops first
    market_data.sort(key=lambda x: x['today_price'], reverse=True)
    return market_data

def get_historical_prices(crop_name, days=7):
    """
    Generates realistic historical price data for the chart.
    """
    if crop_name not in BASE_PRICES:
        return {"dates": [], "prices": []}
        
    base = BASE_PRICES[crop_name]
    today = datetime.date.today()
    
    # We want consistent history for any given day
    random.seed(today.toordinal() + hash(crop_name))
    
    dates = []
    prices = []
    
    current_sim_price = base
    
    # Build prices backward
    for i in range(days - 1, -1, -1):
        target_date = today - datetime.timedelta(days=i)
        dates.append(target_date.strftime("%b %d"))
        
        # Organic daily drift
        drift = random.uniform(-0.04, 0.04)
        current_sim_price = current_sim_price * (1 + drift)
        prices.append(round(current_sim_price, 1))  # type: ignore
        
    return {
        "crop": crop_name,
        "dates": dates,
        "prices": prices
    }
