// Hawaii Real Estate Platform - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initPropertyGallery();
    initPropertySearch();
    initAppointmentBooking();
    initLeadManagement();
    initDashboardCharts();
    initMobileMenu();
    initFormValidation();
    initImageUpload();
    initVirtualTour();
});

// Property Gallery
function initPropertyGallery() {
    const mainImage = document.getElementById('main-image');
    const thumbnails = document.querySelectorAll('.gallery-thumbnail');
    
    if (mainImage && thumbnails.length > 0) {
        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                // Remove active class from all thumbnails
                thumbnails.forEach(t => t.classList.remove('active'));
                
                // Add active class to clicked thumbnail
                this.classList.add('active');
                
                // Update main image
                mainImage.src = this.src;
                mainImage.alt = this.alt;
            });
        });
        
        // Set first thumbnail as active
        if (thumbnails[0]) {
            thumbnails[0].classList.add('active');
        }
    }
}

// Property Search Filters
function initPropertySearch() {
    const searchForm = document.getElementById('property-search-form');
    const filterInputs = document.querySelectorAll('.filter-input');
    
    if (searchForm && filterInputs.length > 0) {
        // Auto-submit form when filters change
        filterInputs.forEach(input => {
            input.addEventListener('change', function() {
                searchForm.submit();
            });
        });
        
        // Clear filters button
        const clearFiltersBtn = document.getElementById('clear-filters');
        if (clearFiltersBtn) {
            clearFiltersBtn.addEventListener('click', function() {
                filterInputs.forEach(input => {
                    if (input.type === 'select-one') {
                        input.selectedIndex = 0;
                    } else {
                        input.value = '';
                    }
                });
                searchForm.submit();
            });
        }
    }
}

// Appointment Booking
function initAppointmentBooking() {
    const appointmentForm = document.getElementById('appointment-form');
    const dateInput = document.getElementById('appointment_date');
    const timeSlots = document.querySelectorAll('.time-slot');
    
    if (dateInput) {
        // Set minimum date to today
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        dateInput.min = tomorrow.toISOString().slice(0, 16);
        
        // Update available time slots when date changes
        dateInput.addEventListener('change', function() {
            updateAvailableTimeSlots(this.value);
        });
    }
    
    // Handle time slot selection
    timeSlots.forEach(slot => {
        slot.addEventListener('click', function() {
            timeSlots.forEach(s => s.classList.remove('selected'));
            this.classList.add('selected');
            
            // Update hidden input with selected time
            const timeInput = document.getElementById('selected-time');
            if (timeInput) {
                timeInput.value = this.dataset.time;
            }
        });
    });
}

function updateAvailableTimeSlots(selectedDate) {
    const timeSlots = document.querySelectorAll('.time-slot');
    const selectedDay = new Date(selectedDate).getDay();
    
    // Business hours: Monday-Saturday 9 AM - 6 PM, Sunday 12 PM - 5 PM
    const businessHours = {
        0: ['12:00', '13:00', '14:00', '15:00', '16:00'], // Sunday
        1: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'], // Monday
        2: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'], // Tuesday
        3: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'], // Wednesday
        4: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'], // Thursday
        5: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00'], // Friday
        6: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']  // Saturday
    };
    
    const availableHours = businessHours[selectedDay] || [];
    
    timeSlots.forEach(slot => {
        const slotTime = slot.dataset.time;
        if (availableHours.includes(slotTime)) {
            slot.style.display = 'block';
            slot.classList.remove('disabled');
        } else {
            slot.style.display = 'none';
            slot.classList.add('disabled');
        }
    });
}

// Lead Management
function initLeadManagement() {
    const statusButtons = document.querySelectorAll('.lead-status-btn');
    const priorityButtons = document.querySelectorAll('.lead-priority-btn');
    
    statusButtons.forEach(button => {
        button.addEventListener('click', function() {
            const leadId = this.dataset.leadId;
            const newStatus = this.dataset.status;
            updateLeadStatus(leadId, newStatus);
        });
    });
    
    priorityButtons.forEach(button => {
        button.addEventListener('click', function() {
            const leadId = this.dataset.leadId;
            const newPriority = this.dataset.priority;
            updateLeadPriority(leadId, newPriority);
        });
    });
}

