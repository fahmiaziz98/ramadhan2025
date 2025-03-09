from typing import Optional
from pydantic import BaseModel, Field

class HadithParser(BaseModel):
    """
    Parser for extracting Hadith details such as source, number, chapter, and text.
    Supports queries referencing English or Arabic hadith content and source.
    """

    source: Optional[str] = Field(
        default=None,
        description="The source of the Hadith (e.g., 'Sahih Bukhari', 'Sahih Muslim')."
    )
    hadith_no: Optional[int] = Field(
        default=None,
        description="The Hadith number as a string (e.g., 88, 2, 3)."
    )
    chapter: Optional[str] = Field(
        default=None,
        description="The chapter or topic of the Hadith (e.g., 'Knowledge', 'Prayer')."
    )
    text_ar: Optional[str] = Field(
        default=None,
        description="If the user provides the Arabic language of the Hadith."
    )
    text_en: Optional[str] = Field(
        default=None,
        description="If the user requests or provides an English/Indonesian translation of the Hadith. "
    )
    limit: int = Field(
        default=1,
        description="The number of Hadith results to return."
    )

class QuranParser(BaseModel):
    """
    Parser for extracting Surah, Ayah, subject(meaning)/Translate/Tafseer
    from a Quran-related query.
    """

    # Surah-related parameters
    surah_name: Optional[str] = Field(
        default=None,
        description="The name of the Surah in the Quran (e.g., 'Al-Baqarah', 'Al-An'am')."
    )

    filter_by_surah: Optional[int] = Field(
        default=None,
        description="Surah number"
    )

    filter_by_ayat: Optional[int] = Field(
        default=None,
        description="Ayah or verse number, if the user mentions"
    )

    surah_type: Optional[str] = Field(
        default=None,
        description="Type of Surah (e.g., 'Makkah', 'Madinah')."
    )

    # Content-related parameters
    query_arabic: Optional[str] = Field(
        default=None,
        description="Arabic text to search for."
    )

    query_text: Optional[str] = Field(
        default=None,
        description="Subject (meaning)/Translation text to search for."
    )

    query_tafseer: Optional[str] = Field(
        default=None,
        description="Tafseer (explanation) text to search for."
    )

    # Result limitation
    limit: int = Field(
        default=1,
        description="The number of results to return."
    )

class Router(BaseModel):
    """
    Router for determining which parser to use.
    """
    router: str = Field(
        default=None,
        description="The router to use, either 'quran' or 'hadith'."
    )