function script(){
	if($("#form_input_question").val() != ""){
		send_request();
		change_text_send_button();
		icon_loading_rotation();
		show_history_label();
	}
	else{
	}
};

let map_id = 0

function send_request(){
	$.ajax({
		url: '/index_question',
		data: $('form').serialize(),
		type: 'POST',
		success: function(data){
			if(data['status'] == 'OK'){
				let bloc_message_map_comment = ""
					bloc_message_map_comment += "<div id='result_question'><ul name='history' id='history_question'></ul></div>";
					bloc_message_map_comment += "<div id='" + map_id + "' name='map'></div>";
					bloc_message_map_comment += "<div id='grandpyapp_comments'></div>";
				$('#history_label').after(bloc_message_map_comment);
				show_history_bloc_with_input()
				setTimeout(() => {
					show_random_positive_anser(data['random_positive_anser']);
				}, 500);
				setTimeout(() => {
					init_map(data['long_name'], data['lat'], data['lng'], map_id);
                    map_id += 1
				}, 1000);
				setTimeout(() => {
                    show_summary_and_link(data['wikipedia_summary']['summary'], data['wikipedia_summary']['url']);
				}, 2000);			
			}
			else{
				let bloc_message_map_comment = ""
				    bloc_message_map_comment += "<div id='result_question'><ul name='history' id='history_question'></ul></div>";
				$('#history_label').after(bloc_message_map_comment);
				show_history_bloc_with_input()
				setTimeout(() => {
					show_random_negative_anser(data['random_negative_anser']);
				}, 500);
			}
		},
		error: function(error){
			console.log(error);
		}
	});
};

function show_history_label(){
	const label = $("#history_label")
	if(label.css("display", "none")){
		label.css("display", "block");
	}
	else{
		label.css("display", "none");
    }
}

function change_text_send_button(){
	const btn = $("#form_send_button")
	const input = $("#form_input_question")
	if(btn.val("Prés à envoyer")){
		btn.val("Envoyé");
	}
	else{
		btn.val("Prés à envoyer");
	}
	setTimeout(() => {
		btn.val("Prés à envoyer")
		input.val("")
	}, 2000);
};

function show_history_bloc_with_input(){
    const res = $("#result_question")
	if(res.css("display", "none")){
		res.css("display", "block");
	}
	else{
		res.css("display", "none");
	}
	let input = $("#form_input_question").val()
	$("#history_question").append("<li id='input' class='list-unstyled'>- " + input + "</li>");
};

function show_random_positive_anser(random_positive_anser){
	$("#history_question").append("<li class='list-unstyled' id='random_positive_anser' name='GrandPyApp_random_response'>* " + random_positive_anser + "</li>");
};

function show_random_negative_anser(random_negative_anser){
	$("#history_question").append("<li class='list-unstyled' id='random_negative_anser' name='GrandPyApp_random_response'>* " + random_negative_anser + "</li>");
};

function show_summary_and_link(summary, link){
	$("#grandpyapp_comments").append("<p id='GrandPyApp_response' name='GrandPyApp_response'>Voici une brève description de ce que tu recherches : <br><br>" + 
		summary + "...</p>" + 
		"<a href=" + link + " target='_blank' name='GrandPyApp_response'>[Pour plus d'informations, clique sur ce lien]</a>");
}

function icon_loading_rotation(){
	const icon = $("#loading_icon")
	if(icon.css("display", "none")){
		icon.css("display", "block");
	}
	else{
		icon.css("display", "none");
	}
	if(icon.css("animation-play-state", "paused")){
		icon.css("animation-play-state", "running");
	}
	else{
		icon.css("animation-play-state", "paused");
	}
	setTimeout(() => {
	icon.css("animation-play-state", "paused");
	icon.css("display", "none");
    }, 2000);
}

function init_map(long_name, lat, lng, map_id){
    if($('[name="map"]').css("display", "none")){
		$('[name="map"]').css("display", "block");
	}
	else{
		$('[name="map"]').css("display", "none");
	}
    
	let query = {lat: lat, lng: lng}
	let options = {
		zoom: 12,
		center: query
	}

	let map = new google.maps.Map(document.getElementById(map_id), options);

	let marker = new google.maps.Marker({
		position: query,
		map: map
	});

	let infoWindow = new google.maps.InfoWindow({
		content: "<h4>Tu es à/au : " + long_name + "</h4>"
	});

	marker.addListener('click', function(){
		infoWindow.open(map, marker);
	});
};
