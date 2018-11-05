$(document).ready(function() {
  $("#more").click(function() {
    $('html, body').animate({
      scrollTop: $('#test').offset().top
    },1000); 
  });
});