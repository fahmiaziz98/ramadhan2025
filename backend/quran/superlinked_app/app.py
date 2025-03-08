from superlinked import framework as sl

from superlinked_app import index, query
from superlinked_app.config import settings

# vectore db
vector_database = vector_database = sl.InMemoryVectorDatabase()

# data parser
data_parser = sl.DataFrameParser(
    schema=index.quran,
    mapping={
        index.quran.id: 'id'
    }
)

# data loader
data_loader_config = sl.DataLoaderConfig(
    "https://raw.githubusercontent.com/fahmiaziz98/ramadhan2025/refs/heads/main/backend/quran/data/data_quran.jsonl",
    sl.DataFormat.JSON,
    pandas_read_kwargs={"lines": True, "chunksize": 100},
)

source = sl.RestSource(index.quran)
data_source = sl.DataLoaderSource(
    index.quran,
    data_loader_config,
    data_parser,
)

executor: sl.RestExecutor = sl.RestExecutor(
    sources=[source, data_source],
    indices=[index.quran_index],
    queries=[sl.RestQuery(sl.RestDescriptor("query"), query.base_query)],
    vector_database=vector_database
)

sl.SuperlinkedRegistry.register(executor)