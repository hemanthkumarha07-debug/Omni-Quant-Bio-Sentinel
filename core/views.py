from django.shortcuts import render
from django.http import JsonResponse
from .ai_agents import OmniQuantSpecialist

def landing(request):
    """Renders the Systems 3.2 Vault entrance."""
    return render(request, 'core/vault.html')

def dashboard(request):
    """Renders the main Fusion Art Dashboard."""
    return render(request, 'core/dashboard.html')

def get_ai_insight(request):
    """API endpoint for the AI Sentinel card."""
    segment = request.GET.get('segment', 'STOCKS')
    ear = float(request.GET.get('ear', 0.25))
    
    # Mock market data for the reasoning engine
    mock_data = {'delta': 0.68, 'volatility': 'High'}
    
    # Generate insight using the newly upgraded specialist
    response = OmniQuantSpecialist.generate_intelligence(segment, ear, mock_data)
    return JsonResponse(response)