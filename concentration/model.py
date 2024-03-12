from __future__ import annotations


import random
import requests
from typing import List, Optional

from .daos import RedisConcentrationDao as RedisDao
from .daos import SQLiteConcentrationDao as SQLiteDao
from .daos import DummyConcentrationDao as DummyDao


class ConcentrationModel:
    """Model for concentration game.

    """

    def __init__(self, dao_identifier: Optional[str] = None, db: int = 0) -> None:
        """Initialize ConcentrationModel.

        Parameters
        ----------
        dao_identifier : str (default=`None`)
            "redis" for Redis, "sqlite" for SQLite.
        db : int
            Redis database number.

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

        cards = []
        for value in values:
            for suit in suits:
                cards.append(value + suit)
        cards = self.shuffle(cards=cards)

        self._dao = DummyDao()
        if dao_identifier == 'redis':
            self._dao = RedisDao(db)
        elif dao_identifier == 'sqlite':
            self._dao = SQLiteDao()

        self._dao.cards = cards
        self._dao.state = ['down'] * 52
        self._dao.matched = [False] * 52

    def shuffle(self, cards: List[str]) -> List[str]:
        """Shuffle the cards.

        The Random.org API is called to access a random seed for shuffling.

        Parameters
        ----------
        cards : List[str]
            The unshuffled cards.

        Returns
        -------
        cards : List[str]
            The shuffled cards.

        """
        url = 'https://www.random.org/integers/?num=1&min=1&max=5&col=1&base=10&format=plain&rnd=new'
        # response = requests.get(url=url)

        # seed = response.json()
        random.seed(a=42)

        random.shuffle(cards)
        return cards

    @property
    def cards(self) -> List[str]:
        """The cards.

        """
        return self._dao.cards

    @cards.setter
    def cards(self, cards: List[str]) -> None:
        """The cards.

        """
        self._dao.cards = cards

    @property
    def state(self) -> List[str]:
        """The state.

        """
        return self._dao.state

    @state.setter
    def state(self, state: List[str]) -> None:
        """The state.

        """
        self._dao.state = state

    @property
    def matched(self) -> List[bool]:
        """The matched.

        """
        return self._dao.matched

    @matched.setter
    def matched(self, matched: List[bool]) -> None:
        """The matched.

        """
        self._dao.matched = matched

    def game_over(self) -> bool:
        """Checks if the game is over.

        Returns
        -------
        status : bool
            `True` if the game is over. `False` otherwise.

        """
        return all(self._dao.matched)
