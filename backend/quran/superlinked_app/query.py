from superlinked import framework as sl
from superlinked_app import index


# Creating Query
base_query = (
    sl.Query(
        index.quran_index,
        weights={
            index.surah_space: sl.Param("surah_weight"),  # int
            index.ayat_space: sl.Param("ayat_weight"),    #int
            index.surah_name_space: sl.Param("surah_name_weight"),
            index.surah_type_space: sl.Param("type_weight"),
            index.arabic_text_space: sl.Param("arabic_text_weight"),
            index.translate_en_space: sl.Param("translate_weight"),
            index.tafseer_space: sl.Param("tafseer_weight"),
        }
    )
    .find(index.quran)
    .similar(index.surah_name_space, param=sl.Param("surah_name"))
    .similar(index.surah_type_space, param=sl.Param("surah_type"))
    .similar(index.arabic_text_space, param=sl.Param("query_arabic"))
    .similar(index.translate_en_space, param=sl.Param("query_text"))
    .similar(index.tafseer_space, param=sl.Param("query_tafseer"))
    .filter(
        index.quran.Surah == sl.Param("filter_by_surah")
    )
    .filter(
        index.quran.Ayat == sl.Param("filter_by_ayat")
    )
    .select_all()
    .limit(sl.Param("limit"))
)