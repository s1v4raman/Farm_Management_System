import os
import uuid

# Attempt to import ML dependencies
try:
    import numpy as np # type: ignore
    import cv2 # type: ignore
    from PIL import Image # type: ignore
    HAS_ML_DEPS = True
except ImportError:
    HAS_ML_DEPS = False
    class _Dummy:
        def __getattr__(self, name): return self
        def __call__(self, *args, **kwargs): return self
    np = _Dummy() # type: ignore
    cv2 = _Dummy() # type: ignore
    Image = _Dummy() # type: ignore

DISEASE_DB = {
    # rice classes
    "rice_bacterial_leaf_blight": {
        "curable": "Yes",
        "pesticide": "Copper oxychloride",
        "prevention": "Improve drainage, avoid excessive nitrogen, remove infected plants."
    },
    "rice_brown_spot": {
        "curable": "Yes",
        "pesticide": "Mancozeb",
        "prevention": "Avoid standing water, rotate crops, improve soil health."
    },
    "rice_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy leaf — no action required."
    },
    "rice_hispa": {
        "curable": "Yes",
        "pesticide": "Chlorpyrifos",
        "prevention": "Keep fields weed-free and monitor early."
    },
    # tomato classes
    "tomato_bacterial_spot": {
        "curable": "Yes",
        "pesticide": "Copper fungicide",
        "prevention": "Remove infected leaves; avoid overhead watering."
    },
    "tomato_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy leaf — no action required."
    },
    "tomato_late_blight": {
        "curable": "No (severe)",
        "pesticide": "Copper fungicide (early stage)",
        "prevention": "Improve airflow, remove heavily infected plants."
    },
    "tomato_leaf_mold": {
        "curable": "Yes",
        "pesticide": "Chlorothalonil",
        "prevention": "Reduce humidity, avoid overhead irrigation."
    },
    "tomato_mosaic_virus": {
        "curable": "No",
        "pesticide": "None",
        "prevention": "Use virus-free seeds and resistant varieties."
    },
    "tomato_septoria_leaf_spot": {
        "curable": "Yes",
        "pesticide": "Mancozeb",
        "prevention": "Remove infected debris and rotate crops."
    },
    "tomato_spider_mites": {
        "curable": "Yes",
        "pesticide": "Neem oil or miticide",
        "prevention": "Monitor regularly and maintain humidity."
    },
    "tomato_target_spot": {
        "curable": "Yes",
        "pesticide": "Azoxystrobin",
        "prevention": "Remove infected tissue and avoid overhead watering."
    },
    "tomato_yellow_leaf_curl_virus": {
        "curable": "No",
        "pesticide": "None",
    },
    # corn classes
    "corn_common_rust": {
        "curable": "Yes",
        "pesticide": "Fungicides containing pyraclostrobin",
        "prevention": "Plant resistant hybrids."
    },
    "corn_northern_leaf_blight": {
        "curable": "Yes",
        "pesticide": "Fungicides like azoxystrobin",
        "prevention": "Crop rotation and tillage."
    },
    "corn_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy leaf — no action required."
    },
    # potato classes
    "potato_early_blight": {
        "curable": "Yes",
        "pesticide": "Chlorothalonil or Mancozeb",
        "prevention": "Crop rotation, maintain adequate soil fertility."
    },
    "potato_late_blight": {
        "curable": "No (severe)",
        "pesticide": "Copper fungicide (early stage)",
        "prevention": "Destroy cull piles, use disease-free seed."
    },
    "potato_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy leaf — no action required."
    },
    
    # --- Major Field Crops (Staples & Cereals) ---
    "wheat_leaf_rust": {
        "curable": "Yes",
        "pesticide": "Tebuconazole or Propiconazole",
        "prevention": "Use rust-resistant wheat varieties and eradicate volunteer wheat."
    },
    "wheat_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy leaf — no action required."
    },
    "millets_blast": {
        "curable": "Yes",
        "pesticide": "Tricyclazole",
        "prevention": "Use resistant varieties, balanced nitrogen application."
    },
    "millets_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "barley_powdery_mildew": {
        "curable": "Yes",
        "pesticide": "Sulfur-based fungicides",
        "prevention": "Avoid dense planting and reduce nitrogen excess."
    },
    "barley_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "oats_crown_rust": {
        "curable": "Yes",
        "pesticide": "Azoxystrobin",
        "prevention": "Eradicate alternate hosts (buckthorn) and use early maturing varieties."
    },
    "oats_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },

    # --- Pulses & Oilseeds (Cash Crops) ---
    "lentils_wilt": {
        "curable": "No (once severe)",
        "pesticide": "Seed treatment with Carbendazim",
        "prevention": "Crop rotation and maintaining soil moisture."
    },
    "lentils_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "chickpeas_ascochyta_blight": {
        "curable": "Yes",
        "pesticide": "Chlorothalonil",
        "prevention": "Use pathogen-free seeds, avoid field working when wet."
    },
    "chickpeas_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "moong_yellow_mosaic": {
        "curable": "No (Viral)",
        "pesticide": "Insecticide for Whiteflies (Imidacloprid)",
        "prevention": "Use disease-resistant seeds and control whitefly populations."
    },
    "moong_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "peas_powdery_mildew": {
        "curable": "Yes",
        "pesticide": "Wettable Sulfur",
        "prevention": "Avoid late sowing and remove crop debris."
    },
    "peas_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "soybean_rust": {
        "curable": "Yes",
        "pesticide": "Pyraclostrobin",
        "prevention": "Apply fungicides early; monitor canopy closely."
    },
    "soybean_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "mustard_white_rust": {
        "curable": "Yes",
        "pesticide": "Metalaxyl",
        "prevention": "Clean cultivation, crop rotation, weed control."
    },
    "mustard_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "groundnut_tikka": {
        "curable": "Yes",
        "pesticide": "Mancozeb or Carbendazim",
        "prevention": "Crop rotation and burn infected plant debris."
    },
    "groundnut_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "sunflower_necrosis": {
        "curable": "No (Viral)",
        "pesticide": "Control Thrips (vector) with Spinosad",
        "prevention": "Field sanitation and removing infected plants early."
    },
    "sunflower_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "castor_blight": {
        "curable": "Yes",
        "pesticide": "Copper Oxychloride",
        "prevention": "Proper spacing for aeration and timely sowing."
    },
    "castor_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },

    # --- Fiber & Industrial Crops ---
    "cotton_bollworm": {
        "curable": "Yes",
        "pesticide": "Cypermethrin or Bt Cotton varieties",
        "prevention": "Use pheromone traps, deep ploughing."
    },
    "cotton_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "sugarcane_red_rot": {
        "curable": "No (Highly destructive)",
        "pesticide": "None for standing crop; seed treatment helps.",
        "prevention": "Use healthy setts, uproot and burn diseased clumps."
    },
    "sugarcane_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "jute_stem_rot": {
        "curable": "Yes",
        "pesticide": "Mancozeb",
        "prevention": "Provide proper drainage, avoid waterlogging."
    },
    "jute_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "tobacco_mosaic": {
        "curable": "No",
        "pesticide": "None",
        "prevention": "Wash hands with soap before handling, remove infected plants."
    },
    "tobacco_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },

    # --- Plantation & Beverage Crops ---
    "tea_blister_blight": {
        "curable": "Yes",
        "pesticide": "Copper fungicide",
        "prevention": "Adjust shade, ensure proper pruning."
    },
    "tea_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "coffee_rust": {
        "curable": "Yes",
        "pesticide": "Triazole or Copper based fungicide",
        "prevention": "Maintain tree health; grow resistant varieties."
    },
    "coffee_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "rubber_abnormal_leaf_fall": {
        "curable": "Yes",
        "pesticide": "Bordeaux mixture",
        "prevention": "Prophylactic spraying before monsoon season."
    },
    "rubber_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "coconut_bud_rot": {
        "curable": "Yes (if detected early)",
        "pesticide": "Bordeaux paste on affected crown",
        "prevention": "Improve drainage, clean crown regularly."
    },
    "coconut_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },

    # --- Vegetables, Fruits, & Specialty Crops ---
    "onion_purple_blotch": {
        "curable": "Yes",
        "pesticide": "Mancozeb + Chlorothalonil",
        "prevention": "Ensure good drainage and crop rotation."
    },
    "onion_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "cauliflower_black_rot": {
        "curable": "No (Bacterial)",
        "pesticide": "Copper sprays (preventative)",
        "prevention": "Use disease-free seeds and avoid overhead irrigation."
    },
    "cauliflower_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "garlic_white_rot": {
        "curable": "No (Soil borne)",
        "pesticide": "Tebuconazole (preventative)",
        "prevention": "Plant in uninfected soil, practice strict crop rotation."
    },
    "garlic_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "mango_anthracnose": {
        "curable": "Yes",
        "pesticide": "Carbendazim or Copper oxychloride",
        "prevention": "Prune dead branches, prompt harvest."
    },
    "mango_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "banana_sigatoka": {
        "curable": "Yes",
        "pesticide": "Propiconazole",
        "prevention": "Deleafing infected leaves, proper drainage."
    },
    "banana_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "grapes_downy_mildew": {
        "curable": "Yes",
        "pesticide": "Mancozeb or Metalaxyl",
        "prevention": "Ensure good canopy airflow, remove fallen leaves."
    },
    "grapes_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "citrus_canker": {
        "curable": "No (Bacterial)",
        "pesticide": "Copper bactericides (suppressive)",
        "prevention": "Plant windbreaks, sanitize tools, avoid physical injury to tree."
    },
    "citrus_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "spices_leaf_spot": {
        "curable": "Yes",
        "pesticide": "Bordeaux mixture",
        "prevention": "Avoid excess shading and waterlogging."
    },
    "spices_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "medicinal_root_rot": {
        "curable": "Manageable",
        "pesticide": "Trichoderma viride in soil",
        "prevention": "Ensure extremely well-draining soil."
    },
    "medicinal_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "tapioca_mosaic": {
        "curable": "No",
        "pesticide": "None",
        "prevention": "Use virus-free planting material, control whiteflies."
    },
    "tapioca_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },

    # --- Alternative/Small Farm Crops ---
    "berries_botrytis": {
        "curable": "Yes",
        "pesticide": "Captan or Fenhexamid",
        "prevention": "Maximize air circulation, avoid over-fertilizing."
    },
    "berries_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "bamboo_rust": {
        "curable": "Yes",
        "pesticide": "Hexaconazole",
        "prevention": "Thin out culms for better aeration."
    },
    "bamboo_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "cactus_rot": {
        "curable": "No",
        "pesticide": "None",
        "prevention": "Do NOT overwater, ensure gritty dry soil."
    },
    "cactus_healthy": {
        "curable": "Not needed",
        "pesticide": "-",
        "prevention": "Healthy crop."
    },
    "rhubarb_crown_rot": {
        "curable": "No",
    }
}

