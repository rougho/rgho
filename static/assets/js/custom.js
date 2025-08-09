// Toast Notifications
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all toasts
    var toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(function(toastElement) {
        var toast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 10000
        });
        
        // Show the toast
        toast.show();
        
        // Add countdown timer
        var timeElement = toastElement.querySelector('.text-muted');
        var timeLeft = 10;
        
        var countdown = setInterval(function() {
            timeLeft--;
            if (timeLeft > 0) {
                timeElement.textContent = timeLeft + 's left';
            } else {
                clearInterval(countdown);
            }
        }, 1000);
        
        // Clear interval when toast is hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            clearInterval(countdown);
        });
    });
});

