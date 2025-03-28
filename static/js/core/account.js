



$(document).on("submit", ".login-form", function (e) {
    e.preventDefault();

    let form = $(this);
    let data = new FormData(form[0]);

    let buttonObj = form.find("button");
    let origText = buttonObj.html();
    changeToLoading(buttonObj, "Logging in...");

    $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),
        timeout: 5000,

        success: function (response) {
            let url = response.success_url;
            window.location.href = url;
        },

        statusCode: {
            400: function (response) {
                normalizeLoadingButton(buttonObj, origText);
                Swal.fire({
                    icon: "error",
                    title: "Login Failed",
                    text: response.responseJSON.detail || "Invalid credentials. Please check your email and password.",
                    confirmButtonColor: "#994d99",
                    confirmButtonText: "Try Again"
                });
            },

            500: function () {
                normalizeLoadingButton(buttonObj, origText);
                Swal.fire({
                    icon: "error",
                    title: "Server Error",
                    text: "Something went wrong on the server. Please try again later.",
                    confirmButtonColor: "#d33",
                    confirmButtonText: "OK"
                });
            }
        }
    });
});




$(document).on("submit", ".registration-form", function (e) {
    e.preventDefault();

    let form = $(this);
    let buttonObj = form.find("button");
    let origText = buttonObj.html();

    changeToLoading(buttonObj, "Creating Account...");

    $.ajax({
        type: "POST",
        url: form.attr("action"),
        data: form.serialize(),

        success: function (response) {
            normalizeLoadingButton(buttonObj, "Register Account");

            let account_id = response.account_id;

            Swal.fire({
                icon: "success",
                title: "Registration Successful!",
                html: `Your account ID: <strong>${account_id}</strong>`,
                confirmButtonText: "Verify Email",
                showCloseButton: true,
                allowOutsideClick: false,
                willClose: () => {
                    window.location.href = form.attr("success_link");
                }
            });
        },

        error: function (response) {
            normalizeLoadingButton(buttonObj, "Register Account");

            let errorMessage = response.responseJSON?.detail || "An error occurred. Please try again or contact support.";

            Swal.fire({
                icon: "error",
                title: "Registration Failed",
                text: errorMessage,
                confirmButtonText: "Retry",
                showCloseButton: true
            });
        },

        statusCode: {
            400: function (response) {
                normalizeLoadingButton(buttonObj, "Register Account");
                handleFormError(form, response.responseJSON);

                Swal.fire({
                    icon: "error",
                    title: "Form Error",
                    text: "Please correct the errors in the form.",
                    confirmButtonText: "Fix Issues",
                    showCloseButton: true
                });
            },

            500: function () {
                normalizeLoadingButton(buttonObj, "Register Account");

                Swal.fire({
                    icon: "error",
                    title: "Server Error",
                    text: "Request timed out. Please retry later.",
                    confirmButtonText: "OK",
                    showCloseButton: true
                });
            }
        }
    });
});



$(document).on("submit", ".registration-form-old", function (e) {
    e.preventDefault()
    buttonObj = $(this).find("button")

  

    
    changeToLoading(buttonObj, "Creating Account")

    //send ajax
    form = $(this)
    data =   form.serialize(),
  
    //crfToken = document.querySelector('[name = csrfmiddlewaretoken]').value,
     
    $.ajax({

        type: "POST",
        url: form.attr("action"),
        data: data,
        success: function (response) {
           
            normalizeLoadingButton(buttonObj,"Register Account")
            account_id = response.account_id
            Swal.fire({
                  
                icon: "success",
                html:"Registration was successful, your account id:  " + account_id,
                showCloseButton: true,
                showCancelButton: false,
                focusConfirm: true,
                willClose: () => {
                    account_id = response.account_id
                    window.location.href = form.attr("success_link")
                },
                confirmButtonAriaLabel: 'Verify Email',
            
            });
           
            
        },
        error : function(response){

            normalizeLoadingButton(buttonObj,"Register Account")
            Swal.fire({
                icon : "error",
                //title:"<i class=' fas fa-exclamation-circle' style='font-size:38px;color:red' ></i>",
                text:"An error occured , please retry or contact support. " + response.responseJSON['detail'],
                showCloseButton: true,
                showCancelButton: false,
                focusConfirm: false,
                confirmButtonAriaLabel: 'Close!',
           
            });
           
        },
        statusCode: {
            400: function (response) {
                normalizeLoadingButton(buttonObj,"Register Account")
                handleFormError(form, response.responseJSON)
                Swal.fire({
                    icon : "error",
                    title:"<i class=' fas fa-exclamation-circle' style='font-size:38px;color:red' ></i>",
                    text:"Please correct the form errors",
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonAriaLabel: 'Close!',
               
                });
              
               
            },

            500: function (response) {
             
                normalizeLoadingButton(form.find(".form-group button"), "Register Account")
                Swal.fire({
                    icon : "error",
                   
                    text:"Request timed out, please retry",
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonAriaLabel: 'Close!',
               
                });
               
            }
        }

    })
})


