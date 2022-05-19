$(function() {

  'use strict';

  $('.js-menu-toggle').click(function(e) {

  	var $this = $(this);

  	

  	if ( $('body').hasClass('show-sidebar') ) {
  		$('body').addClass('show-sidebar');
  		$this.addClass('active');
  	} else {
  		$('body').addClass('show-sidebar');	
  		$this.addClass('active');
  	}

  	e.preventDefault();

  });

  // click outisde offcanvas
	// $(document).mouseup(function(e) {
    // var container = $(".right-sidebar");
    // if (!container.is(e.target) && container.has(e.target).length === 0) {
    //   if ( $('body').hasClass('show-sidebar') ) {
	// 			$('body').removeClass('show-sidebar');
	// 			$('body').find('.js-menu-toggle').removeClass('active');
	// 		}
    // }
	// }); 
	// $(document).onclick(function(e) {
	// 	var container = $(".mytabs");
	// 	if (!container.is(e.target) && container.has(e.target).length === 0) {
	// 	  if ( $('body').hasClass('show-sidebar') ) {
	// 				$('body').removeClass('show-sidebar');
	// 				$('body').find('.js-menu-toggle').removeClass('active');
	// 			}
	// 	}
	// 	}); 

    

});