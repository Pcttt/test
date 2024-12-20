from groq import Groq
import streamlit as st
import pandas as pd
import openpyxl as xl
import io 
from io import BytesIO

generate_button = st.markdown(
    """
    <style>
    .stButton button {
        background-color: transparent; /* Transparent background */
        color: #D47F6A; /* Soft peach text */
        font-size: 16px;
        border-radius: 12px;
        border: 2px solid #FFB3BA; /* Light pastel border */ 
        cursor: pointer; /* Pointer cursor for better UX */
    }
    .stButton button:hover {
        background-color: #FFD1C1; /* Slightly darker pastel coral on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Sidebar for API key input
groq_api_key = st.sidebar.text_input("🔑 Enter your Groq API Key:", type="password")
client = None
if groq_api_key:
    client = Groq(api_key=groq_api_key)  # Assuming this is how the Groq client is initialized.

# Function to generate Kanbun
def generate_kanbun(prompt):
    completion = client.chat.completions.create(
        model="llama3-70b-8192",  # Adjust model name if necessary
         messages=[
            {"role": "system", "content": "You are a skilled Kanbun (Japanese method of reading, annotating and translating lietrary Chinese) poet."},
            {"role": "user", "content": prompt}
        ]
    )
    kanbun = completion.choices[0].message.content.strip()
    return kanbun

# Function to translate Kanbun to a selected language
def translate_kanbun(kanbun, target_language):
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": f"You are an expert in translating Kanbun (Japanese method of reading, annotating and translating lietrary Chinese) into {target_language}."},
            {"role": "user", "content": f"Translate this Kanbun into {target_language}: {kanbun}"}
        ]
    )
    translation = completion.choices[0].message.content.strip()
    return translation

# Function to extract vocabulary from Kanbun and translate to a selected language
def extract_vocabulary(kanbun, target_language):
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": f"You are an expert in analyzing Kanbun (Japanese method of reading, annotating and translating lietrary Chinese) and providing translations with part-of-speech tagging, JLPT levels, and pronunciation in {target_language}."},
            {"role": "user", "content": f"Extract important vocabulary from the following Kanbun text (Japanese method of reading, annotating and translating lietrary Chinese) and provide the {target_language} translation, romaji (pronunciation), example sentences, part-of-speech tags (e.g., noun, verb, adjective, etc.), and JLPT levels sorted from N5 to N1:\n{kanbun}"}
        ]
    )
    vocabulary = completion.choices[0].message.content.strip()
    return vocabulary

# Main application function
def main():
    st.markdown(
    """
    <h1 style="text-align: center; font-size: 2.5em;">
        🌸 Learn Japanese with <span style="border-bottom: 3px solid #FFB3BA;">Kanbun Poetry</span> 🌸
    </h1>
    """,
    unsafe_allow_html=True
    )

    # Brief explanation about Kanbun
    st.markdown("""
    **What is Kanbun?**  
    Kanbun (漢文) refers to classical Chinese literature, widely used historically in Japan. It is known for its poetic elegance and scholarly depth. This application generates Kanbun poetry based on a passage or sentence, translates it into a selected language, and provides key vocabulary for further analysis!
    """)

    st.markdown("""
    **📜 Examples of Kanbun:** 
    """)

    col1, col2 = st.columns([1, 1])  # Two columns with equal width

    with col1:
        st.image("https://i.pinimg.com/736x/cf/8a/dd/cf8add09fa8261f23fcae8347a181fe5.jpg", width=350, use_column_width=False)
    
    # Second image (on the right)
    with col2:
        st.image("https://media.eboard.jp/media/quiz_images/kanbun1_01_20220303.jpg", width=350)

    
    # Pre-filled starter text for the input box
    starter_text = "The cherry blossoms bloom as the sun rises, painting the sky with hues of pink and gold."
    sentence = st.text_area("**🌻 Enter a sentence or passage for the Kanbun poem (e.g., a short story or a descriptive paragraph):**", value=starter_text)

    # Language selection for translation
    languages = [
        "English", "Thai", "Korean", "French", "Spanish", "German", "Italian", "Portuguese", "Chinese (Simplified)",
        "Arabic", "Russian", "Hindi", "Bengali", "Vietnamese", "Turkish", "Indonesian", "Malay", "Swahili", "Dutch", "Greek"
    ]
    target_language = st.selectbox("**🌐 Select the language for translation:**", languages)

    if st.button("✨ Generate Kanbun ✨"):
        if sentence:
            prompt = f"Create a Kanbun (Japanese method of reading, annotating and translating lietrary Chinese) poem based on the following sentence or passage: {sentence}"
            kanbun = generate_kanbun(prompt)

            # Translate Kanbun to the selected language
            translation = translate_kanbun(kanbun, target_language)

            # Extract vocabulary and translate to the selected language
            vocabulary = extract_vocabulary(kanbun, target_language)

            st.markdown("<hr style='border: 1px solid #D3D3D3; margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

            st.subheader("🎋 Generated Kanbun Poem:")
            st.write(kanbun)

            st.markdown("<hr style='border: 1px solid #D3D3D3; margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

            st.subheader(f"🌐 Translation to {target_language}:")
            st.write(translation)

            st.markdown("<hr style='border: 1px solid #D3D3D3; margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

            st.subheader(f"📚 Key Vocabulary in {target_language} (with JLPT levels and examples):")
            st.write(vocabulary)

            st.markdown("<hr style='border: 1px solid #D3D3D3; margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)

            data = {
                "Input Sentence/Passage": [sentence],
                "Kanbun Poem": [kanbun],
                f"Translation to {target_language}": [translation],
                f"Key Vocabulary in {target_language} (with JLPT levels and examples)": [vocabulary]
            }
            df = pd.DataFrame(data)

            # Display DataFrame
            st.subheader("📊 Poem Details in Table Format:")
            st.dataframe(df)

            excel = BytesIO()

            with pd.ExcelWriter(excel, engine='openpyxl') as writer:
                df.to_excel(writer, index = False, sheet_name = "Kanbun")
            excel.seek(0)

            # Download buttons for CSV and Excel
            st.download_button(
                label="📏 Download as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="kanbun_data.csv",
                mime="text/csv"
            )

            st.download_button(
                label="📄 Download as Excel",
                data= excel,
                file_name="kanbun_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key = "kanbun_data_download"
            )
        else:
            st.warning("⚠️ Please enter a sentence or passage to generate a poem ⚠️")

            
        # Add a footer with a gray line, message, and links
    st.markdown(
        """
        <hr style="border: 1px solid #D3D3D3; margin-top: 50px;">
        <p style="text-align: center; font-size: 0.9em; color: #555;">
            Made with 💖 | 
            Check out & ⭐️ <a href="https://github.com/Pcttt/test" target="_blank" style="color: #1E90FF; text-decoration: none;">GitHub Repo</a>
        </p>
        <p style="text-align: center; font-size: 0.8em; color: #555;">
            Powered by 🔋 Streamlit & OpenAI
        </p>
        """,
        unsafe_allow_html=True
    )



if __name__ == "__main__":
    if client:
        main()
    else:
        st.error("Please enter a valid Groq API Key.")
