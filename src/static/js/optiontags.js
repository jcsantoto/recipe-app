$(document).ready(function() {

    console.log(window.myVariable)

    // For option select
    $('#option-tag-box').selectize({
    plugins: ['remove_button'],
    delimiter: ",",
    persist: false,


    });


});