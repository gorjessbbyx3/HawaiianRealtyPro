#!/usr/bin/env python3
"""
Add advanced features to make this a truly top-tier application.
"""

from app import app, db
from models import User, Property, PropertyImage
import os

def create_property_images():
    """Create sample property images using high-quality placeholder images"""
    with app.app_context():
        properties = Property.query.all()
        
        # High-quality Hawaiian property images (using Unsplash for realistic URLs)
        image_sets = [
            [
                'https://images.unsplash.com/photo-1571868628686-aac41354a4bb?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
                'https://images.unsplash.com/photo-1571868628667-f82c1ab5f95b?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
                'https://images.unsplash.com/photo-1571868628686-aac41354a4bb?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80'
            ],
            [
                'https://images.unsplash.com/photo-1582063289852-62e3ba2747f8?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
                'https://images.unsplash.com/photo-1571868628711-aa7473ee6b25?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
                'https://images.unsplash.com/photo-1571868628674-d5e1fd9e6e80?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80'
            ],
            [
                'https://images.unsplash.com/photo-1589735168692-b1b70fc4c8c1?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
                'https://images.unsplash.com/photo-1582063289852-62e3ba2747f8?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80',
                'https://images.unsplash.com/photo-1571868628586-c85a79cbe63d?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80'
            ]
        ]
        
        for i, property_obj in enumerate(properties):
            image_set = image_sets[i % len(image_sets)]
            
            for j, image_url in enumerate(image_set):
                # Check if image already exists
                existing = PropertyImage.query.filter_by(
                    property_id=property_obj.id,
                    image_url=image_url
                ).first()
                
                if not existing:
                    property_image = PropertyImage(
                        property_id=property_obj.id,
                        image_url=image_url,
                        caption=f"Beautiful view {j+1}",
                        is_primary=(j == 0),
                        order_index=j
                    )
                    db.session.add(property_image)
        
        db.session.commit()
        print(f"✓ Created property images for all listings")

def enhance_realtor_profiles():
    """Add profile images and enhanced bios to realtors"""
    with app.app_context():
        realtors = User.query.filter_by(role='realtor').all()
        
        # Professional realtor headshots
        profile_images = [
            'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
            'https://images.unsplash.com/photo-1494790108755-2616b4e73013?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
            'https://images.unsplash.com/photo-1619895862022-09114b41f16f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'
        ]
        
        for i, realtor in enumerate(realtors):
            if not realtor.profile_image:
                realtor.profile_image = profile_images[i % len(profile_images)]
        
        db.session.commit()
        print(f"✓ Enhanced {len(realtors)} realtor profiles")

if __name__ == '__main__':
    print("Adding advanced features...")
    create_property_images()
    enhance_realtor_profiles()
    print("✓ All advanced features added successfully!")