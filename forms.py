from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, DateTimeField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('client', 'Client'), ('realtor', 'Realtor')], default='client')
    
    # Realtor specific fields
    license_number = StringField('License Number', validators=[Optional(), Length(max=50)])
    bio = TextAreaField('Bio', validators=[Optional()])
    years_experience = IntegerField('Years of Experience', validators=[Optional()])

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    property_type = SelectField('Property Type', 
                               choices=[('house', 'House'), ('condo', 'Condo'), ('townhouse', 'Townhouse'), 
                                       ('land', 'Land'), ('commercial', 'Commercial')], 
                               validators=[DataRequired()])
    status = SelectField('Status', 
                        choices=[('active', 'Active'), ('pending', 'Pending'), ('sold', 'Sold')], 
                        default='active')
    bedrooms = IntegerField('Bedrooms', validators=[Optional(), NumberRange(min=0)])
    bathrooms = FloatField('Bathrooms', validators=[Optional(), NumberRange(min=0)])
    square_feet = IntegerField('Square Feet', validators=[Optional(), NumberRange(min=0)])
    lot_size = FloatField('Lot Size (acres)', validators=[Optional(), NumberRange(min=0)])
    year_built = IntegerField('Year Built', validators=[Optional(), NumberRange(min=1800, max=2030)])
    
    # Location
    address = StringField('Address', validators=[DataRequired(), Length(max=200)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    zip_code = StringField('ZIP Code', validators=[Optional(), Length(max=10)])
    
    # Features
    features = TextAreaField('Features (one per line)', validators=[Optional()])
    virtual_tour_url = StringField('Virtual Tour URL', validators=[Optional(), Length(max=500)])
    video_url = StringField('Video URL', validators=[Optional(), Length(max=500)])
    
    # Images
    images = FileField('Property Images', 
                      validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])

class AppointmentForm(FlaskForm):
    property_id = IntegerField('Property ID', validators=[DataRequired()])
    appointment_date = DateTimeField('Appointment Date & Time', 
                                   validators=[DataRequired()], 
                                   format='%Y-%m-%d %H:%M')
    duration = IntegerField('Duration (minutes)', validators=[Optional(), NumberRange(min=15, max=480)], default=60)
    appointment_type = SelectField('Appointment Type', 
                                 choices=[('showing', 'Property Showing'), ('consultation', 'Consultation'), 
                                         ('inspection', 'Inspection')], 
                                 default='showing')
    
    # Client info
    client_name = StringField('Your Name', validators=[DataRequired(), Length(max=100)])
    client_email = StringField('Email', validators=[DataRequired(), Email()])
    client_phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    notes = TextAreaField('Notes or Special Requests', validators=[Optional()])

class LeadForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    message = TextAreaField('Message', validators=[Optional()])
    budget_range = SelectField('Budget Range', 
                              choices=[('', 'Select Budget Range'),
                                      ('under_500k', 'Under $500,000'),
                                      ('500k_1m', '$500,000 - $1,000,000'),
                                      ('1m_2m', '$1,000,000 - $2,000,000'),
                                      ('2m_5m', '$2,000,000 - $5,000,000'),
                                      ('over_5m', 'Over $5,000,000')], 
                              validators=[Optional()])
    preferred_areas = TextAreaField('Preferred Areas', validators=[Optional()])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired()])

class PropertySearchForm(FlaskForm):
    search_query = StringField('Search', validators=[Optional()])
    property_type = SelectField('Property Type', 
                               choices=[('', 'All Types'), ('house', 'House'), ('condo', 'Condo'), 
                                       ('townhouse', 'Townhouse'), ('land', 'Land'), ('commercial', 'Commercial')])
    min_price = FloatField('Min Price', validators=[Optional(), NumberRange(min=0)])
    max_price = FloatField('Max Price', validators=[Optional(), NumberRange(min=0)])
    min_bedrooms = IntegerField('Min Bedrooms', validators=[Optional(), NumberRange(min=0)])
    max_bedrooms = IntegerField('Max Bedrooms', validators=[Optional(), NumberRange(min=0)])
    city = SelectField('City', choices=[('', 'All Cities'), ('Honolulu', 'Honolulu'), ('Hilo', 'Hilo'), 
                                       ('Kailua-Kona', 'Kailua-Kona'), ('Kaneohe', 'Kaneohe'), 
                                       ('Waipahu', 'Waipahu'), ('Pearl City', 'Pearl City'), 
                                       ('Hanalei', 'Hanalei'), ('Lahaina', 'Lahaina')])
