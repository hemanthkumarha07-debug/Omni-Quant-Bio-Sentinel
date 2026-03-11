import json
import pyotp
import requests
import yfinance as yf
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from SmartApi import SmartConnect
from .ai_agents import OmniQuantSpecialist

# --- OMNIQUANT SYSTEM CONFIGURATION ---
SMART_API_KEY = "r7a07H6a"
SMART_CLIENT_ID = "H50438594" 
SMART_PASSWORD = "2004"  
SMART_TOTP_SECRET = "DIK6P2BZAWOPCWOP226FNTY7AE" 
# ---------------------------------------

def landing(request):
    """Renders the Biometric Vault entrance."""
    return render(request, 'core/vault.html')

def dashboard(request):
    """Renders the main Glass-JARVIS Dashboard."""
    return render(request, 'core/dashboard.html')


def get_ai_insight(request):
    """
    Bulletproof API Route: Feeds data to the AI without crashing.
    """
    symbol = request.GET.get('symbol', 'RELIANCE').upper().strip()
    segment = request.GET.get('segment', 'STOCKS').upper()
    ear = float(request.GET.get('ear', 0.28))

    try:
        # 1. SMART PROXY ROUTING FOR YFINANCE
        # 1. SMART PROXY ROUTING FOR YFINANCE
        if segment == 'STOCKS':
            ticker_str = f"{symbol}.NS" if symbol not in ['AAPL', 'TSLA', 'MSFT'] else symbol
        elif segment == 'COMMODITY':
            ticker_str = {"GOLD": "GC=F", "SILVER": "SI=F", "CRUDE": "CL=F"}.get(symbol, f"{symbol}=F")
        elif segment == 'OPTIONS':
            ticker_str = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "FINNIFTY": "^CNXFIN"}.get(symbol, symbol)
        elif segment == 'CRYPTO':
            ticker_str = f"{symbol}-USD"
        elif segment == 'BONDS':   # <-- ADD THIS BLOCK
            ticker_str = {"US10Y": "^TNX", "US02Y": "^IRX", "IN10Y": "^IN10YT=RR"}.get(symbol, symbol)
        else:
            ticker_str = f"{symbol}INR=X"

        # 2. FETCH DATA
        ticker = yf.Ticker(ticker_str)
        df = ticker.history(period="1mo", interval="1d")
        
        price_data = []
        if not df.empty:
            for _, row in df.iterrows():
                price_data.append({
                    "close": round(row['Close'], 2), 
                    "high": round(row['High'], 2), 
                    "low": round(row['Low'], 2)
                })
        else:
            # Fallback so the AI doesn't crash if data is missing
            price_data = [{"close": 0, "high": 0, "low": 0}, {"close": 0, "high": 0, "low": 0}]

        # 3. GENERATE INTELLIGENCE
        response = OmniQuantSpecialist.generate_intelligence(
            segment=segment, 
            symbol=symbol, 
            price_data=price_data, 
            news_data=[], # Passing empty to speed up AI inference, as news is loaded separately in HUD
            ear_score=ear
        )
        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"status": "ERROR", "insight": f"> ERROR PROCESSING DATA: {str(e)}"})


def get_market_news(request):
    """
    High-Availability News Fetcher with API Key Rotation & yfinance Fallback.
    """
    symbol = request.GET.get('symbol', 'RELIANCE').upper().strip()
    clean_symbol = symbol.split('.')[0] # Remove .NS for API compatibility

    # 1. API KEY ROTATION VAULT
    API_KEYS = [
        "62y0imCj5G1e0pTXbevxMPd7MEI6V6kBNNiFN5wE", # Primary Key (from user prompt)
        "2UiPVeqpoHRI7h0gs2caA5b2OaMRV4ajI5iAUEew",               # Fallback 1
        "FGQ4INmP4ixQSj6PxD9uk6XmapRLjaOGeVXXje1W",                       # Fallback 2
        "YGwPgSerbDqVe1NsW5bCWn9gIiX9OYrmpO4RYdlt"                       # Fallback 3
    ]

    formatted_news = []

    # 2. ATTEMPT PRIMARY API WITH FAILOVER
    for key in API_KEYS:
        if key.startswith("YOUR_"): 
            continue # Skip unfilled placeholder keys

        try:
            url = f"https://api.marketaux.com/v1/news/all?symbols={clean_symbol}&filter_entities=true&language=en&api_token={key}"
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    for item in data["data"][:4]:
                        formatted_news.append({
                            "title": item.get("title", "Market Update"),
                            "url": item.get("url", "#"),
                            "source": item.get("source", "MarketAux"),
                            "sentiment": item.get("entities", [{}])[0].get("sentiment_score", 0) if item.get("entities") else 0
                        })
                    break # SUCCESS: Break the loop
                
            elif response.status_code == 429:
                print(f"[SYSTEM] NEWS API Rate Limit hit on key ending in ...{key[-4:]}. Rotating...")
                continue # Try the next key
            else:
                continue

        except requests.exceptions.RequestException:
            continue

    # 3. THE ULTIMATE FALLBACK (If all API keys are exhausted)
    if not formatted_news:
        print(f"[SYSTEM] Engaging yfinance fallback for {symbol}.")
        try:
            yf_symbol = symbol
            if symbol in ["GOLD", "SILVER", "CRUDE"]:
                yf_symbol = {"GOLD": "GC=F", "SILVER": "SI=F", "CRUDE": "CL=F"}.get(symbol)
            elif symbol in ["NIFTY", "BANKNIFTY", "FINNIFTY"]:
                yf_symbol = {"NIFTY": "^NSEI", "BANKNIFTY": "^NSEBANK", "FINNIFTY": "^CNXFIN"}.get(symbol)
            elif symbol in ["US10Y", "US02Y", "IN10Y"]:  # <-- ADD THIS BLOCK
                yf_symbol = {"US10Y": "^TNX", "US02Y": "^IRX", "IN10Y": "^IN10YT=RR"}.get(symbol)
            elif symbol not in ['AAPL', 'TSLA', 'MSFT'] and not symbol.endswith('.NS'):
                yf_symbol = f"{symbol}.NS"

            ticker = yf.Ticker(yf_symbol)
            raw_news = ticker.news
            
            if raw_news:
                for item in raw_news[:4]:
                    formatted_news.append({
                        "title": item.get("title", "Market Update"),
                        "url": item.get("link", "#"),
                        "source": item.get("publisher", "Yahoo Finance"),
                        "sentiment": 1 
                    })
        except Exception as e:
            print(f"[NEWS UPLINK ERROR]: {e}")

    # 4. FINAL FAILSAFE
    if not formatted_news:
        formatted_news.append({
            "title": f"No recent targeted intelligence found for {symbol}. Monitoring broader sector liquidity.",
            "url": "#",
            "source": "OMNI_QUANT_SYS",
            "sentiment": 0
        })

    return JsonResponse({"news": formatted_news})


