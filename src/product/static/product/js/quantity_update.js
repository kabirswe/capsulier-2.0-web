function getProductQuantityUpdate(object) {
    console.log(t_text462);
    view = '';
    view += '<div class="quantity-update-block">';
    view += '<a onclick="if(cart' + object.id + '.value > 1){cart' + object.id + '.value = (cart' + object.id + '.value-1)}">';
    view += '<p class="qb-bravo1" style="background-image: url(' + t_text462 + ')";>-</p>';
    view += '</a>';
    view += '<a><p class="qb-bravo3">';
    view += '<input type="text" id="cart' + object.id + '" name="qty" value="1" min="1" style="background-image: url(' + t_text461 + ');/>';
    view += '</p></a>';
    view += '<a onclick="cart' + object.id + '.value = (+ cart' + object.id + '.value + 1)">';
    view += '<p class="qb-bravo2" style="background-image: url(' + t_text462 + ')");">+</p>';
    view += '</a>';
    view += '</div>';

    return view;

};
