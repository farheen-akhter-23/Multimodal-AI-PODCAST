# 🎿 Multimodal AI Podcast Summarizer

Transform any **Spotify podcast episode** into:
- ✅ A **concise text summary**
- ✅ A **natural audio narration**
- ✅ A **custom AI-generated thumbnail**

This application showcases the power of **multimodal AI**, integrating LLMs, TTS, and text-to-image models into one seamless Streamlit experience.

---

## 🔍 What It Does

> Paste a Spotify podcast URL → Choose your preferred LLM → Get a summarized episode in **text, voice, and image**.

| Modality | Output                           | Tech Used               |
|----------|----------------------------------|--------------------------|
| Text     | Podcast summary                  | GPT-3.5 Turbo / Claude / Mistral |
| Audio    | Voice narration of the summary   | gTTS (Google Text-to-Speech)     |
| Image    | Podcast thumbnail                | OpenAI DALL·E 3                |

---

## 💠 Tech Stack

- `Streamlit` – frontend UI
- `OpenAI GPT-3.5 Turbo` – LLM for summaries
- `Anthropic Claude 3` & `Mistral AI` – alternative LLMs
- `OpenAI DALL·E 3` – generates episode thumbnails
- `gTTS` – converts summary into speech
- `Spotify Web API` – fetches podcast episode metadata

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/farheen-akhter-23/Multimodal-AI-Mood-Tracker.git
cd Multimodal-AI-Mood-Tracker
```

### 2. Create `.env` and add API keys

```env
openai_api_key=your_openai_key
spotify_client_id=your_spotify_client_id
spotify_client_secret=your_spotify_client_secret
anthropic_api_key=your_anthropic_key
mistral_api_key=your_mistral_key
```

> ⚠️ Never commit your `.env` file. It’s included in `.gitignore`.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> Includes: `streamlit`, `openai`, `anthropic`, `gtts`, `requests`, `python-dotenv`, `mistralai`, `Pillow`

### 4. Run the App

```bash
streamlit run app.py
```

---

## 🧠 Example Use Case

Paste a Spotify URL like:

```
https://open.spotify.com/episode/3LxxLtBkZdfxk5Gg9N3R0z
```

Select **GPT-3.5 Turbo**, and watch the app:
- Summarize the podcast
- Narrate the summary as speech
- Generate a visual thumbnail

---

## 🖼 Demo Preview

https://github.com/user-attachments/assets/fc72529f-4fea-4d44-8dca-1a9a4a25b1fd

---

## 📁 Project Structure

```
👃 app.py                        # Streamlit frontend
👃 internvl_infer.py            # Core logic class
👃 .env                         # Secret API keys (ignored)
👃 requirements.txt             # All dependencies
👃 README.md
```

---

## 🤝 Contributing

Pull requests are welcome! If you’d like to add new features (like Whisper for audio input, or Hugging Face image models), please create a new issue or fork the repo and submit a PR.

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

Built with ❤️ by [Farheen Akhter](https://github.com/farheen-akhter-23), showcasing the potential of LLMs + multimodal AI for intelligent podcast summarization and interaction.

