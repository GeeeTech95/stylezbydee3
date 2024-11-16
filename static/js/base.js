var csrfToken = $('input[name = csrfmiddlewaretoken]').val()
var logoUrl = $("#loading-img").attr("src")


function getLoaderVerbose(){

  let html = '<div class="loading-container">' +
  '  <div class="text-center" >' +
  '    <img class="loading-img" src="' + logoUrl + '">' +
  '  </div>' +
  '</div>';


return html
}



$(".mobile-nav-btn").click(function(e){
  var target = $(this).attr("target")
  if(target == "open") {
   
    $(".mobile-nav-btn ion-icon").attr("name","close-outline")
    $(this).attr("target","close")
    openNav()
  }
  else {
   
    $(".mobile-nav-btn ion-icon").attr("name","menu-outline")
    $(this).attr("target","open")
    closeNav()
  }
  


})

// Function to generate a hash code from a string
function generateHashCode(inputString) {
  // Use JSON.stringify to convert the string to a JSON representation
  const jsonString = JSON.stringify(inputString);

  // Use a simple hash function, such as the following
  let hash = 0;
  for (let i = 0; i < jsonString.length; i++) {
    const char = jsonString.charCodeAt(i);
    hash = (hash << 5) - hash + char;
  }

  return hash;
}



function sortDict(originalDict){
  sortedKeys = Object.keys(originalDict).sort();

  // Create a new sorted dictionary
  const sortedDict = {};
  for (const key of sortedKeys) {
    sortedDict[key] = originalDict[key];
  }
  
  return sortedDict
}


function areObjectsIdentical(obj1, obj2) {
  const keys1 = Object.keys(obj1);
  const keys2 = Object.keys(obj2);

  // Check if the objects have the same number of keys
  if (keys1.length !== keys2.length) {
    return false;
  }

  // Sort the keys to ensure key order doesn't matter
  keys1.sort();
  keys2.sort();

  // Check if all keys are identical
  if (!keys1.every((key, index) => key === keys2[index])) {
    return false;
  }

  // Check if the values for each key are identical
  return keys1.every(key => obj1[key] === obj2[key]);
}





function openNav() {
    document.getElementById("cartSideBar").style.width = "80vw";
  }
  
  function closeNav() {
    document.getElementById("cartSideBar").style.width = "0";
  }


  function openFilter() {
    filterObj = document.getElementById("filterSideBar")
    if(filterObj.style.width != "80vw"){
        filterObj.style.width = "80vw";
    }
    else {
        filterObj.style.width = "0";
    }
  }

  function closeFilter() {
    document.getElementById("filterSideBar").style.width = "0";
  }


  $(".modal-btn").click(function(e){
    $($(this).attr("data-target")).modal("show");
  })

  $(".close-modal-btn").click(function(e){
    $($(this).attr("data-target")).modal("hide");
  })


  $(document).ready(function(){
    $(".xcart-btn").hover(function(e){
      //updateCartDisplay()
      $("#cartModal").modal("show")
    })
     //mark active
     let activeNavLink = sessionStorage.getItem("active-nav-link")
     if(activeNavLink == null){
         activeNavLink = ""
     }
     activeNavLink = ".link-item[href='" + activeNavLink + "']"
     $(activeNavLink).addClass("active")
  });

$(".link-item").click(function(e){
  //register the active link
  var val = $(this).attr("href")
  sessionStorage.setItem("active-nav-link",val)
})


/*
(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	var burgerMenu = function() {

		$('.js-colorlib-nav-toggle').on('click', function(event) {
			event.preventDefault();
			var $this = $(this);
			if( $('body').hasClass('menu-show') ) {
				$('body').removeClass('menu-show');
				$('#colorlib-main-nav > .js-colorlib-nav-toggle').removeClass('show');
			} else {
				$('body').addClass('menu-show');
				setTimeout(function(){
					$('#colorlib-main-nav > .js-colorlib-nav-toggle').addClass('show');
				}, 900);
			}
		})
	};
	burgerMenu();


})(jQuery);

*/


function openSearch(){
	$('.search-area').toggleClass('open');
}

function closeSearch(){
	$('.search-area').removeClass("open");
}

function customAlert(message){
  $("#alert-modal .modal-dialog .modal-content #modal-message").html(message)
  $("#alert-modal").modal("show")

}

function isFormFilled(formInputsObj){
  let formIsFilled = true
  formInputsObj.each(function(index){
    input = $(this)
     if(input.attr("required") != undefined){
      if(input.val() === ""){
         formIsFilled = false
      }
     }
  })

  return formIsFilled
}


function handleFormError(form_object, error_response,  popup = true) {
  //apply error

  for (const [field, error] of Object.entries(error_response)) {
      $(".field-error[input-name=" + field + "]").html(error)

  }
  dangerText = "please correct the form errors"

  //check for general errors
  if (error_response.non_field_errors) {
      dangerText = error_response.non_field_errors
  }

  if (popup) {
      customAlert(dangerText)
  }
}

function setCookie(cname, cvalue, exdays=30) {
  //30 days as default expiry
  const d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  let expires = "expires="+ d.toUTCString();
  document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}


// PRELOADER JS
document.addEventListener("DOMContentLoaded", function() {
  console.log("DOM fully loaded and parsed");
  window.addEventListener("load", function() {
      const preloader = document.getElementById("preloader");
      preloader.style.opacity = 0; // Optional: Fade out effect
      setTimeout(() => preloader.remove(), 500); // Remove after fade-out
  });
});
