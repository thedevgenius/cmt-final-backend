import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from faker import Faker

# Import your models (adjust the app names if they are different)
from categories.models import Category
from addresses.models import City
from businesses.models import Business

User = get_user_model()
fake = Faker('en_IN') # Use Indian locale for realistic data

class Command(BaseCommand):
    help = 'Seeds the database with 100 dummy businesses in Kolkata'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seeding...")

        # 1. Ensure we have an Owner (User)
        user, _ = User.objects.get_or_create(
            phone="919999999999", 
            defaults={'email': 'admin@test.com', 'is_active': True}
        )

        # 2. Ensure we have a City (Kolkata)
        kolkata, _ = City.objects.get_or_create(name="Kolkata")

        # 3. Ensure we have some Categories
        category_names = ['Restaurant', 'Healthcare', 'Retail Shop', 'Education', 'Real Estate']
        categories = []
        for name in category_names:
            cat, _ = Category.objects.get_or_create(
                name=name, 
                defaults={'slug': slugify(name), 'category_type': 'DEF'}
            )
            categories.append(cat)

        # 4. Generate 100 Businesses
        businesses_created = 0

        # Kolkata roughly falls within these coordinate bounds
        LAT_MIN, LAT_MAX = 22.4500, 22.7000
        LNG_MIN, LNG_MAX = 88.2500, 88.4500

        for i in range(100):
            company_name = fake.company()
            
            # Generate realistic Kolkata-bound coordinates
            lat = Decimal(str(round(random.uniform(LAT_MIN, LAT_MAX), 8)))
            lng = Decimal(str(round(random.uniform(LNG_MIN, LNG_MAX), 8)))

            # Pick a random primary category
            primary_cat = random.choice(categories)

            # Create the business
            business = Business(
                owner=user,
                primary_category=primary_cat,
                name=company_name,
                # generate a unique handle by combining name and a random number
                handle=f"{slugify(company_name)}-{random.randint(1000, 9999)}",
                description=fake.catch_phrase(),
                phone=fake.phone_number()[:15],
                email=fake.company_email(),
                website=fake.url(),
                address=fake.street_address(),
                # locality=fake.locality(),
                pincode=fake.postcode(),
                city=kolkata,
                latitude=lat,
                longitude=lng,
                is_active=True,
                is_verified=random.choice([True, False]) # Randomly verify some
            )
            
            # We call .save() instead of bulk_create so your custom save() method
            # triggers to automatically generate the UUID and the unique slug
            business.save()

            # Add ManyToMany categories
            # Give it the primary category, plus maybe one extra random one
            business.categories.add(primary_cat)
            if random.random() > 0.5:
                business.categories.add(random.choice(categories))

            businesses_created += 1

            # Print progress every 10 records
            if businesses_created % 10 == 0:
                self.stdout.write(f"Created {businesses_created}/100 businesses...")

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully seeded {businesses_created} businesses in Kolkata!"))