function initMap(){

	$.get(url_shop, function(data){

		var directionsService = new google.maps.DirectionsService;
		var directionsDisplay = new google.maps.DirectionsRenderer;

		var locations =  data.map(function(obj){
			address_data = obj.address.split(',');
			return {
				'name': obj.name,
				'phone': obj.phone,
				'lat': address_data[0],
				'lng': address_data[1],
				'image' : obj.get_image_mq,
				'schedule': obj.schedule_set,
				'website': obj.website
			};
		});

		// setTimeout(function(){

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
				var schedule = '<div class="echo2">';

				locations[i].schedule.map(function(data){
					schedule += '<p><span class="foxtrot1">'+data.get_day_display +': </span>';
					if(data.close){
						schedule +='<span class="foxtrot2">Fermé</span></p>';
					}
					else
					{
						if(data.morning_start_time!==null){schedule += '<span>' + data.morning_start_time.slice(0, 5);}
						if(data.morning_end_time!==null){schedule += '-'+ data.morning_end_time.slice(0, 5);}
						if(data.morning_start_time!==null && data.afternoon_start_time!==null){schedule += ' | '};
						if(data.afternoon_start_time!==null){schedule += data.afternoon_start_time.slice(0, 5);}
						if(data.afternoon_end_time!==null){schedule += '-'+ data.afternoon_end_time.slice(0, 5)+'</span></p>';}
					}
				});
				schedule += '</div>';
				var view = '';
				view += '<div class="charlie1">';
				view += "<img src='"+locations[i].image+"' />";
				view += '<div class="delta1">';
				view += '<h1>'+locations[i].name+'</h1>';
				view += '<div class="echo1">';
				if(locations[i].address2){
					view += '<p>'+ locations[i].address2 +'</p>';
				}
				view += '<p>'+locations[i].phone+'</p>';
				view += '</div>';
				view += schedule;
				view += '<div class="echo3">';
				view += '<a href="' + locations[i].website + '" target="_blank">'+locations[i].website+'</a>';
				view += '</div>';
				view += '<a href="https://www.google.com/maps/dir/?api=1&destination='+locations[i].lat+', '+locations[i].lng+'" target="_blank" class="cap_button cap_button_v2 mm_p_5">Itinéraire</a>';
				view += '</div>';
				view += '</div>';

				infoWindowContent.push(view);

				marker = new google.maps.Marker({
					position: new google.maps.LatLng(locations[i].lat, locations[i].lng),
					map: map,
					icon: marker_image,
					title: name
				});
				markers.push(marker);
				google.maps.event.addListener(marker, 'click', (function(marker, i) {
					return function() {
						infowindow.setContent(infoWindowContent[i]);
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

			// google.maps.event.addListener(infowindow, 'domready', function() {
			//
			// 	// Reference to the DIV that wraps the bottom of infowindow
			// 	var iwOuter = $('.gm-style-iw');
			//
			// 	/* Since this div is in a position prior to .gm-div style-iw.
			// 	* We use jQuery and create a iwBackground variable,
			// 	* and took advantage of the existing reference .gm-style-iw for the previous div with .prev().
			// 	*/
			// 	var iwBackground = iwOuter.prev();
			//
			// 	// Removes background shadow DIV
			// 	iwBackground.children(':nth-child(2)').css({'display' : 'none'});
			//
			// 	// Removes white background DIV
			// 	iwBackground.children(':nth-child(4)').css({'display' : 'none'});
			//
			// 	// Moves the infowindow 115px to the right.
			// 	iwOuter.parent().parent().css({left: '115px'});
			//
			// 	// Moves the shadow of the arrow 76px to the left margin.
			// 	iwBackground.children(':nth-child(1)').attr('style', function(i,s){ return s + 'left: 76px !important;'});
			//
			// 	// Moves the arrow 76px to the left margin.
			// 	iwBackground.children(':nth-child(3)').attr('style', function(i,s){ return s + 'left: 76px !important;'});
			//
			// 	// Changes the desired tail shadow color.
			// 	iwBackground.children(':nth-child(3)').find('div').children().css({'box-shadow': '#FF004E 0px 1px 6px', 'z-index' : '1'});
			//
			// 	// Reference to the div that groups the close button elements.
			// 	var iwCloseBtn = iwOuter.next();
			//
			// 	// Apply the desired effect to the close button
			// 	iwCloseBtn.css({display: 'none'});
			//
			// 	// If the content of infowindow not exceed the set maximum height, then the gradient is removed.
			// 	if($('.iw-content').height() < 140){
			// 		$('.iw-bottom-gradient').css({display: 'none'});
			// 	}
			//
			// 	// The API automatically applies 0.7 opacity to the button after the mouseout event. This function reverses this event to the desired value.
			// 	iwCloseBtn.mouseout(function(){
			// 		$(this).css({opacity: '1'});
			// 	});
			// });


			// Add a marker clusterer to manage the markers.
			var markerCluster = new MarkerClusterer(map, markers,
				{imagePath:cluster_image});

				var styles = [{"featureType":"administrative","elementType":"all","stylers":[{"saturation":"-100"}]},{"featureType":"administrative.province","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"landscape","elementType":"all","stylers":[{"saturation":-100},{"lightness":65},{"visibility":"on"}]},{"featureType":"poi","elementType":"all","stylers":[{"saturation":-100},{"lightness":"50"},{"visibility":"simplified"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":"-100"}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.arterial","elementType":"all","stylers":[{"lightness":"30"}]},{"featureType":"road.local","elementType":"all","stylers":[{"lightness":"40"}]},{"featureType":"transit","elementType":"all","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"water","elementType":"geometry","stylers":[{"hue":"#ffff00"},{"lightness":-25},{"saturation":-97}]},{"featureType":"water","elementType":"labels","stylers":[{"lightness":-25},{"saturation":-100}]}];

				map.setOptions({styles: styles});

			// }, 1000);
		});
	}
