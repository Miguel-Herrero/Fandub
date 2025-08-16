#!/usr/bin/env python3
"""
Audio Quality Analyzer Package

A comprehensive audio quality analysis tool for dubbing workflows.
Analyzes audio files and provides quality metrics, recommendations,
and A/B test fragments for comparison.
"""

__version__ = "2.0.0"
__author__ = "Audio Analysis System"
__description__ = "Audio Quality Analyzer for Dubbing Workflows"

from .analyzer import AudioAnalyzer
from .metrics import AudioMetrics
from .reporters import ReportGenerator
from .config import SUPPORTED_EXTENSIONS, DEFAULT_OUTPUT_DIR

__all__ = [
    'AudioAnalyzer',
    'AudioMetrics', 
    'ReportGenerator',
    'SUPPORTED_EXTENSIONS',
    'DEFAULT_OUTPUT_DIR'
]