@csrf_exempt
def analyze_biometrics(request):
    """Receives EAR uplink from Sentinel.js."""
    return JsonResponse({"status": "STABLE", "ear": 0.28})

@csrf_exempt
def tradingview_webhook(request):
    """Webhook for TradingView Alerts."""
    return JsonResponse({"status": "ACKNOWLEDGED"})


def get_market_data(request):
    """
    Dynamic Market Data Engine.
    NOTE: Currently bypassed by TradingView Widget on the frontend, 
    but kept active as a backend fallback API.
    """
    query = request.GET.get('symbol', '').upper().strip()
    segment = request.GET.get('segment', 'STOCKS').upper()
    
    if not query:
        return JsonResponse({"error": "No query provided."}, status=400)

    chart_data = []

    try:
        # PATH A: OPTIONS (Explicit Broker Path)
        if segment == 'OPTIONS':
            smart_api = SmartConnect(api_key=SMART_API_KEY)
            totp = pyotp.TOTP(SMART_TOTP_SECRET).now()
            session = smart_api.generateSession(SMART_CLIENT_ID, SMART_PASSWORD, totp)
            
            if not session.get('status'):
                return JsonResponse({"error": f"Broker Auth Failed: {session.get('message')}"}, status=401)

            symbol_token = "3045" 
            params = {
                "exchange": "NSE",
                "symboltoken": symbol_token,
                "interval": "ONE_DAY",
                "fromdate": "2026-02-11 09:15",
                "todate": "2026-03-11 15:30"
            }
            
            response_data = smart_api.getCandleData(params)
            if response_data.get('status') and response_data.get('data'):
                for c in response_data['data']:
                    chart_data.append({
                        "time": c[0].split('T')[0],
                        "open": c[1], "high": c[2], "low": c[3], "close": c[4]
                    })
                return JsonResponse({"symbol": query, "data": chart_data})
            return JsonResponse({"error": "No data from Broker for this token."}, status=404)

        # PATH B: STANDARD ASSETS
        else:
            search_candidates = []
            
            if segment == 'STOCKS':
                search_candidates = [f"{query}.NS", query, f"{query}.BO"]
            elif segment == 'FOREX':
                search_candidates = [f"{query}=X", f"{query}INR=X", f"{query}USD=X"]
            elif segment == 'CRYPTO':
                search_candidates = [f"{query}-USD", f"{query}-INR", query]
            elif segment == 'COMMODITY':
                commodity_map = {"GOLD": "GC=F", "SILVER": "SI=F", "CRUDE": "CL=F", "NATGAS": "NG=F", "COPPER": "HG=F", "ALUMINUM": "ALI=F"}
                target = commodity_map.get(query, f"{query}=F")
                search_candidates = [target]
            else:
                search_candidates = [query]

            df = None
            final_symbol = ""

            for symbol in search_candidates:
                ticker = yf.Ticker(symbol)
                df = ticker.history(period="1mo", interval="1d")
                if not df.empty:
                    final_symbol = symbol
                    break
            
            if df is None or df.empty:
                return JsonResponse({"error": f"Asset '{query}' not found."}, status=404)

            for index, row in df.iterrows():
                chart_data.append({
                    "time": index.strftime('%Y-%m-%d'),
                    "open": round(row['Open'], 2),
                    "high": round(row['High'], 2),
                    "low": round(row['Low'], 2),
                    "close": round(row['Close'], 2)
                })
            
            return JsonResponse({"symbol": final_symbol, "data": chart_data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)