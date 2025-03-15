from django.db import models
from django.utils import timezone

class Distributor(models.Model):
    """Model representing a distributor in the supply chain system"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def ytd_average_shipment(self):
        """Calculate year-to-date average quantity of goods shipped"""
        current_year = timezone.now().year
        shipments = self.shipment_set.filter(shipment_date__year=current_year)
        if not shipments.exists():
            return 0
        return shipments.aggregate(models.Avg('quantity'))['quantity__avg']
    
    def last_month_shipment(self):
        """Get the quantity of goods shipped last month"""
        today = timezone.now()
        last_month = today.month - 1 if today.month > 1 else 12
        year = today.year if today.month > 1 else today.year - 1
        shipments = self.shipment_set.filter(shipment_date__month=last_month, shipment_date__year=year)
        if not shipments.exists():
            return 0
        return shipments.aggregate(models.Sum('quantity'))['quantity__sum']

class Shipment(models.Model):
    """Model representing shipment data for distributors"""
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    shipment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.distributor.name} - {self.shipment_date} - {self.quantity}"

class Forecast(models.Model):
    """Model representing forecast data for distributors"""
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    forecast_month = models.PositiveSmallIntegerField()  # 1-12 for months
    forecast_year = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('distributor', 'forecast_month', 'forecast_year')
    
    def __str__(self):
        return f"{self.distributor.name} - {self.forecast_month}/{self.forecast_year} - {self.quantity}"
    
    @property
    def forecast_date(self):
        return f"{self.forecast_month}/{self.forecast_year}"
