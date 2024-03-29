from __future__ import annotations

from typing import Optional

import click
import flask
from flask_cors import CORS

from concentration import logger
from concentration.model import Model
from concentration.redis_model import RedisModel

logger = logger.get_logger(__name__, "debug")

MODEL = None
MODEL_CONSTRUCTOR = None


app = flask.Flask(__name__)
# This is to handle inside WSL to outside looking like a cross server request
CORS(app)

# The face up card indices
INDICES_UP = []

# The number of guesses
GUESSES = 0


@app.route('/health', methods=['GET'])
def health() -> flask.Response:
    """Health check.

    """
    data = {
        'message': 'OK'
    }
    return flask.make_response(data, 200)


@app.route('/reset', methods=['POST'])
def reset() -> flask.Response:
    """Reset game.

    """
    # Specify global scope if going to change the value of a global variable.
    global MODEL, INDICES_UP, GUESSES

    logger.info('Resetting game.')

    MODEL = MODEL_CONSTRUCTOR()
    INDICES_UP = []
    GUESSES = 0

    data = {
        'message': 'OK'
    }
    return flask.make_response(data, 200)


@app.route('/card/<int:index>', methods=['GET'])
def card(index: int) -> flask.Response:
    """Get card info.

    """
    data = {
        'card': MODEL.cards[index],
        'match': MODEL.matched[index],
        'state': MODEL.state[index]
    }

    return flask.make_response(data, 200)


@app.route('/select/<int:index>', methods=['POST'])
def select(index: int) -> flask.Response:
    """Select a card.

    """
    # Specify global scope if going to change the value of a global variable.
    global MODEL, INDICES_UP, GUESSES

    logger.info(f'Selecting card. {index}')

    if len(INDICES_UP) == 2:
        INDICES_UP = []
        MODEL.state = ['down'] * 52

    # Edge cases: Selecting a matched card or selected card.
    if MODEL.matched[index] is True:
        data = {
            'message': 'Card already matched. Try again.'
        }
        return flask.make_response(data, 200)
    elif MODEL.state[index] == 'up':
        data = {
            'message': 'Card already selected. Try again.'
        }
        return flask.make_response(data, 200)

    state = MODEL.state
    state[index] = 'up'
    MODEL.state = state
    INDICES_UP.append(index)

    if len(INDICES_UP) == 2:
        GUESSES += 1
        index1 = INDICES_UP[0]
        index2 = INDICES_UP[1]
        card1 = MODEL.cards[index1]
        card2 = MODEL.cards[index2]

        if card1[0] == card2[0]:
            matched = MODEL.matched
            matched[index1] = True
            matched[index2] = True
            MODEL.matched = matched
    data = {
        'message': 'OK'
    }
    return flask.make_response(data, 200)


@app.route('/guesses', methods=['GET'])
def get_guesses() -> flask.Response:
    """Select a card.
    """
    data = {
        'guesses': GUESSES,
    }

    return flask.make_response(data, 200)


@click.command()
@click.option('--redis', is_flag=True, default=False)
def run(redis: Optional[bool] = False) -> None:
    global MODEL, MODEL_CONSTRUCTOR
    if redis:
        MODEL_CONSTRUCTOR = RedisModel
    else:
        MODEL_CONSTRUCTOR = Model
    MODEL = MODEL_CONSTRUCTOR()
    logger.info("modelled")
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == '__main__':
    run()
