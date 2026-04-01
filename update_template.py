import os

combined_html = """{% extends 'homepage/home.html' %}
{% load static %}

{% block content %}
<link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
<style>
/* Global Dashboard Settings */
.analysis-section {
    padding: 30px;
    max-width: 1400px;
    margin: 0 auto;
}
.nav-pills .nav-link {
    font-size: 1.1rem;
    padding: 15px;
    border-radius: 10px;
    color: var(--text-secondary);
    background: var(--bg-card);
    margin: 0 5px;
    font-weight: 500;
    transition: all 0.3s;
    border: 1px solid var(--border);
}
.nav-pills .nav-link.active {
    background: var(--accent);
    color: white;
    border-color: var(--accent);
    box-shadow: var(--shadow-glow);
}
.nav-pills .nav-link:hover:not(.active) {
    background: var(--bg-card-hover);
    color: var(--text-primary);
}

/* === CLIMATE STYLES === */
.weather-card {
    background: var(--bg-card);
    border-radius: 15px;
    padding: 25px;
    margin-bottom: 30px;
    box-shadow: var(--shadow-md);
    transition: transform 0.3s ease;
    border-top: 5px solid var(--accent);
    border-left: 1px solid var(--border);
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    color: var(--text-primary);
}
.weather-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-glow); border-color: var(--accent); }
.city-name { font-size: 1.5rem; font-weight: bold; color: var(--accent); margin-bottom: 15px; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
.weather-detail { display: flex; align-items: center; margin-bottom: 12px; font-size: 1.1rem; color: var(--text-secondary); }
.weather-detail i { font-size: 1.5rem; margin-right: 15px; color: var(--accent); width: 30px; text-align: center; }
.temp-val { font-weight: bold; color: #f43f5e; }
.hum-val { font-weight: bold; color: #3b82f6; }
.rain-val { font-weight: bold; color: #0ea5e9; }
.wind-val { font-weight: bold; color: #94a3b8; }
.loading-spinner { display: none; margin-left: 10px; width: 1.5rem; height: 1.5rem; }
.day-badge { display: inline-block; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: bold; margin-bottom: 15px; text-transform: uppercase; }
.badge-past { background-color: rgba(255,255,255,0.05); color: var(--text-muted); border: 1px solid rgba(255,255,255,0.1); }
.badge-present { background-color: var(--accent-light); color: var(--accent); border: 1px solid var(--accent); }
.badge-future { background-color: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); }

/* === RECOMMENDER STYLES === */
.recommender-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 20px; box-shadow: var(--shadow-md); padding: 40px; color: var(--text-primary); }
.form-group { margin-bottom: 24px; text-align: left; }
.form-group label { display: block; font-size: 14px; font-weight: 600; color: var(--text-secondary); margin-bottom: 8px; }
.form-group select { width: 100%; padding: 14px 16px; font-size: 15px; background: var(--bg-input); border: 1px solid var(--border); color: var(--text-primary); border-radius: 12px; outline: none; transition: all 0.2s; }
.form-group select:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-light); }
.form-group option { color: var(--text-primary); background: var(--bg-input); }
.submit-btn { width: 100%; padding: 16px; background: var(--accent); color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; transition: all 0.2s; display: flex; justify-content: center; gap: 8px; cursor: pointer; }
.submit-btn:hover { background: var(--accent-hover); box-shadow: var(--shadow-glow); transform: translateY(-2px); }
.result-box { margin-top: 30px; padding: 24px; background: var(--accent-light); border: 1px dashed var(--accent); border-radius: 16px; text-align: center; }
.result-title { font-size: 14px; color: var(--accent); font-weight: 600; text-transform: uppercase; margin-bottom: 12px; }
.result-items { font-size: 24px; font-weight: 700; display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
.crop-pill { background: var(--bg-card); border: 2px solid var(--accent); color: var(--accent); padding: 6px 16px; border-radius: 30px; font-size: 18px; box-shadow: var(--shadow-sm); }

/* === DISEASE STYLES === */
.disease-bg { background: var(--bg-secondary); border-radius: 20px; padding: 30px; color: var(--text-primary); border: 1px solid var(--border); }
.glass-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 20px; padding: 30px; margin-bottom: 30px; box-shadow: var(--shadow-md); }
.glass-card h2 { font-size: 22px; color: var(--text-primary); margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 10px; }
.btn-scan { background: var(--accent); border: none; color: white; padding: 12px 30px; border-radius: 30px; font-weight: 600; transition: all 0.3s; width: 100%; cursor: pointer; }
.btn-scan:hover { background: var(--accent-hover); box-shadow: var(--shadow-glow); transform: translateY(-2px); }
.preview-img { max-width: 100%; max-height: 300px; border-radius: 12px; margin-bottom: 20px; display: none; border: 1px solid var(--border); }
.result-item { background: var(--surface); padding: 15px 20px; border-radius: 12px; border-left: 4px solid var(--accent); margin-bottom: 15px; }
.result-label { font-size: 12px; text-transform: uppercase; color: var(--text-secondary); margin-bottom: 5px; }
.result-value { font-size: 18px; font-weight: 500; color: var(--text-primary); }
.feature-badge { display: inline-block; background: var(--surface); padding: 8px 15px; border-radius: 20px; margin: 5px; font-size: 13px; color: var(--text-secondary); border: 1px solid var(--border); }
</style>

<div class="analysis-section">
    <div class="text-center mb-5">
        <h1 style="color: var(--text-primary); font-weight: 700;">Farm Analysis Dashboard</h1>
        <p style="color: var(--text-secondary);">Comprehensive AI-powered tools for climate tracking, crop planning, and disease diagnosis.</p>
    </div>

    <!-- Navigation Tabs -->
    <ul class="nav nav-pills nav-fill mb-5" id="analysisTabs" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link {% if active_tab == 'climate' %}active{% endif %}" data-bs-toggle="tab" data-bs-target="#climate" type="button" role="tab">
                <i class='bx bx-cloud-light-rain'></i> Daily Climate
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link {% if active_tab == 'recommender' %}active{% endif %}" data-bs-toggle="tab" data-bs-target="#recommender" type="button" role="tab">
                <i class='bx bx-brain'></i> Crop Recommender
            </button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link {% if active_tab == 'disease' %}active{% endif %}" data-bs-toggle="tab" data-bs-target="#disease" type="button" role="tab">
                <i class='bx bx-scan'></i> AI Disease Analysis
            </button>
        </li>
    </ul>

    <!-- Tab Contents -->
    <div class="tab-content" id="analysisTabsContent">
        
        <!-- 1. CLIMATE TAB -->
        <div class="tab-pane fade {% if active_tab == 'climate' %}show active{% endif %}" id="climate" role="tabpanel">
            {% if not show_results %}
            <div class="row justify-content-center">
                <div class="col-md-8 col-lg-6">
                    <div class="weather-card text-center">
                        <h2 style="color: var(--accent); margin-bottom: 30px;"><i class='bx bx-search-alt'></i> Select Region</h2>
                        <form method="GET" action="{% url 'homepage:analysis-dashboard' %}">
                            <input type="hidden" name="action" value="climate">
                            <div class="mb-4 text-start">
                                <label for="country" class="form-label fw-bold text-secondary">
                                    1. Select Country 
                                    <div class="spinner-border text-success spinner-border-sm loading-spinner" id="country-loader" role="status"></div>
                                </label>
                                <select class="form-select" id="country" name="country">
                                    <option value="">-- Choose Country --</option>
                                </select>
                            </div>
                            
                            <div class="mb-4 text-start" id="state-container" style="display: none;">
                                <label for="state" class="form-label fw-bold text-secondary">
                                    2. Select State
                                    <div class="spinner-border text-success spinner-border-sm loading-spinner" id="state-loader" role="status"></div>
                                </label>
                                <select class="form-select" id="state" name="state">
                                    <option value="">-- Choose State --</option>
                                </select>
                            </div>

                            <div class="mb-5 text-start" id="district-container" style="display: none;">
                                <label for="district" class="form-label fw-bold text-secondary">
                                    3. Select District/City
                                    <div class="spinner-border text-success spinner-border-sm loading-spinner" id="district-loader" role="status"></div>
                                </label>
                                <select class="form-select" id="district" name="district">
                                    <option value="">-- Choose District --</option>
                                </select>
                            </div>
                            
                            <button type="submit" class="btn btn-success btn-lg w-100" id="search-btn" disabled>View Analysis</button>
                        </form>
                    </div>
                </div>
            </div>
            {% else %}
            <!-- Weather Results -->
            <div class="text-center mb-4">
                <a href="{% url 'homepage:analysis-dashboard' %}?action=climate" class="btn btn-outline-success btn-sm mb-3"><i class='bx bx-search'></i> Search Another Region</a>
                <h3 style="color: var(--text-primary);">7-Day Climate Analysis for {{ weather_data.city }}, {{ state }}, {{ country }}</h3>
            </div>
            
            <div class="row justify-content-center mb-5">
                <div class="col-md-8">
                    <div class="weather-card" style="background: linear-gradient(135deg, var(--bg-card), var(--bg-card-hover)); border-top: none;">
                        <h4 class="text-center mb-4" style="color: var(--accent);"><i class='bx bx-broadcast'></i> Real-Time Current Conditions</h4>
                        <div class="row text-center">
                            <div class="col-6 col-md-3 mb-3"><i class='bx bxs-thermometer' style="font-size: 2rem; color: #f43f5e;"></i><div class="fw-bold mt-2">Temp</div><div style="color: var(--text-secondary);">{{ weather_data.current.temperature }} °C</div></div>
                            <div class="col-6 col-md-3 mb-3"><i class='bx bx-water' style="font-size: 2rem; color: #3b82f6;"></i><div class="fw-bold mt-2">Humidity</div><div style="color: var(--text-secondary);">{{ weather_data.current.humidity }} %</div></div>
                            <div class="col-6 col-md-3 mb-3"><i class='bx bx-cloud-drizzle' style="font-size: 2rem; color: #0ea5e9;"></i><div class="fw-bold mt-2">Rainfall</div><div style="color: var(--text-secondary);">{{ weather_data.current.rainfall }} mm</div></div>
                            <div class="col-6 col-md-3 mb-3"><i class='bx bx-wind' style="font-size: 2rem; color: #94a3b8;"></i><div class="fw-bold mt-2">Wind</div><div style="color: var(--text-secondary);">{{ weather_data.current.wind_speed }} km/h</div></div>
                        </div>
                    </div>
                </div>
            </div>

            <h4 class="mb-4 text-secondary border-bottom pb-2">Analysis Breakdown</h4>
            <div class="row">
                {% for day in weather_data.forecast %}
                <div class="col-lg-4 col-md-6 mb-4">
                    <div class="weather-card h-100">
                        {% if day.day_type == "Previous Day" %}
                            <div class="day-badge badge-past"><i class='bx bx-history'></i> {{ day.day_type }}</div>
                        {% elif day.day_type == "Present Day" %}
                            <div class="day-badge badge-present"><i class='bx bx-calendar-star'></i> {{ day.day_type }}</div>
                        {% else %}
                            <div class="day-badge badge-future"><i class='bx bx-fast-forward'></i> {{ day.day_type }}</div>
                        {% endif %}
                        <div class="city-name" style="font-size: 1.2rem;"><i class='bx bx-calendar'></i> {{ day.weekday }} <span style="font-size: 0.9rem; color: var(--text-secondary); font-weight: normal; margin-left: 10px;">{{ day.date }}</span></div>
                        <div class="weather-detail mt-3"><i class='bx bxs-up-arrow-circle text-danger'></i> <span>Max Temp: <span class="temp-val">{{ day.temp_max }} °C</span></span></div>
                        <div class="weather-detail"><i class='bx bxs-down-arrow-circle text-info'></i> <span>Min Temp: <span class="temp-val" style="color: #3b82f6;">{{ day.temp_min }} °C</span></span></div>
                        <div class="weather-detail"><i class='bx bx-cloud-drizzle'></i> <span>Daily Rain: <span class="rain-val">{{ day.rainfall }} mm</span></span></div>
                        <div class="weather-detail"><i class='bx bx-wind'></i> <span>Max Wind: <span class="wind-val">{{ day.wind_speed_max }} km/h</span></span></div>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>

        <!-- 2. RECOMMENDER TAB -->
        <div class="tab-pane fade {% if active_tab == 'recommender' %}show active{% endif %}" id="recommender" role="tabpanel">
            <div class="row justify-content-center">
                <div class="col-md-8">
                    <div class="recommender-card">
                        <h2 class="text-center mb-4"><i class='bx bx-brain text-success' style="color: var(--accent) !important;"></i> Smart Crop Recommender</h2>
                        <form method="POST" action="{% url 'homepage:analysis-dashboard' %}">
                            {% csrf_token %}
                            <input type="hidden" name="action" value="crop_recommendation">
                            
                            <div class="form-group">
                                <label>Soil Type</label>
                                <select name="soil" required>
                                    <option value="" disabled selected>Select Soil Parameter</option>
                                    <option value="Red">Red Soil</option>
                                    <option value="Black">Black Soil</option>
                                    <option value="Alluvial">Alluvial Soil</option>
                                    <option value="Loamy">Loamy Soil</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Season</label>
                                <select name="season" required>
                                    <option value="" disabled selected>Select Current Season</option>
                                    <option value="Summer">Summer (Zaid)</option>
                                    <option value="Winter">Winter (Rabi)</option>
                                    <option value="Monsoon">Monsoon (Kharif)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Water Availability</label>
                                <select name="water" required>
                                    <option value="" disabled selected>Select Water Supply</option>
                                    <option value="High">High (Abundant Irrigation)</option>
                                    <option value="Medium">Medium (Moderate Rain/Irrigation)</option>
                                    <option value="Low">Low (Dry/Rainfed)</option>
                                </select>
                            </div>
                            <button type="submit" class="submit-btn"><i class='bx bx-check-shield'></i> Get Recommendations</button>
                        </form>

                        {% if rec_submitted %}
                        <div class="result-box">
                            <div class="result-title"><i class='bx bx-check-circle'></i> Recommended Crops</div>
                            <div class="result-items">
                                {% for crop in recommendations %}
                                    <div class="crop-pill">{{ crop }}</div>
                                {% empty %}
                                    <div class="crop-pill">General Millets</div>
                                {% endfor %}
                            </div>
                        </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>

        <!-- 3. DISEASE TAB -->
        <div class="tab-pane fade {% if active_tab == 'disease' %}show active{% endif %}" id="disease" role="tabpanel">
            <div class="disease-bg">
                <div class="text-center mb-4">
                    <h2><i class='bx bx-scan'></i> AI Crop Disease Analysis</h2>
                    <p class="text-light opacity-75">Upload a clear image of a crop leaf to detect diseases instantly.</p>
                </div>

                {% if disease_error %}
                <div class="alert alert-danger"><i class='bx bx-error-circle'></i> {{ disease_error }}</div>
                {% endif %}

                <div class="row">
                    <div class="col-lg-{% if disease_result %}4{% else %}8 mx-auto{% endif %}">
                        <div class="glass-card text-center">
                            <h2><i class='bx bx-upload'></i> Upload Image</h2>
                            <form action="{% url 'homepage:analysis-dashboard' %}" method="POST" enctype="multipart/form-data">
                                {% csrf_token %}
                                <input type="hidden" name="action" value="disease_analysis">
                                <div class="mb-3 text-start">
                                    <label class="form-label text-light mb-1">Select Crop Type</label>
                                    <select class="form-control" name="plant_type" required>
                                        <option value="" disabled selected style="color: black;">Choose crop...</option>
                                        <optgroup label="Major Field Crops" style="color: black;">
                                            <option value="rice">Rice</option>
                                            <option value="wheat">Wheat</option>
                                            <option value="maize">Maize (Corn)</option>
                                            <option value="millets">Millets</option>
                                            <option value="barley">Barley</option>
                                            <option value="oats">Oats</option>
                                        </optgroup>
                                        <optgroup label="Pulses & Oilseeds" style="color: black;">
                                            <option value="lentils">Lentils</option>
                                            <option value="chickpeas">Chickpeas</option>
                                            <option value="moong">Moong</option>
                                            <option value="peas">Peas</option>
                                            <option value="soybean">Soybean</option>
                                            <option value="mustard">Mustard</option>
                                            <option value="groundnut">Groundnut</option>
                                            <option value="sunflower">Sunflower</option>
                                            <option value="castor">Castor</option>
                                        </optgroup>
                                        <optgroup label="Fiber & Industrial Crops" style="color: black;">
                                            <option value="cotton">Cotton</option>
                                            <option value="sugarcane">Sugarcane</option>
                                        </optgroup>
                                        <optgroup label="Plantation & Beverage" style="color: black;">
                                            <option value="tea">Tea</option>
                                            <option value="coffee">Coffee</option>
                                            <option value="coconut">Coconut</option>
                                        </optgroup>
                                        <optgroup label="Vegetables, Fruits" style="color: black;">
                                            <option value="potato">Potato</option>
                                            <option value="onion">Onion</option>
                                            <option value="tomato">Tomato</option>
                                            <option value="mango">Mango</option>
                                            <option value="banana">Banana</option>
                                        </optgroup>
                                    </select>
                                </div>
                                <div class="mb-3 text-start">
                                    <label class="form-label text-light mb-1">Upload Leaf Image</label>
                                    <input class="form-control" type="file" id="imageInput" name="image" accept="image/*" required onchange="previewFile()">
                                </div>
                                <img id="previewImage" class="preview-img" />
                                <button type="submit" class="btn-scan"><i class='bx bx-search-alt-2'></i> Analyze Leaf</button>
                            </form>
                        </div>
                    </div>

                    {% if disease_result %}
                    <div class="col-lg-8">
                        <div class="glass-card">
                            <h2><i class='bx bx-chart'></i> Analysis Report</h2>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="result-item"><div class="result-label">Detected Plant</div><div class="result-value text-capitalize">{{ disease_result.plant }}</div></div>
                                    <div class="result-item" {% if 'healthy' in disease_result.disease %}style="border-color: #4caf50;"{% else %}style="border-color: #f44336;"{% endif %}>
                                        <div class="result-label">Disease Status</div>
                                        <div class="result-value text-capitalize" {% if 'healthy' in disease_result.disease %}style="color: #a5d6a7;"{% else %}style="color: #ffab91;"{% endif %}>{{ disease_result.disease }}</div>
                                    </div>
                                    <div class="result-item">
                                        <div class="result-label">AI Confidence</div>
                                        <div class="progress mt-2" style="height: 10px; background: rgba(255,255,255,0.1);"><div class="progress-bar bg-success" style="width: {{ disease_result.confidence }}%;"></div></div>
                                        <div class="text-end mt-1 text-success fw-bold">{{ disease_result.confidence }}%</div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="result-item" style="border-color: #2196f3"><div class="result-label">Curable?</div><div class="result-value">{{ disease_result.curable }}</div></div>
                                    <div class="result-item" style="border-color: #ff9800"><div class="result-label">Recommended Pesticide</div><div class="result-value">{{ disease_result.pesticide }}</div></div>
                                    <div class="result-item" style="border-color: #9c27b0"><div class="result-label">Prevention Guidelines</div><div class="result-value" style="font-size: 14px">{{ disease_result.prevention }}</div></div>
                                </div>
                            </div>
                            
                            <h4 class="mt-4 mb-3" style="font-size: 16px; color: rgba(255,255,255,0.6);"><i class='bx bx-code-alt'></i> Extraction Data</h4>
                            <div class="d-flex flex-wrap">
                                <div class="feature-badge"><strong style="color:#a5d6a7">Green:</strong> {{ disease_result.features.green_ratio|floatformat:4 }}</div>
                                <div class="feature-badge"><strong style="color:#a5d6a7">Brown:</strong> {{ disease_result.features.brown_ratio|floatformat:4 }}</div>
                                <div class="feature-badge"><strong style="color:#a5d6a7">Spots:</strong> {{ disease_result.features.spot_count }}</div>
                            </div>
                        </div>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>

    </div>
</div>

<script>
    // Preview disease image
    function previewFile() {
        const preview = document.getElementById('previewImage');
        const file = document.getElementById('imageInput').files[0];
        const reader = new FileReader();
        reader.addEventListener("load", function () {
            preview.src = reader.result;
            preview.style.display = "block";
        }, false);
        if (file) reader.readAsDataURL(file);
    }

    // Climate API logic
    document.addEventListener('DOMContentLoaded', function() {
        const countrySelect = document.getElementById('country');
        const stateSelect = document.getElementById('state');
        const districtSelect = document.getElementById('district');
        if(!countrySelect) return; // if show_results is true, this form isn't present
        
        const stateContainer = document.getElementById('state-container');
        const districtContainer = document.getElementById('district-container');
        const searchBtn = document.getElementById('search-btn');
        const cl = document.getElementById('country-loader');
        const sl = document.getElementById('state-loader');
        const dl = document.getElementById('district-loader');

        cl.style.display = 'inline-block';
        fetch('https://countriesnow.space/api/v0.1/countries/states')
            .then(res => res.json())
            .then(result => {
                cl.style.display = 'none';
                if (!result.error) {
                    result.data.forEach(item => {
                        const option = document.createElement('option');
                        option.value = item.name;
                        option.textContent = item.name;
                        option.dataset.states = JSON.stringify(item.states);
                        countrySelect.appendChild(option);
                    });
                    const pc = "{{ country }}";
                    if (pc && pc !== "None") {
                        countrySelect.value = pc;
                        countrySelect.dispatchEvent(new Event('change'));
                    }
                }
            }).catch(() => cl.style.display = 'none');

        countrySelect.addEventListener('change', function() {
            stateSelect.innerHTML = '<option value="">-- Choose State --</option>';
            districtSelect.innerHTML = '<option value="">-- Choose District --</option>';
            districtContainer.style.display = 'none';
            searchBtn.disabled = true;

            if (this.value) {
                stateContainer.style.display = 'block';
                const ops = this.options[this.selectedIndex];
                const states = JSON.parse(ops.dataset.states || "[]");
                states.forEach(s => {
                    const option = document.createElement('option');
                    option.value = s.name;
                    option.textContent = s.name;
                    stateSelect.appendChild(option);
                });
                const ps = "{{ state }}";
                if (ps && ps !== "None") {
                    stateSelect.value = ps;
                    if(stateSelect.value) stateSelect.dispatchEvent(new Event('change'));
                }
            } else {
                stateContainer.style.display = 'none';
            }
        });

        stateSelect.addEventListener('change', function() {
            districtSelect.innerHTML = '<option value="">-- Choose District --</option>';
            searchBtn.disabled = true;
            if (this.value) {
                districtContainer.style.display = 'block';
                dl.style.display = 'inline-block';
                fetch('https://countriesnow.space/api/v0.1/countries/state/cities', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ country: countrySelect.value, state: this.value })
                }).then(r => r.json()).then(res => {
                    dl.style.display = 'none';
                    if (!res.error && res.data.length > 0) {
                        res.data.forEach(c => {
                            const o = document.createElement('option');
                            o.value = c; o.textContent = c;
                            districtSelect.appendChild(o);
                        });
                        const pd = "{{ district }}";
                        if (pd && pd !== "None") {
                            districtSelect.value = pd;
                            if(districtSelect.value) searchBtn.disabled = false;
                        }
                    } else {
                        const o = document.createElement('option');
                        o.value = this.value; o.textContent = "Whole State";
                        districtSelect.appendChild(o);
                    }
                }).catch(() => dl.style.display = 'none');
            } else {
                districtContainer.style.display = 'none';
            }
        });

        districtSelect.addEventListener('change', function() {
            searchBtn.disabled = !this.value;
        });
    });
</script>
{% endblock %}
"""

with open(r'd:\FARMER MANAGEMENT SYSTEM\My-Farm-Project\Farm_Management_System\homepage\templates\homepage\analysis_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(combined_html)

print("Template written successfully!")
