$(document).ready(function() {
  $(".favorite-btn").click(function() {
    var recipeId = $(this).data("recipe-id");
    var recipeTitle = $("#recipe-title").children("h3").text();

    console.log(recipeTitle)

    var button = $(this);
    var buttonText = button.text().trim()

    // AJAX request
    $.ajax({
      type: "POST",
      url: "/favorite/recipe/" + recipeId,
      data: {title: recipeTitle},
      success: function(response) {

        // Handle the response from the Flask backend


        if (buttonText === "Favorite"){
            button.text("Unfavorite");
            console.log("one");
        }
        else if (buttonText === "Unfavorite") {
            button.text("Favorite");
            console.log("two");
        }




      },

      error: function(error) {
        // Handle the error, if any
        console.log(error);
      }
    });
  });
});
