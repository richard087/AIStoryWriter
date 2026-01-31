"""
Command-line interface for AIStoryWriter.

This module provides the CLI entry points for the AIStoryWriter package.
"""

import argparse
import time
import datetime
import os
import json
import sys

from . import writer


def create_write_parser():
    """Create argument parser for the write command."""
    parser = argparse.ArgumentParser(
        prog="aistorywriter-write",
        description="Generate a full story using AI models"
    )
    
    parser.add_argument("-Prompt", help="Path to file containing the prompt")
    parser.add_argument(
        "-Output",
        default="",
        type=str,
        help="Optional file output path, if none is specified, we will autogenerate a file name based on the story title",
    )
    parser.add_argument(
        "-InitialOutlineModel",
        default=writer.Config.INITIAL_OUTLINE_WRITER_MODEL,
        type=str,
        help="Model to use for writing the base outline content",
    )
    parser.add_argument(
        "-ChapterOutlineModel",
        default=writer.Config.CHAPTER_OUTLINE_WRITER_MODEL,
        type=str,
        help="Model to use for writing the per-chapter outline content",
    )
    parser.add_argument(
        "-ChapterS1Model",
        default=writer.Config.CHAPTER_STAGE1_WRITER_MODEL,
        type=str,
        help="Model to use for writing the chapter (stage 1: plot)",
    )
    parser.add_argument(
        "-ChapterS2Model",
        default=writer.Config.CHAPTER_STAGE2_WRITER_MODEL,
        type=str,
        help="Model to use for writing the chapter (stage 2: dialogue)",
    )
    parser.add_argument(
        "-ChapterS3Model",
        default=writer.Config.CHAPTER_STAGE3_WRITER_MODEL,
        type=str,
        help="Model to use for writing the chapter (stage 3: descriptions)",
    )
    parser.add_argument(
        "-ChapterS4Model",
        default=writer.Config.CHAPTER_STAGE4_WRITER_MODEL,
        type=str,
        help="Model to use for writing the chapter (stage 4: final pass)",
    )
    parser.add_argument(
        "-ChapterRevisionModel",
        default=writer.Config.CHAPTER_REVISION_WRITER_MODEL,
        type=str,
        help="Model to use for revising chapter content",
    )
    parser.add_argument(
        "-RevisionModel",
        default=writer.Config.REVISION_MODEL,
        type=str,
        help="Model to use for story revision",
    )
    parser.add_argument(
        "-EvalModel",
        default=writer.Config.EVAL_MODEL,
        type=str,
        help="Model to use for evaluating story quality",
    )
    parser.add_argument(
        "-InfoModel",
        default=writer.Config.INFO_MODEL,
        type=str,
        help="Model to use for extracting story information",
    )
    parser.add_argument(
        "-ScrubModel",
        default=writer.Config.SCRUB_MODEL,
        type=str,
        help="Model to use for scrubbing content",
    )
    parser.add_argument(
        "-CheckerModel",
        default=writer.Config.CHECKER_MODEL,
        type=str,
        help="Model used to check results",
    )
    parser.add_argument(
        "-TranslatorModel",
        default=writer.Config.TRANSLATOR_MODEL,
        type=str,
        help="Model to use if translation of the story is enabled",
    )
    parser.add_argument(
        "-Translate",
        default="",
        type=str,
        help="Specify a language to translate the story to - will not translate by default. Ex: 'French'",
    )
    parser.add_argument(
        "-TranslatePrompt",
        default="",
        type=str,
        help="Specify a language to translate your input prompt to. Ex: 'French'",
    )
    parser.add_argument("-Seed", default=12, type=int, help="Used to seed models.")
    parser.add_argument(
        "-OutlineMinRevisions",
        default=0,
        type=int,
        help="Number of minimum revisions that the outline must be given prior to proceeding",
    )
    parser.add_argument(
        "-OutlineMaxRevisions",
        default=3,
        type=int,
        help="Max number of revisions that the outline may have",
    )
    parser.add_argument(
        "-ChapterMinRevisions",
        default=0,
        type=int,
        help="Number of minimum revisions that the chapter must be given prior to proceeding",
    )
    parser.add_argument(
        "-ChapterMaxRevisions",
        default=3,
        type=int,
        help="Max number of revisions that the chapter may have",
    )
    parser.add_argument(
        "-NoChapterRevision", action="store_true", help="Disables Chapter Revisions"
    )
    parser.add_argument(
        "-NoScrubChapters",
        action="store_true",
        help="Disables a final pass over the story to remove prompt leftovers/outline tidbits",
    )
    parser.add_argument(
        "-ExpandOutline",
        action="store_true",
        default=True,
        help="Disables the system from expanding the outline for the story chapter by chapter prior to writing the story's chapter content",
    )
    parser.add_argument(
        "-EnableFinalEditPass",
        action="store_true",
        help="Enable a final edit pass of the whole story prior to scrubbing",
    )
    parser.add_argument(
        "-Debug",
        action="store_true",
        help="Print system prompts to stdout during generation",
    )
    parser.add_argument(
        "-SceneGenerationPipeline",
        action="store_true",
        default=True,
        help="Use the new scene-by-scene generation pipeline as an initial starting point for chapter writing",
    )
    
    return parser


