from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

class MySQLConnection:
    """
    Manages the lifecycle of a MySQL database connection using SQLAlchemy.
    """
    def __init__(self, uri: str, source_name: str):
        """
        :param uri: The full database URL (mysql+pymysql://user:pass@host/db)
        :param source_name: The key used by the extractor to find the right query
        """
        self.uri = uri
        self.source_name = source_name
        self._engine = None

    @property
    def connection(self) -> Engine:
        """
        Lazily initializes and returns the SQLAlchemy engine.
        """
        if self._engine is None:
            try:
                # pool_pre_ping=True checks if the connection is alive 
                # before passing it to the extractor
                self._engine = create_engine(
                    self.uri, 
                    pool_pre_ping=True,
                    pool_recycle=3600
                )
            except Exception as e:
                raise ConnectionError(f"Failed to connect to MySQL: {e}")
        
        return self._engine

    def dispose(self):
        """Closes all connections in the pool."""
        if self._engine:
            self._engine.dispose()