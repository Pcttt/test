import groq
import streamlit as st
import pandas as pd

# Add custom styling
st.markdown("""
    <style>
    /* Light mode styling */
        body {
            background-color: #FFF8F0; /* Pastel peach background */
            color: #4D4D4D; /* Neutral dark text color for visibility */
        }
        .stApp {
            background-color: #FFF8F0;
        }
        h1 {
            color: #FFB3BA; /* Pastel pink title color */
            font-family: 'Arial', sans-serif;
            text-align: center;
        }
        .stButton button {
            background-color: #FFDFD3; /* Pastel coral buttons */
            color: #D47F6A; /* Soft peach text */
            font-size: 16px;
            border-radius: 12px;
            border: 2px solid #FFB3BA;
        }
        .stButton button:hover {
            background-color: #FFD1C1; /* Slightly darker pastel coral on hover */
        }
        .stTextInput textarea {
            background-color: #FEECEB; /* Pastel pink input field */
            color: #8B5E5E; /* Soft brown text */
            font-size: 14px;
            border: 2px solid #FFB3BA;
            border-radius: 10px;
        }
        .stDataFrame {
            background-color: #E6F7F1; /* Pastel green for DataFrame */
            border: 2px solid #B2E7C8; /* Green border */
            border-radius: 10px;
        }

    /* Dark mode styling */
     @media (prefers-color-scheme: dark) {
        body {
            background-color: #2E2E2E; /* Dark gray background */
            color: #F5F5F5; /* Light text color */
        }
        .stApp {
            background-color: #2E2E2E;
        }
        h1 {
            color: #FFA6C9; /* Softer pastel pink for dark mode */
        }
        .stButton button {
            background-color: #5C4C51; /* Muted pink for dark mode buttons */
            color: #FFD1E8; /* Light pastel text */
            border: 2px solid #FFA6C9;
        }
        .stButton button:hover {
            background-color: #7A5C6A; /* Darker muted pink on hover */
        }
        .stTextInput textarea {
            background-color: #4B4B4B; /* Dark gray input field */
            color: #FFD1E8; /* Light pastel text */
            border: 2px solid #FFA6C9;
        }
        .stDataFrame {
            background-color: #3A4B3C; /* Dark green for DataFrame */
            border: 2px solid #A5C4A7; /* Muted green border */
        }
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for API key input
groq_api_key = st.sidebar.text_input("🔑 Enter your Groq API Key:", type="password")
if groq_api_key:
    groq.api_key = groq_api_key

# Function to generate Kanbun
def generate_kanbun(prompt):
    client = Groq()
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a skilled Kanbun (classical Chinese) poet."},
            {"role": "user", "content": prompt}
        ]
    )
    kanbun = response['choices'][0]['message']['content'].strip()
    return kanbun

# Function to translate Kanbun to a selected language
def translate_kanbun(kanbun, target_language):
    client = Groq()
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": f"You are an expert in translating Kanbun (classical Chinese) into {target_language}."},
            {"role": "user", "content": f"Translate this Kanbun into {target_language}: {kanbun}"}
        ]
    )
    translation = response['choices'][0]['message']['content'].strip()
    return translation

# Function to extract vocabulary from Kanbun and translate to a selected language
def extract_vocabulary(kanbun, target_language):
   client = Groq()
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": f"You are an expert in analyzing Kanbun (Chinese texts with Japanese reading order) and providing translations with part-of-speech tagging, JLPT levels, and pronunciation in {target_language}."},
            {"role": "user", "content": f"Extract important vocabulary from the following Kanbun text (a Chinese poem with Japanese reading order) and provide the {target_language} translation, romaji (pronunciation), example sentences, part-of-speech tags (e.g., noun, verb, adjective, etc.), and JLPT levels sorted from N5 to N1:\n{kanbun}"}
        ]
    )
    vocabulary = response['choices'][0]['message']['content'].strip()
    return vocabulary

# Main application function
def main():
    st.title("🌸 Learn Japanese with Kanbun Poetry 🌸")

    # Brief explanation about Kanbun
    st.markdown("""
    **What is Kanbun?**  
    Kanbun (漢文) refers to classical Chinese literature, widely used historically in Japan. It is known for its poetic elegance and scholarly depth. This application generates Kanbun poetry based on a passage or sentence, translates it into a selected language, and provides key vocabulary for further analysis!
    """)

    # Pre-filled starter text for the input box
    starter_text = "The cherry blossoms bloom as the sun rises, painting the sky with hues of pink and gold."
    sentence = st.text_area("🌻 Enter a sentence or passage for the Kanbun poem (e.g., a short story or a descriptive paragraph):", value=starter_text)

    # Language selection for translation
    languages = [
        "English", "Thai", "Korean", "French", "Spanish", "German", "Italian", "Portuguese", "Chinese (Simplified)",
        "Arabic", "Russian", "Hindi", "Bengali", "Vietnamese", "Turkish", "Indonesian", "Malay", "Swahili", "Dutch", "Greek"
    ]
    target_language = st.selectbox("🌐 Select the language for translation:", languages)

    if st.button("✨ Generate Kanbun ✨"):
        if sentence:
            prompt = f"Create a Kanbun (classical Chinese) poem based on the following sentence or passage: {sentence}"
            kanbun = generate_kanbun(prompt)

            # Translate Kanbun to the selected language
            translation = translate_kanbun(kanbun, target_language)

            # Extract vocabulary and translate to the selected language
            vocabulary = extract_vocabulary(kanbun, target_language)

            st.subheader("🌈 Generated Kanbun Poem:")
            st.write(kanbun)

            st.subheader(f"🌐 Translation to {target_language}:")
            st.write(translation)

            st.subheader(f"📚 Key Vocabulary in {target_language} (with JLPT levels and examples):")
            st.write(vocabulary)

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

# Download buttons for CSV and Excel
            st.download_button(
                label="💾 Download as CSV",
                data=df.to_csv(index=False).encode('utf-8'),
                file_name="kanbun_data.csv",
                mime="text/csv"
            )

            st.download_button(
                label="📄 Download as Excel",
                data=df.to_excel(index=False, engine='openpyxl').encode('utf-8'),
                file_name="kanbun_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("⚠️ Please enter a sentence or passage to generate a poem ⚠️")

if __name__ == "__main__":
    main()