function updateLeadStatus(leadId, status) {
    // In a real application, this would make an AJAX call
    // For now, we'll redirect to the update URL
    window.location.href = `/crm/lead/${leadId}/update-status?status=${status}`;
}

function updateLeadPriority(leadId, priority) {
    // Similar to status update
    window.location.href = `/crm/lead/${leadId}/update-priority?priority=${priority}`;
}

// Dashboard Charts (using Chart.js)
function initDashboardCharts() {
    const propertyStatsChart = document.getElementById('property-stats-chart');
    const leadsPipelineChart = document.getElementById('leads-pipeline-chart');
    
    if (propertyStatsChart) {
        const ctx = propertyStatsChart.getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Active', 'Pending', 'Sold'],
                datasets: [{
                    data: [
                        parseInt(propertyStatsChart.dataset.active || 0),
                        parseInt(propertyStatsChart.dataset.pending || 0),
                        parseInt(propertyStatsChart.dataset.sold || 0)
                    ],
                    backgroundColor: ['#00a86b', '#ff8c42', '#0077be'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    if (leadsPipelineChart) {
        const ctx = leadsPipelineChart.getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['New', 'Contacted', 'Qualified', 'Converted'],
                datasets: [{
                    label: 'Leads',
                    data: [
                        parseInt(leadsPipelineChart.dataset.new || 0),
                        parseInt(leadsPipelineChart.dataset.contacted || 0),
                        parseInt(leadsPipelineChart.dataset.qualified || 0),
                        parseInt(leadsPipelineChart.dataset.converted || 0)
                    ],
                    backgroundColor: '#0077be',
                    borderRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
}

// Mobile Menu
function initMobileMenu() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('show');
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!mobileMenu.contains(event.target) && !mobileMenuBtn.contains(event.target)) {
                mobileMenu.classList.remove('show');
            }
        });
    }
}

// Form Validation
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Custom validation for specific fields
    const priceInputs = document.querySelectorAll('input[type="number"][data-currency]');
    priceInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value < 0) {
                this.setCustomValidity('Price cannot be negative');
            } else {
                this.setCustomValidity('');
            }
        });
    });
}

// Image Upload Preview
function initImageUpload() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function() {
            const preview = document.getElementById(this.id + '-preview');
            if (preview) {
                preview.innerHTML = '';
                
                Array.from(this.files).forEach(file => {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.className = 'img-thumbnail me-2 mb-2';
                        img.style.width = '100px';
                        img.style.height = '100px';
                        img.style.objectFit = 'cover';
                        preview.appendChild(img);
                    };
                    reader.readAsDataURL(file);
                });
            }
        });
    });
}

// Virtual Tour Integration
function initVirtualTour() {
    const virtualTourBtn = document.getElementById('virtual-tour-btn');
    const virtualTourModal = document.getElementById('virtual-tour-modal');
    const virtualTourIframe = document.getElementById('virtual-tour-iframe');
    
    if (virtualTourBtn && virtualTourModal) {
        virtualTourBtn.addEventListener('click', function() {
            const tourUrl = this.dataset.tourUrl;
            if (tourUrl && virtualTourIframe) {
                virtualTourIframe.src = tourUrl;
            }
        });
        
        // Clear iframe when modal closes
        virtualTourModal.addEventListener('hidden.bs.modal', function() {
            if (virtualTourIframe) {
                virtualTourIframe.src = '';
            }
        });
    }
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatTime(timeString) {
    return new Date(`2000-01-01T${timeString}`).toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Auto-hide alerts after 5 seconds
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        if (alert.classList.contains('show')) {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 500);
        }
    });
}, 5000);

// Loading states for buttons
document.querySelectorAll('button[type="submit"]').forEach(button => {
    button.addEventListener('click', function() {
        if (this.form && this.form.checkValidity()) {
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            this.disabled = true;
        }
    });
});

// Back to top button
const backToTopBtn = document.createElement('button');
backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
backToTopBtn.className = 'btn btn-primary position-fixed bottom-0 end-0 m-3 rounded-circle';
backToTopBtn.style.display = 'none';
backToTopBtn.style.zIndex = '1000';
document.body.appendChild(backToTopBtn);

window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
        backToTopBtn.style.display = 'block';
    } else {
        backToTopBtn.style.display = 'none';
    }
});

backToTopBtn.addEventListener('click', function() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
