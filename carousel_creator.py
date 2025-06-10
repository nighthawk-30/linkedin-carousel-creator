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

Create a 6‑slide LinkedIn carousel. Respond only in JSON with the keys
`slide1` to `slide6` following this structure:

```
{{
  "slide1": "**Bold title statement**",
  "slide2": "Context setting, up to three short lines.",
  "slide3": {{"heading": "Opening line", "bullets": ["pt1", "pt2", "pt3"]}},
  "slide4": {{"heading": "Opening line", "bullets": ["pt1", "pt2", "pt3"]}},
  "slide5": {{"heading": "Opening line", "bullets": ["pt1", "pt2", "pt3"]}},
  "slide6": "Twisted loop closing call to action."
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
            st.markdown(f"**Slide 1:** {data.get('slide1', '')}")
            st.markdown(f"**Slide 2:** {data.get('slide2', '')}")
            for idx in range(3, 6):
                slide = data.get(f'slide{idx}', {})
                if isinstance(slide, dict):
                    st.markdown(f"**Slide {idx}:** {slide.get('heading', '')}")
                    for bullet in slide.get('bullets', []):
                        st.markdown(f"- {bullet}")
                else:
                    st.markdown(f"**Slide {idx}:** {slide}")

            st.markdown(f"**Slide 6:** {data.get('slide6', '')}")

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
