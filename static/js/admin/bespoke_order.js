
   $(document).ready(function() {

    // Handle the "Assigned" button click
    $('.staff-status-btn').on('click', function() {
     
        var orderId = $(this).attr('data-order-id');
        var url = $(this).attr("data-target-url")
        var newStatus = $(this).attr("data-new-status")
     

        
        $('#update-staff-info-status').removeAttr("hidden") //incase it was hidden
        if (newStatus == "accepted"){
            $("#updateStaffInfoStatusModalLabel").html("Accept Job")
            $("#update-staff-info-status").html("Yes, Accept")
            $("#updateStaffInfoStatusModalBody p").html("This job has been assigned to you, Would you like to accept this job?")
       
        }
        else if(newStatus == "completed"){
            $("#updateStaffInfoStatusModalLabel").html("Mark Job As Completeed")
            $("#update-staff-info-status").html("Yes, It's Completed")
            $("#updateStaffInfoStatusModalBody p").html("Would you like to mark this job as completed ?")
        }

        else if(newStatus == "to-be-approved-by-admin"){
            $("#updateStaffInfoStatusModalLabel").html("Pending Approval")
            $("#update-staff-info-status").html("Yes, It's Completed")
            $("#updateStaffInfoStatusModalBody p").html("You have marked this order as completed, waiting for approval from admin !")
            $('#update-staff-info-status').attr("hidden","")
        }
        
        //only for admin
        else if (newStatus == "approved"){
           
            $("#updateStaffInfoStatusModalLabel").html("Approve Job")
            $("#update-staff-info-status").html("Yes, I want to Approve")
            $("#updateStaffInfoStatusModalBody p").html("Staff has marked this delegation as completed, have you evaluated and want to approve ?")
        }
        $('#update-staff-info-status').attr('data-order-id', orderId);
        $('#update-staff-info-status').attr('data-target-url', url);
        $('#update-staff-info-status').attr('data-new-status', newStatus);
         // Show the modal
         $('#updateStaffInfoStatusModal').modal('show');
       
    });

    // Handle the confirmation of job acceptance
    $('#update-staff-info-status').on('click', function() {
        var orderId = $(this).attr('data-order-id');
        var targetUrl = $(this).attr('data-target-url');
        var newStatus = $(this).attr("data-new-status")
      

        // Send AJAX request to create a new log and update the order status
        $.ajax({
            url: targetUrl,  // URL pattern for handling the request
            method: 'POST',
            dataType: 'json',
            data: {
                'order_id': orderId,
                'new_status' : newStatus,
                "csrfmiddlewaretoken": document.querySelector('[name = csrfmiddlewaretoken]').value
            },
            success: function(response) {
                if (response.success) {
                    // Close the modal
                    $('#updateStaffInfoStatusModal').modal('hide');
                   
                    // Update status text
                    var statusButton = $('#update-staff-info-btn-' + orderId);
                    statusButton.text(newStatus.toUpperCase());
                    if(newStatus == "approved"){
                        statusButton.removeClass().addClass('task-btn bg-success text-white fs-14 ');
                        $(".apoprove-delegation-btn").attr("hidden","")
                    }else {
                        statusButton.removeClass('bg-warning').addClass('bg-primary text-white');
                    }
                   
                    statusButton.attr("data-new-status",newStatus)
                    window.location.reload();
                } else {
                    alert(response.error);
                }
            },
            error: function(xhr, errmsg, err) {
                console.error('Error:', errmsg);
                alert('Error in processing, please retry.');
            }
        });
    });



    // When   the Mark Advance Payment button is clicked, show the confirmation modal
    $('.change-order-status-btn').on('click', function() {
   
        targetUrl =  $(this).attr('data-target-url');
        action = $(this).attr('data-action-type');
     
        if (action == "advance-payment"){
            $("#confirmPaymentModalModalLabel").html("Mark Advance Payment")
            $("#confirmPaymentModalBtn").html("Yes, Mark as Paid")
            $("#confirmPaymentModalBody").html("Would you like to mark advance made for this order ?")
        }
        else if(action == "complete-payment"){
            $("#confirmPaymentModalLabel").html("Mark Complete Payment")
            $("#confirmPaymentModalBtn").html("Yes, Mark as Paid")
            $("#confirmPaymentModalBody").html("Would you like to mark complete payment made for this order ?")
        }

        $("#confirmPaymentModalBtn").attr("data-target-url",targetUrl )
        $('#confirmPaymentModal').modal('show');
    });

    // When the user confirms in the modal, send the AJAX request
    $('#confirmPaymentModalBtn').on('click', function() {
        targetUrl =  $(this).attr('data-target-url');
        $.ajax({
            url: targetUrl,
            type: 'POST',
            data: {
                "csrfmiddlewaretoken": document.querySelector('[name = csrfmiddlewaretoken]').value,
            },
            success: function(response) {
                if (response.success) {
            
                    location.reload();  // Reload to update the order status logs
                } else {
         
                }
                $('#confirmPaymentModal').modal('hide');  // Hide the modal
            },
            error: function(xhr, errmsg, err) {
                alert("Error occurred. Please try again.");
                $('#confirmPaymentModal').modal('hide');  // Hide the modal in case of error
            }
        });
    });

});







