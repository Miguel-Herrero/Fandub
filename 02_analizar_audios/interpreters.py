#!/usr/bin/env python3
"""
Audio Metrics Interpreters

This module provides functions to interpret audio quality metrics
and assign quality ratings with emojis based on predefined ranges.
"""

from typing import Tuple, Optional
import logging

try:
    from .config import (
        SAMPLE_RATE_RANGES, BIT_RATE_RANGES, LOUDNESS_RANGES,
        LRA_RANGES, TRUE_PEAK_RANGES, DC_OFFSET_RANGES,
        EMOJI_MAP, QUALITY_SCORES
    )
    from .utils import safe_float, safe_int
except ImportError:
    from config import (
        SAMPLE_RATE_RANGES, BIT_RATE_RANGES, LOUDNESS_RANGES,
        LRA_RANGES, TRUE_PEAK_RANGES, DC_OFFSET_RANGES,
        EMOJI_MAP, QUALITY_SCORES
    )
    from utils import safe_float, safe_int

logger = logging.getLogger(__name__)


def interpret_sample_rate(sample_rate: int) -> Tuple[str, str, int]:
    """
    Interpret sample rate quality.
    
    Args:
        sample_rate: Sample rate in Hz
        
    Returns:
        Tuple of (quality_level, emoji, score)
    """
    sr = safe_int(sample_rate)
    
    for quality, (min_val, max_val) in SAMPLE_RATE_RANGES.items():
        if min_val <= sr <= max_val:
            emoji = EMOJI_MAP.get(quality, '❓')
            score = QUALITY_SCORES.get(quality, 50)
            return quality, emoji, score
    
    # Fallback
    return 'poor', EMOJI_MAP['poor'], QUALITY_SCORES['poor']


def interpret_bit_rate(bit_rate: int, codec: str) -> Tuple[str, str, int]:
    """
    Interpret bit rate quality based on codec.
    
    Args:
        bit_rate: Bit rate in bps
        codec: Audio codec name
        
    Returns:
        Tuple of (quality_level, emoji, score)
    """
    br = safe_int(bit_rate)
    codec_lower = codec.lower()
    
    # Get appropriate ranges for codec
    ranges = BIT_RATE_RANGES.get(codec_lower, BIT_RATE_RANGES['default'])
    
    for quality, (min_val, max_val) in ranges.items():
        if min_val <= br <= max_val:
            emoji = EMOJI_MAP.get(quality, '❓')
            score = QUALITY_SCORES.get(quality, 50)
            return quality, emoji, score
    
    # Fallback
    return 'poor', EMOJI_MAP['poor'], QUALITY_SCORES['poor']


def interpret_loudness(loudness: float) -> Tuple[str, str, int]:
    """
    Interpret integrated loudness (LUFS) quality.
    
    Args:
        loudness: Integrated loudness in LUFS
        
    Returns:
        Tuple of (quality_level, emoji, score)
    """
    lufs = safe_float(loudness)
    
    # Check each range in order of preference
    for quality, (min_val, max_val) in LOUDNESS_RANGES.items():
        if min_val <= lufs <= max_val:
            emoji = EMOJI_MAP.get(quality, '❓')
            score = QUALITY_SCORES.get(quality, 50)
            return quality, emoji, score
    
    # Fallback
    return 'poor', EMOJI_MAP['poor'], QUALITY_SCORES['poor']


def interpret_lra(lra: float) -> Tuple[str, str, int]:
    """
    Interpret Loudness Range (LRA) quality.
    
    Args:
        lra: Loudness Range in LU
        
    Returns:
        Tuple of (quality_level, emoji, score)
    """
    lra_val = safe_float(lra)
    
    for quality, (min_val, max_val) in LRA_RANGES.items():
        if min_val <= lra_val <= max_val:
            emoji = EMOJI_MAP.get(quality, '❓')
            score = QUALITY_SCORES.get(quality, 50)
            return quality, emoji, score
    
    # Fallback
    return 'poor', EMOJI_MAP['poor'], QUALITY_SCORES['poor']


def interpret_true_peak(true_peak: float) -> Tuple[str, str, int]:
    """
    Interpret True Peak quality.
    
    Args:
        true_peak: True Peak in dBFS
        
    Returns:
        Tuple of (quality_level, emoji, score)
    """
    tp = safe_float(true_peak)
    
    for quality, (min_val, max_val) in TRUE_PEAK_RANGES.items():
        if min_val <= tp <= max_val:
            emoji = EMOJI_MAP.get(quality, '❓')
            score = QUALITY_SCORES.get(quality, 50)
            return quality, emoji, score
    
    # Fallback
    return 'poor', EMOJI_MAP['poor'], QUALITY_SCORES['poor']


