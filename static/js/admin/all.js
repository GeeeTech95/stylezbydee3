$(document).ready(function () {
    var targetUrl = ""; // Store the delete URL

    $('.delete-btn').click(function (event) {
        event.preventDefault();  // Prevent default link behavior
        
        targetUrl = $(this).attr('data-target-url');  
        var modalTitle = $(this).attr('data-title');  
        var modalMessage = $(this).attr('data-message');  

        $('#deleteModalLabel').text(modalTitle);  
        $('#deleteModalMessage p').text(modalMessage);
    });

    $('#confirm-delete').click(function () {
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        if (targetUrl) {
           
            $.ajax({
                url: targetUrl,
                type: 'POST',  // Django requires POST for deletion
                data: {
                    "csrfmiddlewaretoken": csrftoken

                },
                success: function () {
                    $('#delete_modal').modal('hide'); // Hide the modal
                    setTimeout(function () {
                        location.reload(); // Reload page after deletion
                    }, 500);
                },
                error: function (xhr, status, error) {
                    console.error("Failed to delete item:", error);
                }
            });
        }
    });
});