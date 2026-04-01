from django.urls import path  # type: ignore
from .views import (  # type: ignore
    Mainpage,
    Show_employees,
    Add_employees,
    Delete_employees,
    Update_employees,
    Show_crops,
    Add_crops,
    Update_crops,
    Delete_crops,
    Show_machinery,
    Add_machinery,
    Delete_machinery,
    Update_machinery,
    Update_machinery_maintenance,
    # Livestock Imports Removed
    Show_crop_expenses,
    Add_crop_expenses,
    Update_crop_expenses,
    Delete_crop_expenses,
    Show_crop_sales,
    Add_crop_sales,
    Delete_crop_sales,
    Update_crop_sales,
    Show_machinery_activities,
    Add_machinery_activities,
    Delete_machinery_activity,
    Update_machinery_activities,
    Show_machinery_maintenance,
    Add_machinery_maintenance,
    Delete_machinery_maintenance,
    Update_machinery_maintenance,

    Select_year_month,
    Milk_production_today,
    Milk_production_by_year,
    Milk_production_by_month,
    Add_milk_production_by_month,
    Delete_milk_production_by_month,
    Update_milk_production_by_month,

    Select_year_month_egg,
    Egg_production_today,
    Egg_production_by_year,
    Egg_production_record,
    Add_egg_production_by_month,
    Delete_egg_production_by_month,
    Update_egg_production_by_month,

    Help,
    crop_disease_analysis,
    daily_climate,
    api_weather,
    crop_recommendation,
    market_prices,
    api_historical_prices,
    analysis_dashboard,
    production_dashboard,
    reports_dashboard,
    settings_page,
    climate_analysis,
    profile_view,
    manage_contact
)

from homepage.farm_expense_views import (  # type: ignore
    show_farm_expenses,
    add_farm_expense,
    update_farm_expense,
    delete_farm_expense
)

from homepage.water_views import (  # type: ignore
    water_dashboard,
    add_water_schedule,
    start_watering,
    mark_completed,
    delete_water_schedule
)

from homepage.retail_views import (  # type: ignore
    retail_dashboard,
    show_retail_crop_sales, add_retail_crop_sale, update_retail_crop_sale, delete_retail_crop_sale,
    show_retail_egg_sales, add_retail_egg_sale, update_retail_egg_sale, delete_retail_egg_sale,
    show_retail_milk_sales, add_retail_milk_sale, update_retail_milk_sale, delete_retail_milk_sale,
    show_retail_machinery_renting, add_retail_machinery_renting, update_retail_machinery_renting, delete_retail_machinery_renting
)

app_name = "homepage"

