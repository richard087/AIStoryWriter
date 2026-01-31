"""
Writer module.

This module contains all story generation and processing functionality.
When run from the repository, this package provides access to the core modules.
When installed as aistorywriter, use: from aistorywriter.writer import *
"""

# Import submodules to make them available
from . import Config
from . import PrintUtils
from . import Statistics
from . import Prompts
from . import LLMEditor
from . import OutlineGenerator
from . import StoryInfo
from . import NovelEditor
from . import Translator
from . import Scrubber

__all__ = [
    "Config",
    "PrintUtils",
    "Statistics",
    "Prompts",
    "LLMEditor",
    "OutlineGenerator",
    "StoryInfo",
    "NovelEditor",
    "Translator",
    "Scrubber",
]
