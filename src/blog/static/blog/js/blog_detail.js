// Bootstrap carousel
$(document).ready(function(){
	jQuery('.web-carousel.carousel[data-type="multi"] .item').each(function(){
		var next = jQuery(this).next();
		if (!next.length) {
			next = jQuery(this).siblings(':first');
		}
		next.children(':first-child').clone().appendTo(jQuery(this));

		for (var i=0;i<3;i++) {
			next=next.next();
			if (!next.length) {
				next = jQuery(this).siblings(':first');
			}
			next.children(':first-child').clone().appendTo($(this));
		}
	});
});

// Slick slider
$(document).ready(function(){
	$('.slider').slick({
		arrows : false,
		centerMode: true,
		// centerPadding: '20%',
		slidesToShow: 1,
		variableWidth: true,
		responsive: [
		{
			breakpoint: 768,
			settings: {
				arrows: true,
				centerMode: true,
				centerPadding: '40px',
				slidesToShow: 1,
			}
		},
		{
			breakpoint: 480,
			settings: {
				arrows: true,
				centerMode: true,
				centerPadding: '40px',
				slidesToShow: 1,
			}
		}
		]
	});

	$('.slick-slider').on('click', '.slick-slide', function (e) {
		e.stopPropagation();
		var index = $(this).data("slick-index");
		if ($('.slick-slider').slick('slickCurrentSlide') !== index) {
			$('.slick-slider').slick('slickGoTo', index);
		}
	});
});
