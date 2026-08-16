"""
Perfect Picture Frames (3P) - THE Solution for Odd Shapes
AI-Powered Frame Recommendations for Unconventional Art

Version 2.0 (August 2026) - Investor-Ready Build
- Migrated to current Groq production models
- Photo uploads are now genuinely analyzed by a vision model
- Model-agnostic design: swap models by editing two constants below

Built with Streamlit and Groq AI
"""

import streamlit as st
from groq import Groq
import base64
from io import BytesIO
from PIL import Image
import os

# ─────────────────────────────────────────────────────────────
# MODEL CONFIGURATION
# Groq deprecates models regularly. If a model stops working,
# check https://console.groq.com/docs/deprecations for the
# current recommended replacements and update these two lines.
# Current as of August 2026:
# ─────────────────────────────────────────────────────────────
VISION_MODEL = "qwen/qwen3.6-27b"      # Multimodal: analyzes uploaded photos
TEXT_MODEL = "openai/gpt-oss-120b"     # Text: dimension & description inputs

# Keep uploads well under Groq's request size limit
MAX_IMAGE_DIMENSION = 1568  # px, longest side

# Page configuration
st.set_page_config(
    page_title="Perfect Picture Frames - 3P Solution for Odd Shapes",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def get_groq_client():
    """Initialize Groq client with API key from session state or environment."""
    if st.session_state.get('groq_api_key'):
        return Groq(api_key=st.session_state.groq_api_key)
    elif os.getenv('GROQ_API_KEY'):
        return Groq(api_key=os.getenv('GROQ_API_KEY'))
    # Streamlit Cloud secrets support (for deployed version)
    try:
        if "GROQ_API_KEY" in st.secrets:
            return Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception:
        pass
    return None


def prepare_image(image: Image.Image) -> str:
    """Resize (if needed) and encode a PIL Image to a base64 JPEG string.

    Resizing keeps requests fast and comfortably under Groq's 20MB
    image limit, even for large phone-camera photos.
    """
    # Convert to RGB (handles PNG transparency, CMYK, etc.)
    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")

    # Downscale if the longest side exceeds our cap
    longest = max(image.size)
    if longest > MAX_IMAGE_DIMENSION:
        scale = MAX_IMAGE_DIMENSION / longest
        new_size = (int(image.width * scale), int(image.height * scale))
        image = image.resize(new_size, Image.LANCZOS)

    buffered = BytesIO()
    image.save(buffered, format="JPEG", quality=88)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


SYSTEM_PROMPT = """You are an expert frame consultant for Perfect Picture Frames (3P),
THE solution for odd-shaped frames. You specialize in helping people find stylish,
affordable frames for non-standard shapes like hexagons, ovals, circles, diamonds,
arches, and irregular shapes.

Provide practical, specific recommendations including:
1. Frame style suggestions that complement the art and shape
2. Affordable online retailers with approximate prices
3. Custom frame shop recommendations (online services and local shop types)
4. DIY framing ideas with materials, steps, and cost estimates

Be specific, actionable, budget-conscious, and enthusiastic about helping solve
their odd-shaped framing challenge!"""


def analyze_with_groq(prompt: str, image_base64: str = None) -> str:
    """Send a request to Groq and return frame recommendations.

    If image_base64 is provided, the vision model receives the actual
    image alongside the prompt. Otherwise the text model is used.
    """
    client = get_groq_client()

    if not client:
        return "⚠️ Please enter your Groq API key in the sidebar to get AI-powered recommendations."

    try:
        if image_base64:
            # Vision request: text + image content blocks
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                },
            ]
            model = VISION_MODEL
        else:
            # Text-only request
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ]
            model = TEXT_MODEL

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_completion_tokens=2048,
        )

        return response.choices[0].message.content

    except Exception as e:
        return (
            f"❌ Error getting recommendations: {str(e)}\n\n"
            "If this mentions a model being decommissioned, check "
            "https://console.groq.com/docs/deprecations for the current "
            "replacement and update the model constants at the top of this file."
        )


