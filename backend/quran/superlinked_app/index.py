from superlinked import framework as sl
from superlinked_app.config import settings


class QuranSchema(sl.Schema):
    """Schema for quran"""
    id: sl.IdField
    Surah: sl.Integer
    Ayat: sl.Integer
    Total_ayah: sl.Integer
    Number_rukus: sl.Integer
    Surah_arabic_name: sl.String 
    Surah_name: sl.String
    Surah_type: sl.String

    Arabic_text: sl.String   # AR Embedd
    Translation_ID: sl.String
    Translation_EN: sl.String
    Tafseer: sl.String

quran = QuranSchema()

# Integer Space
surah_space = sl.NumberSpace(
    number=quran.Surah, min_value=1, max_value=114, mode=sl.Mode.MAXIMUM
)

ayat_space = sl.NumberSpace(
    number=quran.Ayat, min_value=1, max_value=286, mode=sl.Mode.MAXIMUM
)

arabic_text_space = sl.TextSimilaritySpace(
    text=quran.Arabic_text, model=settings.ARABIC_EMBEDDING_MODEL
)

surah_name_space = sl.TextSimilaritySpace(
    text=quran.Surah_name, model=settings.EMBEDDING_MODEL
)
surah_type_space = sl.TextSimilaritySpace(
    text=quran.Surah_type, model=settings.EMBEDDING_MODEL
)

translate_en_space = sl.TextSimilaritySpace(
    text=quran.Translation_EN, model=settings.EMBEDDING_MODEL
)
tafseer_space = sl.TextSimilaritySpace(
    text=quran.Tafseer, model=settings.EMBEDDING_MODEL
)

# Creating Index
quran_index = sl.Index(
    spaces=[
        surah_space,
        ayat_space,
        arabic_text_space,
        surah_name_space,
        surah_type_space,
        translate_en_space,
        tafseer_space,
    ],
    fields=[quran.Surah, quran.Ayat]
)