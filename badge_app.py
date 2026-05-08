"""
AI Badge Self-Assessment App
Participants answer 8 questions, get an instant badge based on their score.
"""

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import json
from datetime import datetime

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="AI Ambassador Sprint – Find Your Badge",
    page_icon="🏅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Mobile-friendly styling
st.markdown("""
    <style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .stButton > button { width: 100%; padding: 12px; font-size: 16px; border-radius: 8px; }
    .stRadio > label { font-size: 15px; }
    .badge-container { text-align: center; padding: 20px; }
    .badge-title { font-size: 28px; font-weight: bold; margin-top: 20px; }
    .badge-score { font-size: 14px; color: #666; margin-top: 10px; }
    .badge-description { font-size: 14px; color: #666; margin-top: 10px; line-height: 1.6; }
    h1 { text-align: center; font-size: 24px; }
    .progress-bar { margin: 15px 0; }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# BADGE CONFIGURATION  (A=0, B=1, C=2, D=3 → max score = 10×3 = 30)
# ============================================================================
BADGE_TIERS = {
    "First Step Starter": {
        "min_score": 0,
        "max_score": 8,
        "color": "#7B8FA1",
        "emoji": "🌱",
        "description": "You're at the beginning of your AI journey. Every expert started here!"
    },
    "Curious Improver": {
        "min_score": 9,
        "max_score": 14,
        "color": "#4A90E2",
        "emoji": "🔍",
        "description": "You're exploring AI tools and building useful habits. Keep going!"
    },
    "Automation Explorer": {
        "min_score": 15,
        "max_score": 20,
        "color": "#7ED321",
        "emoji": "⚙️",
        "description": "You regularly use AI to automate tasks and improve your workflow."
    },
    "Workflow Helper": {
        "min_score": 21,
        "max_score": 26,
        "color": "#F5A623",
        "emoji": "🤝",
        "description": "AI is embedded in how you work. You help others see the value too."
    },
    "Ambassador Ready": {
        "min_score": 27,
        "max_score": 30,
        "color": "#D0021B",
        "emoji": "🚀",
        "description": "You lead by example. You're ready to be an AI Ambassador!"
    }
}

# ============================================================================
# SURVEY QUESTIONS  — exact wording from manager's document
# A=0, B=1, C=2, D=3 (same 4 options for every question)
# ============================================================================
ANSWER_OPTIONS = [
    "A) Not yet",
    "B) Tried once",
    "C) Sometimes",
    "D) Often / confidently"
]

SURVEY_QUESTIONS = [
    {"question": "I have used automation for repeat tasks to save time (summaries, drafts, formatting, follow-ups).", "answers": ANSWER_OPTIONS},
    {"question": "I use a consistent structure when I ask AI for help (goal + context + desired format).", "answers": ANSWER_OPTIONS},
    {"question": "I ask for AI outputs in a reusable format (checklist, table, email draft, slide outline).", "answers": ANSWER_OPTIONS},
    {"question": "I use AI to turn meeting notes into 'Actions / Owners / Deadlines.'", "answers": ANSWER_OPTIONS},
    {"question": "I use AI to draft or improve messages (email/Teams) and then edit before sending.", "answers": ANSWER_OPTIONS},
    {"question": "I have created or reused AI prompt template(s) so I don't start from scratch each time.", "answers": ANSWER_OPTIONS},
    {"question": "I add a quality step to my AI prompts (e.g., 'flag assumptions,' 'list what to verify,' 'check for missing items').", "answers": ANSWER_OPTIONS},
    {"question": "I verify key details before using the AI generated result (facts, numbers, dates, meaning).", "answers": ANSWER_OPTIONS},
    {"question": "I know the AI related safe-data rule and apply it (don't paste confidential/sensitive info into non-approved tools).", "answers": ANSWER_OPTIONS},
    {"question": "I have shared a useful automation/template with others (or I'm willing to).", "answers": ANSWER_OPTIONS},
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_badge_tier(total_score):
    """Determine badge tier based on score."""
    for tier_name, tier_info in BADGE_TIERS.items():
        if tier_info["min_score"] <= total_score <= tier_info["max_score"]:
            return tier_name, tier_info
    return "First Step Starter", BADGE_TIERS["First Step Starter"]

def generate_badge_image(tier_name, tier_info, total_score):
    """Generate a PNG badge image."""
    width, height = 400, 500
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default
    try:
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        desc_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        title_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
    
    # Background color (badge color)
    color_hex = tier_info["color"]
    color_rgb = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    draw.rectangle([(0, 0), (width, height)], fill=color_rgb)
    
    # White text
    text_color = (255, 255, 255)
    
    # Emoji
    emoji = tier_info["emoji"]
    draw.text((width//2, 50), emoji, fill=text_color, font=title_font, anchor="mm")
    
    # Tier name
    draw.text((width//2, 130), tier_name, fill=text_color, font=title_font, anchor="mm")
    
    # Score
    score_text = f"Score: {total_score}/30"
    draw.text((width//2, 200), score_text, fill=text_color, font=text_font, anchor="mm")
    
    # Description (wrapped)
    description = tier_info["description"]
    draw.text((width//2, 270), description, fill=text_color, font=desc_font, anchor="mm", align="center")
    
    # Timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d")
    draw.text((width//2, 450), f"Global Meeting • {timestamp}", fill=text_color, font=desc_font, anchor="mm")
    
    return img

def save_response(responses):
    """Save response to session state for analytics."""
    if 'responses' not in st.session_state:
        st.session_state.responses = []
    st.session_state.responses.append({
        'timestamp': datetime.now().isoformat(),
        'responses': responses,
        'score': sum(responses),  # A=0, B=1, C=2, D=3 → range 0–30
        'tier': calculate_badge_tier(sum(responses))[0]
    })

# ============================================================================
# MAIN APP LOGIC
# ============================================================================

def main():
    st.title("🏅 AI Ambassador Sprint")
    st.caption("Find Your Badge · Scan, answer fast, get your badge. This is a self-check — no right or wrong answers.")
    
    # Initialize session state
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_complete' not in st.session_state:
        st.session_state.quiz_complete = False
    if 'responses' not in st.session_state:
        st.session_state.responses = []
    
    # Start screen
    if not st.session_state.quiz_started:
        st.markdown("""
        ### Welcome! 👋

        Answer 10 quick statements about how you use AI in your work.  
        Your badge is calculated **automatically** — no maths needed.

        | Score | Badge |
        |-------|-------|
        | 0 – 8 | 🌱 First Step Starter |
        | 9 – 14 | 🔍 Curious Improver |
        | 15 – 20 | ⚙️ Automation Explorer |
        | 21 – 26 | 🤝 Workflow Helper |
        | 27 – 30 | 🚀 Ambassador Ready |

        *A = 0 pts · B = 1 pt · C = 2 pts · D = 3 pts*
        """)
        
        if st.button("Start Self-Assessment", use_container_width=True, type="primary"):
            st.session_state.quiz_started = True
            st.rerun()
    
    # Quiz screen
    elif st.session_state.quiz_started and not st.session_state.quiz_complete:
        st.markdown("---")
        
        responses = []
        
        # Display progress
        progress_text = "Question Progress"
        st.markdown(f"**{progress_text}**")
        
        # Questions
        for i, q_data in enumerate(SURVEY_QUESTIONS):
            st.markdown(f"### Question {i+1} of {len(SURVEY_QUESTIONS)}")
            st.markdown(q_data["question"])
            
            # Radio button (1-5 scale)
            response = st.radio(
                label=f"q_{i}",
                options=q_data["answers"],
                index=None,
                label_visibility="collapsed",
                key=f"q_{i}"
            )
            
            if response is not None:
                # Convert answer to score (1-5)
                score = q_data["answers"].index(response)  # A=0, B=1, C=2, D=3
                responses.append(score)
            else:
                responses.append(None)
            
            st.markdown("---")
        
        # Submit button (only enabled if all answered)
        if all(r is not None for r in responses):
            if st.button("Get My Badge! 🎉", use_container_width=True, type="primary"):
                st.session_state.quiz_complete = True
                st.session_state.final_responses = responses
                save_response(responses)
                st.rerun()
        else:
            st.info("👆 Please answer all questions to reveal your badge")
    
    # Result screen
    elif st.session_state.quiz_complete:
        total_score = sum(st.session_state.final_responses)  # A=0, B=1, C=2, D=3 → range 0–30
        tier_name, tier_info = calculate_badge_tier(total_score)
        
        st.markdown("---")
        st.markdown('<div class="badge-container">', unsafe_allow_html=True)
        
        st.markdown(f'<p class="badge-title">{tier_info["emoji"]} Your Badge: {tier_name}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="badge-score">Score: {total_score} / 30</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="badge-description">{tier_info["description"]}</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Generate badge image
        badge_img = generate_badge_image(tier_name, tier_info, total_score)
        
        # Display badge
        st.image(badge_img, use_container_width=True)
        
        # Download button
        img_bytes = io.BytesIO()
        badge_img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        st.download_button(
            label="⬇️ Download Your Badge",
            data=img_bytes,
            file_name=f"AI_Badge_{tier_name}.png",
            mime="image/png",
            use_container_width=True
        )
        
        # Reset button
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Take Again", use_container_width=True):
                st.session_state.quiz_started = False
                st.session_state.quiz_complete = False
                st.session_state.final_responses = []
                st.rerun()
        
        with col2:
            if st.button("Share", use_container_width=True):
                st.write(f"🏅 I just got my **{tier_name}** badge at the AI Ambassador Sprint! What's yours?  \nhttps://ai-badge-globalmeeting.streamlit.app")

if __name__ == "__main__":
    main()
