let  searchParamDict = {}

function buildSearchParamDict(query = location.search.substring(1)) {
    let parameters = {};
    for (const [name, value] of new URLSearchParams(query)) parameters[name] = value;
    return parameters;
}

function buildSearchParamList(query = location.search.substring(1)){
    let parameters = [];
    for (const [name, value] of new URLSearchParams(query)) parameters.push(value);
    return parameters;
}

function insertUrlParam(key, value, title = '', preserve_hash = false) {
    //set value to null in order to delete a key
    if (history.pushState) {
        let searchParams = new URLSearchParams(window.location.search);
        if (value === null) {
            //delete if exists, otherwise return
            if (searchParams.has(key)) {
                searchParams.delete(key)
            }
            else {
                return
            }

        }
        else {
            searchParams.set(key, value);
        }

        let newurl = window.location.protocol + "//" + window.location.host + window.location.pathname
            + '?' + searchParams.toString();
        if (preserve_hash) newurl = newurl + window.location.hash;
        let oldTitle = document.title;
        if (title !== '') {
            window.history.replaceState({ path: newurl }, title, newurl);
            if (document.title !== title) { // fallback if above doesn't work
                document.title = title;
            }
        } else { // in case browsers ever clear titles set with empty string
            window.history.replaceState({ path: newurl }, oldTitle, newurl);
        }
    }
}

function fetchProducts() {
    page = 0
    url = "/api/v1/shop/items/l/"
    searchParams = window.location.search;
    //const data = new URLSearchParams(searchParams);
    data = {}
    if(searchParams != ""){
        data = JSON.parse('{"' + decodeURI(searchParams.replace(/&/g, "\",\"").replace(/=/g,"\":\"")) + '"}')
    }
    data['currency'] = sessionStorage.getItem("currency") || "USD"
   
    $.ajax({
        type: "GET",
        url: url,
        data: data,
        timeout: 3000,
        beforeSend : function(){
            $("#product-list").html(
                getLoaderVerbose()
            )
        },
        success: function (response) {
            $("#product-list").html(response['product_list']['html'])
            $(".product-filters-body:visible").html(response.filters)
            updateFilters()
            
        },
        error: function () {
            popUp("Request timed out, please reload")
        },

        statusCode: {
            400: function (response) {

                popUp(response.responseJSON['details'])
            }

        }

    })

}

function handleFilters(){
    //deactivate all active filters
    let checkBoxes = ["free_delivery","ready_to_ship"]
    searchParamDict = buildSearchParamDict()


    if(searchParamDict.length == 0) {return }
    $(".grid-filter span:visible").removeClass("active")
    for (const [param,value] of  Object.entries(searchParamDict)){
     

        //handle checkboxes differently 
        if(checkBoxes.includes(param) && value == "true"){
            //then we know its a check box
            let input = $("input[name='" + param  + "']")
            input.prop("checked", true);
        }
        else {
            //show clear filter
            $(".clear-filter[target='" +  param + "']").css("display","inline")
            $("#filter-" + param + "-" + value  + ":visible").addClass("active")
        }
    
    }

}

function fillInputValues(){
    //deactivate all active filters
    searchParamDict = buildSearchParamDict()

    if(searchParamDict.length == 0) {return }

    for (const [param,value] of  Object.entries(searchParamDict)){
        $("[name='" + param + "']:visible").val(value)

}
}



function updateFilters() {
    searchParams = window.location.search;
    data = {}
    if(searchParams != ""){
        data = JSON.parse('{"' + decodeURI(searchParams.replace(/&/g, "\",\"").replace(/=/g,"\":\"")) + '"}')
    }
   
    data['currency'] = sessionStorage.getItem("currency") ||  "USD"
    url = "/api/v1/shop/items/update-filters/"
    filterDiv = $(".product-filters-body:visible")

    $.ajax({
        type: "GET",
        url: url,
        data: data,
        
        timeout: 20000,
        
        success: function (response) {
            filterDiv.html(response['filters']['html'])
            
            $(".apply-filter").css("display","none")
            handleFilters()
            fillInputValues()
            closeFilter()
            
            //save the list
            /*filtersList = response['filters_list']
            //update filter count
            filterCount = filtersList.length

            if (filterCount > 0) {
                $(".filter-search span").html(filterCount)
                $(".filter-search span").removeAttr("hidden")
            }
            else {
                $(".filter-search span").attr("hidden", "")
            }
            */


        },
        error: function () {
            //customAlert("error")
        },

        statusCode: {

        }

    })
}



$(document).on("click",".filter span",function(e){
    let code = $(this).attr("code")
   insertUrlParam(code,$(this).attr("slug"))
   fetchProducts()
  
})



$(document).on("change",".filter-input",function(e){
    $(".apply-filter").css("display","inline")
})


$(document).on("click",".apply-filter",function(e){
    $(".filter-input").each( function( index){
        let input = $(this)
        let val;
        if (input.attr("type") == "checkbox"){
           if(! input.is(":checked")){
            val = null //to cause its elimination from url params
        } 
           else {val=true}
        }
        else {
            val = input.val() 
            //check if its empty
            if(val.length < 1){ val = null}
        }
        insertUrlParam(input.attr("name"),val)
     
    });
    closeFilter()
    fetchProducts()
    

})


$(document).on("click",".clear-filter",function(e){
    insertUrlParam($(this).attr("target"),null) //to clear
    closeFilter()
    fetchProducts()

})


$(document).on("click",".clear-search",function(e){
    $("input[name=q]").val("")
    insertUrlParam("q",null) //to clear
    $("#page-title").html("All collection")
    closeFilter()
    fetchProducts()
})

$(document).on("click",".search-form button[type=submit]",function(e){
    $(".search-form").submit()
})




$(document).ready(function () {
    fetchProducts()
    let currency = sessionStorage.getItem("currency") || "USD"
    $("select[name=currency] option:contains('" + currency+ "')").prop("selected", true);
})


/*
$(window).on('resize', function() {
    let resizeTimeout;
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(function() {
      // Handle the resize event after a brief delay
        var screenWidth = window.innerWidth;
        // Reload the page with the same search parameters for mobile
        location.reload();
      // You can perform your desired actions here
    }, 200); // Adjust the delay time as needed
  });
*/


  $(document).on("submit",".search-form",function(e){
    e.preventDefault()
    let q = $(this).find("input").val()
    $("#page-title").html(q)
    insertUrlParam("q",q)
    fetchProducts()
  })

  $(document).on("change","select[name=currency]",function(e){
    value = $(this).val()
    //store in sessions
    sessionStorage.setItem("currency",value)
    fetchProducts()
    setCookie("currency",value)
})