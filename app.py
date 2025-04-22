import streamlit as st
from inference import SpotifyEpisodeSummarizer  # Your class with .create_thumbnail_with_dalle
import os

# Instantiate summarizer
summarizer = SpotifyEpisodeSummarizer()

# Streamlit config
st.set_page_config(page_title="Spotify Podcast Summarizer", layout="centered")
st.title("Spotify Podcast Summarizer")
st.markdown("Convert a podcast into a text summary, audio narration, and an AI-generated thumbnail.")

# Inputs
url = st.text_input("Spotify Podcast Episode URL")
model_choice = st.radio("Choose LLM", ["OpenAI", "Claude", "Mistral"])

# Summarize button
if st.button("Summarize Podcast"):
    if url.strip() == "":
        st.warning("Please enter a Spotify episode URL.")
    else:
        try:
            episode_id = url.split("/")[-1]
            description = summarizer.get_episode_description(episode_id)

            # Generate summary using selected model
            if model_choice == "OpenAI":
                summary = summarizer.generate_summary_openai(description)
            elif model_choice == "Claude":
                summary = summarizer.generate_summary_claude(description)
            else:
                summary = summarizer.generate_summary_mistral(description)

            # Display summary
            st.subheader("Generated Summary")
            st.text_area(label="", value=summary, height=200)

            # Generate and play audio
            audio_path = summarizer.create_audio_summary(summary)
            st.subheader("Audio Summary")
            st.audio(audio_path, format="audio/mp3")

            with open(audio_path, "rb") as f:
                st.download_button(
                    label="Download Audio",
                    data=f,
                    file_name="summary_audio.mp3",
                    mime="audio/mp3"
                )

            # 🔥 Generate thumbnail with DALL·E
            st.subheader("AI-Generated Thumbnail")
            with st.spinner("Generating thumbnail.."):
                thumbnail_path = summarizer.create_thumbnail_with_dalle(summary)

            st.image(thumbnail_path, caption="LLM-Generated Thumbnail", use_column_width=True)

            with open(thumbnail_path, "rb") as f:
                st.download_button(
                    label="Download Thumbnail",
                    data=f,
                    file_name="summary_thumbnail.png",
                    mime="image/png"
                )

        except Exception as e:
            st.error(f"Error: {e}")