$(document).on("submit", ".verify-email-form", function (e) {
    e.preventDefault()
    buttonObj = $(this).find("div button")
    const inputs = document.querySelectorAll(".otp-field input");

    let otp = "";
    inputs.forEach((input) => {
        otp += input.value;
        input.disabled = true;
        input.classList.add("disabled");
    })
    changeToLoading(buttonObj, "Verifying")

    //send ajax
    form = $(this)
    data =  {
        "otp" : otp,
        "csrfmiddlewaretoken": document.querySelector('[name = csrfmiddlewaretoken]').value
    },
  
    //crfToken = document.querySelector('[name = csrfmiddlewaretoken]').value,
     
    $.ajax({

        type: "POST",
        url: form.attr("action"),
        data: data,
        timeout: 3000,
        success: function (response) {
            normalizeLoadingButton(buttonObj, "Verify")
             if(response.success){
                Swal.fire({
                    //title:"<i class='fas fa-hourglass-half' style='font-size:50px;color:#6d4afe' ></i>",
                    icon: 'success',
                    html:"Your email address has been verified successfully!",
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: true,
                    willClose: () => {
                        url = response.success_url
                        window.location.href = form.attr("dashboard_link")
                    },
                    confirmButtonAriaLabel: 'Back To Dasboard',
                
                });
               
                
             }
             else {
                Swal.fire({
                    //title:"<i class='fas fa-hourglass-half' style='font-size:50px;color:#6d4afe' ></i>",
                    icon: 'error',
                    html:response.error,
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: true,
                  
                    confirmButtonAriaLabel: 'OK!',
                
                });

             }
    
        },
      

    })


})




$(document).on("submit", ".kyc-form", function (e) {

    e.preventDefault()
    buttonObj = $(this).find("#kyc-submit-btn")

    changeToLoading(buttonObj, "Uploading")
    
    var formData = new FormData(this); 
    //send ajax
    form = $(this)
    data =   form.serialize(),

    //crfToken = document.querySelector('[name = csrfmiddlewaretoken]').value,
     
    $.ajax({
        data: formData,
        contentType: false,  // Important: Do not set content type, it will be set by FormData
        processData: false, 
        type: "POST",
        url: form.attr("action"),
        data: formData,
        timeout: 3000,
        success: function (response) {
            normalizeLoadingButton(buttonObj, "Submit")
             if(response.success){
        
                Swal.fire({
                  
                    title:"<i class='fas fa-hourglass-half' style='font-size:50px;color:#6d4afe' ></i>",
                    html:"Your KYC request was submitted successfully. It's currently in review!, you will be notified when it's completed.",
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: true,
                    willClose: () => {
                        url = response.success
                        window.location.href = url
                    },
                    confirmButtonAriaLabel: 'OK!',
                
                });
           
          
               
                
             }
             else if(response.error){
              
                Swal.fire({
                    icon : "error",
                    title:"<i class=' fas fa-exclamation-circle' style='font-size:38px;color:red' ></i>",
                    text:response.error,
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonAriaLabel: 'Close!',
               
                });
               
             }

             else if(response.form_errors){
                //customize
                //handleFormError(form,response.form_errors)
                Swal.fire({

                    title:"<i class=' fas fa-exclamation-circle' style='font-size:38px;color:red' ></i><br><span style='font-family:normal;margin-right:10px'>Correct Form Errors</span>",
                    icon: 'error',
                    html:response.form_errors,
                    showCloseButton: true,
                    showCancelButton: false,
                    focusConfirm: false,
                    confirmButtonAriaLabel: 'OK!',
                
                });
              
              }
    
        },
   
         
         
 
        error : function(response){

            normalizeLoadingButton(buttonObj,"Submit")
            Swal.fire({


                icon: 'error',
                html:"An error occured , please retry or contact support.",
                showCloseButton: true,
                showCancelButton: false,
                focusConfirm: false,
                confirmButtonAriaLabel: 'OK!',
            
            });
             
        },

        

    })
})





