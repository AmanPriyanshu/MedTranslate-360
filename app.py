import streamlit as st
from audio_recorder_streamlit import audio_recorder
import whisper
import google.generativeai as genai

product_name = "MediSpeak"  # Product name variable

def translate_through_gemini(text, target_language):
    # Placeholder for the actual translation function.
    # This function should use the Gemini API to translate the text to the target_language.
    # Return the translated text.
    return f"Translated text in {target_language}."

def deanonymize_through_gemini(text):
    # Placeholder for the deanonymization function.
    # This function should process the text to remove or alter personal identifiers for HIPAA compliance.
    # Return the deanonymized text.
    return "Deanonymized text for hospital records."

def main():
    st.title(product_name)  # Adding a title to the app
    st.write("Welcome to MediSpeak, your AI-powered medical documentation assistant.")  # Short description
    genai.configure(api_key=st.secrets["gemini_key"])

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
            translated_text = translate_through_gemini(direct_speech_to_text, language)
            st.success(translated_text)  # Display the translated text
            
            deanonymized_text = deanonymize_through_gemini(direct_speech_to_text)
            st.warning(deanonymized_text)  # Display the deanonymized text for hospital records

if __name__ == '__main__':
    main()