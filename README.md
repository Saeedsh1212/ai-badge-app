# AI Badge Self-Assessment App

A lightweight, mobile-friendly Streamlit app for participants to self-assess their AI standpoint and instantly receive a personalized badge.

## Features

- ✅ 8 self-assessment questions (1-5 scale each)
- ✅ Instant badge calculation and assignment
- ✅ 4 badge tiers: Explorer → Practitioner → Champion → Catalyst
- ✅ Downloadable badge image (PNG)
- ✅ Mobile-friendly UI
- ✅ No login required
- ✅ Works on personal and corporate phones

## Quick Start

### Local Testing

1. Clone or download this repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run badge_app.py
   ```
4. Open your browser to `http://localhost:8501`

### Deploy to Streamlit Cloud (Production)

1. Push this folder to your GitHub repository:
   ```bash
   git add .
   git commit -m "Add AI Badge app"
   git push
   ```

2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and sign in with GitHub

3. Click "New app" and select:
   - Repository: your repo
   - Branch: main
   - Main file path: `ai_badge_app/badge_app.py`

4. Streamlit Cloud will deploy automatically. Your app URL will be:
   ```
   https://yourrepo-youruser.streamlit.app
   ```

5. Generate a QR code pointing to that URL using any QR generator:
   - Google QR code generator: https://qr.new
   - Or print the URL as-is for participants to click

## Customization

### Change Questions
Edit `SURVEY_QUESTIONS` in `badge_app.py`:
```python
SURVEY_QUESTIONS = [
    {
        "question": "Your question here?",
        "answers": ["Option 1", "Option 2", "Option 3", "Option 4", "Option 5"]
    },
    # ... more questions
]
```

### Change Badge Tiers
Edit `BADGE_TIERS` in `badge_app.py`:
```python
BADGE_TIERS = {
    "YourTierName": {
        "min_score": 8,
        "max_score": 15,
        "color": "#4A90E2",
        "emoji": "🔍",
        "description": "Your tier description"
    },
    # ... more tiers
}
```

### Add Company Branding
- Change colors in `BADGE_TIERS` (hex color codes)
- Add logo/footer in `generate_badge_image()` function

## Score Calculation

- 8 questions × 1-5 points each
- Total range: 8-40 points
- Badges assigned by score ranges (configurable)

## Privacy & Data

- **Anonymous by default** — no personal data collected
- Responses are stored in Streamlit's session state only
- For persistent analytics, add a backend database (see advanced section)

## Troubleshooting

**App won't load on Streamlit Cloud?**
- Check `requirements.txt` has all dependencies
- Verify GitHub repo connection
- Check Streamlit Cloud logs

**Badge image won't generate?**
- Ensure Pillow is installed: `pip install Pillow`
- Check system fonts are available (Streamlit Cloud includes standard fonts)

**Mobile form looks broken?**
- Clear browser cache
- Try a different browser
- Test on Chrome/Safari mobile

## Next Steps

For a full production rollout, consider:
- Adding backend database (e.g., Supabase, PostgreSQL) to persist responses
- Adding admin dashboard to view results and export data
- Adding email/Teams notification on completion
- Integrating with Lundbeck brand guidelines

## Support

Questions? Refer to [Streamlit docs](https://docs.streamlit.io) or reach out to Saeed.
