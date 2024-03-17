import streamlit as st
from audio_recorder_streamlit import audio_recorder
import whisper
import google.generativeai as genai

product_name = "MediSpeak"  # Product name variable

def translate_through_gemini(llm_model, text, target_language):
    # This function should use the Gemini API to translate the text to the target_language.
    response = llm_model.generate_content("You're a translator assistant. Your objective is to translate medical notes, into the given target language for the patient. Observe the following input text: \n\n\"\"\"\n"+text+"\n\"\"\"\n\nNow translate it into the language: "+target_language)
    return response

def deanonymize_through_gemini(llm_model, text):
    # This function should process the text to remove or alter personal identifiers for HIPAA compliance.
    response = llm_model.generate_content("You're a privacy-compliancy assistant. Your objective is to ensure the following medical notes, is deanonymized as per HIPAA. This means any instances of age, sex, name, identifiers, and address must be censored using placeholders or k-anonymity. Note with all the details: \n\n\"\"\"\n"+text+"\n\"\"\"\n\n")
    return response

def main():
    st.title(product_name)  # Adding a title to the app
    st.write("Welcome to MediSpeak, your AI-powered medical documentation assistant.")  # Short description
    genai.configure(api_key=st.secrets["gemini_key"])
    llm_model = genai.GenerativeModel('gemini-pro')

    model = whisper.load_model("base")
    audio_bytes = audio_recorder(pause_threshold=2.0)
    
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        with open("sample.wav", "wb") as audio_file:
            audio_file.write(audio_bytes)
            
        result = model.transcribe("sample.wav")
        direct_speech_to_text = result["text"]
        st.write(f'The text in video: \n{direct_speech_to_text}')
        
        st.info(direct_speech_to_text)  # Display the direct speech to text
        
        language = st.text_input("Enter a language of choice for translation:")  # Ask for language input
        translate_button = st.button('Translate')  # Translate button
        
        if translate_button and language:
            translated_text = translate_through_gemini(llm_model, direct_speech_to_text, language)
            st.markdown("## Translated Medical Note:")
            st.success(translated_text)  # Display the translated text
            
            deanonymized_text = deanonymize_through_gemini(llm_model, direct_speech_to_text)
            st.markdown("## Deanonymized Medical Note:")
            st.warning(deanonymized_text)  # Display the deanonymized text for hospital records

if __name__ == '__main__':
    main()