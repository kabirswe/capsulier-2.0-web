function getSingleProductBlock(object) {

    view = '';
    view += '<div class="col-md-2 col-sm-4 col-6 product_block">';
    view += '<div class="pb-alpha1">';
    view += '<a href="' + object.get_absolute_url + '">';
    view += '<div class="mm-bg pb-bravo1" style="background-image: url(' + object.get_image_hq + ')">';
    view += '</div>';
    view += '</a>';
    view += '<div class="pb-bravo2">';
    view += '<form id="add-form_' + object.id + '">';
    // // need to include product info
    view += getProductInfo(object);


    if (object.variation_set[0].inventory > 0 || object.variation_set[0].no_out_of_stock == "true" ) {
        view += '<div class="pb-charlie2">';
        //need to include quantity update
        view += getProductQuantityUpdate(object);
        view += '<div class="pb-delta2">';
        if (user_is_authenticated == "CallableBool(True)" && user_profile_status == "b") {
            view += '<a class="cap_button cap_button_v3" onclick="var q = $("#cart' + object.id + '").val(); var img = $(".product_img_' +  object.id + '").attr("src"); addToCart(' + object.id + ', "' + object.name + '", "' + object.description + '", ' + object.variation_set[0].price_pro + ', q, img)">' + t_text193 + '</a>';
        } else {
            view += '<a class="cap_button cap_button_v3" onclick="var q = $("#cart' + object.id + '").val(); var img =$(".product_img_' + object.id + '").attr("src"); addToCart(' + object.id + ', "' + object.name + '", "' + object.description + '", ' + object.variation_set[0].price_public + ', q, img)">' + t_text193 + '</a>';
        }
        view += '</div>';
        view += '<div class="pb-delta3"></div>';
        view += '</div>';

    } else {
        view += '<div class="pb-charlie3">';
        view += '<div class="pb-delta1">';
        view += '<p class="' + t_text192 + '"></p>';
        view += '</div>';
        view += '</div>';
    }
    view += '</form>';
    view += '</div>';
    view += '</div>';
    view += '</div>';

    return view;
}
