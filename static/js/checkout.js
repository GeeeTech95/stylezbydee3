let currency = ""

$(document).ready(function(e){
    try  {
        productsInCart = []
        cartItems = JSON.parse( localStorage.getItem('cartItems') || "") ;
        cartItems.forEach((element)=>{
            productsInCart.push(element.hashCode)
        })
        
        } catch {
            cartItems = []
        } 
        updateOrderSummary()
})



// Function to update the cart display v
function updateOrderSummary() {
    cartSlider = $("#cart-slider")
    var cartList = $("#order-summary-tab #summary");
    cartList.empty();
    total = 0;
   
    
    if(cartItems.length > 0) {
        $.each(cartItems, function(index, item) {
            currency = item.priceCurrency
            cartList.append(
                '<div class="row mb-4" id=item-' + index + '>' +
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
            
                    '<h6 class="mt-0 sub-text price" item-price=' + item.price.toFixed(2)  + '  id="item-price-' + index +  '" >' +  item.priceCurrency +  ' ' + item.price.toFixed(2) + '</h6>' +
                    '<h5 class="mt-0 sub-text total-price" total-price=' + item.price.toFixed(2)  +' id="item-price-total-' + index + '"  >Total: ' + item.priceCurrency +  ' ' + item.price.toFixed(2) + '</h5>' +
                '</div>' +
                '<div class="col-1" style="display: block;">' +
                    '<a class="update-cart-unit"  action="add" target="#cart-unit-counter-' + index + '" >' +
                        '<ion-icon name="add"   ></ion-icon>' +
                    '</a>' +        
                        '<h6 id="cart-unit-counter-' + index + '">1</h6>' +
                        '<ion-icon name="remove" class="update-cart-unit" action="subtract" target="#cart-unit-counter-' + index + '"></ion-icon>' +   
                '</div>' +
            '</div>' 
                );

            total += item.price;
        });

        $("#order-summary-tab #total").text( currency + " " + total.toFixed(2));
        //show button
        btn = $("#cartModal > .modal-dialog > .modal-content > .modal-body > .footer")
        btn.removeClass("hide")
        //update counter
        $("#cart-counter").html(cartItems.length)
        $("#cart-counter").removeClass("hide")
       
    } else {
        cartList.html('<center>Your Shopping Cart is empty, please add items to your cart and try again !!</center>')
    }    
}


$(document).on("click",".update-cart-unit", function(){
    target = $(this).attr("target")
    splitArray = target.split("-")
    index = splitArray[splitArray.length - 1 ]
    targetObj = $(target)
    currentValue = targetObj.text()
    currentValue = parseFloat(currentValue)
    if ($(this).attr("action") == "add") {
        currentValue ++
    }
    else if ($(this).attr("action") == "subtract") {
        if(currentValue == 1){
            //then its a removal
        }
        else {
            currentValue --
        }
    }
    price = $("#item-price-"+index).attr("item-price")
    total = parseFloat(price) * currentValue
    $("#item-price-total-"+index).html("Total: " + currency + " " + total.toFixed(2))
    $("#item-price-total-"+index).attr("total-price",total.toFixed(2))
    targetObj.html(currentValue)
    updateTotalPrice()

})


function updateTotalPrice(){
    //parse through all total
    sum = 0
    $(".total-price").each(function(index){
        sum = sum + parseFloat($(this).attr("total-price"))
    })
    $("#order-summary-tab #total").text( currency + " "+ sum.toFixed(2));
}


$(document).on('click',".chat-checkout",function(e){
    //show loading modal
    $("#load-modal").modal("show");
    //ensure all details are filled

 
    //check if form has been completely filled
    inputsObj = $("#delivery-details-form input, select")
    if (false){
        //!isFormFilled(inputsObj)
        //activate form tab
        //$("#delivery-info-btn").click()
        customAlert("Please enter your delivery details!")
        return false
    }

    cartData = []
    cartItems.forEach((element,index)=>{
        product = {}
        product['product'] = element.pk
        product['attributes'] = element.attributes
        product['quantity'] = parseInt($("#cart-unit-counter-" + index).html())
        cartData.push(product)
    })
      
    formObj = $("#delivery-details-form") 
    const url = formObj.attr("action")

    var object = {};
    data = new FormData(formObj[0])
    data.forEach((value, key) => {
    // Reflect.has in favor of: object.hasOwnProperty(key)
    if(!Reflect.has(object, key)){
        object[key] = value;

        return;
    }
    if(!Array.isArray(object[key])){
        object[key] = [object[key]];    
    }
    object[key].push(value);
});

    data = {"cart" : cartData, "shipping_details" : JSON.stringify(object)}
    console.log(data)
    //send ajax
    $.ajax({
        type: "POST",
        url: url,
        headers: { "X-CSRFToken": csrfToken,"content-type" : "application/json"},
        data: JSON.stringify(data),
        timeout: 3000,
        beforeSend : function(){
     
        },

        success: function (response) {
           //show success modal

           //redirect to order detail
        },

        error: function () {
            //$(".modal").modal("hide");
            //customAlert("Request timed out, please reload")
        },

        statusCode: {
            400: function (response) {
                $("#load-modal").modal("hide");
                //$('a[href="' + '#delivery-info' + '"]').trigger('click');
               
                if(response.responseJSON['shipping_details_error']){
                    handleFormError(formObj,response.responseJSON['error'])
                    customAlert("Please correct the errors on the delivery info form ")
                }
                else if(response.responseJSON['cart_error']){
                    customAlert(response.responseText)
                }
               
            },
            201: function(response) {
            
                $("#load-modal").modal("hide");
                customAlert("Your order has been created successfully")
                window.location.href = response.detail_url
            }

        }

    })

})
