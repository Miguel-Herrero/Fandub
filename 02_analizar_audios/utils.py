#!/usr/bin/env python3
"""
Audio Analysis Utilities

This module provides utility functions for file handling, FFmpeg operations,
and common tasks used throughout the audio analysis system.
"""

import os
import json
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import logging

try:
    from .config import (
        SUPPORTED_EXTENSIONS, FFMPEG_TIMEOUT, FFMPEG_HIDE_BANNER,
        FFMPEG_NOSTATS, OUTPUT_FILES
    )
except ImportError:
    from config import (
        SUPPORTED_EXTENSIONS, FFMPEG_TIMEOUT, FFMPEG_HIDE_BANNER,
        FFMPEG_NOSTATS, OUTPUT_FILES
    )

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FFmpegError(Exception):
    """Custom exception for FFmpeg-related errors"""
    pass


def check_dependencies() -> Dict[str, bool]:
    """
    Check if required external dependencies are available.
    
    Returns:
        Dict with dependency names and their availability status
    """
    dependencies = {}
    
    # Check FFmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        dependencies['ffmpeg'] = result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        dependencies['ffmpeg'] = False
    
    # Check FFprobe
    try:
        result = subprocess.run(['ffprobe', '-version'], 
                              capture_output=True, text=True, timeout=10)
        dependencies['ffprobe'] = result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        dependencies['ffprobe'] = False
    
    return dependencies


def find_audio_files(directory: Path, extensions: List[str] = None) -> List[Path]:
    """
    Find all audio files in a directory.
    
    Args:
        directory: Directory to search in
        extensions: List of file extensions to look for
        
    Returns:
        List of Path objects for found audio files
    """
    if extensions is None:
        extensions = SUPPORTED_EXTENSIONS
    
    audio_files = []
    
    if not directory.exists():
        logger.error(f"Directory does not exist: {directory}")
        return audio_files
    
    for ext in extensions:
        pattern = f"*.{ext}"
        files = list(directory.glob(pattern))
        audio_files.extend(files)
    
    # Sort by name for consistent ordering
    audio_files.sort(key=lambda x: x.name.lower())
    
    logger.info(f"Found {len(audio_files)} audio files in {directory}")
    return audio_files


def clean_filename(filename: str) -> str:
    """
    Clean filename for use in directory names and safe file operations.
    
    Args:
        filename: Original filename
        
    Returns:
        Cleaned filename safe for filesystem use
    """
    # Remove extension
    name = Path(filename).stem
    
    # Replace problematic characters
    replacements = {
        ' ': '_',
        '(': '',
        ')': '',
        '[': '',
        ']': '',
        '{': '',
        '}': '',
        "'": '',
        '"': '',
        '&': 'and',
        '#': '',
        '%': '',
        '@': '',
        '!': '',
        '?': '',
        '*': '',
        '+': '',
        '=': '',
        '|': '',
        '\\': '',
        '/': '',
        ':': '',
        ';': '',
        '<': '',
        '>': '',
        ',': ''
    }
    
    for old, new in replacements.items():
        name = name.replace(old, new)
    
    # Remove multiple underscores
    while '__' in name:
        name = name.replace('__', '_')
    
    # Remove leading/trailing underscores
    name = name.strip('_')
    
    # Ensure it's not empty
    if not name:
        name = 'unnamed'
    
    return name


