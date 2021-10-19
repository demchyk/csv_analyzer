$(document).ready(function() {


	$(function($) {
			let url = window.location.href;
			$('#navMenus li a').each(function() {
	   		if (url.includes(this.href)) {
	   			$(this).addClass('active');
	  		}
	 		});
	});

	$('#dash_input_submit').hide();

	setInterval(function(){
	    if($('#dashboard_input_file').val()!=""){
	     $('#dash_input_submit').show();
	    }else{
	        $('#dash_input_submit').hide();
	    }
	},1000);

$(function() {

    var start = moment().subtract(29, 'days');
    var end = moment();

    function cb(start, end) {
        $('#reportrange span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
        $('#reportrange input').val(start.format('YYYY-MM-DD') + ' - ' + end.format('YYYY-MM-DD'));
    }

    $('#reportrange').daterangepicker({
        startDate: start,
        endDate: end,
        ranges: {
           'Today': [moment(), moment()],
           'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
           'Last 7 Days': [moment().subtract(6, 'days'), moment()],
           'Last 30 Days': [moment().subtract(29, 'days'), moment()],
           'This Month': [moment().startOf('month'), moment().endOf('month')],
           'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')],
           'This Year': [moment().startOf('year'), moment().endOf('year')],
        }
    }, cb);

    cb(start, end);

});







	var base_color = "rgb(230,230,230)";
	var active_color = "rgb(13, 110, 253)";



	var child = 1;
	var length = $("section").length - 1;
	$("#prev").addClass("disabled");
	$("#submit").addClass("disabled");

	$("section").not("section:nth-of-type(1)").hide();
	$("section").not("section:nth-of-type(1)").css('transform','translateX(100px)');

	var svgWidth = length * 200 + 24;
	$("#svg_wrap").html(
	  '<svg version="1.1" id="svg_form_time" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 ' +
	    svgWidth +
	    ' 24" xml:space="preserve"></svg>'
	);

	function makeSVG(tag, attrs) {
	  var el = document.createElementNS("http://www.w3.org/2000/svg", tag);
	  for (var k in attrs) el.setAttribute(k, attrs[k]);
	  return el;
	}

	for (i = 0; i < length; i++) {
	  var positionX = 12 + i * 200;
	  var rect = makeSVG("rect", { x: positionX, y: 9, width: 200, height: 6 });
	  document.getElementById("svg_form_time").appendChild(rect);
	  // <g><rect x="12" y="9" width="200" height="6"></rect></g>'
	  var circle = makeSVG("circle", {
	    cx: positionX,
	    cy: 12,
	    r: 12,
	    width: positionX,
	    height: 6
	  });
	  document.getElementById("svg_form_time").appendChild(circle);
	}

	var circle = makeSVG("circle", {
	  cx: positionX + 200,
	  cy: 12,
	  r: 12,
	  width: positionX,
	  height: 6
	});
	document.getElementById("svg_form_time").appendChild(circle);

	$('#svg_form_time rect').css('fill',base_color);
	$('#svg_form_time circle').css('fill',base_color);
	$("circle:nth-of-type(1)").css("fill", active_color);

	$("#next").addClass("disabled");
	 
	$(".button").click(function () {
	  $("#svg_form_time rect").css("fill", active_color);
	  $("#svg_form_time circle").css("fill", active_color);
	  var id = $(this).attr("id");
	  if (id == "next") {
	    $("#prev").removeClass("disabled");
	    if (child >= length) {
	      $(this).addClass("disabled");
	      $('#submit').removeClass("disabled");
	    }
	    if (child <= length) {
	      child++;
	    }
	  } else if (id == "prev") {
	    $("#next").removeClass("disabled");
	    $('#submit').addClass("disabled");
	    if (child <= 2) {
	      $(this).addClass("disabled");
	    }
	    if (child > 1) {
	      child--;
	    }
	  }
	  var circle_child = child + 1;
	  $("#svg_form_time rect:nth-of-type(n + " + child + ")").css(
	    "fill",
	    base_color
	  );
	  $("#svg_form_time circle:nth-of-type(n + " + circle_child + ")").css(
	    "fill",
	    base_color
	  );
	  var currentSection = $("section:nth-of-type(" + child + ")");
	  currentSection.fadeIn();
	  currentSection.css('transform','translateX(0)');
	  currentSection.prevAll('section').css('transform','translateX(-100px)');
	  currentSection.nextAll('section').css('transform','translateX(100px)');
	  $('section').not(currentSection).hide();
	  if (child == 1){
	  $("#next").addClass("disabled");
		}
	  if (child == 2 && child < length){
	  	$("#next").removeClass("disabled");
	  }



	});

	$("#prev").click(function () {
		$("#next").removeClass("disabled");
	});


});

( function( $, window, document, undefined )
{
	$( '.inputfile' ).each( function()
	{
		var $input	 = $( this ),
			$label	 = $input.next( 'label' ),
			labelVal = $label.html();

		$input.on( 'change', function( e )
		{
			var fileName = '';
			fileName = e.target.value.split( '\\' ).pop();
			if( fileName ){
				$label.find( 'span' ).html( fileName );
				$("#next").removeClass("disabled");
			}
			else{
				$label.html( labelVal );
				$("#next").addClass("disabled");
			}
		});
		// Firefox bug fix
		$input
		.on( 'focus', function(){ $input.addClass( 'has-focus' ); })
		.on( 'blur', function(){ $input.removeClass( 'has-focus' ); });
	});
})( jQuery, window, document );


