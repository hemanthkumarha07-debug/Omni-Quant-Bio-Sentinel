from django.contrib import admin
from django.urls import path
from core.views import landing, dashboard
# Add this line below to fix the NameError
from sentinel.views import analyze_biometrics 
from markets.views import get_live_greeks

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='vault'),
    path('dashboard/', dashboard, name='dashboard'),
    path('sentinel/analyze/', analyze_biometrics, name='analyze_biometrics'),
    path('markets/live-greeks/', get_live_greeks, name='live_greeks'),
]