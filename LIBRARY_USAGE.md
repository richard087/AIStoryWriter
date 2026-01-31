# AIStoryWriter Library Usage Guide

This document explains how to use AIStoryWriter as an installable library and the new command-line interface.

## Installation

### Development Installation

To install AIStoryWriter in editable mode for development:

```bash
pip install -e .
```

This installs the package in development mode, allowing you to make changes to the code and see them reflected immediately.

### Standard Installation

To install AIStoryWriter as a regular package:

```bash
pip install .
```

Or from PyPI (when available):

```bash
pip install aistorywriter
```

## Using the Library

After installation, you can import and use AIStoryWriter in your Python code:

### Basic Import

```python
from aistorywriter import writer

# Access configuration
print(writer.Config.INITIAL_OUTLINE_WRITER_MODEL)

# Import specific modules
from aistorywriter.writer import Config, PrintUtils, Statistics
```

### Using the Statistics Module

```python
from aistorywriter.writer import Statistics

# Count words in text
text = "The quick brown fox jumps over the lazy dog"
word_count = Statistics.GetWordCount(text)
print(f"Word count: {word_count}")
```

### Using the Logger

```python
from aistorywriter.writer import PrintUtils

# Create a logger instance
logger = PrintUtils.Logger()

# Log messages at different levels
logger.Log("This is info", 5)      # Green
logger.Log("This is debug", 2)     # Blue
logger.Log("This is warning", 6)   # Yellow
logger.Log("This is error", 7)     # Red

# Save stories and debug information
logger.SaveStory("Once upon a time...")
logger.SaveLangchain("my_chain", [
    {"role": "user", "content": "Generate a story"},
    {"role": "assistant", "content": "Once upon a time..."}
])
```

### Configuring Models

```python
from aistorywriter import writer

# Modify configuration at runtime
writer.Config.SEED = 42
writer.Config.INITIAL_OUTLINE_WRITER_MODEL = "google://gemini-1.5-pro"
writer.Config.CHAPTER_STAGE1_WRITER_MODEL = "ollama://llama3:70b@localhost:11434"
```

## Command-Line Interface

After installation, two CLI commands are available:

### Main Command

```bash
aistorywriter -Prompt path/to/prompt.txt [options]
```

### Dedicated Write Command

```bash
aistorywriter-write -Prompt path/to/prompt.txt [options]
```

### Common Options

```bash
# Specify output file path
aistorywriter-write -Prompt prompt.txt -Output Stories/my_story.md

# Use specific models
aistorywriter-write -Prompt prompt.txt \
  -InitialOutlineModel "google://gemini-1.5-pro" \
  -ChapterOutlineModel "ollama://llama3:70b" \
  -ChapterS1Model "ollama://mistral:7b"

# Set seed for reproducibility
aistorywriter-write -Prompt prompt.txt -Seed 12345

# Enable debug mode to see system prompts
aistorywriter-write -Prompt prompt.txt -Debug

# Translate story to another language
aistorywriter-write -Prompt prompt.txt -Translate "French"

# Disable chapter scrubbing
aistorywriter-write -Prompt prompt.txt -NoScrubChapters
```

### For Complete Option Reference

```bash
aistorywriter-write --help
```

## Backward Compatibility

The original `./Write.py` script continues to work exactly as before:

```bash
./Write.py -Prompt ExamplePrompts/Example1/Prompt.txt
```

This is maintained for backward compatibility and existing workflows.

## Package Structure

```
AIStoryWriter/
├── src/aistorywriter/              # Main package source
│   ├── __init__.py
│   ├── cli.py                      # CLI entry points
│   └── writer/                     # Core writing modules
│       ├── Config.py              # Configuration
│       ├── PrintUtils.py          # Logging utilities
│       ├── Statistics.py          # Text analysis
│       ├── Prompts.py             # System prompts
│       ├── OutlineGenerator.py    # Outline generation
│       └── ...
├── Writer/                        # Compatibility shim (old location)
├── Write.py                       # Original CLI script (still works)
├── pyproject.toml                 # Package configuration
├── MANIFEST.in                    # Data files inclusion
└── README.md                      # Main documentation
```

## Module Reference

### `aistorywriter.writer.Config`

Module-level configuration variables that control story generation behavior.

**Key Variables:**
- `SEED` - Random seed for model reproducibility
- `INITIAL_OUTLINE_WRITER_MODEL` - Model for initial outline
- `CHAPTER_OUTLINE_WRITER_MODEL` - Model for chapter outlines
- `CHAPTER_STAGE1/2/3/4_WRITER_MODEL` - Models for different stages
- `REVISION_MODEL` - Model for revisions
- `EVAL_MODEL` - Model for quality evaluation
- `TRANSLATE_LANGUAGE` - Target language for translation

### `aistorywriter.writer.PrintUtils`

Logging and file output utilities.

**Main Classes:**
- `Logger` - Comprehensive logging with colored output and file persistence

**Functions:**
- `PrintMessageHistory(messages)` - Print formatted message history

### `aistorywriter.writer.Statistics`

Text analysis utilities.

**Functions:**
- `GetWordCount(text)` - Count words in text

### `aistorywriter.writer.Prompts`

System prompts used for story generation.

### Other Modules

- `OutlineGenerator` - Generate story outlines
- `LLMEditor` - Edit content using LLM
- `NovelEditor` - Edit full novels
- `Translator` - Translate content
- `Scrubber` - Clean up generated content
- `StoryInfo` - Extract story information
- `Chapter` - Chapter-specific generation
- `Outline` - Outline manipulation
- `Scene` - Scene-based generation
- `Interface` - LLM provider interfaces (Ollama, Google, OpenRouter)

## Migration Guide

### From Direct File Import

**Old way (still works):**
```python
from Writer import Config, PrintUtils
```

**New recommended way:**
```python
from aistorywriter.writer import Config, PrintUtils
```

### From Script Execution

**Old way (still works):**
```bash
./Write.py -Prompt prompt.txt
```

**New recommended way:**
```bash
aistorywriter-write -Prompt prompt.txt
```

**Or if installed:**
```bash
pip install -e .
aistorywriter-write -Prompt prompt.txt
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Installing Development Dependencies

```bash
pip install -e ".[dev]"
```

### Building Distribution

```bash
python -m build
```

### Publishing to PyPI

```bash
twine upload dist/*
```

## Support

For issues, questions, or contributions:

- 🐛 **Report Bugs**: [GitHub Issues](https://github.com/datacrystals/AIStoryWriter/issues)
- 💡 **Discuss Ideas**: [GitHub Discussions](https://github.com/datacrystals/AIStoryWriter/discussions)
- 💬 **Chat Live**: [Discord Server](https://discord.gg/R2SySWDr2s)
- 🖊️ **Contribute**: [Submit a Pull Request](https://github.com/datacrystals/AIStoryWriter/pulls)

## License

AIStoryWriter is licensed under the AGPL-3.0 license. See LICENSE file for details.
