import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jalaram_electric.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product, CustomerProfile

def seed():
    # 1. Create Admin / Shopkeeper user
    admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@jalaramelectric.com', 'is_staff': True, 'is_superuser': True})
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        CustomerProfile.objects.create(user=admin_user, customer_type='retail', phone='9876543210', business_name='Jalaram Electric Store')
        print("Created Superuser: admin / password: admin123")

    # 2. Create Sample Electrician / Contractor user
    contractor_user, c_created = User.objects.get_or_create(username='ramesh_contractor', defaults={'first_name': 'Ramesh Electrician', 'email': 'ramesh@build.com'})
    if c_created:
        contractor_user.set_password('ramesh123')
        contractor_user.save()
        CustomerProfile.objects.create(user=contractor_user, customer_type='contractor', phone='9825012345', business_name='Ramesh Electricals & Wiring')
        print("Created Contractor: ramesh_contractor / password: ramesh123")

    # 3. Create Categories
    categories_data = [
        ('Modular Switches & Sockets', 'Modular switches, regulators, multi-pin sockets and face plates'),
        ('House Wiring & Cables', 'FR/FRLS insulated copper house wires and flexible cables'),
        ('LED Lighting & Fixtures', 'LED batten tubes, ceiling panels, spotlights, and bulbs'),
        ('Switchgear & Circuit Breakers', 'MCB, RCCB, Isolators, and distribution boxes'),
        ('Conduits & Fittings', 'Heavy duty PVC conduit pipes, bends, junction boxes, and saddles'),
        ('Electrician Tools & Consumables', 'Insulation tapes, wire strippers, digital multimeters, testers'),
    ]

    cat_map = {}
    for name, desc in categories_data:
        cat, _ = Category.objects.get_or_create(name=name, defaults={'description': desc})
        cat_map[name] = cat

    # 4. Create Electrical Products with Dual Pricing
    products = [
        # Modular Switches
        ('Modular 1-Way Switch 6A', 'Anchor Roma', 'Modular Switches & Sockets', 'Smooth tactile operation 6A switch in glossy white finish', 28.00, 19.50, 250, 30, 5, 'Piece'),
        ('Modular 6A/16A Universal Socket', 'Anchor Roma', 'Modular Switches & Sockets', 'Dual shutter safety 16A power socket for heavy appliances', 95.00, 72.00, 120, 15, 2, 'Piece'),
        ('8-Module Cover Plate', 'Schneider Opale', 'Modular Switches & Sockets', 'Modern flush aesthetic cover plate for switchboards', 160.00, 120.00, 60, 10, 1, 'Piece'),

        # House Wiring
        ('1.5 sq mm Copper Wire (90m Red)', 'Polycab', 'House Wiring & Cables', 'FRLS Flame Retardant Lead Free copper wire roll', 1850.00, 1580.00, 45, 8, 1, 'Coil'),
        ('2.5 sq mm Copper Wire (90m Yellow)', 'Finolex', 'House Wiring & Cables', 'High conductivity 100% pure electrolytic copper wire coil', 2950.00, 2520.00, 30, 5, 1, 'Coil'),
        ('4.0 sq mm Heavy Load Cable (90m Black)', 'Polycab', 'House Wiring & Cables', 'Ideal for AC, Geyser and main electrical panel lines', 4400.00, 3850.00, 20, 4, 1, 'Coil'),

        # LED Lighting
        ('9W LED Cool Day White Bulb', 'Havells', 'LED Lighting & Fixtures', 'Energy efficient 6500K B22 base LED bulb', 110.00, 78.00, 150, 20, 2, 'Piece'),
        ('20W LED Slim Batten Tube (4ft)', 'Philips', 'LED Lighting & Fixtures', 'Glare-free uniform illumination for living rooms and offices', 280.00, 210.00, 80, 12, 1, 'Piece'),
        ('12W Concealed Ceiling Downlight', 'Syska', 'LED Lighting & Fixtures', 'Slim recessed round LED panel downlight with driver', 240.00, 175.00, 90, 15, 2, 'Piece'),

        # Switchgear
        ('Single Pole 16A C-Curve MCB', 'Havells', 'Switchgear & Circuit Breakers', 'Short circuit and overload protection 10kA breaking capacity', 180.00, 135.00, 70, 10, 1, 'Piece'),
        ('Double Pole 32A Isolator', 'Legrand', 'Switchgear & Circuit Breakers', 'Main supply isolation switch for residential distribution boards', 340.00, 260.00, 40, 6, 1, 'Piece'),

        # Conduits & Fittings
        ('25mm Heavy Duty PVC Conduit (3m)', 'Precision', 'Conduits & Fittings', 'Flame retardant electrical pipe for concealed wiring', 85.00, 62.00, 200, 40, 10, 'Piece'),
        ('25mm PVC Deep Junction Box (4-Way)', 'Precision', 'Conduits & Fittings', 'Round junction box with cover for ceiling slab piping', 25.00, 16.00, 300, 50, 10, 'Piece'),

        # Tools & Consumables
        ('PVC Insulation Tape (Pack of 5)', 'Steelgrip', 'Electrician Tools & Consumables', 'High dielectric strength adhesive electric tape in multi-colors', 60.00, 42.00, 100, 20, 2, 'Box'),
        ('Heavy Duty Neon Line Tester 500V', 'Taparia', 'Electrician Tools & Consumables', 'High visibility spark indicator phase tester screwdriver', 75.00, 52.00, 50, 10, 1, 'Piece'),
    ]

    for name, brand, cat_name, desc, ret, whl, st, low, moq, unit in products:
        Product.objects.get_or_create(
            name=name,
            defaults={
                'brand': brand,
                'category': cat_map[cat_name],
                'description': desc,
                'retail_price': ret,
                'wholesale_price': whl,
                'stock': st,
                'low_stock_limit': low,
                'min_order_qty': moq,
                'unit': unit,
            }
        )

    print(f"Successfully populated {Product.objects.count()} electrical supplies.")

if __name__ == '__main__':
    seed()
