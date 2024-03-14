const API_URL = '127.0.0.1:5000';
const IMAGES_FOLDER = 'resources/images/';

/**
 * API call: POST request to reset the game.
 * @returns The response JSON.
 */
async function apiReset() {
    var url = API_URL + '/reset';

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });

    console.log('API call: /reset');
    var data = await response.json();

    return data;
}

/**
 * API call: GET request to get the number of guesses.
 * @returns The response JSON.
 */
async function apiGuesses() {
    var url = API_URL + '/guesses';

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });

    console.log('API call: /guesses');
    var data = await response.json();

    return data;
}

/**
 * API call: POST request to select a card.
 * @param {Number} index The card index.
 * @returns The response JSON.
 */
async function apiSelect(index) {
    var url = API_URL + '/select/' + index;

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });

    console.log('API call: /select/' + index);
    var data = await response.json();
    console.log(data);

    return data;
}

/**
 * API call: GET request to get card information.
 *
 * @param {Number} index The card index.
 * @returns The response JSON.
 */
async function apiCard(index) {
    var url = API_URL + '/card/' + index;

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    });

    console.log('API call: /card/' + index);
    var data = await response.json();
    console.log(data);

    return data;
}

/**
 * This function is ran when the webpage first loads.
 */
$(async function () {
    // Assign to each image a function to call when clicked.
    // Specifically: select()
    $("img").each(function (key, value) {
        $(this).click({index: key}, select)
    })

    // Assign to the reset button a function to call when clicked.
    // Specifically: reset()
    $("#button").click(reset);
})

/**
 * Selects a card.
 */
async function select(event) {
    var index = event.data.index;
    var data = await apiSelect(index);

    if (data['message'] != 'OK') {
        $('#message').text(data['message']);
    }
    else {
        $('#message').text("");
    }
    var data = await apiGuesses();
    $('#label').text(data['guesses']);
    if (data['message'] != 'OK') {
        $('#message').text(data['message']);
    }
    else {
        $('#message').text("");
    }
    var data = await apiGuesses();
    $('#label').text(data['guesses']);

    await updateCards();
}

/**
 * Updates cards.
 */
async function updateCards() {
    $("img").each(async function (index, card) {
        var gif = IMAGES_FOLDER + "back.gif";

        var data = await apiCard(index);
        if (data['match'] == true || data['state'] == 'up') {
            gif = IMAGES_FOLDER + data['card'] + ".gif";
        }

        $(card).attr("src", gif);
    })
}

/**
 * Resets the game.
 */
async function reset() {
    $('#message').text("");
    await apiReset();
    var data = await apiGuesses();

    $('#label').text(data['guesses']);
    updateCards();
    $('#message').text("");
}
