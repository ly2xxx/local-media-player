import streamlit as st
import os
from pathlib import Path
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="Local Media Player",
    page_icon="🎬",
    layout="wide"
)

# Title and description
st.title("🎬 Local Media Player")
st.markdown("Upload and play your local media files (videos, audio, images) directly in the browser")

# Supported file types
SUPPORTED_VIDEO = ['.mp4', '.webm', '.ogg', '.mov', '.avi']
SUPPORTED_AUDIO = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
SUPPORTED_IMAGE = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']

ALL_SUPPORTED = SUPPORTED_VIDEO + SUPPORTED_AUDIO + SUPPORTED_IMAGE

# Sidebar for file upload
with st.sidebar:
    st.header("📁 Media Source")
    
    input_method = st.radio(
        "Choose input method",
        ["File Upload", "Local Directory", "Web Media"],
        help="Use 'Local Directory' to stream large files without uploading"
    )
    
    uploaded_files = []

    if input_method == "File Upload":
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose media files",
            type=[ext[1:] for ext in ALL_SUPPORTED],  # Remove the dot
            accept_multiple_files=True,
            help="Upload video, audio, or image files"
        )
    elif input_method == "Local Directory":
        st.info("📂 **Local Directory Mode**\n\nSelect a folder in the main area to play files directly from your device.")
    else:  # Web Media
        st.info("🌐 **Web Media Mode**\n\nPlay online content from various platforms.")

        # URL input
        web_url = st.text_input(
            "Enter media URL",
            placeholder="https://example.com/video.mp4 or YouTube/Instagram/etc. URL",
            help="Paste a URL to online media content"
        )

        # Platform detection helper
        if web_url:
            if 'youtube.com' in web_url or 'youtu.be' in web_url:
                st.caption("🎥 YouTube video detected")
            elif 'instagram.com' in web_url:
                st.caption("📸 Instagram content detected")
            elif 'drive.google.com' in web_url:
                st.caption("📁 Google Drive link detected")
            elif any(ext in web_url.lower() for ext in ['.mp4', '.webm', '.mp3', '.wav', '.jpg', '.png', '.gif']):
                st.caption("🔗 Direct media link detected")

    st.markdown("---")
    st.markdown("### Supported Formats")
    st.markdown("**Video:** MP4, WebM, OGG, MOV, AVI")
    st.markdown("**Audio:** MP3, WAV, OGG, M4A, FLAC")
    st.markdown("**Image:** JPG, PNG, GIF, BMP, WebP")

# Main content area
if input_method == "File Upload" and uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) loaded")
    
    # Create tabs for different media types
    tabs = st.tabs([f"📄 {file.name}" for file in uploaded_files])
    
    for tab, uploaded_file in zip(tabs, uploaded_files):
        with tab:
            file_extension = Path(uploaded_file.name).suffix.lower()
            
            # Display file info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Name", uploaded_file.name)
            with col2:
                size_mb = uploaded_file.size / (1024 * 1024)
                st.metric("Size", f"{size_mb:.2f} MB")
            with col3:
                media_type = "Video" if file_extension in SUPPORTED_VIDEO else \
                            "Audio" if file_extension in SUPPORTED_AUDIO else "Image"
                st.metric("Type", media_type)
            
            st.markdown("---")
            
            # Display media based on type
            if file_extension in SUPPORTED_VIDEO:
                st.video(uploaded_file)
                
            elif file_extension in SUPPORTED_AUDIO:
                st.audio(uploaded_file)
                
            elif file_extension in SUPPORTED_IMAGE:
                st.image(uploaded_file, use_container_width=True)
            
            # Download button
            st.download_button(
                label="⬇️ Download",
                data=uploaded_file,
                file_name=uploaded_file.name,
                mime=uploaded_file.type
            )

