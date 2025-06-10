# LinkedIn Carousel Creator

This Streamlit app takes a blog post, podcast transcript, or article and generates a structured LinkedIn carousel using GPT-4.

## How to Deploy on Streamlit Cloud

1. Upload these files to your GitHub repo
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Connect your GitHub and select this repo
5. In the settings, add your OpenAI API key in the `secrets.toml` section.
   You can also set it with the `OPENAI_API_KEY` environment variable.

## Files Included

- `carousel_creator.py` – the main Streamlit app
- `requirements.txt` – lists Python dependencies
- `.streamlit/secrets.toml` – place your OpenAI API key here or set `OPENAI_API_KEY`
