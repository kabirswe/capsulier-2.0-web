var trigger = $('.hamburger'),
inner = $('.hamburger-inner'),
overlay = $('.menuItem'),
isClosed = false;

trigger.click(function () {
	hamburger_cross();      
});

function hamburger_cross() {

	if (isClosed == true) {          
		overlay.fadeOut("slow");
		trigger.removeClass('is-active');
		inner.removeClass('inner-active');
		trigger.addClass('is-closed');
		isClosed = false;
	} else {   
		overlay.fadeIn("slow");
		trigger.removeClass('is-closed');
		trigger.addClass('is-active');
		inner.addClass('inner-active');
		$('.navHeader').attr("style", "position: absolute;z-index: 99999;width: 100%;left: 0;right: 0;background: #edece8;top: 0;    padding: 10px 20px;" );
		isClosed = true;
	}
}


$(function(){

	$('#id_company_name').hide();
	$('#id_siret_number').hide();

	// var status = $("input[name='status']").is(':checked');
	// console.log(status);

	if($("#id_status_2").is(':checked')){
		$('#id_company_name').show();
		$('#id_siret_number').show();
		$('#id_company_name').prop('required',true);
		$('#id_siret_number').prop('required',true);
	} else {
		$('#id_company_name').hide();
		$('#id_siret_number').hide();	
		$('#id_company_name').val('');
		$('#id_siret_number').val('');	
		$('#id_company_name').prop('required',false);
		$('#id_siret_number').prop('required',false);
	}
	
	$("input[name='status']").on('change',function(){
		console.log(this.value);
		if(this.value=='b'){
			$('#id_company_name').show();
			$('#id_siret_number').show();
		$('#id_company_name').prop('required',true);
		$('#id_siret_number').prop('required',true);
		} else {
			$('#id_company_name').hide();
			$('#id_siret_number').hide();		
			$('#id_company_name').val('');
			$('#id_siret_number').val('');	
		$('#id_company_name').prop('required',false);
		$('#id_siret_number').prop('required',false);	
		}
	});

});