document.addEventListener('DOMContentLoaded', function () {
    const addFormButton = document.querySelector('.add-form');
    const staffFormset = document.querySelector('.staff-formset');
    const totalFormsInput = document.querySelector('input[name="staff_info-TOTAL_FORMS"]');

    if (addFormButton && staffFormset && totalFormsInput) {
        addFormButton.addEventListener('click', function () {
            const formCount = parseInt(totalFormsInput.value, 10);
            const lastForm = staffFormset.lastElementChild;
            
            if (lastForm) {
                // Clone the last form in the formset and reset its fields
                const newForm = lastForm.cloneNode(true);

                newForm.querySelectorAll('input, select').forEach(input => {
                    input.name = input.name.replace(/-\d+-/, `-${formCount}-`);
                    input.id = input.id.replace(/-\d+-/, `-${formCount}-`);

                    // Clear input values for the cloned form
                    if (input.type === 'text' || input.type === 'number' || input.tagName.toLowerCase() === 'select') {
                        input.value = '';
                    }

                    // Uncheck checkboxes if any
                    if (input.type === 'checkbox') {
                        input.checked = false;
                    }
                });

                // Update the form label
                const formLabel = newForm.querySelector('h5');
                if (formLabel) {
                    formLabel.textContent = `Staff Assignment ${formCount + 1}`;
                }

                // Append the new form to the formset
                staffFormset.appendChild(newForm);

                // Increment TOTAL_FORMS by 1
                totalFormsInput.value = formCount + 1;
            } else {
                console.error("No form available to clone. Ensure staffFormset has at least one form.");
            }
        });

        // Event delegation for removing forms
        staffFormset.addEventListener('click', function (event) {
            if (event.target.classList.contains('delete-form')) {
                const form = event.target.closest('.staff-form');

                if (form) {
                    // Find the DELETE checkbox in the form
                    const deleteCheckbox = form.querySelector('input[name$="-DELETE"]');
                    if (deleteCheckbox) {
                        deleteCheckbox.checked = true;  // Mark the form as deleted

                        // Hide the form visually
                        form.style.display = 'none';
                    }
                }

                // Update form labels and total form count to exclude deleted forms
                let activeFormsCount = 0;
                Array.from(staffFormset.children).forEach((form, index) => {
                    if (form.style.display !== 'none') {  // Count only visible forms
                        const formLabel = form.querySelector('h5');
                        if (formLabel) {
                            formLabel.textContent = `Staff Assignment ${activeFormsCount + 1}`;
                        }
                        activeFormsCount++;
                    }
                });

                // Update TOTAL_FORMS to reflect active forms
                totalFormsInput.value = activeFormsCount;
            }
        });
    } else {
        console.error("Required elements not found for formset operations.");
    }
});

