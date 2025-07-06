import os
import uuid
from werkzeug.utils import secure_filename
from PIL import Image
import logging

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_IMAGE_SIZE = (1200, 800)
THUMBNAIL_SIZE = (300, 200)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, upload_folder):
    """Save uploaded file with unique filename"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Create full path
        file_path = os.path.join(upload_folder, unique_filename)
        
        try:
            # Save original file
            file.save(file_path)
            
            # Create optimized version
            optimize_image(file_path)
            
            return unique_filename
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return None
    return None

def optimize_image(file_path):
    """Optimize image for web display"""
    try:
        with Image.open(file_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            if img.size[0] > MAX_IMAGE_SIZE[0] or img.size[1] > MAX_IMAGE_SIZE[1]:
                img.thumbnail(MAX_IMAGE_SIZE, Image.Resampling.LANCZOS)
            
            # Save optimized version
            img.save(file_path, 'JPEG', quality=85, optimize=True)
            
    except Exception as e:
        logger.error(f"Error optimizing image: {e}")

def create_thumbnail(file_path, thumbnail_path):
    """Create thumbnail from image"""
    try:
        with Image.open(file_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Create thumbnail
            img.thumbnail(THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, 'JPEG', quality=85, optimize=True)
            
    except Exception as e:
        logger.error(f"Error creating thumbnail: {e}")

def format_currency(amount):
    """Format number as currency"""
    if amount:
        return f"${amount:,.0f}"
    return "$0"

def format_phone(phone):
    """Format phone number"""
    if phone:
        # Remove all non-digit characters
        digits = ''.join(filter(str.isdigit, phone))
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    return phone

def generate_property_slug(title):
    """Generate URL-friendly slug from property title"""
    import re
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug[:50]  # Limit length
