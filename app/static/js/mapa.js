function initialize() {

  // Exibir mapa;
  var myLatlng = new google.maps.LatLng(42.670885, -6.979647);
  var mapOptions = {
    zoom: 17,
    center: myLatlng,
    panControl: false,
    scrollwheel: false,
    // mapTypeId: google.maps.MapTypeId.ROADMAP
    mapTypeControlOptions: {
      mapTypeIds: [google.maps.MapTypeId.ROADMAP, 'map_style']
    }
  }


  // ParÃ¢metros do texto que serÃ¡ exibido no clique;
  var contentString = '<h2>Brigid MIXs</h2>' +
  '<p>Brigid MIXs</p>';
  //'<a href="" target="_blank">Clique aqui para mais informaÃ§Ãµes</a>';
  var infowindow = new google.maps.InfoWindow({
      content: contentString,
      maxWidth: 700
  });


  // Exibir o mapa na div #mapa;
  var map = new google.maps.Map(document.getElementById("mapa"), mapOptions);


  // Marcador personalizado;
  var image = 'http://www.ofaxineiro.com/includes/img/pin.png';
  var marcadorPersonalizado = new google.maps.Marker({
      position: myLatlng,
      map: map,
      icon: image,
      title: 'Brigid MIXs - Torres/RS',
      animation: google.maps.Animation.DROP
  });


//   // Exibir texto ao clicar no Ã­cone;
  google.maps.event.addListener(marcadorPersonalizado, 'click', function() {
    infowindow.open(map,marcadorPersonalizado);
  });


  // Estilizando o mapa;
  // Criando um array com os estilos
  var styles = [{"featureType":"all","stylers":[{"saturation":0},{"hue":"#e7ecf0"}]},{"featureType":"road","stylers":[{"saturation":-70}]},{"featureType":"transit","stylers":[{"visibility":"off"}]},{"featureType":"poi","stylers":[{"visibility":"off"}]},{"featureType":"water","stylers":[{"visibility":"simplified"},{"saturation":-60}]}];

  // crio um objeto passando o array de estilos (styles) e definindo um nome para ele;
  var styledMap = new google.maps.StyledMapType(styles, {
    name: "Mapa Style"
  });

  // Aplicando as configuraÃ§Ãµes do mapa
  map.mapTypes.set('map_style', styledMap);
  map.setMapTypeId('map_style');

}


// FunÃ§Ã£o para carregamento assÃ­ncrono
function loadScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyDeHb17So0QupSGO_d6b8X-OyvJ32UQehs&sensor=false&callback=initialize";
  document.body.appendChild(script);
}

window.onload = loadScript;