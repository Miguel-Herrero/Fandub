#!/usr/bin/env python3
"""
Audio Quality Analyzer

This module provides the main analysis functionality for audio quality assessment.
It coordinates the extraction of metrics, interpretation, and output generation.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
import concurrent.futures
from datetime import datetime

try:
    from . import utils
    from .config import DEFAULT_OUTPUT_DIR, DEFAULT_FRAGMENT_DURATION, DEFAULT_FRAGMENT_START, OUTPUT_FILES
    from .metrics import AudioMetrics
    from .utils import ensure_directory, clean_filename, FFmpegError
except ImportError:
    import utils
    from config import DEFAULT_OUTPUT_DIR, DEFAULT_FRAGMENT_DURATION, DEFAULT_FRAGMENT_START, OUTPUT_FILES
    from metrics import AudioMetrics
    from utils import ensure_directory, clean_filename, FFmpegError

logger = logging.getLogger(__name__)


class AudioAnalyzer:
    """Main audio quality analyzer class."""
    
    def __init__(self, output_dir: str = None, fragment_duration: int = None, 
                 fragment_start: str = None, parallel: bool = True):
        """
        Initialize the AudioAnalyzer.
        
        Args:
            output_dir: Directory for analysis output
            fragment_duration: Duration of A/B test fragments in seconds
            fragment_start: Start time for A/B fragments (HH:MM:SS)
            parallel: Whether to use parallel processing
        """
        self.output_dir = Path(output_dir or DEFAULT_OUTPUT_DIR)
        self.fragment_duration = fragment_duration or DEFAULT_FRAGMENT_DURATION
        self.fragment_start = fragment_start or DEFAULT_FRAGMENT_START
        self.parallel = parallel
        
        self.analyzed_files = []
        self.analysis_results = {}
        
        # Check dependencies
        deps = utils.check_dependencies()
        if not deps.get('ffmpeg') or not deps.get('ffprobe'):
            raise RuntimeError("FFmpeg and FFprobe are required but not found")
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze a single audio file.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            Dictionary with analysis results
        """
        logger.info(f"Analyzing: {file_path.name}")
        
        # Create clean directory name for this file
        clean_name = clean_filename(file_path.name)
        file_output_dir = self.output_dir / clean_name
        ensure_directory(file_output_dir)
        
        # Initialize metrics extractor
        metrics = AudioMetrics(file_path)
        
        try:
            # Step 1: Extract technical information
            logger.debug(f"Extracting technical info for {file_path.name}")
            tech_info = metrics.extract_technical_info()
            
            # Save technical info
            tech_file = file_output_dir / OUTPUT_FILES['tech_info']
            self._save_tech_info(tech_info, tech_file)
            
            # Save ffprobe JSON
            ffprobe_file = file_output_dir / OUTPUT_FILES['ffprobe']
            self._save_ffprobe_json(file_path, ffprobe_file)
            
            # Step 2: Extract EBU R128 loudness measurements
            logger.debug(f"Extracting EBU R128 measurements for {file_path.name}")
            ebu128_file = file_output_dir / OUTPUT_FILES['ebu128']
            utils.extract_ebu128_loudness(file_path, ebu128_file)
            ebu_metrics = metrics.parse_ebu128_file(ebu128_file)
            
            # Step 3: Extract audio statistics
            logger.debug(f"Extracting audio statistics for {file_path.name}")
            astats_file = file_output_dir / OUTPUT_FILES['astats']
            utils.extract_audio_stats(file_path, astats_file)
            astats_metrics = metrics.parse_astats_file(astats_file)
            
            # Step 4: Create A/B test fragment
            logger.debug(f"Creating A/B fragment for {file_path.name}")
            ab_dir = self.output_dir / OUTPUT_FILES['ab_fragments']
            ensure_directory(ab_dir)
            ab_file = ab_dir / f"{clean_name}.wav"
            utils.create_ab_fragment(file_path, ab_file, self.fragment_start, self.fragment_duration)
            
            # Step 5: Interpret all metrics
            logger.debug(f"Interpreting metrics for {file_path.name}")
            interpreted = metrics.interpret_all_metrics()
            
            # Compile results
            result = {
                'file_path': str(file_path),
                'filename': file_path.name,
                'clean_name': clean_name,
                'output_dir': str(file_output_dir),
                'ab_fragment': str(ab_file),
                'analysis_timestamp': datetime.now().isoformat(),
                'metrics': metrics.get_summary(),
                'success': True,
                'error': None
            }
            
            logger.info(f"✓ Analysis completed for {file_path.name} (Score: {metrics.overall_score}/100)")
            return result
            
        except Exception as e:
            logger.error(f"✗ Analysis failed for {file_path.name}: {e}")
            return {
                'file_path': str(file_path),
                'filename': file_path.name,
                'clean_name': clean_filename(file_path.name),
                'success': False,
                'error': str(e),
                'analysis_timestamp': datetime.now().isoformat()
            }
    
    def analyze_files(self, file_paths: List[Path]) -> Dict[str, Any]:
        """
        Analyze multiple audio files.
        
        Args:
            file_paths: List of file paths to analyze
            
        Returns:
            Dictionary with analysis results for all files
        """
        logger.info(f"Starting analysis of {len(file_paths)} files")
        
        # Ensure output directory exists
        ensure_directory(self.output_dir)
        
        results = {}
        
        if self.parallel and len(file_paths) > 1:
            # Parallel processing
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                future_to_file = {
                    executor.submit(self.analyze_file, file_path): file_path 
                    for file_path in file_paths
                }
                
                for future in concurrent.futures.as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        result = future.result()
                        results[file_path.name] = result
                    except Exception as e:
                        logger.error(f"Error in parallel analysis of {file_path.name}: {e}")
                        results[file_path.name] = {
                            'file_path': str(file_path),
                            'filename': file_path.name,
                            'success': False,
                            'error': str(e)
                        }
        else:
            # Sequential processing
            for file_path in file_paths:
                result = self.analyze_file(file_path)
                results[file_path.name] = result
        
        self.analysis_results = results
        self.analyzed_files = file_paths
        
        # Log summary
        successful = sum(1 for r in results.values() if r.get('success', False))
        logger.info(f"Analysis completed: {successful}/{len(file_paths)} files successful")
        
        return results
    
    def analyze_directory(self, directory: Path, extensions: List[str] = None) -> Dict[str, Any]:
        """
        Analyze all audio files in a directory.
        
        Args:
            directory: Directory to search for audio files
            extensions: List of file extensions to include
            
        Returns:
            Dictionary with analysis results
        """
        audio_files = utils.find_audio_files(directory, extensions)
        
        if not audio_files:
            logger.warning(f"No audio files found in {directory}")
            return {}
        
        return self.analyze_files(audio_files)
    
    def _save_tech_info(self, tech_info: Dict[str, Any], output_file: Path) -> None:
        """Save technical information to a text file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Technical Information\n")
                f.write("====================\n\n")
                
                for key, value in tech_info.items():
                    f.write(f"{key.replace('_', ' ').title()}: {value}\n")
                
                f.write(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
        except Exception as e:
            logger.error(f"Error saving technical info to {output_file}: {e}")
    
    def _save_ffprobe_json(self, file_path: Path, output_file: Path) -> None:
        """Save ffprobe JSON output to file."""
        try:
            ffprobe_data = utils.get_ffprobe_info(file_path)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(ffprobe_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Error saving ffprobe JSON to {output_file}: {e}")
    
    def get_recommended_file(self) -> Optional[str]:
        """
        Get the recommended file based on analysis results.
        
        Returns:
            Filename of the recommended file, or None if no analysis done
        """
        if not self.analysis_results:
            return None
        
        # Find file with highest score
        best_file = None
        best_score = -1
        
        for filename, result in self.analysis_results.items():
            if not result.get('success', False):
                continue
            
            score = result.get('metrics', {}).get('overall_score', 0)
            if score > best_score:
                best_score = score
                best_file = filename
        
        return best_file
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the analysis session.
        
        Returns:
            Dictionary with analysis summary
        """
        if not self.analysis_results:
            return {}
        
        successful_results = [
            r for r in self.analysis_results.values() 
            if r.get('success', False)
        ]
        
        if not successful_results:
            return {'error': 'No successful analyses'}
        
        # Calculate statistics
        scores = [
            r.get('metrics', {}).get('overall_score', 0) 
            for r in successful_results
        ]
        
        recommended_file = self.get_recommended_file()
        recommended_result = self.analysis_results.get(recommended_file, {})
        
        return {
            'total_files': len(self.analysis_results),
            'successful_files': len(successful_results),
            'failed_files': len(self.analysis_results) - len(successful_results),
            'average_score': sum(scores) / len(scores) if scores else 0,
            'highest_score': max(scores) if scores else 0,
            'lowest_score': min(scores) if scores else 0,
            'recommended_file': recommended_file,
            'recommended_score': recommended_result.get('metrics', {}).get('overall_score', 0),
            'output_directory': str(self.output_dir),
            'analysis_timestamp': datetime.now().isoformat()
        }
