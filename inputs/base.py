"""Base class for media input handlers."""
from abc import ABC, abstractmethod
import streamlit as st


class MediaInputHandler(ABC):
    """Abstract base class for different media input methods."""

    # Supported file types
    SUPPORTED_VIDEO = ['.mp4', '.webm', '.ogg', '.mov', '.avi']
    SUPPORTED_AUDIO = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
    SUPPORTED_IMAGE = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    SUPPORTED_DOCUMENT = ['.pdf', '.md', '.txt']
    ALL_SUPPORTED = SUPPORTED_VIDEO + SUPPORTED_AUDIO + SUPPORTED_IMAGE + SUPPORTED_DOCUMENT

    def __init__(self):
        """Initialize the handler."""
        pass

    @abstractmethod
    def render_sidebar(self):
        """Render the sidebar controls for this input method.

        Returns:
            Any data needed by render_main_content()
        """
        pass

    @abstractmethod
    def render_main_content(self, data):
        """Render the main content area for this input method.

        Args:
            data: Data returned from render_sidebar()
        """
        pass

    @staticmethod
    def get_media_type(file_extension):
        """Determine the media type from file extension.

        Args:
            file_extension: File extension (with or without dot)

        Returns:
            str: "Video", "Audio", or "Image"
        """
        ext = file_extension.lower()
        if not ext.startswith('.'):
            ext = '.' + ext

        if ext in MediaInputHandler.SUPPORTED_VIDEO:
            return "Video"
        elif ext in MediaInputHandler.SUPPORTED_AUDIO:
            return "Audio"
        elif ext in MediaInputHandler.SUPPORTED_IMAGE:
            return "Image"
        elif ext in MediaInputHandler.SUPPORTED_DOCUMENT:
            return "Document"
        return "Unknown"
