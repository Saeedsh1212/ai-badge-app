# AI Badge App - Deployment Checklist

## Before 20/5 Global Meeting

### Step 1: Finalize Questions & Scoring (Monday meeting)
- [ ] Confirm 8 questions with your manager
- [ ] Finalize badge tier names (currently: Explorer, Practitioner, Champion, Catalyst)
- [ ] Confirm badge descriptions and colors
- [ ] Update `SURVEY_QUESTIONS` and `BADGE_TIERS` in `badge_app.py`

### Step 2: Local Testing (Tuesday)
```bash
# Navigate to app directory
cd /home/safb/pvr-tto/ai_badge_app

# Create/activate venv (optional, good practice)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run badge_app.py
```
- [ ] Test on desktop browser (localhost:8501)
- [ ] Test on mobile browser (use mobile hotspot or WiFi)
- [ ] Verify all questions display correctly
- [ ] Verify badge generation works
- [ ] Test download functionality

### Step 3: Deploy to Streamlit Cloud (Wednesday)

**Prerequisites:**
- GitHub repo ready (business or personal)
- Streamlit Cloud account created

**Steps:**
1. Create a new public GitHub repo called `ai-badge-app` (or similar)
2. Push this folder to that repo:
   ```bash
   git clone https://github.com/YOUR-USERNAME/ai-badge-app.git
   cd ai-badge-app
   # Copy contents of /ai_badge_app/ here
   git add .
   git commit -m "Initial AI Badge app"
   git push
   ```

3. Go to https://streamlit.io/cloud
4. Click "New app"
5. Select:
   - Repository: `YOUR-USERNAME/ai-badge-app`
   - Branch: `main`
   - Main file path: `badge_app.py`
6. Click "Deploy"
7. Wait ~2 minutes for deployment
8. [ ] Test the live URL on mobile

### Step 4: Generate QR Code (Thursday)
- [ ] Copy your Streamlit Cloud URL (e.g., `https://your-app.streamlit.app`)
- [ ] Generate QR code: https://qr.new
- [ ] Download QR code image
- [ ] Print for kiosk booth (recommend 6"×6" or larger)
- [ ] Test QR code scans on mobile phone

### Step 5: Kiosk Setup (Friday 20/5)
- [ ] Display QR code prominently at booth
- [ ] Have one helper brief participants: "Scan & get badge in <2 min"
- [ ] Optional: Display live badge counter on monitor (requires add-on)
- [ ] Have WiFi check: ensure venue WiFi is stable
- [ ] Fallback plan: Paper badges if WiFi fails

## Customization Reference

**Edit questions:** `badge_app.py` → `SURVEY_QUESTIONS` (lines ~60-78)

**Edit badge tiers:** `badge_app.py` → `BADGE_TIERS` (lines ~47-59)

**Change colors:** Update hex codes in `BADGE_TIERS` → `"color": "#HEXCODE"`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Streamlit Cloud won't deploy | Check requirements.txt, verify GitHub connection, restart deployment |
| Mobile form doesn't fit screen | Test in Chrome DevTools mobile mode, file issue |
| Badge image blank | Verify fonts installed, check Pillow version |
| QR code doesn't scan | Print larger, clean QR code image, try different phone camera |
| WiFi connectivity at venue | Have backup: test from mobile hotspot, prepare paper fallback |

## Support Contact
Saeed (email/Slack)
