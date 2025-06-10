import streamlit as st
import openai

# Get API key from Streamlit secrets
openai.api_key = st.secrets["openai_api_key"]

st.title("LinkedIn Carousel Creator")

post_text = st.text_area("Paste your blog post, article, or podcast transcript here")

audience = st.selectbox("Who is this for?", ["SME leaders", "Investors"])
tone = st.selectbox("Choose a tone", ["Inspirational", "Challenging", "Championing", "Educational", "Bold"])

submit = st.button("Generate Carousel")

# Define persona details
persona_descriptions = {
    "Bold Movers": (
        "a decisive, growth-focused business leader (often a founder, CEO, or senior exec) scaling a fast-growing company. "
        "They’re curious about AI and data but focused on outcomes, not tech. "
        "They value speed, clarity, and practical tools over theory."
    ),
    "SME leaders": "a business leader running or scaling a small-to-medium-sized company. They are practical, resource-aware, and value ROI-driven advice.",
    "Investors": "an investor looking for high-growth opportunities. They value insight into performance, risk, and scalability, and prefer strategic, data-driven thinking."
}

if submit and post_text:
    with st.spinner("Generating..."):
        # Inject persona context based on selected audience
        audience_context = persona_descriptions.get(audience, audience)

        prompt = f"""You are a B2B content strategist and LinkedIn expert.

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

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        carousel = response['choices'][0]['message']['content']
        st.markdown("### 📊 Your LinkedIn Carousel")
        st.markdown(carousel)


# Split response into lines and display each slide cleanly
for i, slide in enumerate(carousel.strip().split("\n"), start=1):
    if slide.strip():
        st.markdown(f"**Slide {i}:** {slide.strip()}")
