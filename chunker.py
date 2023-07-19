import hashlib
from typing import Optional,Callable

from langchain.text_splitter import RecursiveCharacterTextSplitter


TEXT_SPLITTER_CHUNK_PARAMS = {
    "chunk_size": 200,
    "chunk_overlap": 56,
    "length_function": len,
}

class BaseConfig:
    """
    Base config.
    """

    def __init__(self):
        pass

    def as_dict(self):
        return vars(self)

class ChunkerConfig(BaseConfig):
    """
    Config for the chunker used in `add` method
    """

    def __init__(
        self,
        chunk_size: Optional[int] = 200,
        chunk_overlap: Optional[int] = 56,
        length_function: Optional[Callable[[str], int]] = len,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.length_function = length_function


class BaseChunker:
    def __init__(self, text_splitter):
        """Initialize the chunker."""
        self.text_splitter = text_splitter

    def create_chunks(self, loader, src):
        """
        Loads data and chunks it.

        :param loader: The loader which's `load_data` method is used to create
        the raw data.
        :param src: The data to be handled by the loader. Can be a URL for
        remote sources or local content for local loaders.
        """
        documents = []
        ids = []
        idMap = {}
        datas = loader.load_data(src)
        metadatas = []
        for data in datas:
            content = data["content"]
            meta_data = data["meta_data"]
            url = meta_data["url"]

            chunks = self.get_chunks(content)

            for chunk in chunks:
                chunk_id = hashlib.sha256((chunk + url).encode()).hexdigest()
                if idMap.get(chunk_id) is None:
                    idMap[chunk_id] = True
                    ids.append(chunk_id)
                    documents.append(chunk)
                    metadatas.append(meta_data)
        return {
            "documents": documents,
            "ids": ids,
            "metadatas": metadatas,
        }

    def get_chunks(self, content):
        """
        Returns chunks using text splitter instance.

        Override in child class if custom logic.
        """
        return self.text_splitter.split_text(content)


class PdfFileChunker(BaseChunker):
    """Chunker for PDF file."""

    def __init__(self, config: Optional[ChunkerConfig] = None):
        if config is None:
            config = TEXT_SPLITTER_CHUNK_PARAMS
        text_splitter = RecursiveCharacterTextSplitter(**config)
        super().__init__(text_splitter)
