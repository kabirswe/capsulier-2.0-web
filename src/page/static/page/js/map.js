function initMap(data) {

	var locations=data.map(function(e){
		var productextra = (e.productextra)? e.productextra.thumbnail_image : 0;
		var address_data1 = (e.productextra)? e.productextra.position : 0;
		var address_data = address_data1.split(',');
		var address_latitude = address_data[0];
		var address_longitude = address_data[1];
		var description = (e.productlang)? e.productlang.description : 0;

		locations = [e.name,address_latitude,address_longitude,productextra,
		e.price,description,e.get_api_absolute_url];
		return locations;
	});

	var map = new google.maps.Map(document.getElementById('map'), {
		maxZoom: 17,
		center: {lat: 48.856614, lng: 2.352222},
		mapTypeId: google.maps.MapTypeId.ROADMAP
		// scrollwheel: false
	});

	var infowindow = new google.maps.InfoWindow;

	var marker, i , markerCluster;
	var markers = [];
	var iconBase = 'http://static.lecapsulier.fr/assets/img/map/marker1.png';
	for (i = 0; i < locations.length; i++) {
		marker = new google.maps.Marker({
			position: new google.maps.LatLng(locations[i][1], locations[i][2]),
			map: map,
			icon: iconBase,
			title: name
		});
		markers.push(marker);
		google.maps.event.addListener(marker, 'click', (function(marker, i) {
			return function() {
				infowindow.setContent(
					"<a href="+locations[i][0]+">" +
					"<img src='"+locations[i][3]+"' class='img-responsive' style='width:100%;'/>" +
					"</a>" +
					"<div style='padding: 5px;'>" +
					"<h1 style='text-transform: uppercase; margin-top: 10px; font-size: 24px;margin-bottom:5px;color:#ab6d4a;'>"+locations[i][0]+"</h1>" +
					"<hr style='width: 3px; height:26px; border-right: solid 1px #ff0000;margin-bottom:5px;margin-top:0;'>" +
					"<p style='font-size: 14px; color: #272427'>"+locations[i][5]+"</p>" +
					"<a href='"+locations[i][6]+"'><span class='btn btn-default' style='border-radius: 0;padding: 5px 20px;color: #ab6d4a;margin-bottom: 20px;margin-top: 20px;width: 120px;border: solid 1px #ab6d4a;background:none;'>EN SAVOIR +</span></a>" +
					"</div>"
					);
				infowindow.open(map, marker);
			};
		})(marker, i , markerCluster));

		google.maps.event.addListener(map, 'click', function() {
			infowindow.close();
		});
	}

	var bounds = new google.maps.LatLngBounds();
	for (var i = 0; i < markers.length; i++) {
		bounds.extend(markers[i].getPosition());
	}

	map.fitBounds(bounds);

	map.addListener('zoom_changed', function() {
		var image;
		if (map.getZoom() >= 17) {
			image = '../../../../static/assets/img/map/marker-round.png';
		}
		else {
			image = 'http://static.lecapsulier.fr/assets/img/map/marker1.png';
		}
		for (var i = 0; i < markers.length; i++) {
			markers[i].setIcon(image);
		}
	});

	google.maps.event.addListener(infowindow, 'domready', function() {

		var iwOuter = $('.gm-style-iw');

		var iwBackground = iwOuter.prev();

			// Removes background shadow DIV
			iwBackground.children(':nth-child(2)').css({'display' : 'none'});

			// Removes white background DIV
			iwBackground.children(':nth-child(4)').css({'display' : 'none'});

			// Changes the desired tail shadow color.
			iwBackground.children(':nth-child(3)').find('div').children().css({'z-index' : '1'});

			// Reference to the div that groups the close button elements.
			var iwCloseBtn = iwOuter.next();

			// Apply the desired effect to the close button
			iwCloseBtn.css({display:'none', opacity: '1', right: '0', top: '3px', border: '7px solid #FF004E', 'border-radius': '13px', 'box-shadow': '0 0 5px #FF004E'});

			// If the content of infowindow not exceed the set maximum height, then the gradient is removed.
			if($('.iw-content').height() < 140){
				$('.iw-bottom-gradient').css({display: 'none'});
			}

			// The API automatically applies 0.7 opacity to the button after the mouseout event. This function reverses this event to the desired value.
			iwCloseBtn.mouseout(function(){
				$(this).css({opacity: '1'});
			});
		});

	var clusterStyles = [
	  {
	    textColor: '#1a181a',
	    url: 'http://static.lecapsulier.fr/assets/img/map/marker1.png',
	    height: 90,
	    width: 43
	  },
	];

	var mcOptions = {
	    styles: clusterStyles,
	};

			        // Add a marker clusterer to manage the markers.
        var markerCluster = new MarkerClusterer(map, markers,
            {imagePath:cluster_image});


	var styles = [{"featureType":"all","elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#000000"},{"lightness":40}]},{"featureType":"all","elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#000000"},{"lightness":16}]},{"featureType":"all","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":17},{"weight":1.2}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":20}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":21}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#000000"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#000000"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":16}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":19}]},{"featureType":"water","elementType":"geometry","stylers":[{"color":"#000000"},{"lightness":17}]}];

	map.setOptions({styles: styles});

}
