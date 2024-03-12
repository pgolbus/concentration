from __future__ import annotations

import logging
import sys
from typing import Optional

import click
import flask
from flask_cors import CORS

from model import ConcentrationModel


APP = flask.Flask(__name__)
CORS(APP)

LOGGER = logging.getLogger()

LOGGER.info('Loading model.')

DAO_IDENTIFIER = None
MODEL = None
APP = flask.Flask(__name__)
CORS(APP)

LOGGER = logging.getLogger()
# Set logger to handle STDERR.
HANDLER = logging.StreamHandler(sys.stderr)
# Format the log messages.
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
HANDLER.setFormatter(FORMATTER)
# Attach the STDERR handler to the logger.
LOGGER.addHandler(HANDLER)
# Set log level to debug
# LOGGER.setLevel(logging.DEBUG)


LOGGER.info('Loading model.')

DAO_IDENTIFIER = None
MODEL = None

# The face up card indices
INDICES_UP = []

# The number of guesses
GUESSES = 0


@APP.route('/health', methods=['GET'])
def health() -> flask.Response:
    """Health check.

    """
    data = {
        'message': 'OK'
    }
    return flask.make_response(data, 200)


@APP.route('/reset', methods=['POST'])
def reset() -> flask.Response:
    """Reset game.

    """
    # Specify global scope if going to change the value of a global variable.
    global MODEL, INDICES_UP, GUESSES

    APP.logger.info('Resetting game.')

    MODEL = ConcentrationModel(dao_identifier=DAO_IDENTIFIER)
    INDICES_UP = []
    GUESSES = 0

    data = {
        'message': 'OK'
    }
    return flask.make_response(data, 200)


@APP.route('/card/<int:index>', methods=['GET'])
def card(index: int) -> flask.Response:
    """Get card info.

    """
    data = {
        'card': MODEL.cards[index],
        'match': MODEL.matched[index],
        'state': MODEL.state[index]
    }

    return flask.make_response(data, 200)


@APP.route('/select/<int:index>', methods=['POST'])
def select(index: int) -> flask.Response:
    """Select a card.

    """
    # Specify global scope if going to change the value of a global variable.
    global MODEL, INDICES_UP, GUESSES

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


@APP.route('/guesses', methods=['GET'])
def get_guesses() -> flask.Response:
    """Select a card.
    """
    data = {
        'guesses': GUESSES,
    }

    return flask.make_response(data, 200)


@click.command()
@click.option('--dao-identifier', default=None)
def run(dao_identifier: Optional[str] = None) -> None:
    global MODEL, DAO_IDENTIFIER
    DAO_IDENTIFIER = dao_identifier
    MODEL = ConcentrationModel(dao_identifier=DAO_IDENTIFIER)
    APP.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    run()
