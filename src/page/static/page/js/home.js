$(document).ready(function () {

    // Select all links with hashes
    $('a[href*="#"]')
      // Exclude links that don't actually link to anything
      .not('[href="#"]')
      .not('[href="#0"]')
      .click(function(event) {
        // On-page links
        if (
          location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
          &&
          location.hostname == this.hostname
        ) {
          // Figure out element to scroll to
          var target = $(this.hash);
          target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
          // Does a scroll target exist?
          if (target.length) {
            // Only prevent default if animation is actually gonna happen
            event.preventDefault();
            $('html, body').animate({
              //targeting the target section and taking off the height of header
              scrollTop: target.offset().top - $('header .fixed-top')[0].clientHeight
            }, 1000);
          }
        }
      });

});
