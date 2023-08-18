$(document).ready(function () {

	// Add text
	$.get(url_text, function (data) {
		// console.log(data);
		$.each(data, function( index, obj ) {
			if (data[index].get_attr == 'src') {
				if ($(".t_text" + data[index].id)[0]){
					$(".t_text" + data[index].id).attr("src",data[index].get_image_free);
				}
				else if ($(".t_bg" + data[index].id)[0]) {
					$(".t_bg" + data[index].id).css('background-image','url( "' + data[index].get_image_free + '")');
				}
				else if ($(".t_sq" + data[index].id)[0]) {
					$(".t_sq" + data[index].id).attr("src",data[index].get_image_square);
				}
			}
			else if (data[index].get_attr == 'href') {
				$(".t_text" + data[index].id).attr("href",data[index].get_text);
			}
			else {
				$(".t_text" + data[index].id).html(data[index].get_text);
			}
		});

		// Loader
		$("#mm-wrapper").css("visibility", "visible");
		$("#mm-loader-wrapper").css("display", "none");
		var b = $('footer').outerHeight();
		var c = $(window).height();
		var d = c - b;
		$("#main-wrapper").css('min-height', d);
		// End Loader
	}, "json");
	// End Add text

	// Main wrapper min-height
	header_height = $(".main_navbar").height();
	$(".header-height").css("height", header_height);

	//-------- Active Mobile Menu ----------//
    $('.mobile-menu').click(function(){
        $(this).toggleClass('open');
        $(".mobile-nav").slideToggle("slow");
    });

	// SignUp
	$('#div_id_company_name').hide();
	$('#div_id_siret_number').hide();
	$('.account_page_base #id_email').attr('placeholder','');
	$('.account_page_base #id_login').attr('placeholder','');
	$('.account_page_base #id_password').attr('placeholder','');
	$('.account_page_base #id_password1').attr('placeholder','');
	$('.account_page_base #id_password2').attr('placeholder','');
	$('.account_page_base #id_oldpassword').attr('placeholder','');

	if($("#id_status_2").is(':checked')){
		$('#div_id_company_name').show();
		$('#div_id_siret_number').show();
		$('#id_company_name').prop('required',true);
		$('#id_siret_number').prop('required',true);
	} else {
		$('#div_id_company_name').hide();
		$('#div_id_siret_number').hide();
		$('#id_company_name').prop('required',false);
		$('#id_siret_number').prop('required',false);
	}

	$("input[name='status']").on('change',function(){
		console.log(this.value);
		if(this.value=='b'){
			$('#div_id_company_name').show();
			$('#div_id_siret_number').show();
			$('#id_company_name').prop('required',true);
			$('#id_siret_number').prop('required',true);
		} else {
			$('#div_id_company_name').hide();
			$('#div_id_siret_number').hide();
			$('#id_company_name').prop('required',false);
			$('#id_siret_number').prop('required',false);
		}
	});

});

function get_placeholder(tag_id, data_id) {
	url = url_text + data_id;
	$.get(url, function (data) {
		$(tag_id).attr('placeholder', data.get_text);
	});
}

// function get_span1(tag_id, data_id) {
// 	url = url_text + data_id;
// 	$.get(url, function (data) {
// 		$(tag_id).html('<span id="test1" class="foxtrot2 test1">' + data.get_text + '</span></p>');
// 		console.log('test');
// 	});
// }

function get_html_fadeIn(tag_id, data_id, fadein_value) {
	url = url_text + data_id;
	$.get(url, function (data) {
		$(tag_id).html(data.get_text).fadeIn();
	});
}
