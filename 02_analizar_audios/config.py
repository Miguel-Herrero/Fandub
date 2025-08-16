#!/usr/bin/env python3
"""
Audio Analysis Configuration

This module contains all configuration parameters for audio quality analysis,
including interpretation ranges, thresholds, and default settings.
"""

# Supported audio file extensions
SUPPORTED_EXTENSIONS = [
    'mp3', 'mp4', 'wav', 'flac', 'aac', 'm4a', 'mkv', 'avi', 'mov'
]

# Default analysis settings
DEFAULT_FRAGMENT_DURATION = 30  # seconds
DEFAULT_FRAGMENT_START = "00:00:10"  # HH:MM:SS format
DEFAULT_OUTPUT_DIR = "_analysis"

# FFmpeg settings
FFMPEG_TIMEOUT = 300  # seconds
FFMPEG_HIDE_BANNER = True
FFMPEG_NOSTATS = True

# Quality scoring weights
SCORING_WEIGHTS = {
    'sample_rate': 0.15,
    'bit_rate': 0.25,
    'loudness': 0.20,
    'lra': 0.15,
    'true_peak': 0.15,
    'dc_offset': 0.10
}

# Sample Rate interpretation ranges (Hz)
SAMPLE_RATE_RANGES = {
    'excellent': (48000, float('inf')),  # ≥48kHz
    'good': (44100, 47999),              # 44.1-47.9kHz
    'acceptable': (32000, 44099),        # 32-44kHz
    'poor': (0, 31999)                   # <32kHz
}

# Bit Rate interpretation ranges (bps) by codec
BIT_RATE_RANGES = {
    'mp3': {
        'excellent': (320000, float('inf')),
        'good': (256000, 319999),
        'acceptable': (192000, 255999),
        'poor': (0, 191999)
    },
    'aac': {
        'excellent': (256000, float('inf')),
        'good': (192000, 255999),
        'acceptable': (128000, 191999),
        'poor': (0, 127999)
    },
    'default': {  # For lossless or unknown codecs
        'excellent': (1000000, float('inf')),
        'good': (500000, 999999),
        'acceptable': (200000, 499999),
        'poor': (0, 199999)
    }
}

# Integrated Loudness interpretation ranges (LUFS)
LOUDNESS_RANGES = {
    'optimal': (-18, -16),      # Streaming level
    'excellent': (-23, -19),    # Broadcast standard
    'good': (-27, -24),         # Conservative level
    'high': (-16, -14),         # High but acceptable
    'low': (-35, -28),          # Low but acceptable
    'very_high': (-14, float('inf')),  # >-14 LUFS
    'very_low': (float('-inf'), -35)   # <-35 LUFS
}

# LRA (Loudness Range) interpretation ranges (LU)
LRA_RANGES = {
    'excellent_wide': (15, 25),    # Wide dynamic range
    'excellent_medium': (7, 14),   # Medium dynamic range
    'good': (4, 6),                # Controlled dynamic range
    'acceptable': (2, 3),          # Limited dynamic range
    'poor': (0, 1)                 # Very limited dynamic range
}

# True Peak interpretation ranges (dBFS)
TRUE_PEAK_RANGES = {
    'excellent': (float('-inf'), -3.0),  # ≤-3.0 dBFS
    'good': (-3.0, -1.0),                # -3.0 to -1.0 dBFS
    'acceptable_low': (-1.0, -0.1),      # -1.0 to -0.1 dBFS
    'acceptable_high': (-0.1, 0.0),      # -0.1 to 0.0 dBFS
    'poor': (0.0, float('inf'))          # >0.0 dBFS (clipping)
}

# DC Offset interpretation ranges (absolute value)
DC_OFFSET_RANGES = {
    'excellent': (0.0, 0.001),      # ≤0.001
    'good': (0.001, 0.01),          # 0.001-0.01
    'acceptable': (0.01, 0.05),     # 0.01-0.05
    'poor': (0.05, float('inf'))    # >0.05
}

# Emoji mappings for interpretation
EMOJI_MAP = {
    'excellent': '✅',
    'optimal': '✅',
    'good': '✅',
    'acceptable': '⚠️',
    'high': '⚠️',
    'low': '⚠️',
    'acceptable_low': '⚠️',
    'acceptable_high': '⚠️',
    'excellent_wide': '✅',
    'excellent_medium': '✅',
    'poor': '❌',
    'very_high': '❌',
    'very_low': '❌'
}

# Quality score mappings
QUALITY_SCORES = {
    'excellent': 100,
    'optimal': 100,
    'good': 85,
    'acceptable': 70,
    'high': 75,
    'low': 75,
    'acceptable_low': 70,
    'acceptable_high': 70,
    'excellent_wide': 100,
    'excellent_medium': 100,
    'poor': 40,
    'very_high': 30,
    'very_low': 30
}

# Output file names
OUTPUT_FILES = {
    'quality_report': 'quality_report.md',
    'ab_fragments': '_ab',
    'tech_info': 'tech.txt',
    'ebu128': 'ebu128.txt',
    'astats': 'astats.txt',
    'ffprobe': 'ffprobe.json'
}

# Report templates
REPORT_HEADER = """# Reporte Comparativo de Calidad de Audio

## Resumen Ejecutivo

**Archivo recomendado:** `{recommended_file}`
**Puntuación de calidad:** {score}/100
**Codec:** {codec}
**Configuración:** {sample_rate}Hz, {channels} canales

{problems_summary}
"""

REPORT_TABLE_HEADER = """## Tabla Comparativa Detallada

| Archivo | Puntuación | Codec | Sample Rate | Canales | Bit Rate | Loudness | LRA | True Peak |
|---------|------------|-------|-------------|---------|----------|----------|-----|----------|"""

REPORT_ANALYSIS_HEADER = """## Análisis Detallado por Archivo"""

REPORT_AB_SECTION = """## Fragmentos A/B para Escucha

Escucha los fragmentos generados para confirmar la decisión:

```bash
{ab_commands}
```"""
