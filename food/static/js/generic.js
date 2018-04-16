var $star_rating = $('.star-rating .fa');

var SetRatingStar = function() {
  return $star_rating.each(function() {
    if (parseInt($star_rating.siblings('input.rating-value').val()) >= parseInt($(this).data('rating'))) {
      return $(this).removeClass('fa-star-o').addClass('fa-star');
    } else {
      return $(this).removeClass('fa-star').addClass('fa-star-o');
    }
  });
};

$star_rating.on('click', function() {
  $star_rating.siblings('input.rating-value').val($(this).data('rating'));
  return SetRatingStar();
});

SetRatingStar();
$(document).ready(function() {

});

/****************************************
***       BASE-GENERIC-SEARCH         ***
****************************************/

$(document).ready(function() {
  $('.search-products-form').on('click', '.search-toggle', function() {
    if ($('[name="search-products-bar"]').is(":visible")) {
      $('[name="search-products-bar"]').css("display", "none");
      $('[id="close-search-icon"]').css("display", "none");
      $('[id="open-search-icon"]').css("display", "block");
    } else {
      $('[name="search-products-bar"]').css("display", "block");
      $('[id="open-search-icon"]').css("display", "none");
      $('[id="close-search-icon"]').css("display", "block");
    }
  });
});