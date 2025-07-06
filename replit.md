# Hawaii Elite Realty - Real Estate Platform

## Overview

Hawaii Elite Realty is a comprehensive real estate platform built with Flask and Python, designed to showcase luxury Hawaiian properties. The application serves both real estate professionals and clients, providing property listings, appointment booking, lead management, and CRM functionality.

## System Architecture

The application follows a traditional Flask web application architecture with the following key components:

### Backend Architecture
- **Framework**: Flask with Blueprint-based modular structure
- **Database**: SQLAlchemy ORM with SQLite default (configurable for PostgreSQL)
- **Authentication**: Flask-Login with role-based access control
- **Security**: Flask-WTF CSRF protection, password hashing with Werkzeug
- **File Handling**: Image upload and optimization with PIL

### Frontend Architecture
- **Templates**: Jinja2 templating engine
- **Styling**: Bootstrap 5 with custom CSS
- **JavaScript**: Vanilla JavaScript for interactivity
- **Responsive Design**: Mobile-first approach

## Key Components

### User Management
- Multi-role system (admin, realtor, client)
- User registration and authentication
- Profile management for realtors with specializations and bio

### Property Management
- Property listings with detailed information
- Image galleries with thumbnail support
- Virtual tour integration capability
- Property search and filtering
- Status tracking (active, pending, sold)

### CRM System
- Lead management and tracking
- Appointment booking system
- Contact message handling
- Dashboard with statistics for realtors

### File Management
- Image upload with validation
- Automatic image optimization and resizing
- Secure file storage in static directory

## Data Flow

1. **User Authentication**: Users register/login through Flask-Login system
2. **Property Browsing**: Public access to property listings with search functionality
3. **Appointment Booking**: Authenticated users can book property viewings
4. **Lead Management**: Realtors manage leads through dedicated CRM interface
5. **Property Management**: Realtors can add/edit property listings
6. **Virtual Tours**: Integration ready for external virtual tour services

## External Dependencies

### Python Packages
- Flask and extensions (SQLAlchemy, Login, WTF)
- Werkzeug for security utilities
- PIL (Pillow) for image processing
- WTForms for form handling

### Frontend Dependencies
- Bootstrap 5 for responsive UI
- Font Awesome for icons
- Custom CSS for Hawaiian-themed styling

### File Storage
- Local file storage in static/uploads directory
- Image optimization pipeline for web display

## Deployment Strategy

The application is configured for flexible deployment:

- **Development**: SQLite database with debug mode
- **Production**: Environment variable configuration for DATABASE_URL
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies
- **Session Management**: Configurable secret key via environment variables
- **Upload Limits**: 16MB max file size with validation

## Changelog

- July 06, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.