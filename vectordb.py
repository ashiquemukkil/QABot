import logging
import chromadb

class BaseVectorDB:
    """Base class for vector database."""

    def __init__(self):
        self.client = self._get_or_create_db()
        self.collection = self._get_or_create_collection()

    def _get_or_create_db(self):
        """Get or create the database."""
        raise NotImplementedError

    def _get_or_create_collection(self):
        raise NotImplementedError


class ChromaDB(BaseVectorDB):
    """Vector database using ChromaDB."""

    def __init__(self, db_dir=None, ef=None, host=None, port=None):
        self.ef = ef

        if host and port:
            logging.info(f"Connecting to ChromaDB server: {host}:{port}")
            self.client_settings = chromadb.config.Settings(
                chroma_api_impl="rest",
                chroma_server_host=host,
                chroma_server_http_port=port,
            )
        else:
            if db_dir is None:
                db_dir = "db"
            self.client_settings = chromadb.config.Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=db_dir,
                anonymized_telemetry=False,
            )
        super().__init__()

    def _get_or_create_db(self):
        """Get or create the database."""
        return chromadb.Client(self.client_settings)

    def _get_or_create_collection(self):
        """Get or create the collection."""
        return self.client.get_or_create_collection(
            "embedchain_store",
            embedding_function=self.ef,
        )
