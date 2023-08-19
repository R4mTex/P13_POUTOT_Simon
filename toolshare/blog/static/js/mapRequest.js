let mapID = 0

$(document).ready(function () {
	data = {
		status: $('#status').val(),
		longName: $('#longName').val(),
		lat: parseFloat($('#lat').val()),
		lng: parseFloat($('#lng').val()),
	};
	if(data['status'] == 'OK'){
		let divMap = "<div id='" + mapID + "' name='map'></div>";	
		$('#location').after(divMap);
		initMap(data['longName'], data['lat'], data['lng'], mapID);
		mapID += 1
	}
})

function initMap(longName, lat, lng, mapID){
    if($('[name="map"]').css("display", "none")){
		$('[name="map"]').css("display", "block");
	}
	else{
		$('[name="map"]').css("display", "none");
	}
    
	let query = { lat: lat, lng: lng }
	let options = {
		zoom: 12,
		center: query
	}

	let map = new google.maps.Map(document.getElementById(mapID), options);

	let marker = new google.maps.Marker({
		position: query,
		map: map
	});

	let infoWindow = new google.maps.InfoWindow({
		content: "<h5>You are at : " + longName + "</h5>"
	});

	marker.addListener('click', function(){
		infoWindow.open(map, marker);
	});
};
