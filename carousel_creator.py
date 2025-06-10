import streamlit as st
import openai
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai_api_key"])

# Get API key from Streamlit secrets
openai.api_key = st.secrets["openai_api_key"]

st.title("LinkedIn Carousel Creator")

# --- User Inputs ---
post_text = st.text_area("Paste your blog post, article, or podcast transcript here")

audience = st.selectbox(
    "Who is this for?",
    ["SME leaders", "Investors"]
)

tone = st.selectbox(
    "Choose a tone",
    ["Inspirational", "Challenging", "Championing", "Educational", "Bold"]
)

submit = st.button("Generate Carousel")

# --- Persona Descriptions ---
persona_descriptions = {
    "SME leaders": (
        "a business leader running or scaling a small-to-medium-sized company. "
        "They are practical, resource-aware, and value ROI-driven advice."
    ),
    "Investors": (
        "an investor looking for high-growth opportunities. They value insight "
        "into performance, risk, and scalability, and prefer strategic, data-driven thinking."
    )
}

# --- Carousel Generation ---
if submit and post_text:
    with st.spinner("Generating..."):
        try:
            # Build prompt with context
            audience_context = persona_descriptions.get(audience, audience)
            prompt = f"""
You are a B2B content strategist and LinkedIn expert.

Audience: {audience} – {audience_context}
Tone: {tone}

Turn the following content into a LinkedIn carousel.

Return a structured carousel with:
- 1 Hook slide
- 4–5 short, punchy slides
- 1 CTA slide

Use short, direct lines. Return only the slide text as a list.

Content:
{post_text}
"""

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            carousel = response.choices[0].message.content
            st.markdown("### 📊 Your LinkedIn Carousel")
            for i, slide in enumerate(carousel.strip().split("\n"), start=1):
                slide = slide.strip()
                if slide:
                    st.markdown(f"**Slide {i}:** {slide}")

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