# Custom CSS with 3P branding
st.markdown("""
<style>
    /* Main brand colors - purple, teal, coral */
    .main-header {
        font-size: 3.2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .tagline {
        text-align: center;
        font-size: 1.4rem;
        font-weight: 600;
        color: #764ba2;
        margin-bottom: 2rem;
        letter-spacing: 0.5px;
    }
    .sub-tagline {
        text-align: center;
        font-size: 1rem;
        color: #666;
        margin-bottom: 2.5rem;
        font-style: italic;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px 10px 0 0;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e9ecef;
    }
    .recommendation-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1.5rem 0;
    }
    .feature-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.3rem;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 4px solid #2196F3;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e9;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header with 3P branding
st.markdown('<h1 class="main-header">Perfect Picture Frames</h1>', unsafe_allow_html=True)
st.markdown('<p class="tagline">3P - THE Solution for Odd Shapes</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-tagline">AI-powered frame recommendations for hexagons, ovals, circles, and every shape in between</p>', unsafe_allow_html=True)

# Feature badges
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<span class="feature-badge">📷 True Photo Analysis</span>', unsafe_allow_html=True)
with col2:
    st.markdown('<span class="feature-badge">🤖 AI-Powered</span>', unsafe_allow_html=True)
with col3:
    st.markdown('<span class="feature-badge">💰 Budget-Friendly</span>', unsafe_allow_html=True)
with col4:
    st.markdown('<span class="feature-badge">🎨 Style Matching</span>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Sidebar for API key and information
with st.sidebar:
    st.header("⚙️ Configuration")

    api_key_input = st.text_input(
        "Groq API Key",
        type="password",
        value=st.session_state.get('groq_api_key', ''),
        help="Get your free API key from https://console.groq.com"
    )

    if api_key_input:
        st.session_state.groq_api_key = api_key_input
        st.markdown('<div class="success-box">✅ API key configured and ready!</div>', unsafe_allow_html=True)
    elif get_groq_client():
        st.markdown('<div class="success-box">✅ API key loaded from environment</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Enter your Groq API key to unlock AI recommendations")

    st.divider()

    st.markdown(f"""
    ### 🚀 Quick Start Guide

    **Get Your Free API Key:**
    1. Visit [console.groq.com](https://console.groq.com)
    2. Sign up (no credit card needed)
    3. Create an API key
    4. Paste it above ☝️

    ### 🤖 Under the Hood
    - **Photo analysis**: `{VISION_MODEL}`
    - **Text recommendations**: `{TEXT_MODEL}`
    - Ultra-fast Groq LPU inference

    ### 💡 Pro Tips
    - **Upload clear photos** for best results
    - **Be specific** about dimensions
    - **Mention your budget** for tailored options
    - **Describe the setting** (room, style)

    ### 🎯 What Makes 3P Different?
    Unlike generic frame searches, we specialize in:
    - ✨ Odd & unusual shapes
    - 🎨 Style-matched recommendations
    - 💰 Budget-conscious options
    - 🔨 DIY alternatives
    """)

    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #888; font-size: 0.85rem;'>
        <p><strong>Perfect Picture Frames</strong></p>
        <p>Version 2.0 • August 2026 • Built with ❤️</p>
    </div>
    """, unsafe_allow_html=True)

# Main content area with tabs
tab1, tab2, tab3 = st.tabs(["📷 Upload Photo", "📏 Enter Dimensions", "✏️ Describe Shape"])

# ─────────────────────────────────────────────────────────────
# Tab 1: Photo Upload (now with REAL image analysis)
# ─────────────────────────────────────────────────────────────
with tab1:
    st.markdown("### Upload a photo of your artwork or item")
    st.markdown('<div class="info-box">💡 <strong>Best results:</strong> Clear, well-lit photos showing the full shape of your artwork. Our vision AI actually looks at your image.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="Supported formats: PNG, JPG, JPEG, WEBP"
        )

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Your uploaded artwork", use_container_width=True)

            st.markdown("---")
            st.markdown("#### Additional Details (Optional but Helpful)")

            art_style = st.text_input(
                "Art style or medium",
                placeholder="e.g., modern abstract, vintage poster, watercolor landscape, oil painting"
            )

            budget = st.select_slider(
                "💰 Your budget range",
                options=["Under $50", "$50-$100", "$100-$200", "$200-$500", "$500+", "Custom (no limit)"],
                value="$50-$100"
            )

            room_context = st.text_input(
                "Where will this hang?",
                placeholder="e.g., living room, bedroom, office, gallery wall"
            )

            special_notes = st.text_area(
                "Any special requirements?",
                placeholder="e.g., must be lightweight, eco-friendly materials, needs glass protection",
                height=80
            )

            if st.button("🎨 Get My Perfect Frame Recommendations", type="primary", use_container_width=True, key="photo_submit"):
                with st.spinner("🔍 Our vision AI is analyzing your artwork and finding the perfect frames..."):
                    prompt = f"""Look carefully at this image of artwork and provide frame recommendations from Perfect Picture Frames (3P).

**Details provided by the customer:**
- Style: {art_style if art_style else 'Please determine from the image'}
- Budget: {budget}
- Location: {room_context if room_context else 'Not specified'}
- Special requirements: {special_notes if special_notes else 'None'}

Please provide a comprehensive recommendation including:

1. **Shape & Visual Analysis**: Based on what you SEE in the image, identify the exact shape of this artwork (hexagon, oval, circle, irregular, etc.), its apparent colors, style, and any unique characteristics.

2. **Frame Style Recommendations**: Suggest 3-4 specific frame styles that complement both the shape and what you observe in the artwork. For each, explain WHY it works.

3. **Affordable Retailer Options**: List specific online stores where odd-shaped frames in this budget range can be purchased, with approximate prices and direct search terms to use.

4. **Custom Framing Services**: Recommend 2-3 reputable online custom frame services that specialize in unusual shapes, with price estimates.

5. **DIY Solutions**: Provide creative DIY framing ideas including materials needed, step-by-step instructions, where to source materials, and estimated total cost.

Make recommendations specific, actionable, and enthusiastic!"""

                    image_b64 = prepare_image(image)
                    recommendations = analyze_with_groq(prompt, image_base64=image_b64)
                    st.session_state.last_recommendations = recommendations

    with col2:
        if st.session_state.get('last_recommendations'):
            st.markdown("### 🎯 Your Personalized 3P Recommendations")
            st.markdown(f'<div class="recommendation-box">{st.session_state.last_recommendations}</div>', unsafe_allow_html=True)

            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    "💾 Download Recommendations",
                    data=st.session_state.last_recommendations,
                    file_name="3P_frame_recommendations.txt",
                    use_container_width=True,
                    key="dl_photo"
                )
            with col_b:
                if st.button("🔄 Try Different Options", use_container_width=True, key="retry_photo"):
                    del st.session_state.last_recommendations
                    st.rerun()

