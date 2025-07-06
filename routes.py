import os
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import or_, and_
from app import db
from models import User, Property, PropertyImage, Appointment, Lead, ContactMessage
from forms import (LoginForm, RegisterForm, PropertyForm, AppointmentForm, 
                  LeadForm, ContactForm, PropertySearchForm)
from utils import save_uploaded_file, format_currency, format_phone

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
property_bp = Blueprint('property', __name__, url_prefix='/properties')
realtor_bp = Blueprint('realtor', __name__, url_prefix='/realtors')
booking_bp = Blueprint('booking', __name__, url_prefix='/booking')
crm_bp = Blueprint('crm', __name__, url_prefix='/crm')

# Main routes
@main_bp.route('/')
def index():
    # Get featured properties (latest 6)
    featured_properties = Property.query.filter_by(status='active').order_by(Property.created_at.desc()).limit(6).all()
    
    # Get top realtors
    top_realtors = User.query.filter_by(role='realtor', is_active=True).limit(3).all()
    
    return render_template('index.html', 
                         featured_properties=featured_properties, 
                         top_realtors=top_realtors)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', form=form)

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'error')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'error')
            return render_template('register.html', form=form)
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            role=form.role.data,
            license_number=form.license_number.data if form.role.data == 'realtor' else None,
            bio=form.bio.data if form.role.data == 'realtor' else None,
            years_experience=form.years_experience.data if form.role.data == 'realtor' else None
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'realtor':
        # Realtor dashboard data
        properties = Property.query.filter_by(realtor_id=current_user.id).all()
        upcoming_appointments = Appointment.query.filter_by(realtor_id=current_user.id)\
            .filter(Appointment.appointment_date >= datetime.utcnow())\
            .order_by(Appointment.appointment_date).limit(5).all()
        recent_leads = Lead.query.filter_by(realtor_id=current_user.id)\
            .order_by(Lead.created_at.desc()).limit(5).all()
        
        stats = {
            'total_properties': len(properties),
            'active_properties': len([p for p in properties if p.status == 'active']),
            'pending_properties': len([p for p in properties if p.status == 'pending']),
            'sold_properties': len([p for p in properties if p.status == 'sold']),
            'total_leads': Lead.query.filter_by(realtor_id=current_user.id).count(),
            'new_leads': Lead.query.filter_by(realtor_id=current_user.id, status='new').count()
        }
        
        return render_template('dashboard.html', 
                             properties=properties,
                             upcoming_appointments=upcoming_appointments,
                             recent_leads=recent_leads,
                             stats=stats)
    else:
        # Client dashboard
        appointments = Appointment.query.filter_by(client_id=current_user.id)\
            .order_by(Appointment.appointment_date.desc()).all()
        return render_template('dashboard.html', appointments=appointments)

# Property routes
@property_bp.route('/')
def properties():
    form = PropertySearchForm()
    query = Property.query.filter_by(status='active')
    
    # Apply search filters
    if request.args.get('search_query'):
        search_term = f"%{request.args.get('search_query')}%"
        query = query.filter(or_(
            Property.title.ilike(search_term),
            Property.description.ilike(search_term),
            Property.address.ilike(search_term),
            Property.city.ilike(search_term)
        ))
    
    if request.args.get('property_type'):
        query = query.filter_by(property_type=request.args.get('property_type'))
    
    if request.args.get('min_price'):
        query = query.filter(Property.price >= float(request.args.get('min_price')))
    
    if request.args.get('max_price'):
        query = query.filter(Property.price <= float(request.args.get('max_price')))
    
    if request.args.get('min_bedrooms'):
        query = query.filter(Property.bedrooms >= int(request.args.get('min_bedrooms')))
    
    if request.args.get('max_bedrooms'):
        query = query.filter(Property.bedrooms <= int(request.args.get('max_bedrooms')))
    
    if request.args.get('city'):
        query = query.filter_by(city=request.args.get('city'))
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    properties = query.order_by(Property.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False)
    
    return render_template('properties.html', properties=properties, form=form)

@property_bp.route('/<int:property_id>')
def property_detail(property_id):
    property = Property.query.get_or_404(property_id)
    
    # Get related properties (same city, different property)
    related_properties = Property.query.filter(
        and_(Property.city == property.city, Property.id != property.id, Property.status == 'active')
    ).limit(3).all()
    
    return render_template('property_detail.html', 
                         property=property, 
                         related_properties=related_properties)

@property_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_property():
    if current_user.role != 'realtor':
        flash('Only realtors can add properties', 'error')
        return redirect(url_for('main.index'))
    
    form = PropertyForm()
    if form.validate_on_submit():
        property = Property(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            property_type=form.property_type.data,
            status=form.status.data,
            bedrooms=form.bedrooms.data,
            bathrooms=form.bathrooms.data,
            square_feet=form.square_feet.data,
            lot_size=form.lot_size.data,
            year_built=form.year_built.data,
            address=form.address.data,
            city=form.city.data,
            zip_code=form.zip_code.data,
            features=form.features.data,
            virtual_tour_url=form.virtual_tour_url.data,
            video_url=form.video_url.data,
            realtor_id=current_user.id
        )
        
        db.session.add(property)
        db.session.flush()  # Get the property ID
        
        # Handle file uploads
        if form.images.data:
            files = request.files.getlist('images')
            for i, file in enumerate(files):
                if file and file.filename:
                    filename = save_uploaded_file(file, current_app.config['UPLOAD_FOLDER'])
                    if filename:
                        image = PropertyImage(
                            property_id=property.id,
                            image_url=f"uploads/{filename}",
                            is_primary=(i == 0),
                            order_index=i
                        )
                        db.session.add(image)
        
        db.session.commit()
        flash('Property added successfully!', 'success')
        return redirect(url_for('property.property_detail', property_id=property.id))
    
    return render_template('add_property.html', form=form)

