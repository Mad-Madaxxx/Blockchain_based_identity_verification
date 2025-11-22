// Main JavaScript file for Blockchain Identity Verification System

// Utility function to format dates
function formatDate(timestamp) {
    return new Date(timestamp * 1000).toLocaleString();
}

// Utility function to copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        alert('Copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy:', err);
    });
}

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.display = 'none';
        }, 5000);
    });
});

// Form validation helper
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// DID validation helper
function validateDID(did) {
    return did.startsWith('did:identity:') && did.length > 20;
}

// Show loading state
function showLoading(element) {
    element.innerHTML = '<p>Loading...</p>';
}

// Show error message
function showError(element, message) {
    element.innerHTML = `<div class="error-box"><p>Error: ${message}</p></div>`;
}

// Show success message
function showSuccess(element, message) {
    element.innerHTML = `<div class="success-box"><p>${message}</p></div>`;
}

