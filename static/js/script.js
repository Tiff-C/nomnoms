$(document).ready(function(){
    /**
     * Initializes JS elements once document has finished loading.
     */
    $('.sidenav').sidenav();
    $('.tooltipped').tooltip();
    $('select').formSelect();
});

// code based off Shouts.Dev post (see ReadMe: Credits)
$("#addIngredientRow").click(function () {
    /**
     * Dynamically adds an ingredient row to add_recipe form
     */
    let html = `
    <div id="inputIngredientRow">
        <div class="input-field">
            <i class="prefix material-icons yellow-text text-darken-4">kitchen</i>
            <input id="recipe_ingredient" name="recipe_ingredient" minlength="3" maxlength="30" type="text" pattern="^[a-zA-Z0-9\.\'\_\s]{3,30}$" class="validate">
            <label for="recipe_ingredient">
                Recipe Ingredients
                <i class="tiny material-icons tooltipped" data-position="top" data-tooltip="Ingredients required for this recipe, use + to add a new field.">help</i>
            </label>
        </div>
        <div class="input-group-append">
            <button id="removeIngredientRow" type="button" class="btn red darken-2">
                <i class="medium material-icons">remove</i>
            </button>
        </div>
    </div>`;

    $('#newIngredientRow').append(html);
});

// code based off Shouts.Dev post (see ReadMe: Credits)
$(document).on('click', '#removeIngredientRow', function () {
    /**
     * Dynamically removes an ingredient row to add_recipe form
     */
    $(this).closest('#inputIngredientRow').remove();
});

// code based off Shouts.Dev post (see ReadMe: Credits)
$("#addInstructionRow").click(function () {
    /**
     * Dynamically adds an instruction row to add_recipe form
     */
    let html = `
    <div id="inputInstructionRow">
        <div class="input-field">
            <i class="prefix material-icons yellow-text text-darken-4">kitchen</i>
            <input id="recipe_instruction" name="recipe_instruction" minlength="5" maxlength="100" type="text" pattern="^[a-zA-Z0-9\.\'\_\s]{5,100}{1,50}$" class="validate">
            <label for="recipe_instruction">
                Recipe Instructions
                <i class="tiny material-icons tooltipped" data-position="top" data-tooltip="Cooking instructions for this recipe, use + to add a new field.">help</i>
            </label>
        </div>
        <div class="input-group-append">
            <button id="removeInstructionRow" type="button" class="btn red darken-2">
                <i class="medium material-icons">remove</i>
            </button>
        </div>
    </div>`;

    $('#newInstructionRow').append(html);
});

// code based off Shouts.Dev post (see ReadMe: Credits)
$(document).on('click', '#removeInstructionRow', function () {
    /**
     * Dynamically removes an instruction row to add_recipe form
     */
    $(this).closest('#inputInstructionRow').remove();
});