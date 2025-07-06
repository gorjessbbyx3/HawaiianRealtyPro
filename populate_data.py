#!/usr/bin/env python3
"""
Populate the Hawaii Elite Realty database with sample data.
This script creates sample realtors, properties, and other data.
"""

from app import app, db
from models import User, Property, PropertyImage, Lead, ContactMessage
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_sample_realtors():
    """Create sample realtor accounts"""
    realtors = [
        {
            'username': 'malia_patel',
            'email': 'malia.patel@hawaiieliterealty.com',
            'first_name': 'Malia',
            'last_name': 'Patel',
            'phone': '(808) 555-0101',
            'role': 'realtor',
            'license_number': 'HI-RE-2024-001',
            'bio': 'Specializing in luxury oceanfront properties across Oahu and Maui. With over 15 years of experience in Hawaiian real estate, I help clients find their perfect island paradise.',
            'years_experience': 15,
            'specializations': 'Luxury Homes, Oceanfront Properties, Investment Properties'
        },
        {
            'username': 'kai_nakamura',
            'email': 'kai.nakamura@hawaiieliterealty.com',
            'first_name': 'Kai',
            'last_name': 'Nakamura',
            'phone': '(808) 555-0102',
            'role': 'realtor',
            'license_number': 'HI-RE-2024-002',
            'bio': 'Expert in Big Island properties with a focus on sustainable living and eco-friendly homes. Fluent in Japanese and English, serving both local and international clients.',
            'years_experience': 12,
            'specializations': 'Eco-Friendly Homes, Big Island Properties, International Clients'
        },
        {
            'username': 'leilani_wong',
            'email': 'leilani.wong@hawaiieliterealty.com',
            'first_name': 'Leilani',
            'last_name': 'Wong',
            'phone': '(808) 555-0103',
            'role': 'realtor',
            'license_number': 'HI-RE-2024-003',
            'bio': 'Kauai specialist with deep knowledge of the Garden Isle. I focus on helping families find their dream homes in paradise, from beachfront estates to mountain retreats.',
            'years_experience': 8,
            'specializations': 'Kauai Properties, Family Homes, Vacation Rentals'
        }
    ]
    
    created_realtors = []
    for realtor_data in realtors:
        # Check if realtor already exists
        existing = User.query.filter_by(email=realtor_data['email']).first()
        if not existing:
            realtor = User(
                username=realtor_data['username'],
                email=realtor_data['email'],
                first_name=realtor_data['first_name'],
                last_name=realtor_data['last_name'],
                phone=realtor_data['phone'],
                role=realtor_data['role'],
                license_number=realtor_data['license_number'],
                bio=realtor_data['bio'],
                years_experience=realtor_data['years_experience'],
                specializations=realtor_data['specializations']
            )
            realtor.set_password('RealtorPass123!')
            db.session.add(realtor)
            created_realtors.append(realtor)
    
    db.session.commit()
    return created_realtors

