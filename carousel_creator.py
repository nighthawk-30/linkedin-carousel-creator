import streamlit as st
import openai

# Get API key from Streamlit secrets
openai.api_key = st.secrets["openai_api_key"]

st.title("LinkedIn Carousel Creator")

post_text = st.text_area("Paste your blog post, article, or podcast transcript here")

audience = st.selectbox("Who is this for?", ["SME leaders", "Investors", "Marketing teams", "Tech founders"])
tone = st.selectbox("Choose a tone", ["Sharp", "Human", "Energetic", "Consultative", "Bold"])

submit = st.button("Generate Carousel")

if submit and post_text:
    with st.spinner("Generating..."):
        prompt = f"""
You are a B2B content strategist and LinkedIn expert.

Turn the following content into a LinkedIn carousel.

Audience: {audience}
Tone: {tone}

Return a structured carousel with:
- 1 Hook slide
- 4–5 short, punchy slides
- 1 CTA slide

Use short, direct lines. Return only the slide text as a list.

Content:
{post_text}
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        carousel = response['choices'][0]['message']['content']
        st.markdown("### 📊 Your LinkedIn Carousel")
        st.markdown(carousel)
