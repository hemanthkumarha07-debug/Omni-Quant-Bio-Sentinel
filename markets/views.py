from django.http import JsonResponse
from .options_engine import OptionsGreeks # The math class we built earlier
import random

def get_live_greeks(request):
    """Generates simulated live Greek data for the dashboard."""
    # In a production app, you would fetch 'S' (Spot Price) from an API
    spot_price = 22450 + random.uniform(-10, 10)
    
    # We'll calculate Greeks for a few strike prices
    strikes = [22400, 22450, 22500]
    data = []
    
    for K in strikes:
        # Calculate using Black-Scholes: S, K, T (days/365), r, sigma
        greeks = OptionsGreeks.calculate_greeks(spot_price, K, 0.02, 0.07, 0.18)
        data.append({
            "strike": K,
            "ltp": round(spot_price + (K - spot_price) * 0.1, 2),
            "delta": greeks["delta"],
            "gamma": greeks["gamma"],
            "theta": greeks["theta"]
        })
        
    return JsonResponse({"greeks": data})