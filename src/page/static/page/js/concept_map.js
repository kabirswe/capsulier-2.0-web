$(document).ready(function() {
	initMap();
});

function initMap(){

	$.get(url_concept_map, function(data) {
		// console.log(data);

		var directionsService = new google.maps.DirectionsService;
		var directionsDisplay = new google.maps.DirectionsRenderer;

		var locations =  data.map(function(obj){
			address_data = obj.address.split(',');
			return {
				'name': obj.name,
				'lat': address_data[0],
				'lng': address_data[1],
				'marker' : obj.marker,
			};
		});
		var map = new google.maps.Map(document.getElementById('map'), {
			maxZoom: 17,
			// center: {lat: 48.856614, lng: 2.352222},
			scrollwheel: false,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		});

		var infowindow = new google.maps.InfoWindow();

		var marker, i , markerCluster;
		var markers = [];
		var infoWindowContent =[];
		for (i = 0; i < locations.length; i++) {
			var view = '';
			view += '<div class="charlie1">';
			view += '<div class="delta1">';
			view += '<h4>'+locations[i].name+'</h4>';
			view += '</div>';
			view += '</div>';

			infoWindowContent.push(view);

			marker = new google.maps.Marker({
				position: new google.maps.LatLng(locations[i].lat, locations[i].lng),
				map: map,
				icon: locations[i].marker,
				title: name
			});
			markers.push(marker);
			google.maps.event.addListener(marker, 'click', (function(marker, i) {
				return function() {
					infowindow.setContent(infoWindowContent[i]);
					infowindow.open(map, marker);
				};
			})(marker, i , markerCluster));


			google.maps.event.trigger(marker, 'click');
			// $('.gmnoprint img').trigger('click');
		}

		var bounds = new google.maps.LatLngBounds();
		for (var i = 0; i < markers.length; i++) {
			bounds.extend(markers[i].getPosition());
		}

		map.fitBounds(bounds);


		// Add a marker clusterer to manage the markers.
		var markerCluster = new MarkerClusterer(map, markers,
			{imagePath:cluster_image});

			var styles = [{"featureType":"administrative","elementType":"all","stylers":[{"saturation":"-100"}]},{"featureType":"administrative.province","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"landscape","elementType":"all","stylers":[{"saturation":-100},{"lightness":65},{"visibility":"on"}]},{"featureType":"poi","elementType":"all","stylers":[{"saturation":-100},{"lightness":"50"},{"visibility":"simplified"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":"-100"}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.arterial","elementType":"all","stylers":[{"lightness":"30"}]},{"featureType":"road.local","elementType":"all","stylers":[{"lightness":"40"}]},{"featureType":"transit","elementType":"all","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"water","elementType":"geometry","stylers":[{"hue":"#ffff00"},{"lightness":-25},{"saturation":-97}]},{"featureType":"water","elementType":"labels","stylers":[{"lightness":-25},{"saturation":-100}]}];

			map.setOptions({styles: styles});
		});
	}
