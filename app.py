import streamlit as st
from utils.get_api import get_hadith_data, get_quran_data
from utils.parser import LLMOutputParser


st.set_page_config(page_title="Quran Hadith Search Engine", layout="wide")
st.title("Quran Hadith Search Engine")
st.sidebar.markdown("""
# Description
This application serves as a powerful search engine for the Quran and Hadith, enabling users to quickly find relevant verses and narrations based on their queries.
# Example Query
- I am looking for hadiths in the field of knowledge, include 5 hadiths from Sahih Bukhari
- Can you find hadith number 88 from Sahih Bukhari?
- What is the number and who is the narrator of this hadith?
حدثني محمد بن يوسف، قال حدثنا أبو مسهر، قال حدثني محمد بن حرب، حدثني الزبيدي، عن الزهري، عن محمود بن الربيع، قال عقلت من النبي صلى الله عليه وسلم مجة مجها في وجهي وأنا ابن خمس سنين من دلو
- Tafseer 2:45
- What is the meaning of verse 7 in Surah Al-Kahf?
- Show the Arabic text of Surah Al-Ikhlas Ayah 2
- Translate verse 5 from Surah Al-Mulk into Indonesian
- Give me the Arabic text for Ayah 255 from Surah Al-Baqarah

""")


router = LLMOutputParser(type="router")

def generate_response(input_text):
    output = router.generate(input_text)
    if output.router == "hadith":
        st.info(f"Router output: {output}")
        response = get_hadith_data(input_text)  # Mendapatkan string markdown
    else:
        st.info(f"Router output: {output}")
        response = get_quran_data(input_text)
    entries = response.strip().split("\n\n" + "-" * 50 + "\n\n")  # Pisahkan berdasarkan separator

    if not entries or response.strip() == "":
        st.warning("No results found. Please refine your query.")
        return


    col1, col2 = st.columns(2) 

    for i, entry in enumerate(entries):
        with col1 if i % 2 == 0 else col2:
            hadith_lines = entry.strip().split("\n\n") 
            formatted_entry = ""
            metadata_section = ""

            for line in hadith_lines:
                if line.startswith("**Metadata:**"):  
                    metadata_section = line  
                else:
                    formatted_entry += line + "\n\n"

            st.markdown(formatted_entry)  
            if metadata_section:
                st.caption(metadata_section)  
            st.write(20*"---") 
st.write("Enter your query below to search for Hadith or Quranic verses.")

with st.container():
    with st.form("my_form"):
        text = st.text_area("Enter text:", "", height=150) 
        submitted = st.form_submit_button("Submit")

        if submitted:
            generate_response(text)