urlpatterns = [
    path("mainpage/", Mainpage, name="mainpage"),
    path("analysis-dashboard/", analysis_dashboard, name="analysis-dashboard"),
    path("production-dashboard/", production_dashboard, name="production-dashboard"),
    path("reports-dashboard/", reports_dashboard, name="reports-dashboard"),
    path("crop-disease-analysis/", crop_disease_analysis, name="crop-disease-analysis"),
    path("daily-climate/", daily_climate, name="daily-climate"),
    path("climate-analysis/", climate_analysis, name="climate-analysis"),
    path("api/weather/", api_weather, name="api-weather"),
    path("crop-recommendation/", crop_recommendation, name="crop-recommendation"),
    path("market-prices/", market_prices, name="market-prices"),
    path("api/historical-prices/", api_historical_prices, name="api-historical-prices"),
    
    # Farm Expenses
    path("show-farm-expenses/", show_farm_expenses, name="show-farm-expenses"),
    path("add-farm-expense/", add_farm_expense, name="add-farm-expense"),
    path("update-farm-expense/<int:id>/", update_farm_expense, name="update-farm-expense"),
    path("delete-farm-expense/<int:id>/", delete_farm_expense, name="delete-farm-expense"),

    # Water Management
    path("water-dashboard/", water_dashboard, name="water-dashboard"),
    path("add-water-schedule/", add_water_schedule, name="add-water-schedule"),
    path("start-watering/<int:id>/", start_watering, name="start-watering"),
    path("mark-completed/<int:id>/", mark_completed, name="mark-completed"),
    path("delete-water-schedule/<int:id>/", delete_water_schedule, name="delete-water-schedule"),

    # Retail Operations
    path("retail-dashboard/", retail_dashboard, name="retail-dashboard"),
    
    path("show-retail-crop-sales/", show_retail_crop_sales, name="show-retail-crop-sales"),
    path("add-retail-crop-sale/", add_retail_crop_sale, name="add-retail-crop-sale"),
    path("update-retail-crop-sale/<int:id>/", update_retail_crop_sale, name="update-retail-crop-sale"),
    path("delete-retail-crop-sale/<int:id>/", delete_retail_crop_sale, name="delete-retail-crop-sale"),

    path("show-retail-egg-sales/", show_retail_egg_sales, name="show-retail-egg-sales"),
    path("add-retail-egg-sale/", add_retail_egg_sale, name="add-retail-egg-sale"),
    path("update-retail-egg-sale/<int:id>/", update_retail_egg_sale, name="update-retail-egg-sale"),
    path("delete-retail-egg-sale/<int:id>/", delete_retail_egg_sale, name="delete-retail-egg-sale"),

    path("show-retail-milk-sales/", show_retail_milk_sales, name="show-retail-milk-sales"),
    path("add-retail-milk-sale/", add_retail_milk_sale, name="add-retail-milk-sale"),
    path("update-retail-milk-sale/<int:id>/", update_retail_milk_sale, name="update-retail-milk-sale"),
    path("delete-retail-milk-sale/<int:id>/", delete_retail_milk_sale, name="delete-retail-milk-sale"),

    path("show-retail-machinery-renting/", show_retail_machinery_renting, name="show-retail-machinery-renting"),
    path('add-retail-machinery-renting/', add_retail_machinery_renting, name="add-retail-machinery-renting"),
    path('update-retail-machinery-renting/<int:id>/', update_retail_machinery_renting, name="update-retail-machinery-renting"),
    path('delete-retail-machinery-renting/<int:id>/', delete_retail_machinery_renting, name="delete-retail-machinery-renting"),

    # Retail Livestock Sales Removed

    path("show_employees/", Show_employees, name="show-employees"),
    path("add_employees/", Add_employees, name="add-employees"),
    path("delete_employees/<int:Eid>/", Delete_employees, name="delete-employees"),
    path("update_employees/<int:Eid>/", Update_employees, name="update-employees"),

    path("show_crops/", Show_crops, name="show-crops"),
    path("add-crops/", Add_crops, name="add-crops"),
    path("update_crops/<int:Cid>/", Update_crops, name="update-crops"),
    path("delete_crops/<int:Cid>/", Delete_crops, name="delete-crops"),

    path('show_machinery/', Show_machinery, name="show-machinery"),
    path("add-machinery/", Add_machinery, name="add-machinery"),
    path("delete_machinery/<str:Number_plate>/", Delete_machinery, name="delete-machinery",),
    path("update_machinery/<str:Number_plate>/", Update_machinery, name="update-machinery"),

    # Production Livestock Removed

    path('show_cropexpenses/<int:Cid>/', Show_crop_expenses, name='show-cropexpenses'),
    path('add_cropexpenses/<int:Cid>/', Add_crop_expenses, name="add-cropexpenses"),
    path('update_cropexpense/<int:Cid>/<slug:Expense_date>/', Update_crop_expenses, name='update-cropexpenses'),
    path('delete_cropexpenses/<int:Cid>/<slug:Expense_date>/', Delete_crop_expenses, name='delete-cropexpenses'),

    path('show_cropsales/<int:Cid>/', Show_crop_sales, name="show-cropsales"),
    path('add_cropsales/<int:Cid>/', Add_crop_sales, name='add-cropsales'),
    path('delete_cropsales/<int:Cid>/<slug:Sale_date>/', Delete_crop_sales, name='delete-cropsales'),
    path('update_cropsales/<int:Cid>/<slug:Sale_date>/', Update_crop_sales, name='update-cropsales'),

    path('show_machineryactivities/<str:Number_plate>/', Show_machinery_activities, name='show-machineryactivities'),
    path('add_machineryactivirties/<str:Number_plate>/', Add_machinery_activities, name="add-machineryactivities"),
    path('delete_machineryactivities/<str:Number_plate>/<slug:Activity_date>/', Delete_machinery_activity, name='delete-machineryactivities'),
    path('update_machineryactivities/<str:Number_plate>/<slug:Activity_date>/', Update_machinery_activities, name='update-machineryactivities'),

    path('show_machinerymaintenance/<str:Number_plate>/', Show_machinery_maintenance, name='show-machinerymaintenance'),
    path('add_machinerymaintenance/<str:Number_plate>/', Add_machinery_maintenance, name='add-machinerymaintenance'),
    path('delete_machinerymaintenance/<str:Number_plate>/<slug:Date>/', Delete_machinery_maintenance,name='delete-machinerymaintenance'),
    path('update_machinerymaintenance/<str:Number_plate>/<slug:Date>/', Update_machinery_maintenance, name='update-machinerymaintenance'),

    path('select_yearmonth/', Select_year_month, name='select-yearmonth'),
    path('milk_production/today/', Milk_production_today, name='milk-production-today'),
    path('milk_production/year/<int:selected_year>/', Milk_production_by_year, name='milk-productionbyyear'),
    path('milk_productionbymonth/<int:selected_year>/<int:selected_month>/', Milk_production_by_month, name='milk-productionbymonth'),
    path('add_milkproductionbymonth/<int:selected_year>/<int:selected_month>/', Add_milk_production_by_month, name='add-milkproductionbymonth'),
    path('delete_milkproductionbymonth/<int:selected_year>/<int:selected_month>/<int:Day>/', Delete_milk_production_by_month,name='delete-milkproductionbymonth'),
    path('update_milkproductionbymonth/<int:selected_year>/<int:selected_month>/<int:Day>/', Update_milk_production_by_month,name='update-milkproductionbymonth'),

    path('select_yearandmonth/', Select_year_month_egg, name='select-yearandmonth'),
    path('egg_production/today/', Egg_production_today, name='egg-production-today'),
    path('egg_production/year/<int:selected_year>/', Egg_production_by_year, name='egg-productionbyyear'),
    path('egg_productionrecord/<int:selected_year>/<int:selected_month>/', Egg_production_record, name='egg-productionrecord'),
    path('add_eggproductionbymonth/<int:selected_year>/<int:selected_month>/', Add_egg_production_by_month, name='add-eggproduction'),
    path('delete_eggproductionbymonth/<int:selected_year>/<int:selected_month>/<int:Day>/', Delete_egg_production_by_month, name='delete-eggproductionbymonth'),
    path('update_eggproductionbymonth/<int:selected_year>/<int:selected_month>/<int:Day>/',Update_egg_production_by_month, name='update-eggproduction'),

    path('help/', Help, name='help'),
    path('settings/', settings_page, name='settings'),
    path('profile/', profile_view, name='profile'),
    path('manage-contact/', manage_contact, name='manage_contact'),
]
