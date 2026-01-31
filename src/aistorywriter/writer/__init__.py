"""
Writer module for AIStoryWriter.

Core module containing all story generation and processing functionality.
"""

from . import Config
from . import PrintUtils
from . import Statistics
from . import Prompts

# Also expose with lowercase names for consistency
config = Config
printutils = PrintUtils
statistics = Statistics
prompts = Prompts

__all__ = [
    "Config",
    "PrintUtils",
    "Statistics",
    "Prompts",
    "config",
    "printutils",
    "statistics",
    "prompts",
]