def create_sample_properties(realtors):
    """Create sample property listings"""
    properties = [
        {
            'title': 'Luxury Oceanfront Estate - Diamond Head',
            'description': 'Breathtaking oceanfront estate with panoramic views of Diamond Head crater. This exceptional property features 6 bedrooms, 8 bathrooms, infinity pool, private beach access, and world-class amenities. Perfect for luxury living or high-end vacation rental investment.',
            'price': 12500000.00,
            'property_type': 'house',
            'status': 'active',
            'bedrooms': 6,
            'bathrooms': 8.0,
            'square_feet': 8500,
            'lot_size': 2.3,
            'year_built': 2018,
            'address': '4567 Diamond Head Road',
            'city': 'Honolulu',
            'zip_code': '96815',
            'features': 'Ocean Views\nPrivate Beach\nInfinity Pool\nGourmet Kitchen\nWine Cellar\nHome Theater\nGuest House\nGated Entry',
            'virtual_tour_url': 'https://example.com/tour/diamond-head-estate'
        },
        {
            'title': 'Modern Maui Hillside Villa',
            'description': 'Contemporary architectural masterpiece nestled in the hills of Maui with stunning valley and ocean views. Features sustainable design, solar power, rainwater collection, and seamless indoor-outdoor living spaces.',
            'price': 3750000.00,
            'property_type': 'house',
            'status': 'active',
            'bedrooms': 4,
            'bathrooms': 4.5,
            'square_feet': 4200,
            'lot_size': 1.8,
            'year_built': 2020,
            'address': '789 Maui Hillside Drive',
            'city': 'Kailua-Kona',
            'zip_code': '96740',
            'features': 'Mountain Views\nSolar Power\nRainwater Collection\nInfinity Pool\nOutdoor Kitchen\nZen Garden\nGuest Suite\nSmart Home Technology'
        },
        {
            'title': 'Kauai Beachfront Paradise',
            'description': 'Rare beachfront property on the pristine shores of Kauai. This tropical paradise offers direct beach access, mature coconut palms, and unobstructed ocean views. Perfect for those seeking the ultimate Hawaiian lifestyle.',
            'price': 8900000.00,
            'property_type': 'house',
            'status': 'active',
            'bedrooms': 5,
            'bathrooms': 6.0,
            'square_feet': 6800,
            'lot_size': 3.2,
            'year_built': 2015,
            'address': '321 Kauai Beach Lane',
            'city': 'Hanalei',
            'zip_code': '96714',
            'features': 'Beachfront\nOcean Views\nTropical Gardens\nInfinity Pool\nOutdoor Pavilion\nTiki Bar\nGuest Cottage\nPrivate Dock'
        },
        {
            'title': 'Big Island Volcanic Vista Estate',
            'description': 'Spectacular estate on the Big Island with dramatic volcanic landscape views. This unique property combines luxury living with the raw beauty of Hawaiian geology, featuring custom architecture and premium finishes.',
            'price': 4200000.00,
            'property_type': 'house',
            'status': 'active',
            'bedrooms': 4,
            'bathrooms': 5.0,
            'square_feet': 5200,
            'lot_size': 4.5,
            'year_built': 2019,
            'address': '987 Volcano View Circle',
            'city': 'Hilo',
            'zip_code': '96720',
            'features': 'Volcano Views\nLava Rock Features\nInfinity Pool\nWine Cellar\nArt Studio\nGuest Wing\nHelicopter Pad\nNative Landscaping'
        },
        {
            'title': 'Luxury Honolulu High-Rise Condo',
            'description': 'Sophisticated penthouse condo in prestigious Honolulu tower. Floor-to-ceiling windows showcase panoramic city and ocean views. Premium building amenities include concierge, fitness center, and rooftop infinity pool.',
            'price': 2850000.00,
            'property_type': 'condo',
            'status': 'active',
            'bedrooms': 3,
            'bathrooms': 3.5,
            'square_feet': 2800,
            'lot_size': None,
            'year_built': 2021,
            'address': '456 Luxury Tower Boulevard, Unit 4501',
            'city': 'Honolulu',
            'zip_code': '96813',
            'features': 'City Views\nOcean Views\nConcierge Service\nFitness Center\nRooftop Pool\nValet Parking\nWine Storage\nSmart Home'
        },
        {
            'title': 'Maui Mountain Retreat',
            'description': 'Serene mountain retreat offering privacy and tranquility in Maui\'s upcountry. Perfect for those seeking a peaceful escape with cool mountain air, native forest, and spectacular sunrise views over the island.',
            'price': 1950000.00,
            'property_type': 'house',
            'status': 'pending',
            'bedrooms': 3,
            'bathrooms': 2.5,
            'square_feet': 2400,
            'lot_size': 5.8,
            'year_built': 2017,
            'address': '654 Mountain View Trail',
            'city': 'Lahaina',
            'zip_code': '96761',
            'features': 'Mountain Views\nNative Forest\nSolar Power\nRainwater Collection\nOrganic Garden\nYoga Deck\nFire Pit\nNature Trails'
        }
    ]
    
    created_properties = []
    for i, prop_data in enumerate(properties):
        # Assign realtor cyclically
        realtor = realtors[i % len(realtors)]
        
        # Check if property already exists
        existing = Property.query.filter_by(address=prop_data['address']).first()
        if not existing:
            property_obj = Property(
                title=prop_data['title'],
                description=prop_data['description'],
                price=prop_data['price'],
                property_type=prop_data['property_type'],
                status=prop_data['status'],
                bedrooms=prop_data['bedrooms'],
                bathrooms=prop_data['bathrooms'],
                square_feet=prop_data['square_feet'],
                lot_size=prop_data['lot_size'],
                year_built=prop_data['year_built'],
                address=prop_data['address'],
                city=prop_data['city'],
                state='Hawaii',
                zip_code=prop_data['zip_code'],
                features=prop_data['features'],
                virtual_tour_url=prop_data.get('virtual_tour_url'),
                realtor_id=realtor.id
            )
            db.session.add(property_obj)
            created_properties.append(property_obj)
    
    db.session.commit()
    return created_properties

