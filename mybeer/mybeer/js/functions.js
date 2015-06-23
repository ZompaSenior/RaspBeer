//------ Protezione csrf
var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
//------ FINE Protezione csrf

/*DIALOG*/

function sDialog(dataHtml, container)
{
	if(typeof(container)==='undefined') container = '';
	if(typeof(dataHtml)==='undefined') dataHtml = '';
	
	if (container=='' && dataHtml!='')
	{
		//$('html').css('position','fixed');
		//$('#d_box').html(dataHtml);
		$('body').css('overflow-y','hidden');
		
		var elem = $('<div/>').html(dataHtml).contents();
		$('#d_box').html(elem);
				
		setTimeout(function(){
			check_dbox_dimension();
			$('#d_cont').show();
		}, 50);
	}
	
	if (dataHtml==''){
		setTimeout(function(){
			check_dbox_dimension();
			$('#d_cont').show();
		}, 50);
	}
}

function openSDialog(jump){
	$.get(jump, function(html) {
		sDialog(html);
	});
}

function openNoteSDialog(jump){
	$.ajax({
		type: 'GET',
		url: jump,
		dataType: 'json',
	}).done(function( resp ) {
		sDialog(resp['html']);
	});
}

function msgDialog(dataHtml){
	if(dataHtml!=''){
		var elem = $('<div/>').html(dataHtml).contents();
		$('#msg_box div.msg').html(elem);
		$('#msg_cont').show();
	}
}

function check_dbox_dimension(){
	//primo elemento nella d_box deve essere sempre div
	var content = $('#d_box > div');
	var d_cont_h = $('#d_cont').height();
	var d_box_h = $('#d_box').height();

//  	console.log('finestra: ' + window.innerHeight);
//  	console.log('content: ' + content.height());
//  	console.log('d_cont: ' + $('#d_cont').height());
//  	console.log('d_box: ' + $('#d_box').height());
	
	if (content.height() >  window.innerHeight){
		$('#d_cont').height(700);
		$('#d_cont').css('overflow-y', 'scroll');
	}
}

function show_spinner(cont){
	var spinner_html = $('#spinner_cont').html();
	$(cont).html(spinner_html);
	$(cont).children('.spinner').show();
}

function hide_spinner(cont){
	$(cont).html('');
	// $('#'+cont_id+'.spinner').hide();
}