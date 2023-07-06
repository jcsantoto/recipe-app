$(document).ready(function() {

    $('#input-tag-box').selectize({
    plugins: ['remove_button'],
    delimiter: ",",
    persist: false,
    showAddOptionOnCreate: true,
    create: function(input) {
      return {
        value: input,
        text: input
      };
    }
    });

});


