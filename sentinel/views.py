import base64
import cv2
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .biometrics import BioSentinelEngine
from command_center.models import SentinelLog

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