def interpret_dc_offset(dc_offset: float) -> Tuple[str, str, int]:
    """
    Interpret DC Offset quality.
    
    Args:
        dc_offset: DC Offset (absolute value)
        
    Returns:
        Tuple of (quality_level, emoji, score)
    """
    dc = abs(safe_float(dc_offset))
    
    for quality, (min_val, max_val) in DC_OFFSET_RANGES.items():
        if min_val <= dc <= max_val:
            emoji = EMOJI_MAP.get(quality, '❓')
            score = QUALITY_SCORES.get(quality, 50)
            return quality, emoji, score
    
    # Fallback
    return 'poor', EMOJI_MAP['poor'], QUALITY_SCORES['poor']


def calculate_overall_quality_score(metrics: dict, weights: dict = None) -> int:
    """
    Calculate overall quality score based on individual metrics.
    
    Args:
        metrics: Dictionary with metric interpretations
        weights: Optional custom weights for metrics
        
    Returns:
        Overall quality score (0-100)
    """
    try:
        from .config import SCORING_WEIGHTS
    except ImportError:
        from config import SCORING_WEIGHTS
    
    if weights is None:
        weights = SCORING_WEIGHTS
    
    total_score = 0.0
    total_weight = 0.0
    
    # Map metric names to their scores
    metric_scores = {
        'sample_rate': metrics.get('sample_rate_score', 50),
        'bit_rate': metrics.get('bit_rate_score', 50),
        'loudness': metrics.get('loudness_score', 50),
        'lra': metrics.get('lra_score', 50),
        'true_peak': metrics.get('true_peak_score', 50),
        'dc_offset': metrics.get('dc_offset_score', 50)
    }
    
    for metric, score in metric_scores.items():
        weight = weights.get(metric, 0.0)
        total_score += score * weight
        total_weight += weight
    
    if total_weight == 0:
        return 50  # Default score if no weights
    
    return int(round(total_score / total_weight))


def detect_problems(metrics: dict) -> list:
    """
    Detect potential problems based on metric interpretations.
    
    Args:
        metrics: Dictionary with metric interpretations
        
    Returns:
        List of problem descriptions
    """
    problems = []
    
    # Check for poor quality metrics
    if metrics.get('sample_rate_quality') == 'poor':
        sr = metrics.get('sample_rate', 0)
        problems.append(f"⚠️ Sample rate muy bajo: {sr}Hz")
    
    if metrics.get('bit_rate_quality') == 'poor':
        br = metrics.get('bit_rate', 0) // 1000
        problems.append(f"⚠️ Bit rate muy bajo: {br}kbps")
    
    if metrics.get('loudness_quality') in ['very_high', 'very_low']:
        lufs = metrics.get('loudness', 0)
        if metrics.get('loudness_quality') == 'very_high':
            problems.append(f"⚠️ Loudness muy alto: {lufs} LUFS (posible limitación)")
        else:
            problems.append(f"⚠️ Loudness muy bajo: {lufs} LUFS (posibles problemas de grabación)")
    
    if metrics.get('true_peak_quality') == 'poor':
        tp = metrics.get('true_peak', 0)
        problems.append(f"⚠️ True Peak con clipping: {tp} dBFS")
    
    if metrics.get('dc_offset_quality') == 'poor':
        dc = metrics.get('dc_offset', 0)
        problems.append(f"⚠️ DC Offset alto: {dc}")
    
    if metrics.get('lra_quality') == 'poor':
        lra = metrics.get('lra', 0)
        problems.append(f"⚠️ Rango dinámico muy limitado: {lra} LU")
    
    return problems


def get_quality_summary(problems: list) -> str:
    """
    Generate a quality summary based on detected problems.
    
    Args:
        problems: List of problem descriptions
        
    Returns:
        Summary string
    """
    if not problems:
        return "**Sin problemas detectados**"
    
    if len(problems) == 1:
        return f"**Problema detectado:**\n- {problems[0]}"
    
    problem_list = "\n- ".join(problems)
    return f"**Problemas detectados:**\n- {problem_list}"


def format_metric_with_emoji(value: any, emoji: str, unit: str = "") -> str:
    """
    Format a metric value with its emoji for display.
    
    Args:
        value: The metric value
        emoji: The emoji to display
        unit: Optional unit string
        
    Returns:
        Formatted string with emoji and value
    """
    return f"{emoji} {value}{unit}"