elif input_method == "Local Directory":
    # HTML/JS Code for Client-Side Player
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            :root {
                --bg-color: #0e1117;
                --text-color: #fafafa;
                --secondary-bg: #262730;
                --accent: #ff4b4b;
                --font: "Source Sans Pro", sans-serif;
            }
            body {
                font-family: var(--font);
                color: var(--text-color);
                background-color: var(--bg-color);
                margin: 0;
                padding: 0;
                display: flex;
                height: 100vh;
                overflow: hidden;
            }
            ::-webkit-scrollbar {
                width: 8px;
                height: 8px;
            }
            ::-webkit-scrollbar-track {
                background: var(--bg-color); 
            }
            ::-webkit-scrollbar-thumb {
                background: #555; 
                border-radius: 4px;
            }
            ::-webkit-scrollbar-thumb:hover {
                background: #888; 
            }
            
            /* Sidebar for File List */
            #sidebar {
                width: 300px;
                background-color: var(--secondary-bg);
                border-right: 1px solid #333;
                display: flex;
                flex-direction: column;
                padding: 1rem;
                box-sizing: border-box;
                flex-shrink: 0;
            }
            
            #main-content {
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 2rem;
                overflow-y: auto;
                box-sizing: border-box;
            }

            .buttons-container {
                display: flex;
                gap: 10px;
                margin-bottom: 1rem;
                flex-direction: column;
            }
            
            input[type="file"] {
                display: none;
            }
            
            .custom-file-upload {
                border: 1px solid #4a4a4a;
                display: inline-block;
                padding: 8px 16px;
                cursor: pointer;
                background-color: #333;
                border-radius: 4px;
                width: 100%;
                text-align: center;
                box-sizing: border-box;
                transition: background 0.3s;
                font-weight: bold;
                font-size: 0.9rem;
            }
            
            .custom-file-upload:hover {
                background-color: #444;
                border-color: #666;
            }

            .note {
                font-size: 0.75rem;
                color: #888;
                margin-top: 4px;
                font-style: italic;
            }

            #file-list {
                overflow-y: auto;
                flex-grow: 1;
                margin-top: 1rem;
            }

            .file-item {
                padding: 10px;
                cursor: pointer;
                border-radius: 4px;
                margin-bottom: 4px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
                font-size: 14px;
                color: #d0d0d0;
                display: flex;
                align-items: center;
            }

            .file-item:hover {
                background-color: #3c3f47;
                color: white;
            }

            .file-item.active {
                background-color: var(--accent);
                color: white;
            }

            .icon {
                margin-right: 10px;
                font-size: 1.2em;
            }

            /* Player Styles */
            #player-container {
                width: 100%;
                max-width: 900px;
                text-align: center;
            }
            
            video, audio {
                width: 100%;
                max-height: 70vh;
                border-radius: 8px;
                outline: none;
                background: black;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }
            
            img {
                max-width: 100%;
                max-height: 70vh;
                object-fit: contain;
                border-radius: 4px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }

            #empty-state {
                color: #888;
                text-align: center;
            }
            
            #current-file-info {
                margin-top: 1rem;
                font-size: 1.2rem;
                font-weight: 500;
                color: #ddd;
            }
            
            .instructions {
                font-size: 0.9em;
                color: #aaa;
                margin-top: 0.5rem;
            }

        </style>
    </head>
    <body>

        <div id="sidebar">
            <div class="buttons-container">
                <div>
                    <label for="dir-input" class="custom-file-upload">
                        📂 Select Folder
                    </label>
                    <input type="file" id="dir-input" webkitdirectory directory multiple />
                    <div class="note">Files may be hidden in dialog</div>
                </div>
                
                <div>
                    <label for="file-input" class="custom-file-upload">
                        📄 Select Files
                    </label>
                    <input type="file" id="file-input" multiple />
                    <div class="note">Select specific files</div>
                </div>
            </div>
            
            <div id="file-list"></div>
        </div>

        <div id="main-content">
            <div id="empty-state">
                <h2>No Media Selected</h2>
                <p>Use the sidebar to select media from your device.</p>
                <div class="instructions">
                    Supported: MP4, MKV, MP3, PNG, JPG, etc.<br>
                    Files are played locally and not uploaded.
                </div>
            </div>
            
            <div id="player-container" style="display: none;">
                <div id="media-wrapper"></div>
                <div id="current-file-info"></div>
            </div>
        </div>

        <script>
            const dirInput = document.getElementById('dir-input');
            const fileInput = document.getElementById('file-input');
            const fileList = document.getElementById('file-list');
            const playerContainer = document.getElementById('player-container');
            const mediaWrapper = document.getElementById('media-wrapper');
            const emptyState = document.getElementById('empty-state');
            const fileInfo = document.getElementById('current-file-info');

            const SUPPORTED_EXT = new Set([
                'mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv', // Video
                'mp3', 'wav', 'm4a', 'flac',        // Audio
                'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg' // Image
            ]);

            function handleFileSelect(e) {
                const files = Array.from(e.target.files).filter(f => {
                    const ext = f.name.split('.').pop().toLowerCase();
                    return SUPPORTED_EXT.has(ext);
                }).sort((a, b) => a.name.localeCompare(b.name, undefined, {numeric: true, sensitivity: 'base'}));

                renderFileList(files);
                
                if (files.length > 0) {
                    emptyState.style.display = 'none';
                    playerContainer.style.display = 'block';
                    loadFile(files[0]); // Auto-load first file
                    // Highlight first
                     if (fileList.firstChild) fileList.firstChild.classList.add('active');
                } else {
                    emptyState.style.display = 'block';
                    playerContainer.style.display = 'none';
                    emptyState.innerHTML = "<h2>No supported media files found</h2><p>Try selecting a different source.</p>";
                }
            }

            dirInput.addEventListener('change', handleFileSelect);
            fileInput.addEventListener('change', handleFileSelect);

            function renderFileList(files) {
                fileList.innerHTML = '';
                files.forEach((file, index) => {
                    const div = document.createElement('div');
                    div.className = 'file-item';
                    div.dataset.index = index;
                    
                    // Icon based on type
                    const ext = file.name.split('.').pop().toLowerCase();
                    let icon = '<span class="icon">📄</span>';
                    if (['mp4','webm','mov','avi','mkv'].includes(ext)) icon = '<span class="icon">🎥</span>';
                    else if (['mp3','wav','m4a','flac'].includes(ext)) icon = '<span class="icon">🎵</span>';
                    else if (['jpg','jpeg','png','gif','webp','bmp','svg'].includes(ext)) icon = '<span class="icon">🖼️</span>';

                    div.innerHTML = `${icon} ${file.name}`;
                    
                    div.onclick = () => {
                        document.querySelectorAll('.file-item').forEach(el => el.classList.remove('active'));
                        div.classList.add('active');
                        loadFile(file);
                    };
                    fileList.appendChild(div);
                });
            }

            function loadFile(file) {
                const url = URL.createObjectURL(file);
                const ext = file.name.split('.').pop().toLowerCase();
                
                mediaWrapper.innerHTML = '';
                fileInfo.innerText = file.name;

                let element;

                if (['mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'].includes(ext)) {
                    element = document.createElement('video');
                    element.controls = true;
                    element.autoplay = true;
                    // Basic type inference
                    let mime = `video/${ext}`;
                    if(ext === 'mov') mime = 'video/quicktime';
                    if(ext === 'mkv') mime = 'video/x-matroska';
                    element.type = mime; 
                } else if (['mp3', 'wav', 'm4a', 'flac', 'ogg'].includes(ext)) {
                    element = document.createElement('audio');
                    element.controls = true;
                    element.autoplay = true;
                } else {
                    element = document.createElement('img');
                }

                element.src = url;
                mediaWrapper.appendChild(element);
            }
        </script>
    </body>
    </html>
    """
    
    # Render the custom component
    components.html(html_code, height=700, scrolling=False)

elif input_method == "Web Media" and web_url:
    st.success(f"🌐 Loading web media from URL")

    # Display URL info
    st.info(f"**Source:** {web_url}")

    st.markdown("---")

    # Handle different types of web media
    try:
        # YouTube videos
        if 'youtube.com/watch' in web_url or 'youtu.be/' in web_url:
            st.subheader("🎥 YouTube Video")
            # Extract video ID
            if 'youtu.be/' in web_url:
                video_id = web_url.split('youtu.be/')[-1].split('?')[0]
            else:
                video_id = web_url.split('v=')[-1].split('&')[0]

            # Embed YouTube video
            youtube_embed = f"""
            <iframe width="100%" height="600"
                src="https://www.youtube.com/embed/{video_id}"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
            </iframe>
            """
            st.markdown(youtube_embed, unsafe_allow_html=True)

        # Instagram posts
        elif 'instagram.com' in web_url:
            st.subheader("📸 Instagram Content")
            st.info("💡 **Tip:** Instagram embeds may have restrictions. For best results, use direct video/image URLs.")

            # Try to embed Instagram post
            instagram_embed = f"""
            <iframe src="{web_url}embed" width="100%" height="700" frameborder="0" scrolling="no" allowtransparency="true"></iframe>
            """
            st.markdown(instagram_embed, unsafe_allow_html=True)

        # Google Drive files
        elif 'drive.google.com' in web_url:
            st.subheader("📁 Google Drive Media")

            # Extract file ID and create direct link
            if '/file/d/' in web_url:
                file_id = web_url.split('/file/d/')[-1].split('/')[0]
                # Try to use Google Drive preview
                drive_embed = f"""
                <iframe src="https://drive.google.com/file/d/{file_id}/preview" width="100%" height="600" allow="autoplay"></iframe>
                """
                st.markdown(drive_embed, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please use a Google Drive direct file link (File > Share > Copy link)")

        # Direct media URLs (video, audio, image)
        elif any(ext in web_url.lower() for ext in ['.mp4', '.webm', '.ogg', '.mov']):
            st.subheader("🎥 Video")
            st.video(web_url)

        elif any(ext in web_url.lower() for ext in ['.mp3', '.wav', '.ogg', '.m4a', '.flac']):
            st.subheader("🎵 Audio")
            st.audio(web_url)

        elif any(ext in web_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']):
            st.subheader("🖼️ Image")
            st.image(web_url, use_container_width=True)

        # Generic iframe embed for other URLs
        else:
            st.subheader("🌐 Web Content")
            st.info("💡 Attempting to load content. Some platforms may restrict embedding.")

            # Try generic iframe
            generic_embed = f"""
            <iframe src="{web_url}" width="100%" height="600" frameborder="0" allowfullscreen></iframe>
            """
            st.markdown(generic_embed, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("**Supported platforms:**")
            st.markdown("- 🎥 YouTube videos")
            st.markdown("- 📸 Instagram posts")
            st.markdown("- 📁 Google Drive media files")
            st.markdown("- 🔗 Direct media URLs (.mp4, .mp3, .jpg, etc.)")
            st.markdown("- 🌐 Most video streaming platforms")

    except Exception as e:
        st.error(f"❌ Error loading media: {str(e)}")
        st.info("💡 Try using a direct media URL or check if the platform allows embedding.")

else:
    # Welcome message when no files are uploaded/selected
    st.info("👈 Choose a file source in the sidebar to get started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎥 Video Player")
        st.markdown("Play video files directly in your browser. Supports MP4, WebM, and more.")
    
    with col2:
        st.markdown("### 🎵 Audio Player")
        st.markdown("Listen to audio files with built-in controls. Supports MP3, WAV, and more.")
    
    with col3:
        st.markdown("### 🖼️ Image Viewer")
        st.markdown("View images with high quality rendering. Supports JPG, PNG, GIF, and more.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Built with Streamlit • All processing happens in your browser"
    "</div>",
    unsafe_allow_html=True
)
