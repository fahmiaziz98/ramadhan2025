from superlinked_app import index

from superlinked import framework as sl
from superlinked_app import index

# Creating Query
base_query = (
    sl.Query(
        index.hadist_index,
        weights={
            index.hadith_no_space: sl.Param("hadith_no_weight"),
            index.chapter_space: sl.Param("chapter_weight"),
            index.source_space: sl.Param("source_weight"),
            index.text_en_space: sl.Param("text_en_weight"),
            index.text_ar_space: sl.Param("text_ar_weight"),
        }
    )
    .find(index.hadist)
    .similar(index.chapter_space, param=sl.Param("query_chapter"))
    .similar(index.source_space, param=sl.Param("query_source"))
    .similar(index.text_ar_space, param=sl.Param("query_arabic"))
    .similar(index.text_en_space, param=sl.Param("query_text"))
    .filter(
        index.hadist.hadith_no == sl.Param("filter_by_hadith_no")
    )
    .select_all()
    .limit(sl.Param("limit"))
)