def run_ffmpeg_command(cmd: List[str], timeout: int = None) -> Tuple[int, str, str]:
    """
    Run an FFmpeg command with proper error handling.
    
    Args:
        cmd: Command list to execute
        timeout: Timeout in seconds
        
    Returns:
        Tuple of (return_code, stdout, stderr)
        
    Raises:
        FFmpegError: If command fails or times out
    """
    if timeout is None:
        timeout = FFMPEG_TIMEOUT
    
    try:
        logger.debug(f"Running FFmpeg command: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return result.returncode, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        raise FFmpegError(f"FFmpeg command timed out after {timeout} seconds")
    except FileNotFoundError:
        raise FFmpegError("FFmpeg not found. Please install FFmpeg.")
    except Exception as e:
        raise FFmpegError(f"Error running FFmpeg command: {e}")


def get_ffprobe_info(file_path: Path) -> Dict[str, Any]:
    """
    Extract technical information from audio/video file using ffprobe.
    
    Args:
        file_path: Path to the media file
        
    Returns:
        Dictionary with ffprobe information
        
    Raises:
        FFmpegError: If ffprobe fails
    """
    cmd = [
        'ffprobe',
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        str(file_path)
    ]
    
    returncode, stdout, stderr = run_ffmpeg_command(cmd)
    
    if returncode != 0:
        raise FFmpegError(f"ffprobe failed: {stderr}")
    
    try:
        return json.loads(stdout)
    except json.JSONDecodeError as e:
        raise FFmpegError(f"Failed to parse ffprobe JSON output: {e}")


def extract_ebu128_loudness(file_path: Path, output_file: Path) -> None:
    """
    Extract EBU R128 loudness measurements using FFmpeg.
    
    Args:
        file_path: Path to the audio file
        output_file: Path to save the EBU R128 output
        
    Raises:
        FFmpegError: If FFmpeg command fails
    """
    cmd = ['ffmpeg']
    
    if FFMPEG_HIDE_BANNER:
        cmd.extend(['-hide_banner'])
    
    if FFMPEG_NOSTATS:
        cmd.extend(['-nostats'])
    
    # Add input file
    cmd.extend(['-i', str(file_path)])
    
    # For video files, map only audio stream
    if file_path.suffix.lower() in ['.mp4', '.mkv', '.avi', '.mov']:
        cmd.extend(['-map', '0:a:0'])
    
    # Add EBU R128 filter and output
    cmd.extend([
        '-af', 'ebur128=peak=true',
        '-f', 'null',
        '-'
    ])
    
    returncode, stdout, stderr = run_ffmpeg_command(cmd)
    
    if returncode != 0:
        raise FFmpegError(f"EBU R128 analysis failed: {stderr}")
    
    # Write stderr to output file (EBU R128 data is in stderr)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(stderr)


def extract_audio_stats(file_path: Path, output_file: Path) -> None:
    """
    Extract detailed audio statistics using FFmpeg astats filter.
    
    Args:
        file_path: Path to the audio file
        output_file: Path to save the astats output
        
    Raises:
        FFmpegError: If FFmpeg command fails
    """
    cmd = ['ffmpeg']
    
    if FFMPEG_HIDE_BANNER:
        cmd.extend(['-hide_banner'])
    
    if FFMPEG_NOSTATS:
        cmd.extend(['-nostats'])
    
    # Add input file
    cmd.extend(['-i', str(file_path)])
    
    # For video files, map only audio stream
    if file_path.suffix.lower() in ['.mp4', '.mkv', '.avi', '.mov']:
        cmd.extend(['-map', '0:a:0'])
    
    # Add astats filter and output
    cmd.extend([
        '-af', 'astats',
        '-f', 'null',
        '-'
    ])
    
    returncode, stdout, stderr = run_ffmpeg_command(cmd)
    
    if returncode != 0:
        raise FFmpegError(f"Audio stats analysis failed: {stderr}")
    
    # Write stderr to output file (astats data is in stderr)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(stderr)


def create_ab_fragment(file_path: Path, output_file: Path, 
                      start_time: str, duration: int) -> None:
    """
    Create an A/B test fragment from an audio file.
    
    Args:
        file_path: Path to the source audio file
        output_file: Path to save the fragment
        start_time: Start time in HH:MM:SS format
        duration: Duration in seconds
        
    Raises:
        FFmpegError: If FFmpeg command fails
    """
    cmd = ['ffmpeg']
    
    if FFMPEG_HIDE_BANNER:
        cmd.extend(['-hide_banner'])
    
    if FFMPEG_NOSTATS:
        cmd.extend(['-nostats'])
    
    # Add input file with start time and duration
    cmd.extend([
        '-ss', start_time,
        '-i', str(file_path),
        '-t', str(duration)
    ])
    
    # For video files, extract only audio
    if file_path.suffix.lower() in ['.mp4', '.mkv', '.avi', '.mov']:
        cmd.extend(['-vn'])  # No video
    
    # Output as WAV for consistent A/B testing
    cmd.extend([
        '-acodec', 'pcm_s16le',
        '-ar', '48000',
        '-y',  # Overwrite output file
        str(output_file)
    ])
    
    returncode, stdout, stderr = run_ffmpeg_command(cmd)
    
    if returncode != 0:
        raise FFmpegError(f"A/B fragment creation failed: {stderr}")


def ensure_directory(path: Path) -> None:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path: Directory path to ensure exists
    """
    path.mkdir(parents=True, exist_ok=True)


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert a value to float.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Float value or default
    """
    if value in ['N/A', '', 'nan', None]:
        return default
    
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """
    Safely convert a value to int.
    
    Args:
        value: Value to convert
        default: Default value if conversion fails
        
    Returns:
        Integer value or default
    """
    try:
        if value in ['N/A', '', 'nan', None]:
            return default
        return int(float(value))
    except (ValueError, TypeError):
        return default
