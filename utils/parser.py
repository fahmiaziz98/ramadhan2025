import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from utils.schema import HadithParser, QuranParser, Router
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class LLMOutputParser:
    """Generates Hadith details from user queries using the Google Generative AI model."""

    def __init__(self, model: str = "gemini-1.5-flash", type: str = "hadith"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model = model
        self.gemini = ChatGoogleGenerativeAI(
            api_key=self.api_key, 
            temperature=0, 
            model=model
        )
        self.groq = ChatGroq(
                model="llama3-8b-8192",
                api_key=os.getenv("GROQ_API_KEY"),
                temperature=0,
                verbose=True,
            )
        if type == "hadith":
            self.prompt = ChatPromptTemplate.from_messages(
                [("system", self._system_message_hadith()), ("human", "{input}")]
            )
            self.llm_parser = self.prompt | self.gemini.with_structured_output(HadithParser)
        elif type == "quran":
            self.prompt = ChatPromptTemplate.from_messages(
                [("system", self._system_message_quran()), ("human", "{input}")]
            )
            
            self.llm_parser = self.prompt | self.groq.with_structured_output(QuranParser)
        else:
            self.prompt = ChatPromptTemplate.from_messages(
                [("system", self._system_message_router()), ("human", "{input}")]
            )
            self.llm_parser = self.prompt | self.gemini.with_structured_output(Router)

    def _system_message_router(self) -> str:
        """Returns the system message for the prompt to determine whether the query is about the Quran or Hadith."""
        return (
            "You are an intelligent assistant capable of accurately identifying whether a user query is related to the quran or hadith. "
            "Based on the query, route it accordingly and extract relevant details:\n\n"

            "**quran Route:**\n"
            "- If user ask surah, ayah, translation and tafseer, assign it to 'quran'.\n"

            "**hadith Route:**\n"
            "- If user ask hadith, source, number, chapter, and more assign it to 'hadith'.\n"

        )

    
    def _system_message_hadith(self) -> str:
        """Returns the system message for the prompt."""
        return (
            "You are an assistant designed to extract Hadith details from user queries accurately. "
            "Follow these rules strictly:\n"
            "- If a Hadith number is mentioned, assign it to 'hadith_no'.\n"
            "- If a Hadith source is mentioned, assign it to 'source'.\n"
            "- If a chapter or topic is mentioned, assign it to 'chapter'.\n"
            "- If the user provides Hadith content in Arabic, assign it to 'text_ar'.\n"
            "- If the user provides Hadith content in English/Indonesia, assign it to 'text_en'.\n"
            "- Default to limit = 1 unless specified by the user.\n"
            "- Never guess unknown fields; set them to None."
        )
    
    def _system_message_quran(self) -> str:
        """Returns the system message for the prompt."""
        return (
            "System"
            "You are an Islamic scholar assistant, designed to analyze user queries about the Quran accurately. "
            "Extract relevant parameters to query a Quran database and return the results in JSON format.\n"
            "Follow these rules strictly:\n"
            "- If a Surah name is mentioned, assign it to 'surah_name'.\n"
            "- If a Surah number is mentioned, assign it to 'filter_by_surah'.\n"
            "- If an Ayah (verse) number is mentioned, assign it to 'filter_by_ayat'.\n"
            "- If the Surah type (Makkah/Madinah) is explicitly mentioned, assign it to 'surah_type'.\n"
            "- If the user provides Arabic text to search, assign it to 'query_arabic'.\n"
            "- If the user asks about meaning/translation, assign the extracted phrase to 'query_text'.\n"
            "- If the user asks about tafseer (explanation), assign the extracted phrase to 'query_tafseer'.\n"
            "- Default to 'limit' = 5 unless specified by the user.\n"
            "- Never guess unknown fields; set them to None.\n"
            "\n"
            "### Examples:\n"
            "- 'Surah Al-Ikhlas, verse 1' → 'surah_name': 'Al-Ikhlas', 'filter_by_ayat': 1\n"
            "- 'Give me the translation of *Surah 2, Ayah 255*' → 'filter_by_surah': 2, 'filter_by_ayat': 255, '\n"
            "- 'Show tafseer for *Al-Fatiha*' → 'surah_name': 'Al-Fatiha', '\n"
            "- 'Find the verse containing *اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ*' → 'query_arabic': 'اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ'\n"
            "- 'Tell me about Surah 114' → 'filter_by_surah': 114\n"
            "- 'Translate 2:45' → 'filter_by_surah': 2, 'filter_by_ayat': 45\n"
        )



    def generate(self, prompt: str) -> dict:
        """Generates Hadith details from a user query."""
        return self.llm_parser.invoke(prompt)
