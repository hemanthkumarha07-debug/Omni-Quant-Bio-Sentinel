import base64
import cv2
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .biometrics import BioSentinelEngine
from command_center.models import SentinelLog
from markets.services.angel_auth import AngelOneAuthService
from django.views.decorators.http import require_POST
# Initialize engine globally to avoid reloading the 100MB .dat file on every request
engine = BioSentinelEngine()

@csrf_exempt
def analyze_biometrics(request):
    if request.method == "POST":
        data = json.loads(request.body)
        img_data = data.get('image').split(',')[1]
        
        # Decode image
        nparr = np.frombuffer(base64.b64decode(img_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Analyze
        status = engine.get_stress_status(frame)
    
    if status == "LOCKDOWN":
        SentinelLog.objects.create(
            event_type="STRESS_LOCKDOWN",
            ear_score=0.18, # Mock value for example
            market_snapshot={"delta": 0.65, "gamma": 0.0012},
            ai_recommendation="Circuit Breaker Engaged"
        )
    return JsonResponse({"status": status})

@csrf_exempt
@require_POST
def tradingview_webhook(request):
    try:
        # Parse the incoming JSON payload from TradingView
        payload = json.loads(request.body)
        
        # Extract variables from the payload
        action = payload.get('action')
        symbol = payload.get('symbol')
        quantity = payload.get('quantity')
        
        # Security: Verify the passphrase to ensure the request is actually from you
        passphrase = payload.get('passphrase')
        if passphrase != "YourSecureSecret123":
            return JsonResponse({"error": "Unauthorized"}, status=401)

        # Initialize broker connection
        # Note: In production, it's faster to pull an already-active JWT from a database/cache 
        # rather than logging in on every single webhook request.
        auth_service = AngelOneAuthService()
        token_data = auth_service.login_and_get_token()
        
        if token_data["success"]:
            # The logic to execute the trade via Angel One API goes here
            print(f"Executing {action} for {quantity} units of {symbol}")
            
            return JsonResponse({"status": "success", "message": "Signal received and processed"})
        else:
            return JsonResponse({"error": "Broker authentication failed"}, status=500)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)