$(document).ready(function() {

    $('#overview').hide();
    $('#overview').fadeIn();

  $('#dynamic a').on('click', function(event) {

    event.preventDefault();

    $('#dynamic a').removeClass('active');

    $(this).addClass('active');

    // Get the target content section ID
    var target = $(this).data('target');

    // Check if the section has not been loaded
    if (!$('#' + target).hasClass('loaded')) {
      // Make an AJAX request based on the clicked link
      $.ajax({
        url: '/account/' + target,
        type: 'GET',
        success: function(response) {
          // Update the content section with the received data

          $('#' + target).html(response);
          $('#' + target).addClass('loaded');
        },
        error: function(error) {
          console.log('Error:', error);
        }
      });


    }

    $('.content-section').each(function() {
        $(this).hide();
    });

    $('#' + target).fadeIn();

  });

});