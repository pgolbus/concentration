from __future__ import annotations

from typing import List
from . import ConcentrationDao as Dao


class DummyConcentrationDao(Dao):
    """Concentration DAO for no database.

    """

    def __init__(self) -> None:
        """Initialize DummyConcentrationDao.

        """
        super().__init__()

        self._cards = None
        self._matched = None

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
    def matched(self) -> list[str]:
        """The matched.

        """
        return self._matched

    @matched.setter
    def matched(self, matched: List[bool]) -> None:
        """The matched.

        """
        self._matched = matched