# ─────────────────────────────────────────────────────────────
# Tab 2: Dimension Input
# ─────────────────────────────────────────────────────────────
with tab2:
    st.markdown("### Enter your artwork's dimensions and shape")
    st.markdown('<div class="info-box">💡 <strong>Perfect for:</strong> When you know the exact measurements and shape type</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        shape_type = st.selectbox(
            "🔷 Select your shape type",
            [
                "Hexagon", "Oval", "Circle", "Octagon", "Diamond",
                "Arch/Arched Top", "Pentagon", "Triangle", "Star",
                "Heart", "Cloud/Organic", "Irregular/Custom", "Other"
            ]
        )

        dimension_input = st.text_input(
            "📏 Enter exact dimensions",
            placeholder='e.g., 15" wide x 20" tall, diameter 18", 12" per side',
            help="Be as specific as possible for best recommendations"
        )

        art_description = st.text_area(
            "🎨 Describe your artwork",
            placeholder="What does it look like? Colors, style, subject matter, mood...\n\nExample: Abstract watercolor with blues and greens creating a peaceful ocean scene.",
            height=120
        )

        budget_dim = st.select_slider(
            "💰 Your budget range",
            options=["Under $50", "$50-$100", "$100-$200", "$200-$500", "$500+", "Custom (no limit)"],
            value="$50-$100",
            key="budget_dimensions"
        )

        color_preference = st.text_input(
            "🎨 Frame color preference (optional)",
            placeholder="e.g., natural wood, matte black, white, gold, silver"
        )

        style_preference = st.multiselect(
            "Style preferences (optional)",
            ["Modern/Contemporary", "Traditional/Classic", "Rustic/Farmhouse",
             "Minimalist", "Ornate/Decorative", "Industrial", "Bohemian"],
            help="Select all that apply"
        )

        if st.button("🎨 Get My Perfect Frame Recommendations", type="primary", use_container_width=True, key="dimension_submit"):
            if dimension_input:
                with st.spinner("🔍 Finding perfect frames for your specific shape and size..."):
                    style_pref_text = ", ".join(style_preference) if style_preference else "Open to suggestions"

                    prompt = f"""Provide frame recommendations from Perfect Picture Frames (3P) for this odd-shaped artwork:

**Artwork Specifications:**
- Shape: {shape_type}
- Dimensions: {dimension_input}
- Description: {art_description if art_description else 'Not provided - make general recommendations'}
- Budget: {budget_dim}
- Color preference: {color_preference if color_preference else 'Open to suggestions'}
- Style preference: {style_pref_text}

Please provide:

1. **Shape-Specific Guidance**: Tips for framing this {shape_type.lower()} shape - challenges and how to overcome them.

2. **Frame Style Recommendations**: 3-4 specific styles with explanations of why each works with this shape and art style.

3. **Affordable Online Retailers**: Where to buy {shape_type.lower()} frames in the {budget_dim} range - website names, price ranges, search terms.

4. **Custom Frame Shop Options**: 2-3 reputable services with price estimates, turnaround times, and quality levels.

5. **DIY Framing Guide**: Materials list, tools, sourcing, step-by-step assembly, total cost, difficulty and time required.

Make recommendations specific, practical, and budget-conscious!"""

                    recommendations = analyze_with_groq(prompt)
                    st.session_state.last_recommendations_dim = recommendations
            else:
                st.warning("⚠️ Please enter dimensions first!")

    with col2:
        if st.session_state.get('last_recommendations_dim'):
            st.markdown("### 🎯 Your Personalized 3P Recommendations")
            st.markdown(f'<div class="recommendation-box">{st.session_state.last_recommendations_dim}</div>', unsafe_allow_html=True)

            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    "💾 Download Recommendations",
                    data=st.session_state.last_recommendations_dim,
                    file_name="3P_frame_recommendations.txt",
                    use_container_width=True,
                    key="dl_dim"
                )
            with col_b:
                if st.button("🔄 Try Different Options", use_container_width=True, key="retry_dim"):
                    del st.session_state.last_recommendations_dim
                    st.rerun()

