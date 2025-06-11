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
    ["SME leaders", "Investors", "Bold Mover"]
)

tone = st.selectbox(
    "Choose a tone",
    ["Inspirational", "Challenging", "Championing", "Educational", "Bold"]
)

tone_descriptions = {
    "Inspirational": (
        "Use motivational language that encourages the reader to take positive action "
        "and highlights success stories."
    ),
    "Challenging": (
        "Adopt a provocative stance that questions the status quo and pushes the reader "
        "to rethink their assumptions."
    ),
    "Championing": (
        "Sound supportive and enthusiastic, positioning yourself as the reader's advocate "
        "and celebrating their potential."
    ),
    "Educational": (
        "Maintain a clear, instructive tone that explains concepts step by step, focusing on "
        "practical takeaways."
    ),
    "Bold": (
        "Be assertive and confident with punchy language that makes strong statements and "
        "encourages decisive action."
    ),
}

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
    ),
    "Bold Mover": (
        "The Bold Mover is a forward-thinking business leader—often a founder, CEO, or senior exec—in a fast-growing company. They’re ambitious, restless, and focused on scaling up, acquiring, or preparing for investment or exit. They're not afraid to experiment, especially with tech and data, but they demand clear outcomes and speed."
        "Core Traits: Decisive and growth-focused, Comfortable with calculated risk, Curious about AI, data, and automation—but not technical, Values expertise, but expects agility and straight talk, Balances vision with commercial pressure"
        "Pain Points: Lack of clarity on how to use AI or data to actually drive growth, Frustrated by slow agencies or vague consultants, Pressure to hit big targets with lean teams"
        "Goals: Use smart tools (like AI agents) to gain a competitive edge, Simplify decision-making with better insights, Scale fast, raise funding, or prep for sale"
        "What They Want from Us: Clear, fast answers—not theory, Tools, not just slides, Partners who get business, not just tech"
    )
}

# --- Carousel Generation ---
if submit and post_text:
    with st.spinner("Generating..."):
        try:
            # Build prompt with context
            audience_context = persona_descriptions.get(audience, audience)
            tone_context = tone_descriptions.get(tone, "")
            prompt = f"""
You are a B2B content strategist and LinkedIn expert.

Audience: {audience} – {audience_context}
Tone: {tone} – {tone_context}

Create a LinkedIn carousel with up to 12 slides. Decide how many slides and bullet points each slide needs. Respond only in JSON using keys `slide1`, `slide2`, etc. Follow this structure:

```
{{
  "slide1": "**Bold title statement**",
  "slide2": "Context setting, up to three short lines.",
  "slide3": {{"heading": "Opening line", "bullets": ["pt1", "pt2"]}},
  ...,
  "slideN": "Twisted loop closing call to action."
}}
```

Use Markdown for emphasis but ensure the JSON is valid.

Content:
{post_text}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )

            import json, re
            carousel_raw = response.choices[0].message.content
            # Remove code fences if present
            carousel_clean = re.sub(r"^```(?:json)?|```$", "", carousel_raw, flags=re.MULTILINE).strip()
            try:
                data = json.loads(carousel_clean)
            except json.JSONDecodeError:
                st.error("Failed to parse response. Raw output:")
                st.text(carousel_raw)
                st.stop()

            st.markdown("### 📊 Your LinkedIn Carousel")
            for idx in range(1, 13):
                key = f'slide{idx}'
                if key not in data:
                    continue
                slide = data[key]
                if isinstance(slide, dict):
                    st.markdown(f"**Slide {idx}:** {slide.get('heading', '')}")
                    for bullet in slide.get('bullets', []):
                        st.markdown(f"- {bullet}")
                else:
                    st.markdown(f"**Slide {idx}:** {slide}")

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
