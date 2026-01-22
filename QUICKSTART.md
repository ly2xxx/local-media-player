# 🚀 Quick Start Guide

## Run Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use

1. **Upload Files**: Use the sidebar to upload media files
2. **Switch Between Files**: Click on tabs to view different files
3. **Play Media**: Videos and audio files will have playback controls
4. **View Details**: Each file shows its name, size, and type
5. **Download**: Use the download button to save files

## Features

- ✅ Play videos (MP4, WebM, OGG, MOV, AVI)
- ✅ Play audio (MP3, WAV, OGG, M4A, FLAC)
- ✅ View images (JPG, PNG, GIF, BMP, WebP)
- ✅ Multiple file support with tabs
- ✅ File information display
- ✅ Download capability
- ✅ Responsive design

## Troubleshooting

**App won't start?**
- Make sure Streamlit is installed: `pip install streamlit`
- Check Python version: `python --version` (needs 3.8+)

**File won't play?**
- Check if the file format is supported (see README)
- Try converting to a web-friendly format (MP4 for video, MP3 for audio)

**Browser issues?**
- Try a different browser (Chrome, Firefox, Edge recommended)
- Clear browser cache and reload
