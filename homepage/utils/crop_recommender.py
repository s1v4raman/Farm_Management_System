# Utils for Crop Recommendation Module

def recommend_crop(soil, season, water):
    """
    A rule-based intelligent crop recommender.
    Maps combinations of Soil Type, Season, and Water Availability to the best crops.
    """
    # Normalize inputs for robust matching
    s = soil.lower()
    seas = season.lower()
    w = water.lower()

    # Rule dictionary mapping to lists of suggested crops
    recommendations = {
        "red": {
            "summer": {"high": ["Groundnut", "Cotton", "Maize"], "medium": ["Groundnut", "Millet"], "low": ["Millet", "Sorghum"]},
            "winter": {"high": ["Wheat", "Gram", "Mustard"], "medium": ["Gram", "Linseed"], "low": ["Linseed"]},
            "monsoon": {"high": ["Rice", "Sugarcane"], "medium": ["Cotton", "Maize"], "low": ["Millet", "Pulse"]}
        },
        "black": {
            "summer": {"high": ["Cotton", "Sugarcane"], "medium": ["Cotton", "Sunflower"], "low": ["Sunflower", "Sorghum"]},
            "winter": {"high": ["Wheat", "Gram", "Linseed"], "medium": ["Gram", "Safflower"], "low": ["Safflower"]},
            "monsoon": {"high": ["Rice", "Soybean", "Cotton"], "medium": ["Soybean", "Maize"], "low": ["Pigeon Pea", "Sorghum"]}
        },
        "alluvial": {
            "summer": {"high": ["Rice", "Jute", "Sugarcane"], "medium": ["Maize", "Cotton"], "low": ["Millet"]},
            "winter": {"high": ["Wheat", "Mustard", "Barley"], "medium": ["Gram", "Peas"], "low": ["Lentil"]},
            "monsoon": {"high": ["Rice", "Jute"], "medium": ["Maize", "Cotton"], "low": ["Millet", "Sorghum"]}
        },
        "loamy": {
             "summer": {"high": ["Sugarcane", "Tomato", "Potato"], "medium": ["Maize", "Groundnut"], "low": ["Millet", "Sorghum"]},
             "winter": {"high": ["Wheat", "Mustard", "Peas"], "medium": ["Gram", "Barley"], "low": ["Lentil"]},
             "monsoon": {"high": ["Rice", "Cotton"], "medium": ["Maize", "Soybean"], "low": ["Pearl Millet"]}
        }
    }

    # Default fallback in case of missing matches
    default_crops = ["Millet", "Sorghum"]
    
    # Traverse rules safely
    soil_rules = recommendations.get(s, {})
    season_rules = soil_rules.get(seas, {})
    suggested_crops = season_rules.get(w, default_crops)

    return suggested_crops
