from __future__ import annotations

from typing import List
from abc import ABC, abstractmethod
import logging


class ConcentrationDao(ABC):
    """Abstract class for concentration data access objects (DAOs).

    """

    def __init__(self) -> None:
        """Initalize ConcentrationDao.

        """
        self._logger = logging.getLogger(__name__)
        self._state = None

    @property
    @abstractmethod
    def cards(self) -> List[str]:
        """The cards.

        """
        raise NotImplementedError()

    @cards.setter
    @abstractmethod
    def cards(self, cards: List[str]):
        """The cards.

        """
        raise NotImplementedError()

    @property
    def state(self) -> List[str]:
        """The state.

        """
        return self._state

    @state.setter
    def state(self, state: List[str]):
        """The state.

        """
        self._state = state

    @property
    @abstractmethod
    def matched(self) -> List[bool]:
        """The matched.

        """
        raise NotImplementedError()

    @matched.setter
    @abstractmethod
    def matched(self, moves: List[bool]):
        """The matched.

        """
        raise NotImplementedError()
