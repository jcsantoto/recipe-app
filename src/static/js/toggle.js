 const targetItem = $('#toggle-search-bar');

$('#toggle-by-name, #toggle-by-ingredient').on('change', changeState);

function changeState() {

  if ($('#toggle-by-name').is(':checked')) {
    targetItem.attr('placeholder', 'Search by name')
    destroySelectize();
  } else if ($('#toggle-by-ingredient').is(':checked')) {
    targetItem.attr('placeholder', 'Search by ingredients')
    applySelectize();
  }

}

// Step 4: Apply selectize() function
function applySelectize() {
  if (!targetItem.hasClass('selectized')) {
    targetItem.selectize({
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
  }
}

// Step 5: Destroy selectize() function
function destroySelectize() {
  if (targetItem.hasClass('selectized')) {
    targetItem[0].selectize.destroy();

    const divWithStyle = $('div').filter(function() {
      return $(this).attr('style') === 'position: absolute; width: 0px; height: 0px; overflow: hidden;';
    });
    divWithStyle.remove();

  }
}