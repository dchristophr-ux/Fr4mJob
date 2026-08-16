# 🖼️ Perfect Picture Frames (3P)
## THE Solution for Odd Shapes

An AI-powered web application that helps people find stylish, affordable frames for odd-shaped artwork and photos. Hexagon, oval, circle, arch, or completely custom — 3P covers the shapes generic frame retailers ignore.

**Version 2.0 (August 2026)** — rebuilt on current production AI models, with genuine vision-based photo analysis.

---

## ✨ What Makes 3P Special?

- 📷 **True Photo Analysis** - Upload your art; a vision AI model actually looks at the image and identifies the shape, colors, and style
- 📏 **Precision Input** - Enter exact dimensions for any of 13 shape types
- ✏️ **Custom Shape Descriptions** - Describe truly unique, irregular shapes
- 🤖 **AI-Powered Intelligence** - Groq's ultra-fast LPU inference for near-instant recommendations
- 💰 **Budget-Conscious** - Options for every price range
- 🎨 **Style Matching** - Frame suggestions that complement your art
- 🔨 **DIY Guidance** - Complete instructions for making your own
- 💾 **Downloadable Results** - Save recommendations as a text file with one click

---

## 🤖 AI Models (Current as of August 2026)

| Purpose | Model | Why |
|---------|-------|-----|
| Photo analysis | `qwen/qwen3.6-27b` | Groq's current multimodal (vision) model — 131K context, up to 5 images per request |
| Text recommendations | `openai/gpt-oss-120b` | Groq's flagship general/reasoning model and recommended replacement for the retired Llama line |

**Model-agnostic design**: model IDs live in two constants at the top of `perfect_picture_frames.py`. When Groq deprecates a model (they do this regularly — see [console.groq.com/docs/deprecations](https://console.groq.com/docs/deprecations)), swap the constant and you're done.

---

## 🚀 Quick Start Guide

### Step 1: Get Your Free Groq API Key (2 minutes)

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account (no credit card required)
3. Navigate to **"API Keys"** → Click **"Create API Key"**
4. Copy your new API key and save it securely

### Step 2: Install & Run (3 minutes)

```bash
# Install required packages
pip install -r requirements.txt

# Launch Perfect Picture Frames
streamlit run perfect_picture_frames.py
```

Browser opens automatically at `http://localhost:8501` 🎉

### Step 3: Configure & Use

1. Paste your Groq API key in the sidebar (or set the `GROQ_API_KEY` environment variable)
2. Choose your input method (photo / dimensions / description)
3. Get AI-powered frame recommendations!

---

## 📖 How to Use

### Option 1: 📷 Upload Photo
- Upload image of your artwork (PNG, JPG, JPEG, WEBP)
- Large photos are automatically resized for fast, reliable analysis
- The vision AI identifies the shape and style directly from the image

### Option 2: 📏 Enter Dimensions
- Select shape type (hexagon, oval, star, heart, etc.)
- Enter exact measurements
- Describe art, set budget and style preferences

### Option 3: ✏️ Describe Custom Shape
- Write detailed shape description
- Add artwork context
- Get creative custom solutions

---

## 🛠️ Troubleshooting

**"Please enter your Groq API key"**
- Verify complete key is pasted (no extra spaces)
- Ensure key is valid from console.groq.com

**Error mentions a model being "decommissioned"**
- Groq retired that model — check [console.groq.com/docs/deprecations](https://console.groq.com/docs/deprecations)
- Update `VISION_MODEL` or `TEXT_MODEL` at the top of `perfect_picture_frames.py`

**App won't start**
```bash
pip install streamlit --upgrade
pip install -r requirements.txt --force-reinstall
```

---

## 🚀 Deployment

### Streamlit Cloud (Easiest - FREE)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo and deploy
4. In app settings → Secrets, add: `GROQ_API_KEY = "your_key"`
   (The app automatically reads Streamlit secrets — no code changes needed)

### Local Network
```bash
streamlit run perfect_picture_frames.py --server.address 0.0.0.0
```

---

## 🔐 Security

- Never share API keys publicly
- Don't commit keys to Git
- Use environment variables or Streamlit secrets in production:
```bash
export GROQ_API_KEY="your_key_here"
```

---

## 📚 Tech Stack

- **Frontend**: Streamlit (Python — no HTML/CSS/JS required)
- **AI Engine**: Groq API (Qwen 3.6 27B vision + GPT-OSS 120B)
- **Image Processing**: Pillow (auto-resize, format conversion)
- **Language**: Python 3.9+

---

## 📝 Version History

**v2.0 (August 2026)** — Investor-ready rebuild
- Migrated to current Groq production models (previous models fully deprecated)
- **Fixed**: photo uploads are now actually sent to and analyzed by the vision model
- Added automatic image resizing for large phone photos
- Added one-click download of recommendations
- Added Streamlit Cloud secrets support for clean deployment
- Model IDs extracted to constants for painless future migrations

**v1.0 (2025)** — Initial release
- 3P branding, three input methods, Groq integration

---

<div align="center">

**🖼️ Perfect Picture Frames**
*3P - THE Solution for Odd Shapes*

Powered by Groq AI • Built with Streamlit • Made with ❤️

</div>
