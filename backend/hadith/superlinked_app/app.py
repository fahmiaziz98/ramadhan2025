from superlinked import framework as sl
from superlinked.framework.dsl.storage.qdrant_vector_database import QdrantVectorDatabase

from superlinked_app import index, query
from superlinked_app.config import settings

vector_database = QdrantVectorDatabase(
    settings.QDRANT_URL_BASE,    
    settings.QDRANT_API_KEY,      
)

data_parser = sl.DataFrameParser(
    schema=index.hadist,
    mapping={
        index.hadist.id: 'id'
    }
)

data_loader_config = sl.DataLoaderConfig(
    "https://raw.githubusercontent.com/fahmiaziz98/ramadhan2025/refs/heads/main/backend/hadith/data/data_hadith.jsonl",
    sl.DataFormat.JSON,
    pandas_read_kwargs={"lines": True, "chunksize": 100},
)

source = sl.RestSource(index.hadist)
data_source = sl.DataLoaderSource(
    index.hadist,
    data_loader_config,
    data_parser,
)
executor: sl.RestExecutor = sl.RestExecutor(
    sources=[source, data_source],
    indices=[index.hadist_index],
    queries=[sl.RestQuery(sl.RestDescriptor("query"), query.base_query)],
    vector_database=vector_database
)

sl.SuperlinkedRegistry.register(executor)
