$(document).ready(function() {
  $(".favorite-btn").click(function() {
    var recipeId = $(this).data("recipe-id");
    var button = $(this);
    var buttonText = button.text().trim()

    // AJAX request
    $.ajax({
      type: "POST",
      url: "/recipe/" + recipeId,
      data: { /* Additional data if needed */ },
      success: function(response) {

        // Handle the response from the Flask backend

        console.log(buttonText === "Favorite")
        console.log(buttonText === "Unfavorite")


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
