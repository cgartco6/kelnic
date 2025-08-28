// Main JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Navigation and general functionality
    initializeNavigation();
    initializeModals();
    initializeForms();
});

function initializeNavigation() {
    // Smooth scrolling for navigation links
    document.querySelectorAll('nav a').forEach(link => {
        link.addEventListener('click', function(e) {
            if (this.getAttribute('href').startsWith('#')) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    targetSection.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
}

function initializeModals() {
    // Modal functionality
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        const closeButton = modal.querySelector('.close-modal');
        if (closeButton) {
            closeButton.addEventListener('click', () => {
                modal.classList.remove('active');
            });
        }
    });
}

function initializeForms() {
    // Form validation and submission
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            // Form validation logic here
        });
    });
}
