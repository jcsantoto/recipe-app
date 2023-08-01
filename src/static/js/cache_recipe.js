$(document).ready(function() {

    // Check if the recipe data is available in Local Storage using jQuery
    const recipeId = parseInt(window.location.pathname.split('/').pop(), 10);
    const cachedRecipeData = localStorage.getItem(`cachedRecipeData_${recipeId}`);

    // If cached data is available
    if (cachedRecipeData) {

        // Parse it and display the recipe information
        displayRecipe(JSON.parse(cachedRecipeData));
        sendRecipeData(cachedRecipeData, recipeId);


    }

    // If no cached data or the data has expired
    else {
        // Fetch the recipe information from the API using jQuery
        fetchRecipeData(recipeId)
            .done(recipe => {
                localStorage.setItem(`cachedRecipeData_${recipeId}`, JSON.stringify(recipe));
                displayRecipe(recipe)
                sendRecipeData(cachedRecipeData, recipeId);


            });
    }


});

function displayRecipe(recipe) {

    // Display the recipe information on the webpage using jQuery
    const recipeTitleDiv = $('#recipe-title');
    const recipeSummaryDiv = $('#recipe-summary');
    const recipeIngredientsDiv = $('#recipe-ingredients');
    const recipeInstructionsDiv = $('#recipe-instructions');
    const recipePriceDiv = $('#recipe-price');
    const recipeNutrientDiv = $('#recipe-nutrients');

    // Clear any existing content
    recipeTitleDiv.empty();
    recipeSummaryDiv.empty();
    recipeIngredientsDiv.empty();
    recipeInstructionsDiv.empty();
    recipePriceDiv.empty()
    recipeNutrientDiv.empty()

    recipeTitleDiv.append(`<h3> ${recipe.title} </h3>`);
    recipeSummaryDiv.append(`<p> ${recipe.summary} </p>`)
    recipePriceDiv.append(`<p> ${recipe.price} </p>`)

    let ingredientHTML = `<ul style="list-style-type:square;">`

    recipe.ingredients.forEach(ingredient => {
        ingredientHTML += `
        <li>
            ${ingredient.amount}
            ${ingredient.unit}
            ${ingredient.name}
        </li>`
    });

    ingredientHTML += `</ul>`
    recipeIngredientsDiv.append(ingredientHTML)


    let nutrientHTML = `
    <table>
        <tr>
            <th> Nutrient </th>
            <th> Amount </th>
            <th> % Daily Value </th>
        </tr>`


    recipe.macros.forEach(macro => {
        nutrientHTML += `
        <tr>
            <td> ${macro.name} </td>
            <td> ${macro.amount} </td>
            <td> ${macro.percentOfDailyNeeds} </td>
        </tr>`
    });
    nutrientHTML += `</table>`
    recipeNutrientDiv.append(nutrientHTML)


    let instructionHTML = ``

    recipe.instructions.forEach(step => {
        instructionHTML += `

            <b>Step ${step.number}</b>
            <br>

            <div style="margin-top: 1px;">
                <p>
                    ${step.step}
                </p>
            </div>`
    });

    recipeInstructionsDiv.append(instructionHTML)


}

// Function to fetch recipe data from the API using jQuery
function fetchRecipeData(recipeId) {
    return $.getJSON(`/retrieve-recipe/${recipeId}`);
}


function sendRecipeData(recipe, recipeId){

    data = JSON.parse(recipe)

    if (isUserAuthenticated){
        post_data = JSON.stringify({ingredients: data.ingredients,
                       dairyFree: data.dairyFree,
                       glutenFree: data.glutenFree,
                       title: data.title
                       })
    }
    else{
        post_data = JSON.stringify({title: data.title})
    }

    $.ajax({
            url: '/recipe/' + recipeId, // Replace with your server-side route URL
            method: 'POST',
            data: post_data,
            contentType: 'application/json',
            success: function (response) {

                const recipeIntolDiv = $('#recipe-intolerances');

                response.forEach(intolerance=> {
                    recipeIntolDiv.append(`<span> Warning: The following recipe may contain ${intolerance} which
                    you have specified as an allergen <br> </span>`)
                });



            },
            error: function (error) {
                console.log(error);


            },
        });

}


