
$(document).ready(function() {
    $('.salary-paid-btn').click(function(event) {
       
        event.preventDefault();

        // Get the URL from the button's data attribute
        let button = $(this);
        let url = button.data('target-url');

        // Perform the AJAX request
        $.ajax({
            url: url,
            type: 'POST',
            data : {
                "csrfmiddlewaretoken": document.querySelector('[name = csrfmiddlewaretoken]').value
            },
            success: function(response) {
                // Update the button text to "Paid" and disable it
                button.text('Paid').prop('disabled', true);
            },
            error: function(xhr, status, error) {
                console.error("Failed to mark salary as paid:", error);
            }
        });
    });
});


