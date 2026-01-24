"""Local directory input handler."""
import streamlit as st
import streamlit.components.v1 as components
from .base import MediaInputHandler


class LocalDirectoryInput(MediaInputHandler):
    """Handler for local directory media playback."""

    def render_sidebar(self):
        """Render local directory info in sidebar.

        Returns:
            bool: True to indicate local directory mode is active
        """
        st.info("📂 **Local Directory Mode**\n\nSelect a folder in the main area to play files directly from your device.")
        return True

    def render_main_content(self, is_active):
        """Render the local directory player in the main content area.

        Args:
            is_active: Boolean from render_sidebar() indicating if mode is active
        """
        if not is_active:
            return

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
