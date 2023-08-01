$(document).ready(function() {
  // Add ingredient field

  var numIngredients = 0;
  var numSteps = 0;
  var removeBtn = $("<button>").text("Remove").addClass("remove-btn");

  $(".add-ingredient-btn").click(function() {

    numIngredients++;
    var container = $("#ingredients-container");

    var rowArea = $("<div>").attr({
        class: "row",
        style: "margin-top: 2%;"
    })
    var ingredientDiv = $("<div>").attr({
        class: "col"
    })
    var amountDiv = ingredientDiv.clone();
    var unitDiv = ingredientDiv.clone();


    var ingredientInput = $("<input>").attr({
      type: "text",
      name: "ingredients-"+numIngredients+"-ingredient",
      id: "ingredients-"+numIngredients+"-ingredient",
      class: "form-control form-control-lg"
    });

    var amountInput = $("<input>").attr({
      type: "number",
      step: "1",
      name: "ingredients-"+numIngredients+"-amount",
      id: "ingredients-"+numIngredients+"-amount",
      class: "form-control form-control-lg"
    });


    var unitInput = $("<input>").attr({
      type: "text",
      name: "ingredients-"+numIngredients+"-unit",
      id: "ingredients-"+numIngredients+"-unit",
      class: "form-control form-control-lg"
    });

    ingredientDiv.append(ingredientInput);
    amountDiv.append(amountInput);
    unitDiv.append(unitInput);

    rowArea.append(ingredientDiv);
    rowArea.append(amountDiv);
    rowArea.append(unitDiv);
    rowArea.append(removeBtn.clone());

    rowArea.insertBefore(this);

  });

  // Add instruction field
  $(".add-instruction-btn").click(function() {

    numSteps++;
    var container = $("#instructions-container");
    var stepDiv = $("<div>").attr({
        class: "row",
        style: "margin-top: 2%;"
    })

    var stepInput = $("<textarea>").attr({
        name: "instructions-"+numSteps+"-step",
        id: "instructions-"+numSteps+"-step",
        class: "form-control form-control-lg"
    });

    stepDiv.append(stepInput)
    stepDiv.insertBefore(this);


  });
});

// Remove button
$(document).on("click", ".remove-btn", function() {
    $(this).parent().remove();
});
