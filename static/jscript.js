$(document).ready(function() {


	$(function($) {
			let url = window.location.href;
			$('#navMenus li a').each(function() {
	   		if (this.href === url) {
	   			$(this).addClass('active');
	  		}
	 		});
	});

});


