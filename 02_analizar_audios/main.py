#!/usr/bin/env python3
"""
Audio Quality Analyzer - Main CLI Interface

Command-line interface for the audio quality analysis system.
Provides comprehensive analysis of audio files for dubbing workflows.
"""

import argparse
import sys
import logging
from pathlib import Path
from typing import List, Optional

from . import AudioAnalyzer, ReportGenerator, SUPPORTED_EXTENSIONS, DEFAULT_OUTPUT_DIR
from .config import DEFAULT_FRAGMENT_DURATION, DEFAULT_FRAGMENT_START
from . import utils

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def setup_argument_parser() -> argparse.ArgumentParser:
    """Set up command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Audio Quality Analyzer for Dubbing Workflows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all audio files in a directory
  python -m audio_analyzer -i /path/to/audio/files
  
  # Analyze specific files
  python -m audio_analyzer -f file1.mp3 file2.wav
  
  # Custom output directory and fragment settings
  python -m audio_analyzer -i samples -o analysis_results -t 45 -s 00:01:00
  
  # Disable parallel processing
  python -m audio_analyzer -i samples --no-parallel
  
Supported formats: """ + ", ".join(SUPPORTED_EXTENSIONS)
    )
    
    # Input options (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '-i', '--input-dir',
        type=str,
        help='Directory containing audio files to analyze'
    )
    input_group.add_argument(
        '-f', '--files',
        nargs='+',
        type=str,
        help='Specific audio files to analyze'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=DEFAULT_OUTPUT_DIR,
        help=f'Output directory for analysis results (default: {DEFAULT_OUTPUT_DIR})'
    )
    
    # Fragment options
    parser.add_argument(
        '-t', '--fragment-duration',
        type=int,
        default=DEFAULT_FRAGMENT_DURATION,
        help=f'Duration of A/B test fragments in seconds (default: {DEFAULT_FRAGMENT_DURATION})'
    )
    parser.add_argument(
        '-s', '--fragment-start',
        type=str,
        default=DEFAULT_FRAGMENT_START,
        help=f'Start time for A/B fragments in HH:MM:SS format (default: {DEFAULT_FRAGMENT_START})'
    )
    
    # Processing options
    parser.add_argument(
        '--no-parallel',
        action='store_true',
        help='Disable parallel processing (process files sequentially)'
    )
    parser.add_argument(
        '--extensions',
        nargs='+',
        type=str,
        default=SUPPORTED_EXTENSIONS,
        help='File extensions to include (default: all supported)'
    )
    
    # Output options
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress console output except errors'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser


def validate_arguments(args) -> bool:
    """
    Validate command line arguments.
    
    Args:
        args: Parsed arguments
        
    Returns:
        True if arguments are valid, False otherwise
    """
    # Validate input directory
    if args.input_dir:
        input_path = Path(args.input_dir)
        if not input_path.exists():
            logger.error(f"Input directory does not exist: {input_path}")
            return False
        if not input_path.is_dir():
            logger.error(f"Input path is not a directory: {input_path}")
            return False
    
    # Validate input files
    if args.files:
        for file_path in args.files:
            path = Path(file_path)
            if not path.exists():
                logger.error(f"Input file does not exist: {path}")
                return False
            if not path.is_file():
                logger.error(f"Input path is not a file: {path}")
                return False
    
    # Validate fragment duration
    if args.fragment_duration <= 0:
        logger.error("Fragment duration must be positive")
        return False
    
    # Validate fragment start time format
    import re
    time_pattern = r'^(\d{1,2}):(\d{2}):(\d{2})$'
    if not re.match(time_pattern, args.fragment_start):
        logger.error("Fragment start time must be in HH:MM:SS format")
        return False
    
    return True


def main() -> int:
    """
    Main entry point for the CLI application.
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    # Parse arguments
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # Set up logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate arguments
    if not validate_arguments(args):
        return 1
    
    # Check dependencies
    print("🎵 Audio Quality Analyzer")
    print("=" * 50)
    
    deps = utils.check_dependencies()
    if not deps.get('ffmpeg'):
        logger.error("FFmpeg not found. Please install FFmpeg.")
        return 1
    if not deps.get('ffprobe'):
        logger.error("FFprobe not found. Please install FFmpeg.")
        return 1
    
    try:
        # Initialize analyzer
        analyzer = AudioAnalyzer(
            output_dir=args.output,
            fragment_duration=args.fragment_duration,
            fragment_start=args.fragment_start,
            parallel=not args.no_parallel
        )
        
        # Determine files to analyze
        if args.input_dir:
            print(f"📁 Analyzing directory: {args.input_dir}")
            print(f"🔍 Extensions: {', '.join(args.extensions)}")
            
            input_path = Path(args.input_dir)
            results = analyzer.analyze_directory(input_path, args.extensions)
        else:
            print(f"📄 Analyzing {len(args.files)} files")
            
            file_paths = [Path(f) for f in args.files]
            results = analyzer.analyze_files(file_paths)
        
        if not results:
            logger.error("No files were analyzed successfully")
            return 1
        
        # Generate report
        print("\n📊 Generating report...")
        report_generator = ReportGenerator(results, analyzer.output_dir)
        report_file = report_generator.generate_markdown_report()
        
        if report_file:
            print(f"✅ Report generated: {report_file}")
        else:
            logger.error("Failed to generate report")
            return 1
        
        # Print summary
        if not args.quiet:
            report_generator.print_console_summary()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
