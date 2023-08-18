(function($) {
	function module_hide(id) {
		if ($('.model-text #id_' + id + '_boolean').is(":checked") === false ) {
			$('.model-text #id_' + id + '_boolean').parent().parent().parent().css("display", "none");
		}
		$('.model-text .clearable-file-input #' + id + '-clear_id').parent().css("display", "none");
		$('.model-text #' + id + '-clear_id').css("display", "none");
	}
	$( document ).ready(function() {
		$('.model-text .field-page').css("display", "none");
		module_hide('t_CharField');
		module_hide('t_EmailField');
		module_hide('t_FileField');
		module_hide('t_GeopositionField');
		module_hide('t_ImageField');
		module_hide('t_RichTextField');
		module_hide('t_TextField');
		module_hide('t_URLField');
		module_hide('t_VideoField');
		$('.select2-container').css("width", "auto");
	});
})(django.jQuery);
