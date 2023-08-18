function get_map(id, latitude, longitude, icon2) {

    var myLatLng = {lat: latitude, lng: longitude};

    var mapProp = {
        center:myLatLng,
        zoom:6,
        mapTypeId:google.maps.MapTypeId.ROADMAP,
        scrollwheel: false
    };
    var mapc=new google.maps.Map(document.getElementById("map" + id),mapProp);

    var marker = new google.maps.Marker({
        position: myLatLng,
        icon: icon2,
        map: mapc,
        title: 'Le Capsulier!'
    });

    var styles = [{"featureType":"administrative","elementType":"all","stylers":[{"saturation":"-100"}]},{"featureType":"administrative.province","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"landscape","elementType":"all","stylers":[{"saturation":-100},{"lightness":65},{"visibility":"on"}]},{"featureType":"poi","elementType":"all","stylers":[{"saturation":-100},{"lightness":"50"},{"visibility":"simplified"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":"-100"}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.arterial","elementType":"all","stylers":[{"lightness":"30"}]},{"featureType":"road.local","elementType":"all","stylers":[{"lightness":"40"}]},{"featureType":"transit","elementType":"all","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"water","elementType":"geometry","stylers":[{"hue":"#ffff00"},{"lightness":-25},{"saturation":-97}]},{"featureType":"water","elementType":"labels","stylers":[{"lightness":-25},{"saturation":-100}]}];
        mapc.setOptions({styles: styles});
}

$(document).ready(function(){
	$(".top-to-bottom").on('click', function(event) {
		if (this.hash !== "") {
			event.preventDefault();
			var hash = this.hash;
			$('html, body').animate({
				scrollTop: $(hash).offset().top
			}, 1000, 'easeInOutExpo', function(){
				window.location.hash = hash;
			});
		}
	});
});