def create_sample_leads(realtors, properties):
    """Create sample leads for the CRM system"""
    leads = [
        {
            'name': 'Sarah Johnson',
            'email': 'sarah.johnson@email.com',
            'phone': '(415) 555-0234',
            'message': 'Interested in luxury oceanfront properties in Oahu. Looking for a vacation home with 4+ bedrooms.',
            'budget_range': '2m_5m',
            'preferred_areas': 'Oahu, Diamond Head area',
            'status': 'new',
            'priority': 'high'
        },
        {
            'name': 'David Chen',
            'email': 'david.chen@email.com',
            'phone': '(650) 555-0567',
            'message': 'Seeking eco-friendly home on Big Island for full-time residence. Solar power and sustainable features important.',
            'budget_range': '1m_2m',
            'preferred_areas': 'Big Island, Hilo area',
            'status': 'contacted',
            'priority': 'medium'
        },
        {
            'name': 'Maria Rodriguez',
            'email': 'maria.rodriguez@email.com',
            'phone': '(213) 555-0789',
            'message': 'Looking for investment property in Maui, preferably with vacation rental potential.',
            'budget_range': '500k_1m',
            'preferred_areas': 'Maui, Lahaina',
            'status': 'qualified',
            'priority': 'medium'
        }
    ]
    
    for i, lead_data in enumerate(leads):
        # Assign realtor and property cyclically
        realtor = realtors[i % len(realtors)]
        property_obj = properties[i % len(properties)]
        
        # Check if lead already exists
        existing = Lead.query.filter_by(email=lead_data['email']).first()
        if not existing:
            lead = Lead(
                name=lead_data['name'],
                email=lead_data['email'],
                phone=lead_data['phone'],
                message=lead_data['message'],
                budget_range=lead_data['budget_range'],
                preferred_areas=lead_data['preferred_areas'],
                status=lead_data['status'],
                priority=lead_data['priority'],
                realtor_id=realtor.id,
                property_id=property_obj.id,
                source='website'
            )
            db.session.add(lead)
    
    db.session.commit()

def create_admin_user():
    """Create an admin user for testing"""
    admin_email = 'admin@hawaiieliterealty.com'
    existing_admin = User.query.filter_by(email=admin_email).first()
    
    if not existing_admin:
        admin = User(
            username='admin',
            email=admin_email,
            first_name='Admin',
            last_name='User',
            phone='(808) 555-0100',
            role='admin'
        )
        admin.set_password('AdminPass123!')
        db.session.add(admin)
        db.session.commit()
        return admin
    return existing_admin

def main():
    """Main function to populate the database"""
    with app.app_context():
        print("Creating sample data for Hawaii Elite Realty...")
        
        # Create admin user
        admin = create_admin_user()
        print(f"✓ Created admin user: {admin.email}")
        
        # Create realtors
        realtors = create_sample_realtors()
        print(f"✓ Created {len(realtors)} realtors")
        
        # Create properties
        properties = create_sample_properties(realtors)
        print(f"✓ Created {len(properties)} properties")
        
        # Create leads
        create_sample_leads(realtors, properties)
        print("✓ Created sample leads")
        
        print("\nSample data created successfully!")
        print("You can now:")
        print("- Login as admin: admin@hawaiieliterealty.com / AdminPass123!")
        print("- Login as realtor: malia.patel@hawaiieliterealty.com / RealtorPass123!")
        print("- Browse properties and test all features")

if __name__ == '__main__':
    main()