# Automatically add generic disease fallback entries for newly added crops
# This maps the generic features (e.g. "{plant}_leaf_spot") to actionable data.
_GENERIC_CROPS = [
    "wheat", "millets", "barley", "oats",
    "lentils", "chickpeas", "moong", "peas", "soybean", "mustard", "groundnut", "sunflower", "castor",
    "cotton", "sugarcane", "jute", "tobacco",
    "tea", "coffee", "rubber", "coconut",
    "onion", "cauliflower", "garlic", "mango", "banana", "grapes", "citrus",
    "spices", "medicinal", "tapioca",
    "berries", "bamboo", "cactus", "rhubarb"
]

for crop in _GENERIC_CROPS:
    DISEASE_DB[f"{crop}_leaf_spot"] = {
        "curable": "Yes",
        "pesticide": "Broad-spectrum fungicide (e.g. Mancozeb, Copper-based)",
        "prevention": "Improve air circulation, avoid overhead watering, and remove infected leaves."
    }
    DISEASE_DB[f"{crop}_nutrient_deficiency"] = {
        "curable": "Yes",
        "pesticide": "Apply balanced NPK fertilizer with micronutrients",
        "prevention": "Test soil regularly, maintain proper pH, and ensure consistent watering."
    }

def read_image_cv(path):
    if not HAS_ML_DEPS or cv2 is None or np is None or Image is None:
        raise Exception("Machine Learning dependencies (opencv-python, numpy, Pillow) are not installed.")
        
    # return image as BGR (OpenCV) and RGB (PIL style)
    bgr = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if bgr is None:
        # fallback to PIL open -> convert to cv2 format
        pil = Image.open(path).convert("RGB")
        rgb = np.array(pil)
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return bgr, rgb

