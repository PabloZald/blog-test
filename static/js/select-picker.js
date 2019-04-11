$('.selectpicker').attr({'data-live-search': 'true',});
if( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
  $('.selectpicker').selectpicker('mobile');
}
// Add Class
$('.selectpicker').selectpicker('setStyle', 'bg-white btn-lg', 'add');