try {
    productPk = JSON.parse(document.getElementById("product_pk").textContent) 
    productImage =  JSON.parse(document.getElementById("product_thumbnail").textContent) 
}

catch {

}


let selectedAttributes   =   {} //for server 
let cartItems = [] //for UI
let productsInCartHashes = []   //stores the hashcode of all items added in cart
var cartTotal = 0;


function removeItemFromProductsInCart(itemHash){
    productsInCartHashes = productsInCartHashes.filter(item => item !== itemHash);
}


function removeItemFromCartItems(itemHash){
    newList = []
    cartItems.forEach((element)=>{
        //add others, while skipping the match if its a match
        if(element.hashCode != itemHash) {
            newList.push(element)
        }
    })
    cartItems.length = 0 //empty it
    cartItems.push(...newList)
    

}

function loadCart() {
    
    try  {
        
        cartItems = JSON.parse( localStorage.getItem('cartItems') || "") ;
        cartItems.forEach((element)=>{
            //var itemInCart =  {}
            //itemInCart[element.pk] = element.attributes
            //append the hash
            productsInCartHashes.push(element.hashCode)
        })
        } catch {
            cartItems = []
        } 
          
    updateCartDisplay()    
}


function areAllAttributesSelected (){
  //checks weather all the attributes for a product are selected
  error = null
   $(".product-attr-selector").each(function(index){
   attr = $(this).attr("attribute_name")
   if(!Object.keys(selectedAttributes).includes(attr)) {
    error = "please select a/an " + attr + " option"
    return false;
   }
   })

   if(error === null){
     return true
   }
   else {
    customAlert(error)
    return false
   }
   
  
}



$(document).on("click",".select-attr",function(e){
    let code = $(this).attr("code")
    //remove active from other options
    $(".select-attr[code=" + code + "]").removeClass("active")
    //activate this particular option
    $(this).addClass("active")
    selectedAttributes[$(this).attr("attribute_name")] = $(this).attr("text-value")
})




$(document).ready(function() {
    loadCart()
});



/*
function checkForDuplicates(objs){
    for (const obj of objs) {
        if (productPk in obj) {
          const storedValue = obj[productPk];
          if (JSON.stringify(storedValue) === JSON.stringify(selectedAttributes)) {
            return true;
          }
        }
      }
      return false;
    }
*/




$(".add-to-cart").click(function() {

    //make sure all attributes are included
    if(!areAllAttributesSelected()) {
        Swal.fire({
                  
            title:"<i class='bx bx-warning' style='font-size:50px;color:#6d4afe' ></i>",
            html:"You are yet to select product attributes ",
            icon: 'error',
            showCloseButton: true,
            showCancelButton: false,
            focusConfirm: true,
            willClose: () => {
               
            },

            confirmButtonAriaLabel: 'OK!',
            customClass: {
                confirmButton: 'default-btn', // Apply custom class to confirm button
                icon: 'custom-warning-icon' // Apply custom class to icon
            },
        
        });
        return false 
    }
    
    var itemHash = generateHashCode(productName + "-"+  productPk +"-" + 
    JSON.stringify(sortDict(selectedAttributes)))


    if (productsInCartHashes.includes(itemHash)) {
        customAlert("Item with these exact attributes are already in cart, you can increase their unit before checkout")
        return 
    }
    else {
    var productName = $("#product-title").attr("value");
    var productPrice = parseFloat($("#price").text());
    var priceCurrency =$("#price-currency").text();
    var productImage = $("#product-thumbnail").attr("src")
  
    // Add the item to the cart array
    cartItems.push({
        name: productName,
        price: productPrice,
        priceCurrency: priceCurrency,
        image: productImage,
        attributes: selectedAttributes,
        pk: productPk,
        hashCode : itemHash
    });
   

    //var itemInCart =  {}
    //itemInCart[productPk] = selectedAttributes
    
    //add the hash
    productsInCartHashes.push(itemHash)
    console.log('yoko money')
    
    // Update local storage
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    
    // Update the cart display
    updateCartDisplay();
    $("#cartModal").modal("show")
    
    //empty attributes
    selectedAttributes = {}
    //clear selections
    $(".select-attr").removeClass("active")
   
}
});

function buildAttributesHtmlList(attributes) {
    attrs = ""
    for (const [param,value] of  Object.entries(attributes)){ 
        attrs = attrs +  '<li>' + param + ': ' +  '<b>' + value + '</b></li>'
    }
    return attrs
}

// Function to update the cart display v
function updateCartDisplay() {
    cartSlider = $("#cart-slider")
    var cartList = $("#cartModal > .modal-dialog > .modal-content > .modal-body > .body");
    cartList.empty();
    total = 0;
    currency = ""
    
    if(cartItems.length > 0) {
        $.each(cartItems, function(index, item) {
            currency = item.priceCurrency
            cartList.append(
                '<div class="row mb-4" id=cart-item-' + index + '>' +
                '<div class="col-4">' +
                    '<img src="' + item.image +'">' +
                '</div>' +
                '<div class="col-7" style="text-align: left;">' +
                    '<h6 >' +
                        item.name +
                    '</h6>' +
                
                    '<ul >' +
                        buildAttributesHtmlList(item.attributes) +
                    '</ul>' + 
            
                    '<h6 class="mt-0 sub-text">' + item.priceCurrency +  ' ' + item.price + '</h6>' +
                '</div>' +
                '<div class="col-1" style="display: block;">' +
                     
                        '<ion-icon item-hash="' + item.hashCode + '" target="#cart-item-' + index + '" class="cart-remove-item" name="remove-outline" id="cart-remove-item' + index + '">1</ion-icon>' +
                       
                '</div>' +
            '</div>' 
                );

            total += item.price;
        });

        $("#cart-total").text( currency +" "+ total.toFixed(2));
        //show button
        btn = $("#cartModal > .modal-dialog > .modal-content > .modal-body > .footer")
        btn.removeClass("hide")
        //update counter
        $("#cart-counter").html(cartItems.length)
        $("#cart-counter").removeClass("hide")
       
    } else {
        cartList.html('No items added yet')
    }    
}

$(document).on("click",".cart-remove-item",function(e){
    target = $(this).attr("target")
    itemHash = $(this).attr("item-hash")
    removeItemFromProductsInCart(itemHash)
    removeItemFromCartItems(itemHash)
    //update local storage
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    updateCartDisplay()
  


})


$("#clear-cart").click(function() {
    // Clear the cart array and local storage
    cartItems = [];
    productsInCartHashes = [];
    localStorage.removeItem('cartItems');
    //hide buttons
    btn = $("#cartModal > .modal-dialog > .modal-content > .modal-body > .footer")
    btn.addClass("hide")
    //update price
    $("#cart-total").html(0)
    //close modal
    $("#cartModal").modal("hide")
    //hide counter
    $("#cart-counter").addClass('hide')
    // Update the cart display
    updateCartDisplay();
});