def compute_features(rgb):
    if not HAS_ML_DEPS or cv2 is None or np is None:
        raise Exception("Machine Learning dependencies (opencv-python, numpy, Pillow) are not installed.")
        
    # rgb is HxWx3 numpy uint8
    h, w = rgb.shape[:2]
    total = h * w

    # Convert to HSV for color-based heuristics
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    h_ch, s_ch, v_ch = cv2.split(hsv)

    # Green mask: hue between 25 and 100 roughly
    green_mask = cv2.inRange(hsv, (25, 40, 40), (100, 255, 255))
    green_ratio = np.count_nonzero(green_mask) / total

    # Brown/dark spots mask: low V and moderate S, or red/brown hues
    brown_mask1 = cv2.inRange(hsv, (5, 60, 20), (30, 255, 200))   # brown/yellow range
    dark_mask = cv2.inRange(hsv, (0, 0, 0), (180, 255, 60))
    brown_mask = cv2.bitwise_or(brown_mask1, dark_mask)
    brown_ratio = np.count_nonzero(brown_mask) / total

    # Yellow mask (nutrient issues / mosaic)
    yellow_mask = cv2.inRange(hsv, (15, 60, 60), (35, 255, 255))
    yellow_ratio = np.count_nonzero(yellow_mask) / total

    # Spot detection: find contours on brown mask after morphology
    kernel = np.ones((5,5), np.uint8)
    clean = cv2.morphologyEx(brown_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    contours, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    spot_count = 0
    spot_areas = []
    for c in contours:
        a = cv2.contourArea(c)
        if a > 30:                # filter noise - threshold depends on image resolution
            spot_count += 1
            spot_areas.append(a)
    avg_spot_area = float(np.mean(spot_areas)) if len(spot_areas)>0 else 0.0  # type: ignore

    # Leaf bounding box aspect ratio (to help decide rice vs tomato)
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    _, thr = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
    thr = cv2.morphologyEx(thr, cv2.MORPH_CLOSE, np.ones((5,5),np.uint8))
    contours2, _ = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours2:
        c = max(contours2, key=cv2.contourArea)  # type: ignore
        x,y,ww,hh = cv2.boundingRect(c)
        aspect = hh / (ww+1e-6)
        leaf_area_ratio = cv2.contourArea(c) / total
    else:
        aspect = 1.0
        leaf_area_ratio = 0.0

    features = {
        "green_ratio": green_ratio,
        "brown_ratio": brown_ratio,
        "yellow_ratio": yellow_ratio,
        "spot_count": spot_count,
        "avg_spot_area": avg_spot_area,
        "aspect": aspect,
        "leaf_area_ratio": leaf_area_ratio
    }
    return features

def classify_plant_and_disease(features, plant_type=None):
    if plant_type:
        plant = plant_type
    else:
        # PLANT: rice leaves tend to be long & narrow -> high aspect ratio
        aspect = features["aspect"]
        leaf_area = features["leaf_area_ratio"]
        # if leaf is very long (aspect > 2.0) and area smallish -> rice
        if aspect > 0.45 and leaf_area < 0.15:
            plant = "rice"
        else:
            plant = "tomato"

    # DISEASE rules (heuristics)
    g = features["green_ratio"]
    b = features["brown_ratio"]
    y = features["yellow_ratio"]
    sc = features["spot_count"]
    avgA = features["avg_spot_area"]

    # Default healthy checks
    if g > 0.60 and b < 0.03 and y < 0.04:
        # mostly green
        disease = f"{plant}_healthy"
        conf = min(99.0, g * 100)
        return plant, disease, conf

    if plant == "rice":
        # Rice rules
        if sc >= 8 and avgA > 300:
            disease = "rice_bacterial_leaf_blight"
            conf = min(95.0, 40 + b*200 + sc*2)
        elif b > 0.05 and sc >= 4:
            disease = "rice_brown_spot"
            conf = min(94.0, 30 + b*200 + sc*3)
        elif y > 0.05 and g < 0.5:
            disease = "rice_hispa"
            conf = min(90.0, 20 + y*200)
        else:
            disease = "rice_healthy"
            conf = max(30.0, (1 - b) * 70)
    elif plant == "tomato":
        # Tomato rules
        if sc >= 10 and avgA < 400 and b > 0.03:
            disease = "tomato_bacterial_spot"
            conf = min(95.0, 30 + sc*2 + b*200)
        elif b > 0.12 and avgA > 600:
            disease = "tomato_late_blight"
            conf = min(96.0, 40 + b*160)
        elif y > 0.12 and g < 0.5 and sc < 5:
            disease = "tomato_mosaic_virus"
            conf = min(92.0, 35 + y*200)
        elif b > 0.04 and sc >= 5:
            disease = "tomato_leaf_mold"
            conf = min(90.0, 25 + b*150)
        elif sc >= 15 and avgA < 200:
            disease = "tomato_spider_mites"
            conf = min(92.0, 30 + sc)
        else:
            disease = "tomato_healthy"
            conf = max(20.0, (1 - b)*70)
    elif plant == "corn":
        # Corn rules
        if b > 0.1 and sc > 5:
            disease = "corn_northern_leaf_blight"
            conf = min(94.0, 30 + b*200)
        elif y > 0.05 and sc >= 8:
            disease = "corn_common_rust"
            conf = min(92.0, 40 + y*180)
        else:
            disease = "corn_healthy"
            conf = max(30.0, (1 - b) * 70)
    elif plant == "potato":
        # Potato rules
        if b > 0.15:
            disease = "potato_late_blight"
            conf = min(95.0, 40 + b*160)
        elif b > 0.05 and sc >= 5:
            disease = "potato_early_blight"
            conf = min(92.0, 30 + b*200)
        else:
            disease = "potato_healthy"
            conf = max(30.0, (1 - b)*70)
    else:
        # Generic rules for other crops
        if b > 0.15 or sc > 10:
            disease = f"{plant}_leaf_spot"
            conf = min(90.0, 40 + b*100)
        elif y > 0.15:
            disease = f"{plant}_nutrient_deficiency"
            conf = min(85.0, 30 + y*100)
        else:
            disease = f"{plant}_healthy"
            conf = max(20.0, (1 - b)*70)

    return plant, disease, round(float(conf), 2)  # type: ignore
