from __future__ import annotations

import logging
import random
from typing import List

from . import logger



class Model:
    """Model for concentration game.

    """

    def __init__(self) -> None:
        """Initialize ConcentrationModel.
        """
        values = [
            '2',
            '3',
            '4',
            '5',
            '6',
            '7',
            '8',
            '9',
            '10',
            'j',
            'q',
            'k',
            'a'
        ]
        suits = [
            'c',
            'd',
            'h',
            's'
        ]

        self._logger = logger.get_logger(__name__)
        self._logger.info("Setting up the game.")
        self._cards = []
        for v in values:
            for s in suits:
                self._cards.append(f"{v}{s}")
        random.seed(42)
        random.shuffle(self._cards)

        self._state = ['down'] * 52
        self._matched = [False] * 52

    @property
    def cards(self) -> List[str]:
        """The cards.

        """
        return self._cards

    @cards.setter
    def cards(self, cards: List[str]) -> None:
        """The cards.

        """
        self._cards = cards

    @property
    def state(self) -> List[str]:
        """The state.

        """
        return self._state

    @state.setter
    def state(self, state: List[str]) -> None:
        """The state.

        """
        self._state = state

    @property
    def matched(self) -> List[bool]:
        """The matched.

        """
        return self._matched

    @matched.setter
    def matched(self, matched: List[bool]) -> None:
        """The matched.

        """
        self._matched = matched

    def game_over(self) -> bool:
        """Checks if the game is over.

        Returns
        -------
        status : bool
            `True` if the game is over. `False` otherwise.

        """
        return all(self.matched)
