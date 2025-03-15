from django.shortcuts import render
from django.utils import timezone
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Distributor, Shipment, Forecast
import json
import random

def dashboard(request):
    """View for the main dashboard page"""
    return render(request, 'augur_app/dashboard.html')

@api_view(['GET'])
def get_distributors(request):
    """API endpoint to get all distributors with their metrics"""
    distributors = Distributor.objects.filter(active=True)
    data = []
    
    for distributor in distributors:
        data.append({
            'id': distributor.id,
            'name': distributor.name,
            'ytdAvg': distributor.ytd_average_shipment(),
            'lastMonth': distributor.last_month_shipment(),
            'forecast': get_forecast_for_distributor(distributor)
        })
    
    return Response(data)

@api_view(['GET'])
def get_distributor_details(request, distributor_id):
    """API endpoint to get detailed information for a specific distributor"""
    try:
        distributor = Distributor.objects.get(id=distributor_id, active=True)
    except Distributor.DoesNotExist:
        return Response({'error': 'Distributor not found'}, status=404)
    
    # Get monthly shipment data for the past year
    today = timezone.now()
    monthly_data = []
    
    for i in range(12):
        month = (today.month - i - 1) % 12 + 1
        year = today.year if month <= today.month else today.year - 1
        
        shipments = Shipment.objects.filter(
            distributor=distributor,
            shipment_date__month=month,
            shipment_date__year=year
        )
        
        quantity = shipments.aggregate(total=models.Sum('quantity'))['total'] or 0
        monthly_data.append({
            'month': month,
            'year': year,
            'quantity': quantity
        })
    
    # Reverse to get chronological order
    monthly_data.reverse()
    
    # Get forecast for next month
    next_month = (today.month % 12) + 1
    next_year = today.year if next_month > today.month else today.year + 1
    
    try:
        forecast = Forecast.objects.get(
            distributor=distributor,
            forecast_month=next_month,
            forecast_year=next_year
        )
        forecast_quantity = forecast.quantity
    except Forecast.DoesNotExist:
        forecast_quantity = 0
    
    return Response({
        'id': distributor.id,
        'name': distributor.name,
        'ytdAvg': distributor.ytd_average_shipment(),
        'lastMonth': distributor.last_month_shipment(),
        'forecast': forecast_quantity,
        'monthlyData': monthly_data
    })

def get_forecast_for_distributor(distributor):
    """Helper function to get forecast for a distributor"""
    today = timezone.now()
    next_month = (today.month % 12) + 1
    next_year = today.year if next_month > today.month else today.year + 1
    
    try:
        forecast = Forecast.objects.get(
            distributor=distributor,
            forecast_month=next_month,
            forecast_year=next_year
        )
        return forecast.quantity
    except Forecast.DoesNotExist:
        # If no forecast exists, return a placeholder value
        # In a real application, this would be handled differently
        return 0