# ─────────────────────────────────────────────────────────────
# Tab 3: Custom Shape Description
# ─────────────────────────────────────────────────────────────
with tab3:
    st.markdown("### Describe your unique or irregular shape")
    st.markdown('<div class="info-box">💡 <strong>Perfect for:</strong> Truly unique shapes that don\'t fit standard categories</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### 🎨 Paint a Picture with Words")

        shape_description = st.text_area(
            "Describe your shape in detail",
            placeholder="""Be creative and specific! Examples:

"An irregular cloud-like shape, wider at the top (about 20 inches) tapering to 12 inches at the bottom, with flowing curved edges. Total height 24 inches."

"A traditional rectangle, but the top two corners are cut off at 45-degree angles, creating a house/pentagon shape. 16 inches wide at the base, 20 inches tall."

The more detail, the better our AI can help!""",
            height=180
        )

        art_context = st.text_area(
            "What's the artwork about?",
            placeholder="Describe your art piece:\n- Style and medium\n- Colors and mood\n- Subject matter",
            height=120
        )

        budget_draw = st.select_slider(
            "💰 Your budget range",
            options=["Under $50", "$50-$100", "$100-$200", "$200-$500", "$500+", "Custom (no limit)"],
            value="$100-$200",
            key="budget_draw"
        )

        special_requirements = st.text_area(
            "Special requirements or constraints?",
            placeholder="e.g., must be lightweight, UV-protective glass, eco-friendly materials, rapid turnaround",
            height=80
        )

        display_location = st.text_input(
            "Where will this be displayed?",
            placeholder="e.g., above fireplace mantle, modern office, child's bedroom"
        )

        if st.button("🎨 Get My Perfect Frame Recommendations", type="primary", use_container_width=True, key="draw_submit"):
            if shape_description:
                with st.spinner("🔍 Analyzing your unique shape and crafting custom solutions..."):
                    prompt = f"""Provide expert framing recommendations from Perfect Picture Frames (3P) for this uniquely shaped artwork:

**Custom Shape Description:**
{shape_description}

**Additional Context:**
- Artwork details: {art_context if art_context else 'Not specified'}
- Budget: {budget_draw}
- Display location: {display_location if display_location else 'Not specified'}
- Special requirements: {special_requirements if special_requirements else 'None mentioned'}

Please provide:

1. **Shape Feasibility Analysis**: Is this feasible for standard framing? What challenges exist? What approaches work best?

2. **Recommended Framing Approach**: Custom cut mat vs custom frame vs creative mounting? Shadow box, float mounting, or traditional?

3. **Frame Style Options**: 3-4 specific recommendations and why each works with irregular edges.

4. **Where to Get It Made**: Online custom services (names, specialties, price estimates), local shop types, turnaround times.

5. **Creative DIY Alternatives**: Approaches for different skill levels, materials, instructions, sourcing, costs, time investment.

6. **Pro Tips**: Mounting considerations, hanging hardware, care needs.

Be creative, practical, and encouraging!"""

                    recommendations = analyze_with_groq(prompt)
                    st.session_state.last_recommendations_draw = recommendations
            else:
                st.warning("⚠️ Please describe your shape first!")

    with col2:
        if st.session_state.get('last_recommendations_draw'):
            st.markdown("### 🎯 Your Personalized 3P Recommendations")
            st.markdown(f'<div class="recommendation-box">{st.session_state.last_recommendations_draw}</div>', unsafe_allow_html=True)

            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    "💾 Download Recommendations",
                    data=st.session_state.last_recommendations_draw,
                    file_name="3P_frame_recommendations.txt",
                    use_container_width=True,
                    key="dl_draw"
                )
            with col_b:
                if st.button("🔄 Try Different Options", use_container_width=True, key="retry_draw"):
                    del st.session_state.last_recommendations_draw
                    st.rerun()

# Footer with 3P branding
st.divider()
st.markdown("""
<div style='text-align: center; padding: 2.5rem 1rem; background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%); border-radius: 15px; margin-top: 2rem;'>
    <h3 style='color: #764ba2; margin-bottom: 1rem;'>🖼️ Perfect Picture Frames</h3>
    <p style='font-size: 1.2rem; font-weight: 600; color: #667eea; margin-bottom: 1rem;'>
        3P - THE Solution for Odd Shapes
    </p>
    <p style='color: #666; font-size: 0.95rem; margin-bottom: 0.5rem;'>
        Making unconventional shapes conventionally beautiful
    </p>
    <p style='color: #888; font-size: 0.85rem;'>
        Powered by Groq AI • Built with Streamlit • Made with ❤️
    </p>
</div>
""", unsafe_allow_html=True)
