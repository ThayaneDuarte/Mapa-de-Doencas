var map;
var erro=document.getElementById("erro");

function initialize() {	
	if (navigator.geolocation)
	{
	    navigator.geolocation.getCurrentPosition(showPosition,showError);
	}
	else
	{
		erro.innerHTML="Geolocalização não é suportada nesse browser.";
	}	
}
initialize();

function showPosition(position)
{
  	lat=position.coords.latitude;
  	lon=position.coords.longitude;
  	latlon=new google.maps.LatLng(lat, lon)
  		
	var options = {
	    zoom: 15,
		center: latlon,
	    mapTypeId: google.maps.MapTypeId.ROADMAP
	};
	
	map = new google.maps.Map(document.getElementById("mapa"), options);
	var marker4 = new google.maps.Marker({
    position: new google.maps.LatLng(position.coords.latitude, position.coords.longitude),
    title: "Malária",
    map: map});
    	carregarPontos();
	
}
 
function showError(error)
{
	switch(error.code)
	{
		case error.PERMISSION_DENIED:
			erro.innerHTML="Usuário rejeitou a solicitação de Geolocalização."
			break;
		case error.POSITION_UNAVAILABLE:
			erro.innerHTML="Localização indisponível."
			break;
		case error.TIMEOUT:
		    erro.innerHTML="O tempo da requisição expirou."
		    break;
		case error.UNKNOWN_ERROR:
		    erro.innerHTML="Algum erro desconhecido aconteceu."
		    break;
	}
}
function abrirInfoBox(id, marker) {
	if (typeof(idInfoBoxAberto) == 'number' && typeof(infoBox[idInfoBoxAberto]) == 'object') {
		infoBox[idInfoBoxAberto].close();
	}

	infoBox[id].open(map, marker);
	idInfoBoxAberto = id;
}

function carregarPontos() {	
	var marker1 = new google.maps.Marker({
    position: new google.maps.LatLng(-19.928934, -43.980203),
    title: "Cancer",
    map: map});
    var marker2 = new google.maps.Marker({
    position: new google.maps.LatLng(-22.87877194865705, -47.05914315872184),
    title: "Gripe",
    map: map});
    var marker3 = new google.maps.Marker({
    position: new google.maps.LatLng(-22.882132704079144, -47.060530090490715),
    title: "Afta",
    map: map});
  	
	
}
