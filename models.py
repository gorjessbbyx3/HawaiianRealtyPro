from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='client')  # admin, realtor, client
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Realtor specific fields
    license_number = db.Column(db.String(50))
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(200))
    years_experience = db.Column(db.Integer)
    specializations = db.Column(db.Text)
    
    # Relationships
    properties = db.relationship('Property', backref='realtor', lazy=True)
    appointments = db.relationship('Appointment', foreign_keys='Appointment.realtor_id', backref='realtor', lazy=True)
    client_appointments = db.relationship('Appointment', foreign_keys='Appointment.client_id', backref='client', lazy=True)
    leads = db.relationship('Lead', backref='assigned_realtor', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.username}>'

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    property_type = db.Column(db.String(50), nullable=False)  # house, condo, land, etc.
    status = db.Column(db.String(20), default='active')  # active, sold, pending
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Float)
    square_feet = db.Column(db.Integer)
    lot_size = db.Column(db.Float)
    year_built = db.Column(db.Integer)
    
    # Location
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), default='Hawaii')
    zip_code = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Features
    features = db.Column(db.Text)  # JSON string of features
    virtual_tour_url = db.Column(db.String(500))
    video_url = db.Column(db.String(500))
    
    # Metadata
    realtor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('PropertyImage', backref='property', lazy=True, cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='property', lazy=True)
    leads = db.relationship('Lead', backref='property', lazy=True)
    
    @property
    def formatted_price(self):
        return f"${self.price:,.0f}"
    
    @property
    def main_image(self):
        if self.images:
            return self.images[0].image_url
        return None
    
    def __repr__(self):
        return f'<Property {self.title}>'

class PropertyImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.String(200))
    is_primary = db.Column(db.Boolean, default=False)
    order_index = db.Column(db.Integer, default=0)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    realtor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Appointment details
    appointment_date = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, default=60)  # minutes
    appointment_type = db.Column(db.String(50), default='showing')  # showing, consultation, etc.
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    
    # Client info (for non-registered users)
    client_name = db.Column(db.String(100))
    client_email = db.Column(db.String(120))
    client_phone = db.Column(db.String(20))
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Appointment {self.appointment_date}>'

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text)
    
    # Lead source and context
    source = db.Column(db.String(50), default='website')  # website, referral, social, etc.
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'))
    realtor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Lead management
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, converted, lost
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    budget_range = db.Column(db.String(50))
    preferred_areas = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_contact = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Lead {self.name}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage {self.subject}>'