def apply_write_args(args):
    """Apply parsed arguments to the writer configuration."""
    writer.Config.SEED = args.Seed
    writer.Config.INITIAL_OUTLINE_WRITER_MODEL = args.InitialOutlineModel
    writer.Config.CHAPTER_OUTLINE_WRITER_MODEL = args.ChapterOutlineModel
    writer.Config.CHAPTER_STAGE1_WRITER_MODEL = args.ChapterS1Model
    writer.Config.CHAPTER_STAGE2_WRITER_MODEL = args.ChapterS2Model
    writer.Config.CHAPTER_STAGE3_WRITER_MODEL = args.ChapterS3Model
    writer.Config.CHAPTER_STAGE4_WRITER_MODEL = args.ChapterS4Model
    writer.Config.CHAPTER_REVISION_WRITER_MODEL = args.ChapterRevisionModel
    writer.Config.EVAL_MODEL = args.EvalModel
    writer.Config.REVISION_MODEL = args.RevisionModel
    writer.Config.INFO_MODEL = args.InfoModel
    writer.Config.SCRUB_MODEL = args.ScrubModel
    writer.Config.CHECKER_MODEL = args.CheckerModel
    writer.Config.TRANSLATOR_MODEL = args.TranslatorModel
    writer.Config.TRANSLATE_LANGUAGE = args.Translate
    writer.Config.TRANSLATE_PROMPT_LANGUAGE = args.TranslatePrompt
    writer.Config.OUTLINE_MIN_REVISIONS = args.OutlineMinRevisions
    writer.Config.OUTLINE_MAX_REVISIONS = args.OutlineMaxRevisions
    writer.Config.CHAPTER_MIN_REVISIONS = args.ChapterMinRevisions
    writer.Config.CHAPTER_MAX_REVISIONS = args.ChapterMaxRevisions
    writer.Config.CHAPTER_NO_REVISIONS = args.NoChapterRevision
    writer.Config.SCRUB_NO_SCRUB = args.NoScrubChapters
    writer.Config.EXPAND_OUTLINE = args.ExpandOutline
    writer.Config.ENABLE_FINAL_EDIT_PASS = args.EnableFinalEditPass
    writer.Config.DEBUG = args.Debug
    writer.Config.SCENE_GENERATION_PIPELINE = args.SceneGenerationPipeline
    if args.Output:
        writer.Config.OPTIONAL_OUTPUT_NAME = args.Output


def main_write():
    """Entry point for the aistorywriter-write command."""
    parser = create_write_parser()
    args = parser.parse_args()
    
    if not args.Prompt:
        parser.error("The -Prompt argument is required")
    
    apply_write_args(args)
    run_write(args.Prompt)


def run_write(prompt_path):
    """Execute the story writing process."""
    start_time = time.time()
    
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()
    
    logger = writer.PrintUtils.Logger()
    logger.Log("Starting Story Generation", 5)
    logger.Log(f"Prompt: {prompt[:100]}...", 3)
    
    # The actual generation logic would go here
    # This is a minimal implementation to show structure
    logger.Log("Story generation complete", 5)
    
    elapsed = time.time() - start_time
    logger.Log(f"Generation took {elapsed:.2f} seconds", 3)


def main():
    """Main entry point for CLI."""
    main_write()


if __name__ == "__main__":
    main()
