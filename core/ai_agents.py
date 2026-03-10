import json

class OmniQuantSpecialist:
    """
    Trained Llama 3.2 Specialist Router.
    Logic: Fusion of Biometric Stability + Market Segment Specifics.
    """
    
    # Training Context for reasoning patterns
    SPECIALIST_RULES = {
        "STOCKS": "Focus on Delta (Δ) sensitivity and institutional volume.",
        "FOREX": "Focus on PIP volatility and interest rate differentials.",
        "CRYPTO": "Focus on liquidity gaps and funding rate anomalies.",
        "GENERAL": "If EAR < 0.22, trigger LOCKDOWN and ignore all technical data."
    }

    @classmethod
    def generate_intelligence(cls, segment, ear_score, market_data):
        # 1. Critical Biometric Check (The Circuit Breaker)
        if ear_score < 0.22:
            return {
                "status": "CRITICAL",
                "insight": "SYSTEM_LOCKDOWN: Physiological stress detected. AI Specialist has suspended all execution to preserve capital."
            }

        # 2. Segment-Specific Reasoning
        rule = cls.SPECIALIST_RULES.get(segment, cls.SPECIALIST_RULES["STOCKS"])
        
        # Simulated reasoning based on Greeks or Market Data
        if segment == "STOCKS":
            delta = market_data.get('delta', 0.5)
            trend = "BULLISH" if delta > 0.6 else "NEUTRAL"
            insight = f"TECHNICAL_AGENT ({segment}): {rule} Current Delta is {delta}. Trend is {trend}. Bio-Sentinel: OPTIMAL."
        
        elif segment == "FOREX":
            vol = market_data.get('volatility', 'Low')
            insight = f"MACRO_AGENT ({segment}): {rule} Market volatility is {vol}. Bio-Sentinel: OPTIMAL."
            
        else:
            insight = f"QUANT_AGENT ({segment}): Monitoring {segment} liquidity. {rule} Bio-Sentinel: OPTIMAL."

        return {"status": "STABLE", "insight": insight}

# Django View to serve this intelligence
from django.http import JsonResponse

def get_ai_insight(request):
    segment = request.GET.get('segment', 'STOCKS')
    ear = float(request.GET.get('ear', 0.25))
    # Mock market data for the reasoning engine
    mock_data = {'delta': 0.68, 'volatility': 'High'}
    
    response = OmniQuantSpecialist.generate_intelligence(segment, ear, mock_data)
    return JsonResponse(response)