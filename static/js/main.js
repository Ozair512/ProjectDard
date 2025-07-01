// Main JavaScript for Project Dard

// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeVoting();
    initializeFormValidation();
    initializeTooltips();
    initializeLanguageSwitcher();
    initializeCharacterCount();
    initializeAutoResize();
});

// Initialize voting functionality
function initializeVoting() {
    const voteButtons = document.querySelectorAll('.vote-btn');
    
    voteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const commentId = this.dataset.commentId;
            const voteType = this.dataset.voteType;
            
            // Disable button temporarily
            this.disabled = true;
            this.classList.add('loading');
            
            // Make AJAX request
            fetch(`/vote_comment/${commentId}/${voteType}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        showAlert('Error: ' + data.error, 'danger');
                        return;
                    }
                    
                    // Update vote counts
                    const commentItem = document.querySelector(`[data-comment-id="${commentId}"]`);
                    const likeCountSpan = commentItem.querySelector('.like-count');
                    const dislikeCountSpan = commentItem.querySelector('.dislike-count');
                    
                    if (likeCountSpan) likeCountSpan.textContent = data.likes;
                    if (dislikeCountSpan) dislikeCountSpan.textContent = data.dislikes;
                    
                    // Handle hidden comment
                    if (data.hidden) {
                        commentItem.style.opacity = '0.5';
                        commentItem.innerHTML += '<div class="alert alert-warning mt-2"><i class="fas fa-eye-slash me-2"></i>This comment has been hidden due to community feedback.</div>';
                    }
                    
                    // Visual feedback
                    this.classList.add('animate__animated', 'animate__pulse');
                    setTimeout(() => {
                        this.classList.remove('animate__animated', 'animate__pulse');
                    }, 1000);
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('An error occurred while voting.', 'danger');
                })
                .finally(() => {
                    // Re-enable button
                    this.disabled = false;
                    this.classList.remove('loading');
                });
        });
    });
}

// Initialize form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            
            this.classList.add('was-validated');
        });
    });
}

// Initialize tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize language switcher
function initializeLanguageSwitcher() {
    const languageLinks = document.querySelectorAll('a[href*="/set_language/"]');
    
    languageLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Show loading state
            const currentLang = document.querySelector('.navbar-nav .dropdown-toggle');
            if (currentLang) {
                currentLang.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Loading...';
            }
        });
    });
}

// Initialize character count for textareas
function initializeCharacterCount() {
    const textareas = document.querySelectorAll('textarea[maxlength]');
    
    textareas.forEach(textarea => {
        const maxLength = parseInt(textarea.getAttribute('maxlength'));
        
        // Create counter element
        const counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.innerHTML = `<span class="char-count">0</span>/${maxLength} characters`;
        
        // Insert after textarea
        textarea.parentNode.insertBefore(counter, textarea.nextSibling);
        
        // Update counter on input
        textarea.addEventListener('input', function() {
            const currentLength = this.value.length;
            const charCountSpan = counter.querySelector('.char-count');
            
            charCountSpan.textContent = currentLength;
            
            // Change color based on limit
            if (currentLength > maxLength * 0.9) {
                charCountSpan.style.color = '#dc3545';
            } else if (currentLength > maxLength * 0.8) {
                charCountSpan.style.color = '#ffc107';
            } else {
                charCountSpan.style.color = '#28a745';
            }
        });
        
        // Trigger initial update
        textarea.dispatchEvent(new Event('input'));
    });
}

// Initialize auto-resize for textareas
function initializeAutoResize() {
    const textareas = document.querySelectorAll('textarea');
    
    textareas.forEach(textarea => {
        // Set initial height
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
        
        // Auto-resize on input
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
}

// Show alert message
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container.mt-5.pt-4');
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.setAttribute('role', 'alert');
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Insert at the beginning of the container
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
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

// Handle form submissions with loading states
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function() {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Please wait...';
        }
    });
});

// Handle back button
window.addEventListener('popstate', function(event) {
    // Reload page on back button to ensure fresh content
    location.reload();
});

// Add fade-in animation to cards
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll('.card').forEach(card => {
    observer.observe(card);
});

// Handle language direction changes
function updateTextDirection() {
    const html = document.documentElement;
    const currentLang = html.getAttribute('lang');
    
    if (currentLang === 'fa') {
        html.setAttribute('dir', 'rtl');
        document.body.classList.add('rtl');
    } else {
        html.setAttribute('dir', 'ltr');
        document.body.classList.remove('rtl');
    }
}

// Call on page load
updateTextDirection();

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + / for search (if implemented)
    if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"]');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals/dropdowns
    if (e.key === 'Escape') {
        // Close any open dropdowns
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
            const dropdown = bootstrap.Dropdown.getInstance(menu.previousElementSibling);
            if (dropdown) {
                dropdown.hide();
            }
        });
    }
});

// Print functionality
function printPage() {
    window.print();
}

// Export functionality (if needed)
function exportData(format) {
    // This would be implemented based on specific requirements
    console.log(`Exporting data in ${format} format`);
}

// Theme toggle (if dark/light mode toggle is added)
function toggleTheme() {
    document.body.classList.toggle('light-theme');
    
    // Save preference
    localStorage.setItem('theme', 
        document.body.classList.contains('light-theme') ? 'light' : 'dark'
    );
}

// Load saved theme preference
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
    document.body.classList.add('light-theme');
}

// Utility functions
const utils = {
    // Format date
    formatDate: function(date, language = 'en') {
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        
        return new Date(date).toLocaleDateString(language === 'fa' ? 'fa-IR' : 'en-US', options);
    },
    
    // Truncate text
    truncateText: function(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substr(0, maxLength) + '...';
    },
    
    // Escape HTML
    escapeHtml: function(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    },
    
    // Get URL parameter
    getUrlParameter: function(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }
};

// Make utils available globally
window.DardUtils = utils;

// Console log for debugging (remove in production)
console.log('Project Dard JavaScript loaded successfully');