@property_bp.route('/<int:property_id>/virtual-tour')
def virtual_tour(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('virtual_tour.html', property=property)

# Realtor routes
@realtor_bp.route('/')
def realtors():
    realtors = User.query.filter_by(role='realtor', is_active=True).all()
    return render_template('realtors.html', realtors=realtors)

@realtor_bp.route('/<int:realtor_id>')
def realtor_profile(realtor_id):
    realtor = User.query.filter_by(id=realtor_id, role='realtor').first_or_404()
    properties = Property.query.filter_by(realtor_id=realtor_id, status='active').all()
    return render_template('realtor_profile.html', realtor=realtor, properties=properties)

# Booking routes
@booking_bp.route('/property/<int:property_id>', methods=['GET', 'POST'])
def book_appointment(property_id):
    property = Property.query.get_or_404(property_id)
    form = AppointmentForm()
    form.property_id.data = property_id
    
    if form.validate_on_submit():
        appointment = Appointment(
            property_id=property_id,
            realtor_id=property.realtor_id,
            client_id=current_user.id if current_user.is_authenticated else None,
            appointment_date=form.appointment_date.data,
            duration=form.duration.data,
            appointment_type=form.appointment_type.data,
            client_name=form.client_name.data,
            client_email=form.client_email.data,
            client_phone=form.client_phone.data,
            notes=form.notes.data
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash('Appointment booked successfully! The realtor will contact you to confirm.', 'success')
        return redirect(url_for('property.property_detail', property_id=property_id))
    
    return render_template('booking.html', form=form, property=property)

@booking_bp.route('/appointments')
@login_required
def appointments():
    if current_user.role == 'realtor':
        appointments = Appointment.query.filter_by(realtor_id=current_user.id)\
            .order_by(Appointment.appointment_date.desc()).all()
    else:
        appointments = Appointment.query.filter_by(client_id=current_user.id)\
            .order_by(Appointment.appointment_date.desc()).all()
    
    return render_template('appointments.html', appointments=appointments)

# CRM routes
@crm_bp.route('/leads')
@login_required
def leads():
    if current_user.role != 'realtor':
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    leads = Lead.query.filter_by(realtor_id=current_user.id)\
        .order_by(Lead.created_at.desc()).all()
    
    return render_template('leads.html', leads=leads)

@crm_bp.route('/lead/<int:lead_id>/update-status')
@login_required
def update_lead_status(lead_id):
    if current_user.role != 'realtor':
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    lead = Lead.query.filter_by(id=lead_id, realtor_id=current_user.id).first_or_404()
    new_status = request.args.get('status')
    
    if new_status in ['new', 'contacted', 'qualified', 'converted', 'lost']:
        lead.status = new_status
        lead.last_contact = datetime.utcnow()
        db.session.commit()
        flash('Lead status updated', 'success')
    
    return redirect(url_for('crm.leads'))

# Property inquiry (creates lead)
@property_bp.route('/<int:property_id>/inquire', methods=['POST'])
def property_inquiry(property_id):
    property = Property.query.get_or_404(property_id)
    form = LeadForm()
    
    if form.validate_on_submit():
        lead = Lead(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            message=form.message.data,
            property_id=property_id,
            realtor_id=property.realtor_id,
            source='website',
            budget_range=form.budget_range.data,
            preferred_areas=form.preferred_areas.data
        )
        
        db.session.add(lead)
        db.session.commit()
        
        flash('Your inquiry has been sent to the realtor!', 'success')
        return redirect(url_for('property.property_detail', property_id=property_id))
    
    # If form validation fails, redirect back with error
    flash('Please fill out all required fields', 'error')
    return redirect(url_for('property.property_detail', property_id=property_id))

# Analytics route
@crm_bp.route('/analytics')
@login_required
def analytics():
    if current_user.role not in ['realtor', 'admin']:
        flash('Access denied', 'error')
        return redirect(url_for('main.index'))
    
    # Calculate analytics data
    if current_user.role == 'realtor':
        properties = Property.query.filter_by(realtor_id=current_user.id).all()
        leads = Lead.query.filter_by(realtor_id=current_user.id).order_by(Lead.created_at.desc()).limit(5).all()
        appointments = Appointment.query.filter_by(realtor_id=current_user.id).all()
    else:  # admin
        properties = Property.query.all()
        leads = Lead.query.order_by(Lead.created_at.desc()).limit(5).all()
        appointments = Appointment.query.all()
    
    # Calculate metrics
    total_properties = len(properties)
    total_leads = len(Lead.query.filter_by(realtor_id=current_user.id if current_user.role == 'realtor' else None).all() if current_user.role == 'realtor' else Lead.query.all())
    total_appointments = len(appointments)
    
    # Calculate average property price
    if properties:
        avg_property_price = sum(p.price for p in properties) / len(properties)
    else:
        avg_property_price = 0
    
    # Get top performing properties (for demonstration)
    top_properties = properties[:5] if properties else []
    
    return render_template('analytics.html',
                         total_properties=total_properties,
                         total_leads=total_leads,
                         total_appointments=total_appointments,
                         avg_property_price=avg_property_price,
                         top_properties=top_properties,
                         recent_leads=leads)

# Template filters
@main_bp.app_template_filter('currency')
def currency_filter(amount):
    return format_currency(amount)

@main_bp.app_template_filter('phone')
def phone_filter(phone):
    return format_phone(phone)
