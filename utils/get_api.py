import os
import json
import logging
import requests
from utils.parser import LLMOutputParser
from utils.utils import convert_to_markdown, setup_logger
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
logger = setup_logger()


def get_hadith_data(query: str) -> str:
    """
    Retrieves Hadith data using the appropriate tools when a user inquires about Hadith.

    Args:
        query (str): User query.

    Returns:
        str: A markdown-formatted string containing the retrieved Hadith information.
    """
    llm = LLMOutputParser(type="hadith")
    output = llm.generate(query)
    logger.info(query)
    logger.info(f"LLM output: {output}")
    param_mapping = {
        "source": ("query_source", "source_weight"),
        "hadith_no": ("filter_by_hadith_no", "hadith_no_weight"),
        "chapter": ("query_chapter", "chapter_weight"),
        "text_ar": ("query_arabic", "text_ar_weight"),
        "text_en": ("query_text", "text_en_weight"),
    }

    query_params = {
        "filter_by_hadith_no": None,
        "hadith_no_weight": 0,
        "query_chapter": None,
        "chapter_weight": 0,
        "query_source": None,
        "source_weight": 0,
        "query_text": None,
        "query_arabic": None,
        "text_ar_weight": 0,
        "text_en_weight": 0,
        "limit": output.limit,
    }

    # Update parameter query based on output parser
    for attr, (query_param, weight_param) in param_mapping.items():
        if getattr(output, attr) is not None:
            query_params[query_param] = getattr(output, attr)
            query_params[weight_param] = 1

    logger.info(f"Query params: {query_params}")

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    }

    response = requests.post(os.getenv("API_HADITH"), headers=headers, data=json.dumps(query_params))

    if response.status_code == 200:
        data = response.json()
        return convert_to_markdown(data)
    else:
        logger.error(f"Request failed with status code {response.status_code}")
        raise Exception(f"Request failed with status code {response.status_code}")

def get_quran_data(query: str) -> str:
    """
    Retrieves Quran data using the appropriate tools when a user inquires about Quran.

    Args:
        query (str): User query.

    Returns:
        str: A markdown-formatted string containing the retrieved Hadith information.
    """
    llm = LLMOutputParser(type="quran")
    output = llm.generate(query)
    logger.info(query)
    logger.info(f"LLM output: {output}")
    param_mapping = {
        "surah_name": ("surah_name", "surah_name_weight"),
        "filter_by_surah": ("filter_by_surah", "surah_weight"),
        "filter_by_ayat": ("filter_by_ayat", "ayat_weight"),
        "surah_type": ("surah_type", "type_weight"),
        "query_arabic": ("query_arabic", "arabic_text_weight"),
        "query_text": ("query_text", "translate_weight"),
        "query_tafseer": ("query_tafseer", "tafseer_weight"),
    }

    query_params = {
        "surah_name": None,
        "surah_name_weight": 0,
        "filter_by_surah": None,
        "surah_weight": 0,
        "filter_by_ayat": None,
        "ayat_weight": 0,
        "surah_type": None,
        "type_weight": 0,
        "query_arabic": None,
        "arabic_text_weight": 0,
        "query_text": None,
        "translate_weight": 0,
        "query_tafseer": None,
        "tafseer_weight": 0,
        "limit": output.limit
    }

    # Update parameter query berdasarkan output parser
    for attr, (query_param, weight_param) in param_mapping.items():
        if getattr(output, attr) is not None:
            query_params[query_param] = getattr(output, attr)
            query_params[weight_param] = 1

    logger.info(f"Query params: {query_params}")
    
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    }

    response = requests.post(os.getenv("API_QURAN"), headers=headers, data=json.dumps(query_params))

    if response.status_code == 200:
        data = response.json()
        return convert_to_markdown(data)
    else:
        logger.error(f"Request failed with status code {response.status_code}")
        raise Exception(f"Request failed with status code {response.status_code}")