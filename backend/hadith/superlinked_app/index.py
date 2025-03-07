# Schema
from superlinked import framework as sl
from superlinked_app.config import settings


class HadistSchema(sl.Schema):
    """Schema for hadist"""
    id: sl.IdField
    chapter_no: sl.Integer
    hadith_no: sl.Integer
    source: sl.String
    chapter: sl.String  # pake embedding arab-en
    text_ar: sl.String  # pake embedding arab-en
    text_en: sl.String

hadist = HadistSchema()

# IntegerSpace
chapter_no = sl.NumberSpace(
    number=hadist.chapter_no, min_value=0, max_value=98, mode=sl.Mode.MAXIMUM
)
hadith_no_space = sl.NumberSpace(
    number=hadist.hadith_no, min_value=-1, max_value=7784, mode=sl.Mode.MAXIMUM
)

# StringSpace
text_en_space = sl.TextSimilaritySpace(
    text=hadist.text_en, model=settings.EMBEDDING_MODEL
)
source_space = sl.TextSimilaritySpace(
    text=hadist.source, model=settings.EMBEDDING_MODEL
)

# Arabic - En Space
chapter_space = sl.TextSimilaritySpace(
    text=hadist.chapter, model=settings.ARABIC_EMBEDDING_MODEL
)
text_ar_space = sl.TextSimilaritySpace(
    text=hadist.text_ar, model=settings.ARABIC_EMBEDDING_MODEL
)

# Creating Index
hadist_index = sl.Index(
    spaces=[
        source_space,
        hadith_no_space,
        chapter_space,
        text_ar_space,
        text_en_space,
    ],
    fields=[hadist.source, hadist.hadith_no, hadist.text_en]
)