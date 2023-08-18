function getProductInfo(object) {

    view = '';
    view += '<div class="product-info-block">';
    view += '<a href="' + object.get_absolute_url + '">';
    view += '<p class="pi-delta1">' + object.name + '</p>';
    view += '</a>';
    view += '<hr style="border-color:' + object.productextra.color + '">';
    if (object.productlang != null) {
        if (object.productlang.description_short != "") {
            view += '<p class="pi-delta2">' + object.productlang.description_short + '</p>';
        }
        if (object.productlang.description_short2 != "") {
            view += '<p class="pi-delta4">' + object.productlang.description_short2 + '</p>';
        }
    }
    view += '<input type="hidden" name="item" value="' + object.variation_set[0].id + '" />';
    if (user_is_authenticated == "CallableBool(True)" && user_profile_status == "b") {
        view += '<p class="pi-delta5">"' + object.variation_set[0].price_public + ' €"</p>';
    }
    view += '<p class="pi-delta6" id="price_' + object.id + '">';
    if (user_is_authenticated == "CallableBool(True)" && user_profile_status == "b") {
        view += '<span>'+ object.variation_set[0].price_pro + ' € </span>';
    } else {
        view += '<span>'+ object.variation_set[0].price_public + ' € </span>';
    }
    view += '</p>';
    if (object.productlang != null) {
        if (object.productlang.description_short3 != "") {
            view += '<p class="pi-delta7">' + object.productlang.description_short3 + '</p>';
        }
    }
    view += '</div>';

    return view;

};
