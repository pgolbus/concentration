from __future__ import annotations

from typing import List
import os

import redis
from redis.exceptions import ConnectionError
from . import ConcentrationDao as Dao


class RedisConcentrationDao(Dao):
    """Concentration DAO for Redis.

    """

    def __init__(self, db: int = 0) -> None:
        """Initialize RedisConcentrationDao.

        Parameters
        ----------
        db : int
            The database number.

        """
        super().__init__()
        self._logger.info("Connecting to Redis.")
        self._redis = self.redis_connect(db)

    def redis_connect(self, db: int) -> redis.Redis:
        """Connect to the Redis server.

        Parameters
        ----------
        db : int
            The database number.

        Returns
        -------
        connection : redis.Redis
            A Redis connection.

        """
        # redis_hostname = "redis" # os.getenv("REDIS_HOSTNAME")
        # redis_port = 6379 # os.getenv("REDIS_PORT")
        redis_hostname = os.getenv("REDIS_HOSTNAME")
        redis_port = os.getenv("REDIS_PORT")
        self._logger.debug(f"Connecting to {redis_hostname} on port {redis_port} w/ db {db}.")
        try:
            return redis.Redis(host=redis_hostname, port=redis_port, db=db, decode_responses=True)
        except ConnectionError:
            raise ConnectionError("Could not connect to Redis.")

    @property
    def cards(self) -> List[str]:
        """The cards.

        """
        self._logger.info("Getting cards from Redis.")
        cards = self._redis.lrange("cards", 0, -1)
        self._logger.debug(cards)
        return cards

    @cards.setter
    def cards(self, cards: List[str]) -> None:
        """The cards.

        """
        self._logger.info("Setting cards in Redis.")
        self._logger.debug(cards)
        self._redis.delete("cards")
        self._redis.rpush("cards", *cards)

    @property
    def state(self) -> List[str]:
        """The state.

        """
        self._logger.info("Getting state from Redis.")
        state = self._redis.lrange("state", 0, -1)
        self._logger.debug(state)
        return state

    @state.setter
    def state(self, state) -> None:
        """The state.

        """
        self._logger.info("Setting state in Redis.")
        self._logger.debug(state)
        self._redis.delete("state")
        self._redis.rpush("state", *state)

    @property
    def matched(self) -> list[str]:
        """The matched.

        """
        self._logger.info("Getting matched from Redis.")
        matched = self._redis.lrange("matched", 0, -1)
        self._logger.debug(matched)
        return matched

    @matched.setter
    def matched(self, matched: List[bool]) -> None:
        """The matched.

        """
        self._logger.info("Setting matched in Redis.")
        self._logger.debug(matched)
        self._redis.delete("matched")
        self._redis.rpush("matched", *[str(m) for m in matched])
