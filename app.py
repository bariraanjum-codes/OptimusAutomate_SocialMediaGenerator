import streamlit as st
import requests

# ============================================
# GROQ API KEY
# ============================================
GROQ_API_KEY = "gsk_YOUR_ACTUAL_KEY_HERE"

API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.1-8b-instant"

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="AI Social Media Content Generator",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS - CLEAN & PROFESSIONAL
# ============================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%);
    }

    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 35px 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }

    .hero-title {
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        color: white !important;
        margin-bottom: 8px !important;
        letter-spacing: -0.5px !important;
    }

    .hero-subtitle {
        font-size: 1rem !important;
        color: rgba(255,255,255,0.85) !important;
        font-weight: 400 !important;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        padding: 6px 18px;
        border-radius: 50px;
        font-size: 0.85rem;
        color: white;
        margin-top: 12px;
        backdrop-filter: blur(10px);
    }

    /* Cards */
    .content-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        border: 1px solid rgba(226, 232, 240, 0.8);
        margin-bottom: 15px;
    }

    .content-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
        color: #1e293b !important;
        margin-bottom: 15px !important;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Input Styling */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 12px !important;
        font-size: 0.95rem !important;
    }

    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
    }

    .stSelectbox > div > div {
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 4px 16px !important;
        transition: all 0.3s ease !important;
        border: none !important;
        min-height: 32px !important;
        line-height: 1.2 !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
    }

    .stButton > button[kind="secondary"] {
        background: #f1f5f9 !important;
        color: #475569 !important;
        border: 2px solid #e2e8f0 !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: #e2e8f0 !important;
    }
             
    .stButton {
        margin-bottom: 0px !important;
        margin-top: 0px !important;
    }

    /* Output Boxes */
    .output-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #86efac;
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
    }

    .output-box-calendar {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 2px solid #93c5fd;
        border-radius: 16px;
        padding: 20px;
        margin-top: 15px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.6);
        padding: 8px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        color: #64748b !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    /* Messages */
    .stSuccess, .stError, .stInfo, .stWarning {
        border-radius: 12px !important;
        border: none !important;
    }

    .stSuccess {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%) !important;
        color: #166534 !important;
    }

    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%) !important;
        color: #991b1b !important;
    }

    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%) !important;
        color: #1e40af !important;
    }

    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%) !important;
        color: #92400e !important;
    }

    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }

    /* Divider */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent) !important;
        margin: 25px 0 !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 15px;
        color: #94a3b8;
        font-size: 0.85rem;
    }

    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* CRITICAL FIX: Remove extra white space */
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }

    /* CRITICAL FIX: Remove empty column gaps */
    [data-testid="column"] {
        gap: 0px !important;
    }
            
    [data-testid="column"] > div {
    gap: 0px !important;
    margin-bottom: 0px !important;
    }

    /* CRITICAL FIX: Remove all extra margins */
    .stMarkdown, .stTextArea, .stSelectbox {
        margin-bottom: 0px !important;
        margin-top: 0px !important;
    }

    /* CRITICAL FIX: Remove empty space from columns */
    .stVerticalBlock {
        gap: 0.5rem !important;
    }

    /* CRITICAL FIX: Streamlit auto-generated empty containers */
    [data-testid="stVerticalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
        margin-bottom: 0px !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-color: #667eea !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNCTIONS
# ============================================
def check_api_key():
    if not GROQ_API_KEY or "YOUR_ACTUAL_KEY" in GROQ_API_KEY or GROQ_API_KEY == "gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx":
        return False, " API Key missing! Please paste your actual Groq API key in the code."
    if not GROQ_API_KEY.startswith("gsk_"):
        return False, " API Key format looks wrong. Groq keys start with 'gsk_'"
    return True, "✅ API Key format looks good."

def generate_post(topic, platform, tone, length, variation=0):
    platform_tips = {
        "LinkedIn": "Professional tone. Industry insights. 3-5 hashtags. Value-driven. Use emojis sparingly.",
        "Twitter/X": "Short, punchy, under 280 chars. 2-3 hashtags. Strong hook. Engaging and conversational.",
        "Instagram": "Friendly, emojis, storytelling. 10-15 hashtags. Visual appeal. Use line breaks for readability."
    }

    variation_prompts = [
        "",
        "Make this version more creative and unique.",
        "Focus on storytelling and emotional connection.",
        "Include a compelling call-to-action.",
        "Use a question-based hook to engage readers."
    ]

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    extra_instruction = variation_prompts[variation % len(variation_prompts)]

    prompt = f"""Create a {length} social media post for {platform}.
Topic/Brand: {topic}
Tone: {tone}
Guidelines: {platform_tips.get(platform, '')}
{extra_instruction}
Return ONLY the post content, no extra explanation."""

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert social media marketer with 10+ years of experience."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.8 + (variation * 0.05),
        "max_tokens": 1000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code != 200:
            error_detail = response.text
            return f" API Error (Status {response.status_code}):\n{error_detail}"
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.Timeout:
        return " Error: Request timed out. Please check your internet connection."
    except requests.exceptions.ConnectionError:
        return " Error: Cannot connect to Groq API. Please check your internet."
    except Exception as e:
        return f" Error: {str(e)}"

def generate_calendar(brand_desc, days, platform, variation=0):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    variation_themes = [
        "",
        "Focus on educational content and thought leadership.",
        "Emphasize user-generated content and community building.",
        "Create a mix of promotional and value-driven content."
    ]

    extra_theme = variation_themes[variation % len(variation_themes)]

    prompt = f"""Create a {days}-day content calendar for {platform}.
Brand/Product: {brand_desc}
{extra_theme}
Return a structured markdown table with: Day | Post Topic | Content Idea | Suggested Hashtags | Best Posting Time
Make it detailed and actionable."""

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a top-tier social media strategist."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7 + (variation * 0.05),
        "max_tokens": 2000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code != 200:
            error_detail = response.text
            return f" API Error (Status {response.status_code}):\n{error_detail}"
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f" Error: {str(e)}"

def refine_post(original_post, refinement_instruction, platform, tone):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""Here is an existing social media post for {platform}:

{original_post}

Please refine this post with the following instruction: {refinement_instruction}
Tone: {tone}
Return ONLY the refined post content, no extra explanation."""

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert social media editor."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=30)
        if response.status_code != 200:
            error_detail = response.text
            return f" API Error (Status {response.status_code}):\n{error_detail}"
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f" Error: {str(e)}"

# ============================================
# HERO SECTION
# ============================================
st.markdown("""
<div class="hero-container">
    <div class="hero-title"> AI Social Media Content Generator</div>
    <div class="hero-subtitle">Create stunning, platform-optimized content in seconds</div>
    <div class="hero-badge"> OptimusAutomate Internship Project</div>
</div>
""", unsafe_allow_html=True)

# API Key Check
key_ok, key_msg = check_api_key()
if not key_ok:
    st.error(key_msg)
    st.info(" Get your free API key from: https://console.groq.com/keys")
    st.stop()

    

# ============================================
# TABS
# ============================================
tab1, tab2 = st.tabs([" Single Post Generator", " Content Calendar Planner"])

# ============================================
# TAB 1: SINGLE POST
# ============================================
with tab1:
    st.markdown('<div class="section-header">✍️ Generate Social Media Post</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        topic = st.text_area(
            " Topic / Brand Description:",
            height=120,
            placeholder="e.g., Launching an AI-powered fitness app that tracks workouts and suggests personalized meal plans...",
            help="Describe your topic, product, or brand in detail for better results",
            key="post_topic"
        )
        platform = st.selectbox(
            " Platform:",
            ["LinkedIn ", "Twitter/X ", "Instagram "],
            help="Choose the platform for optimized content",
            key="post_platform"
        )

    with col2:
        tone = st.selectbox(
            " Tone:",
            ["Professional", "Casual", "Excited", "Inspirational", "Funny", "Authoritative", "Friendly"],
            help="Select the tone that matches your brand voice",
            key="post_tone"
        )
        length = st.selectbox(
            " Length:",
            ["Short", "Medium", "Long"],
            help="Choose the length of your post",
            key="post_length"
        )

    # Generate Button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        generate_clicked = st.button(" Generate Post", type="primary", use_container_width=True, key="gen_post_btn")

    # Initialize session state
    if 'generated_post' not in st.session_state:
        st.session_state.generated_post = None
    if 'post_variation' not in st.session_state:
        st.session_state.post_variation = 0
    if 'show_refine' not in st.session_state:
        st.session_state.show_refine = False
    if 'post_topic_saved' not in st.session_state:
        st.session_state.post_topic_saved = ""
    if 'post_platform_saved' not in st.session_state:
        st.session_state.post_platform_saved = "LinkedIn 💼"
    if 'post_tone_saved' not in st.session_state:
        st.session_state.post_tone_saved = "Professional"
    if 'post_length_saved' not in st.session_state:
        st.session_state.post_length_saved = "Short"

    # Handle Generate
    if generate_clicked:
        if not topic.strip():
            st.warning(" Please enter a topic or brand description!")
        else:
            st.session_state.post_topic_saved = topic
            st.session_state.post_platform_saved = platform
            st.session_state.post_tone_saved = tone
            st.session_state.post_length_saved = length

            with st.spinner(" AI is crafting your perfect post..."):
                platform_clean = platform.split(" ")[0]
                post = generate_post(topic, platform_clean, tone, length, st.session_state.post_variation)
                st.session_state.generated_post = post
                st.session_state.show_refine = False
            st.rerun()

    # Display Output
    if st.session_state.generated_post:
        st.markdown('<div class="output-box">', unsafe_allow_html=True)
        st.markdown("###  Your Generated Post:")
        st.markdown(st.session_state.generated_post)
        st.markdown('</div>', unsafe_allow_html=True)

        col_regen, col_refine = st.columns(2)

        with col_regen:
            if st.button(" Regenerate", type="secondary", use_container_width=True, key="regen_post"):
                st.session_state.post_variation += 1
                with st.spinner("✨ Generating new variation..."):
                    platform_clean = st.session_state.post_platform_saved.split(" ")[0]
                    post = generate_post(
                        st.session_state.post_topic_saved,
                        platform_clean,
                        st.session_state.post_tone_saved,
                        st.session_state.post_length_saved,
                        st.session_state.post_variation
                    )
                    st.session_state.generated_post = post
                st.rerun()

        with col_refine:
            if st.button(" Refine", type="secondary", use_container_width=True, key="refine_btn"):
                st.session_state.show_refine = not st.session_state.show_refine
                st.rerun()

    # Refine Section
    if st.session_state.show_refine and st.session_state.generated_post:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("###  Refine Your Post")
        refinement = st.text_area(
            "What would you like to change?",
            placeholder="e.g., Make it more engaging, add a call-to-action, shorten it, make it more formal...",
            height=80,
            key="refine_input"
        )

        col_refine_btn, col_cancel = st.columns([1, 1])
        with col_refine_btn:
            if st.button(" Apply Refinement", type="primary", use_container_width=True, key="apply_refine"):
                if refinement.strip():
                    with st.spinner(" Refining your post..."):
                        platform_clean = st.session_state.post_platform_saved.split(" ")[0]
                        refined = refine_post(
                            st.session_state.generated_post,
                            refinement,
                            platform_clean,
                            st.session_state.post_tone_saved
                        )
                        st.session_state.generated_post = refined
                        st.session_state.show_refine = False
                    st.rerun()
                else:
                    st.warning(" Please enter a refinement instruction!")

        with col_cancel:
            if st.button(" Cancel", type="secondary", use_container_width=True, key="cancel_refine"):
                st.session_state.show_refine = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# TAB 2: CONTENT CALENDAR
# ============================================
with tab2:
    st.markdown('<div class="section-header">📅 Content Calendar Planner</div>', unsafe_allow_html=True)

    brand = st.text_area(
        " Describe your Brand/Product:",
        height=120,
        placeholder="e.g., Sustainable fashion brand targeting Gen Z with eco-friendly clothing made from recycled materials...",
        help="The more details you provide, the better the calendar will be",
        key="cal_brand"
    )

    col_cal1, col_cal2 = st.columns(2)

    with col_cal1:
        days = st.slider(
            " Calendar Duration (Days):",
            min_value=3,
            max_value=14,
            value=7,
            help="Select how many days of content you want to plan",
            key="cal_days"
        )

    with col_cal2:
        cal_plat = st.selectbox(
            " Platform:",
            ["LinkedIn ", "Twitter/X ", "Instagram "],
            help="Choose the platform for your content calendar",
            key="cal_platform"
        )

    col_cal_btn1, col_cal_btn2, col_cal_btn3 = st.columns([1, 2, 1])
    with col_cal_btn2:
        cal_generate_clicked = st.button(" Generate Calendar", type="primary", use_container_width=True, key="gen_cal_btn")

    if 'generated_calendar' not in st.session_state:
        st.session_state.generated_calendar = None
    if 'calendar_variation' not in st.session_state:
        st.session_state.calendar_variation = 0
    if 'cal_brand_saved' not in st.session_state:
        st.session_state.cal_brand_saved = ""
    if 'cal_days_saved' not in st.session_state:
        st.session_state.cal_days_saved = 7
    if 'cal_plat_saved' not in st.session_state:
        st.session_state.cal_plat_saved = "LinkedIn 💼"

    if cal_generate_clicked:
        if not brand.strip():
            st.warning(" Please describe your brand or product!")
        else:
            st.session_state.cal_brand_saved = brand
            st.session_state.cal_days_saved = days
            st.session_state.cal_plat_saved = cal_plat

            with st.spinner(" Planning your content calendar..."):
                platform_clean = cal_plat.split(" ")[0]
                calendar = generate_calendar(brand, days, platform_clean, st.session_state.calendar_variation)
                st.session_state.generated_calendar = calendar
            st.rerun()

    if st.session_state.generated_calendar:
        st.markdown('<div class="output-box-calendar">', unsafe_allow_html=True)
        st.markdown(f"###  Your {st.session_state.cal_days_saved}-Day Content Calendar:")
        st.markdown(st.session_state.generated_calendar)
        st.markdown('</div>', unsafe_allow_html=True)

        col_regen_cal1, col_regen_cal2, col_regen_cal3 = st.columns([1, 2, 1])
        with col_regen_cal2:
            if st.button(" Regenerate Calendar", type="secondary", use_container_width=True, key="regen_cal"):
                st.session_state.calendar_variation += 1
                with st.spinner(" Generating new calendar..."):
                    platform_clean = st.session_state.cal_plat_saved.split(" ")[0]
                    calendar = generate_calendar(
                        st.session_state.cal_brand_saved,
                        st.session_state.cal_days_saved,
                        platform_clean,
                        st.session_state.calendar_variation
                    )
                    st.session_state.generated_calendar = calendar
                st.rerun()

# ============================================
# FOOTER
# ============================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    <p> Built with Streamlit & Groq AI | OptimusAutomate Internship Project</p>
    <p style="font-size: 0.75rem; margin-top: 5px;">Powered by Llama 3.1 | Create. Engage. Grow. </p>
</div>
""", unsafe_allow_html=True)