$(document).ready(function() {

    // Check if the recipe data is available in Local Storage using jQuery
    const recipeId = parseInt(window.location.pathname.split('/').pop(), 10);
    const cachedRecipeData = localStorage.getItem(`cachedRecipeData_${recipeId}`);

    console.log(recipeId);


    // If cached data is available
    if (cachedRecipeData) {

        // Parse it and display the recipe information
        displayRecipe(JSON.parse(cachedRecipeData));
        console.log("Displaying cached data");
    }

    // If no cached data or the data has expired
    else {
        // Fetch the recipe information from the API using jQuery
        fetchRecipeData(recipeId)
            .done(recipe => {
                localStorage.setItem(`cachedRecipeData_${recipeId}`, JSON.stringify(recipe));
                displayRecipe(recipe);
            });
    }


});

function displayRecipe(recipe) {

    // Display the recipe information on the webpage using jQuery
    const recipeTitleDiv = $('#recipe-title');
    const recipeSummaryDiv = $('#recipe-summary');
    const recipeIngredientsDiv = $('#recipe-ingredients');
    const recipeInstructionsDiv = $('#recipe-instructions');

    // Clear any existing content
    recipeTitleDiv.empty();
    recipeSummaryDiv.empty();
    recipeIngredientsDiv.empty();
    recipeInstructionsDiv.empty();

    recipeTitleDiv.append(`<h3> ${recipe.title} </h3>`);
    recipeSummaryDiv.append(`<p> ${recipe.summary} </p>`)

    const ingredientUL = $("<ul>").attr({
        style: "list-style-type:square; line-height: 0px;"
    })

    recipe.ingredients.forEach(ingredient => {

        ingredientUL.append($("<p>").append($("<ul>").append(`${ingredient.amount}`)))
    });



    recipeIngredientsDiv.append(ingredientUL)





    console.log(recipe.title);



}

// Function to fetch recipe data from the API using jQuery
function fetchRecipeData(recipeId) {
    console.log("Retrieving from database");
    return $.getJSON(`/retrieve-recipe/${recipeId}`);
}


