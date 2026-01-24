"""Web media input handler."""
import streamlit as st
from .base import MediaInputHandler


class WebMediaInput(MediaInputHandler):
    """Handler for web-based media content."""

    def render_sidebar(self):
        """Render web media URL input in sidebar.

        Returns:
            str: The web URL entered by the user
        """
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

        return web_url

    def render_main_content(self, web_url):
        """Render the web media content in the main area.

        Args:
            web_url: The web URL from render_sidebar()
        """
        if not web_url:
            return

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
