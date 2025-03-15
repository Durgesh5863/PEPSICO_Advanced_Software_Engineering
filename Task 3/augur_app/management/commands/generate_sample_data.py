import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from augur_app.models import Distributor, Shipment, Forecast

class Command(BaseCommand):
    help = 'Generates sample data for the Augur dashboard'

    def add_arguments(self, parser):
        parser.add_argument(
            '--distributors',
            type=int,
            default=6,
            help='Number of distributors to create'
        )

    def handle(self, *args, **options):
        num_distributors = options['distributors']
        self.stdout.write(self.style.SUCCESS(f'Generating {num_distributors} distributors with shipment and forecast data'))
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Forecast.objects.all().delete()
        Shipment.objects.all().delete()
        Distributor.objects.all().delete()
        
        # Create distributors
        distributors = []
        distributor_names = [
            'Northeast Distributors',
            'Southern Supply Chain',
            'Midwest Distribution',
            'Western Logistics',
            'Central Shipping',
            'Pacific Northwest Supply',
            'Atlantic Coast Delivery',
            'Great Lakes Distribution',
            'Southwest Logistics',
            'Mountain Region Supply'
        ]
        
        locations = [
            'New York', 'Atlanta', 'Chicago', 'Los Angeles', 'Dallas',
            'Seattle', 'Boston', 'Detroit', 'Phoenix', 'Denver'
        ]
        
        for i in range(min(num_distributors, len(distributor_names))):
            distributor = Distributor.objects.create(
                name=distributor_names[i],
                code=f'DIST{i+1:03d}',
                location=locations[i],
                active=True
            )
            distributors.append(distributor)
            self.stdout.write(f'Created distributor: {distributor.name}')
        
        # Generate shipment data for the past 12 months
        self.stdout.write('Generating shipment data for the past 12 months...')
        today = timezone.now().date()
        
        for distributor in distributors:
            base_quantity = random.randint(800, 2500)  # Base shipment quantity
            
            for month_offset in range(12):
                # Calculate the date for this month's data
                current_date = today.replace(day=15) - timedelta(days=30 * month_offset)
                
                # Add some randomness to the shipment quantity
                monthly_factor = 1 + (random.random() * 0.4 - 0.2)  # +/- 20%
                seasonal_factor = 1 + 0.15 * ((current_date.month % 12) / 12)  # Seasonal variation
                
                quantity = int(base_quantity * monthly_factor * seasonal_factor)
                
                Shipment.objects.create(
                    distributor=distributor,
                    quantity=quantity,
                    shipment_date=current_date
                )
            
            self.stdout.write(f'Generated shipment data for {distributor.name}')
        
        # Generate forecast data for next month
        self.stdout.write('Generating forecast data for next month...')
        next_month = (today.month % 12) + 1
        next_year = today.year if next_month > today.month else today.year + 1
        
        for distributor in distributors:
            # Get last month's shipment
            last_month = today.month - 1 if today.month > 1 else 12
            last_year = today.year if today.month > 1 else today.year - 1
            
            try:
                last_shipment = Shipment.objects.get(
                    distributor=distributor,
                    shipment_date__month=last_month,
                    shipment_date__year=last_year
                )
                last_quantity = last_shipment.quantity
            except Shipment.DoesNotExist:
                # If no shipment exists for last month, use a random value
                last_quantity = random.randint(800, 2500)
            
            # Generate forecast with some variation from last month
            forecast_factor = 1 + (random.random() * 0.3 - 0.15)  # +/- 15%
            forecast_quantity = int(last_quantity * forecast_factor)
            
            Forecast.objects.create(
                distributor=distributor,
                forecast_month=next_month,
                forecast_year=next_year,
                quantity=forecast_quantity
            )
            
            self.stdout.write(f'Generated forecast data for {distributor.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data generation complete!'))