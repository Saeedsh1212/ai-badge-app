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
    page_title="AI Badge Self-Assessment",
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
# BADGE CONFIGURATION
# ============================================================================
BADGE_TIERS = {
    "Explorer": {
        "min_score": 8,
        "max_score": 15,
        "color": "#4A90E2",
        "emoji": "🔍",
        "description": "You're just starting your AI journey. Keep exploring and learning!"
    },
    "Practitioner": {
        "min_score": 16,
        "max_score": 24,
        "color": "#7ED321",
        "emoji": "🎯",
        "description": "You have solid AI foundations and apply it in your work."
    },
    "Champion": {
        "min_score": 25,
        "max_score": 32,
        "color": "#F5A623",
        "emoji": "⭐",
        "description": "You're actively driving AI innovation in your area."
    },
    "Catalyst": {
        "min_score": 33,
        "max_score": 40,
        "color": "#D0021B",
        "emoji": "🚀",
        "description": "You're leading AI transformation. Your impact is inspiring."
    }
}

# ============================================================================
# SURVEY QUESTIONS (CUSTOMIZE THESE)
# ============================================================================
SURVEY_QUESTIONS = [
    {
        "question": "How confident are you in understanding AI concepts?",
        "answers": ["Not at all", "Slightly", "Moderately", "Very", "Extremely"]
    },
    {
        "question": "How often do you use AI tools in your daily work?",
        "answers": ["Never", "Rarely", "Sometimes", "Often", "Always"]
    },
    {
        "question": "How much impact do you think AI will have on your role?",
        "answers": ["None", "Minimal", "Moderate", "Significant", "Transformative"]
    },
    {
        "question": "How willing are you to learn new AI skills?",
        "answers": ["Not at all", "Somewhat reluctant", "Neutral", "Very willing", "Highly motivated"]
    },
    {
        "question": "How do you view AI in your organization?",
        "answers": ["Threat", "Neutral risk", "Interesting option", "Important tool", "Strategic priority"]
    },
    {
        "question": "How much have you collaborated on AI projects?",
        "answers": ["Never", "Minimal", "Some experience", "Regular", "Extensive"]
    },
    {
        "question": "How open are you to AI-driven change?",
        "answers": ["Very resistant", "Hesitant", "Neutral", "Supportive", "Enthusiastic"]
    },
    {
        "question": "How would you rate your overall AI readiness?",
        "answers": ["Very unprepared", "Unprepared", "Neutral", "Well prepared", "Highly prepared"]
    }
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_badge_tier(total_score):
    """Determine badge tier based on score."""
    for tier_name, tier_info in BADGE_TIERS.items():
        if tier_info["min_score"] <= total_score <= tier_info["max_score"]:
            return tier_name, tier_info
    return "Explorer", BADGE_TIERS["Explorer"]

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
    score_text = f"Score: {total_score}/40"
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
        'score': sum(responses) + 8,  # 1-5 per question, min 8
        'tier': calculate_badge_tier(sum(responses) + 8)[0]
    })

# ============================================================================
# MAIN APP LOGIC
# ============================================================================

def main():
    st.title("🏅 AI Badge Self-Assessment")
    st.caption("Discover your AI standpoint in less than 2 minutes")
    
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
        ### Welcome to the AI Badge Challenge! 🚀
        
        Answer 8 quick questions about your AI journey and receive your personalized badge instantly.
        
        **Badge Tiers:**
        - 🔍 **Explorer** (8-15): Starting your AI journey
        - 🎯 **Practitioner** (16-24): Building AI skills actively
        - ⭐ **Champion** (25-32): Driving AI innovation
        - 🚀 **Catalyst** (33-40): Leading AI transformation
        
        Ready? Let's go!
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
                score = q_data["answers"].index(response) + 1
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
        total_score = sum(st.session_state.final_responses) + 8  # Add 8 because 8 questions × min 1 = 8
        tier_name, tier_info = calculate_badge_tier(total_score)
        
        st.markdown("---")
        st.markdown('<div class="badge-container">', unsafe_allow_html=True)
        
        st.markdown(f'<p class="badge-title">{tier_info["emoji"]} Your Badge: {tier_name}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="badge-score">Score: {total_score} / 40</p>', unsafe_allow_html=True)
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
                st.write(f"🏅 I just got my **{tier_name}** AI Badge! What's yours?")

if __name__ == "__main__":
    main()
