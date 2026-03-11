from django.contrib import admin
from django.urls import path
from core.views import landing, dashboard
from core import views
from sentinel.views import analyze_biometrics 
from markets.views import get_live_greeks

urlpatterns = [
    # Django Admin Panel (For checking your Sentinel Logs later)
    path('admin/', admin.site.urls),

    # Main UI Routes
    path('', views.landing, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # API Routes for the J.A.R.V.I.S. HUD
    path('get-ai-insight/', views.get_ai_insight, name='ai_insight'),
    path('api/market-data/', views.get_market_data, name='market_data'),
    path('sentinel/analyze/', views.analyze_biometrics, name='analyze_biometrics'),
    path('webhook/tv/', views.tradingview_webhook, name='tradingview_webhook'),
    path('api/market-news/', views.get_market_news, name='market_news'),
    path('api/ai-insight/', views.get_ai_insight, name='ai_insight'),

]

