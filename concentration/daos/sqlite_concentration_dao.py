from __future__ import annotations

from typing import List
import sqlite3
from . import ConcentrationDao as Dao

# lock = Lock()

class SQLiteConcentrationDao(Dao):
    """Concentration DAO for SQLite.

    """

    def __init__(self) -> None:
        """Initialize SQLiteConcentrationDao.

        """
        super().__init__()

        self._logger.info("Connecting to SQLite.")
        self._connection = sqlite3.connect(database='concentration.db', check_same_thread=False)

        self._cursor = self._connection.cursor()

        # Clear data (if exists)
        try:
            self.execute_sql_command(command="DROP TABLE data")
        except sqlite3.OperationalError:
            pass

        self._cursor.execute("CREATE TABLE data(name, list)")

    def execute_sql_command(self, command: str) -> sqlite3.Cursor:
        """Execute an SQL command.

        Parameters
        ----------
        command : str
            The SQL command.

        Returns
        -------
        result : sqlite3.Cursor

        """
        with self._connection:
            cursor = self._connection.cursor()
            result = cursor.execute(command)
            self._connection.commit()

        return result

    def list_to_string(self, a_list: List) -> str:
        """Convert a list to a string.

        Parameters
        ----------
        a_list : List
            The list.

        Returns
        -------
        a_string : str
            The string representation of ``a_list``.

        """
        a_string = ','.join(str(entry) for entry in a_list)
        return a_string

    def string_to_list(self, a_string: str) -> List:
        """Convert a list to a string.

        Parameters
        ----------
        a_string : str
            The string.

        Returns
        -------
        string : List
            The list representation of ``a_string``.

        """
        a_list = []

        for entry in a_string.split(','):
            if entry == 'True':
                entry = True
            elif entry == 'False':
                entry = False
            a_list.append(entry)

        return a_list

    @property
    def cards(self) -> List[str]:
        """The cards.

        """
        self._logger.info("Getting cards from SQLite.")
        cards = self.execute_sql_command(command="SELECT list FROM data where name='cards'")
        cards = cards.fetchone()[0]
        cards = self.string_to_list(a_string=cards)
        return cards

    @cards.setter
    def cards(self, cards: List[str]) -> None:
        """The cards.

        """
        self._logger.info("Setting cards in SQLite.")
        self._logger.debug(cards)

        # Delete old entry
        self.execute_sql_command(command="DELETE FROM data WHERE name='cards'")
        self._connection.commit()

        # Add new entry
        cards = self.list_to_string(cards)
        self.execute_sql_command(command=f"INSERT INTO data VALUES('cards', '{cards}')")
        self._connection.commit()

    @property
    def state(self) -> List[str]:
        """The state.

        """
        self._logger.info("Getting state from SQLite.")
        state = self.execute_sql_command(command="SELECT list FROM data where name='state'")
        state = state.fetchone()[0]
        state = self.string_to_list(a_string=state)
        return state

    @state.setter
    def state(self, state) -> None:
        """The state.

        """
        self._logger.info("Setting state in SQLite.")
        self._logger.debug(state)

        # Delete old entry
        self._cursor.execute("DELETE FROM data WHERE name='state'")
        self._connection.commit()

        # Add new entry
        state = self.list_to_string(state)
        self.execute_sql_command(command=f"INSERT INTO data VALUES('state', '{state}')")
        self._connection.commit()

    @property
    def matched(self) -> list[str]:
        """The matched.

        """
        self._logger.info("Getting matched from SQLite.")
        matched = self.execute_sql_command(command="SELECT list FROM data where name='matched'")
        matched = matched.fetchone()[0]
        matched = self.string_to_list(a_string=matched)
        return matched

    @matched.setter
    def matched(self, matched: List[bool]) -> None:
        """The matched.

        """
        self._logger.info("Setting matched in SQLite.")
        self._logger.debug(matched)

        # Delete old entry
        self._cursor.execute("DELETE FROM data WHERE name='matched'")
        self._connection.commit()

        # Add new entry
        matched = self.list_to_string(matched)
        self.execute_sql_command(command=f"INSERT INTO data VALUES('matched', '{matched}')")
        self._connection.commit()
