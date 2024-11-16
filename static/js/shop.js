try {
const productImagesCount = JSON.parse(document.getElementById("product_images_count").textContent) || 0
const relatedProductsCount = JSON.parse(document.getElementById("related_products_count").textContent) || 0
let favouriteProductsPk = JSON.parse(localStorage.getItem("favouriteProductsPk") || [])
} catch {
    
}

function markFavouritedProducts(){
    //mark liked products
    favouriteBtns = $(".favourite-btn")
    favouriteBtns.each(function(index){
        btn = $(this)
         if( favouriteProductsPk.includes(btn.attr("pk"))){
            btn.attr("name","heart")
            btn.addClass("active")
         }
      })

}


$(document).on("click",".favourite-btn",function(e){
    pk = $(this).attr("pk")
    btn =  $(this)
    if (btn.hasClass('active')){
        btn.attr("name","heart-outline")
        btn.removeClass("active")
        //remove from favorited list
        newArray = favouriteProductsPk.filter(number => number != pk)
        //save
        localStorage.setItem("favouriteProductsPk",JSON.stringify(newArray))
    }

    else {
        btn.attr("name","heart")
        btn.addClass("active")
        //add to favourited list
        favouriteProductsPk.push(pk)
        //save
        localStorage.setItem("favouriteProductsPk",JSON.stringify(favouriteProductsPk))
    }
})


$(document).ready(function(){

    markFavouritedProducts()

    if(productImagesCount  > 1){
    $(".product-detail-img-sliders").owlCarousel(
        {
            rtl:false,
            loop:true,
            margin:10,
            nav:true,
            responsive:{
                0:{
                    items:productImagesCount
                },
                600:{
                    items:productImagesCount
                },
                1000:{
                    items:productImagesCount
                }
            }
        }
    );
    }
    

    $(".product-list-sliders").owlCarousel(
        {
            rtl:true,
            loop:true,
            margin:10,
            nav:true,
            responsive:{
                0:{
                    items:relatedProductsCount
                },
                600:{
                    items:relatedProductsCount
                },
                1000:{
                    items:relatedProductsCount
                }
            }
        }
    );

    $(document).on("click",".click-tab",function(e) {
        let target = "#" + $(this).attr("target");
        $(target).tab("show");
    })
  });


 




$(".product-detail-img-sliders").on("click", "img", function(e){
    $(".product-detail-img-sliders img").removeClass('active')
    $(this).addClass("active")
    $(".product-img-view").attr("src",$(this).attr("src"))
})







