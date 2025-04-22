import requests
import os
import anthropic 
from openai import OpenAI
from mistralai.client import MistralClient
from mistralai import Mistral, UserMessage
from gtts import gTTS
from dotenv import load_dotenv

load_dotenv() 

class SpotifyEpisodeSummarizer:
    def __init__(self):
        # Initialize with your API keys
        self.spotify_client_id = os.getenv('spotify_client_id')
        self.spotify_client_secret = os.getenv('spotify_client_secret')
        self.openai_api_key = os.getenv('openai_api_key')
        self.anthropic_api_key = os.getenv('anthropic_api_key')
        self.mistral_api_key = os.getenv('mistral_api_key')
        self.spotify_token = None
        self.claude_client = anthropic.Anthropic(api_key=os.getenv('anthropic_api_key'))

    def get_spotify_token(self):
        """Get Spotify access token"""
        auth_url = "https://accounts.spotify.com/api/token"
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': os.getenv('spotify_client_id'),
            'client_secret': os.getenv('spotify_client_secret')
        })
        self.spotify_token = auth_response.json()['access_token']

    def get_episode_description(self, episode_id, market="US"):
        """Fetch episode description from Spotify API"""
        if not self.spotify_token:
            self.get_spotify_token()

        endpoint = f"https://api.spotify.com/v1/episodes/{episode_id}"
        headers = {
            "Authorization": f"Bearer {self.spotify_token}",
            "Content-Type": "application/json"
        }
        params = {"market": market}
        
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()['description']
        else:
            raise Exception(f"Error fetching episode: {response.status_code}")

    def generate_summary_openai(self, description):
        """Generate summary using ChatGPT"""
        client = OpenAI(api_key=os.getenv('openai_api_key'))
        
        prompt = f"""Create a concise and engaging summary of this podcast episode:
        {description}
        
        End the summary with: "For the full episode, listen on Spotify and click the link here."
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    
    def generate_summary_claude(self, description):
        """Generate summary using Claude"""
        message = self.claude_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": f"Create a concise and engaging summary of this podcast episode: {description}\n\nEnd the summary with: 'For the full episode, listen on Spotify and click the link here.'"
                }
            ]
        )
        return message.content[0].text
    
    def generate_summary_mistral(self, description):
        """Generate summary using Mistral AI"""
        try:
            client = Mistral(api_key=os.getenv('mistral_api_key'))
            
            messages = [
                {
                    "role": "user",
                    "content": f"Create a concise and engaging summary of this podcast episode: {description}\n\nEnd the summary with: 'For the full episode, listen on Spotify and click the link here.'"
                }
            ]
            
            chat_response = client.chat.complete(
                model="mistral-large-latest",
                messages=messages
            )
            
            return chat_response.choices[0].message.content
        except Exception as e:
            print(f"Mistral AI API error: {str(e)}")
            raise

    def create_audio_summary(self, text, output_file="summary.mp3"):
        """Convert summary to audio using gTTS"""
        tts = gTTS(text=text, lang='en')
        tts.save(output_file)
        return output_file
    
    def create_thumbnail_with_dalle(self, summary_text, output_file="summary_thumbnail.png"):
        """Generate a thumbnail image using OpenAI's DALL·E from the summary text"""
        client = OpenAI(api_key= os.getenv('openai_key_image'))

        # Convert summary into an image prompt
        prompt = f"Create a minimal podcast thumbnail based on this summary: {summary_text}"

        try:
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )

            image_url = response.data[0].url

            # Download and save the image
            image_data = requests.get(image_url).content
            with open(output_file, "wb") as f:
                f.write(image_data)

            return output_file
        except Exception as e:
            print(f"DALL·E image generation failed: {e}")
            raise
