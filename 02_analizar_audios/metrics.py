#!/usr/bin/env python3
"""
Audio Metrics Extraction and Processing

This module handles the extraction and processing of audio quality metrics
from various sources including ffprobe, EBU R128, and astats.
"""

import re
import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging

try:
    from . import utils
    from .utils import safe_float, safe_int
    from .interpreters import (
        interpret_sample_rate, interpret_bit_rate, interpret_loudness,
        interpret_lra, interpret_true_peak, interpret_dc_offset,
        calculate_overall_quality_score, detect_problems
    )
except ImportError:
    import utils
    from utils import safe_float, safe_int
    from interpreters import (
        interpret_sample_rate, interpret_bit_rate, interpret_loudness,
        interpret_lra, interpret_true_peak, interpret_dc_offset,
        calculate_overall_quality_score, detect_problems
    )

logger = logging.getLogger(__name__)


class AudioMetrics:
    """Class to handle audio metrics extraction and interpretation."""
    
    def __init__(self, file_path: Path):
        """
        Initialize AudioMetrics for a specific file.
        
        Args:
            file_path: Path to the audio file
        """
        self.file_path = file_path
        self.raw_metrics = {}
        self.interpreted_metrics = {}
        self.problems = []
        self.overall_score = 0
    
    def extract_technical_info(self) -> Dict[str, Any]:
        """
        Extract technical information using ffprobe.
        
        Returns:
            Dictionary with technical information
        """
        try:
            ffprobe_data = utils.get_ffprobe_info(self.file_path)
            
            # Find audio stream
            audio_stream = None
            for stream in ffprobe_data.get('streams', []):
                if stream.get('codec_type') == 'audio':
                    audio_stream = stream
                    break
            
            if not audio_stream:
                logger.warning(f"No audio stream found in {self.file_path}")
                return {}
            
            # Extract basic info
            tech_info = {
                'codec': audio_stream.get('codec_name', 'unknown'),
                'sample_rate': safe_int(audio_stream.get('sample_rate', 0)),
                'channels': safe_int(audio_stream.get('channels', 0)),
                'bit_rate': safe_int(audio_stream.get('bit_rate', 0)),
                'duration': safe_float(audio_stream.get('duration', 0)),
                'format': ffprobe_data.get('format', {}).get('format_name', 'unknown')
            }
            
            # If bit_rate is not in stream, try format
            if tech_info['bit_rate'] == 0:
                format_bit_rate = ffprobe_data.get('format', {}).get('bit_rate')
                tech_info['bit_rate'] = safe_int(format_bit_rate)
            
            self.raw_metrics.update(tech_info)
            return tech_info
            
        except Exception as e:
            logger.error(f"Error extracting technical info from {self.file_path}: {e}")
            return {}
    
    def parse_ebu128_file(self, ebu128_file: Path) -> Dict[str, float]:
        """
        Parse EBU R128 loudness measurements from file.
        
        Args:
            ebu128_file: Path to EBU R128 output file
            
        Returns:
            Dictionary with loudness measurements
        """
        if not ebu128_file.exists():
            logger.warning(f"EBU R128 file not found: {ebu128_file}")
            return {}
        
        try:
            with open(ebu128_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse summary section
            summary_match = re.search(r'Summary:(.*?)(?=\[|$)', content, re.DOTALL)
            if not summary_match:
                logger.warning(f"No summary found in EBU R128 file: {ebu128_file}")
                return {}
            
            summary = summary_match.group(1)
            
            # Extract values using regex
            loudness_match = re.search(r'I:\s*(-?\d+\.?\d*)\s*LUFS', summary)
            lra_match = re.search(r'LRA:\s*(\d+\.?\d*)\s*LU', summary)
            peak_match = re.search(r'Peak:\s*(-?\d+\.?\d*)\s*dBFS', summary)
            
            ebu_metrics = {}
            
            if loudness_match:
                ebu_metrics['integrated_loudness'] = safe_float(loudness_match.group(1))
            
            if lra_match:
                ebu_metrics['lra'] = safe_float(lra_match.group(1))
            
            if peak_match:
                ebu_metrics['true_peak'] = safe_float(peak_match.group(1))
            
            self.raw_metrics.update(ebu_metrics)
            return ebu_metrics
            
        except Exception as e:
            logger.error(f"Error parsing EBU R128 file {ebu128_file}: {e}")
            return {}
    
    def parse_astats_file(self, astats_file: Path) -> Dict[str, float]:
        """
        Parse audio statistics from astats file.
        
        Args:
            astats_file: Path to astats output file
            
        Returns:
            Dictionary with audio statistics
        """
        if not astats_file.exists():
            logger.warning(f"Astats file not found: {astats_file}")
            return {}
        
        try:
            with open(astats_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            astats_metrics = {}
            
            # Extract RMS level (Overall)
            rms_match = re.search(r'RMS level dB:\s*(-?\d+\.?\d*)', content)
            if rms_match:
                astats_metrics['rms_level'] = safe_float(rms_match.group(1))
            
            # Extract Peak level (Overall)
            peak_match = re.search(r'Peak level dB:\s*(-?\d+\.?\d*)', content)
            if peak_match:
                astats_metrics['peak_level'] = safe_float(peak_match.group(1))
            
            # Extract DC offset (Overall)
            dc_match = re.search(r'DC offset:\s*(-?\d+\.?\d*)', content)
            if dc_match:
                astats_metrics['dc_offset'] = safe_float(dc_match.group(1))
            
            # Extract dynamic range
            dr_match = re.search(r'Dynamic range:\s*(\d+\.?\d*)', content)
            if dr_match:
                astats_metrics['dynamic_range'] = safe_float(dr_match.group(1))
            
            self.raw_metrics.update(astats_metrics)
            return astats_metrics
            
        except Exception as e:
            logger.error(f"Error parsing astats file {astats_file}: {e}")
            return {}
    
    def interpret_all_metrics(self) -> Dict[str, Any]:
        """
        Interpret all extracted metrics and calculate quality scores.
        
        Returns:
            Dictionary with interpreted metrics
        """
        interpreted = {}
        
        # Interpret sample rate
        if 'sample_rate' in self.raw_metrics:
            quality, emoji, score = interpret_sample_rate(self.raw_metrics['sample_rate'])
            interpreted.update({
                'sample_rate_quality': quality,
                'sample_rate_emoji': emoji,
                'sample_rate_score': score
            })
        
        # Interpret bit rate
        if 'bit_rate' in self.raw_metrics and 'codec' in self.raw_metrics:
            quality, emoji, score = interpret_bit_rate(
                self.raw_metrics['bit_rate'], 
                self.raw_metrics['codec']
            )
            interpreted.update({
                'bit_rate_quality': quality,
                'bit_rate_emoji': emoji,
                'bit_rate_score': score
            })
        
        # Interpret loudness
        if 'integrated_loudness' in self.raw_metrics:
            quality, emoji, score = interpret_loudness(self.raw_metrics['integrated_loudness'])
            interpreted.update({
                'loudness_quality': quality,
                'loudness_emoji': emoji,
                'loudness_score': score
            })
        
        # Interpret LRA
        if 'lra' in self.raw_metrics:
            quality, emoji, score = interpret_lra(self.raw_metrics['lra'])
            interpreted.update({
                'lra_quality': quality,
                'lra_emoji': emoji,
                'lra_score': score
            })
        
        # Interpret true peak
        if 'true_peak' in self.raw_metrics:
            quality, emoji, score = interpret_true_peak(self.raw_metrics['true_peak'])
            interpreted.update({
                'true_peak_quality': quality,
                'true_peak_emoji': emoji,
                'true_peak_score': score
            })
        
        # Interpret DC offset
        if 'dc_offset' in self.raw_metrics:
            quality, emoji, score = interpret_dc_offset(self.raw_metrics['dc_offset'])
            interpreted.update({
                'dc_offset_quality': quality,
                'dc_offset_emoji': emoji,
                'dc_offset_score': score
            })
        
        # Calculate overall score
        combined_metrics = {**self.raw_metrics, **interpreted}
        self.overall_score = calculate_overall_quality_score(combined_metrics)
        interpreted['overall_score'] = self.overall_score
        
        # Detect problems
        self.problems = detect_problems(combined_metrics)
        interpreted['problems'] = self.problems
        
        self.interpreted_metrics = interpreted
        return interpreted
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a complete summary of all metrics.
        
        Returns:
            Dictionary with complete metrics summary
        """
        return {
            'file_path': str(self.file_path),
            'filename': self.file_path.name,
            'raw_metrics': self.raw_metrics,
            'interpreted_metrics': self.interpreted_metrics,
            'overall_score': self.overall_score,
            'problems': self.problems
        }
    
    def format_bit_rate_display(self) -> str:
        """Format bit rate for display."""
        bit_rate = self.raw_metrics.get('bit_rate', 0)
        if bit_rate > 0:
            return f"{bit_rate // 1000}kbps"
        return "N/A"
    
    def format_duration_display(self) -> str:
        """Format duration for display."""
        duration = self.raw_metrics.get('duration', 0)
        if duration > 0:
            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            if hours > 0:
                return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                return f"{minutes:02d}:{seconds:02d}"
        return "N/A"
