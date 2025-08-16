#!/usr/bin/env python3
"""
Report Generation

This module handles the generation of analysis reports in various formats.
"""

from pathlib import Path
from typing import Dict, Any, List
import logging
from datetime import datetime

try:
    from .config import (
        REPORT_HEADER, REPORT_TABLE_HEADER, REPORT_ANALYSIS_HEADER,
        REPORT_AB_SECTION, OUTPUT_FILES
    )
    from .interpreters import get_quality_summary, format_metric_with_emoji
except ImportError:
    from config import (
        REPORT_HEADER, REPORT_TABLE_HEADER, REPORT_ANALYSIS_HEADER,
        REPORT_AB_SECTION, OUTPUT_FILES
    )
    from interpreters import get_quality_summary, format_metric_with_emoji

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates analysis reports in various formats."""
    
    def __init__(self, analysis_results: Dict[str, Any], output_dir: Path):
        """
        Initialize the report generator.
        
        Args:
            analysis_results: Results from AudioAnalyzer
            output_dir: Directory to save reports
        """
        self.analysis_results = analysis_results
        self.output_dir = output_dir
        self.successful_results = [
            r for r in analysis_results.values() 
            if r.get('success', False)
        ]
    
    def generate_markdown_report(self) -> Path:
        """
        Generate a comprehensive markdown report.
        
        Returns:
            Path to the generated report file
        """
        if not self.successful_results:
            logger.error("No successful analysis results to generate report")
            return None
        
        report_file = self.output_dir / OUTPUT_FILES['quality_report']
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                # Write header
                self._write_header(f)
                
                # Write comparison table
                self._write_comparison_table(f)
                
                # Write detailed analysis
                self._write_detailed_analysis(f)
                
                # Write A/B section
                self._write_ab_section(f)
            
            logger.info(f"Markdown report generated: {report_file}")
            return report_file
            
        except Exception as e:
            logger.error(f"Error generating markdown report: {e}")
            return None
    
    def _write_header(self, f) -> None:
        """Write the report header section."""
        # Get recommended file info
        recommended_file = self._get_recommended_file()
        if not recommended_file:
            return
        
        result = self.analysis_results[recommended_file]
        metrics = result.get('metrics', {})
        raw_metrics = metrics.get('raw_metrics', {})
        interpreted = metrics.get('interpreted_metrics', {})
        
        # Format problems summary
        problems = interpreted.get('problems', [])
        problems_summary = get_quality_summary(problems)
        
        # Write header
        header = REPORT_HEADER.format(
            recommended_file=recommended_file,
            score=metrics.get('overall_score', 0),
            codec=raw_metrics.get('codec', 'unknown'),
            sample_rate=raw_metrics.get('sample_rate', 0),
            channels=raw_metrics.get('channels', 0),
            problems_summary=problems_summary
        )
        
        f.write(header)
        f.write("\n")
    
    def _write_comparison_table(self, f) -> None:
        """Write the comparison table section."""
        f.write(REPORT_TABLE_HEADER)
        f.write("\n")
        
        # Sort results by score (highest first)
        sorted_results = sorted(
            self.successful_results,
            key=lambda x: x.get('metrics', {}).get('overall_score', 0),
            reverse=True
        )
        
        for result in sorted_results:
            filename = result['filename']
            metrics = result.get('metrics', {})
            raw_metrics = metrics.get('raw_metrics', {})
            interpreted = metrics.get('interpreted_metrics', {})
            
            # Format values with emojis
            sample_rate_display = format_metric_with_emoji(
                f"{raw_metrics.get('sample_rate', 0)}Hz",
                interpreted.get('sample_rate_emoji', '❓')
            )
            
            bit_rate_display = format_metric_with_emoji(
                f"{raw_metrics.get('bit_rate', 0) // 1000}kbps" if raw_metrics.get('bit_rate', 0) > 0 else "N/A",
                interpreted.get('bit_rate_emoji', '❓')
            )
            
            loudness_display = format_metric_with_emoji(
                f"{raw_metrics.get('integrated_loudness', 0)} LUFS",
                interpreted.get('loudness_emoji', '❓')
            )
            
            lra_display = format_metric_with_emoji(
                f"{raw_metrics.get('lra', 0)} LU",
                interpreted.get('lra_emoji', '❓')
            )
            
            true_peak_display = format_metric_with_emoji(
                f"{raw_metrics.get('true_peak', 0)} dBTP",
                interpreted.get('true_peak_emoji', '❓')
            )
            
            # Write table row
            f.write(f"| `{filename}` | **{metrics.get('overall_score', 0)}/100** | "
                   f"{raw_metrics.get('codec', 'unknown')} | {sample_rate_display} | "
                   f"{raw_metrics.get('channels', 0)} | {bit_rate_display} | "
                   f"{loudness_display} | {lra_display} | {true_peak_display} |\n")
        
        f.write("\n")
    
    def _write_detailed_analysis(self, f) -> None:
        """Write the detailed analysis section."""
        f.write(REPORT_ANALYSIS_HEADER)
        f.write("\n\n")
        
        # Sort results by score (highest first)
        sorted_results = sorted(
            self.successful_results,
            key=lambda x: x.get('metrics', {}).get('overall_score', 0),
            reverse=True
        )
        
        for i, result in enumerate(sorted_results, 1):
            filename = result['filename']
            metrics = result.get('metrics', {})
            raw_metrics = metrics.get('raw_metrics', {})
            interpreted = metrics.get('interpreted_metrics', {})
            
            f.write(f"### {i}. {filename}\n\n")
            f.write(f"**Puntuación:** {metrics.get('overall_score', 0)}/100\n\n")
            
            # Technical specifications
            f.write("**Especificaciones técnicas:**\n")
            f.write(f"- Codec: {raw_metrics.get('codec', 'unknown')}\n")
            f.write(f"- Sample Rate: {raw_metrics.get('sample_rate', 0)}Hz\n")
            f.write(f"- Canales: {raw_metrics.get('channels', 0)}\n")
            
            bit_rate = raw_metrics.get('bit_rate', 0)
            if bit_rate > 0:
                f.write(f"- Bit Rate: {bit_rate // 1000}kbps\n")
            else:
                f.write("- Bit Rate: N/A\n")
            
            f.write("\n")
            
            # Quality metrics
            f.write("**Métricas de calidad:**\n")
            
            if 'integrated_loudness' in raw_metrics:
                f.write(f"- Integrated Loudness: {raw_metrics['integrated_loudness']} LUFS\n")
            
            if 'lra' in raw_metrics:
                f.write(f"- Loudness Range (LRA): {raw_metrics['lra']} LU\n")
            
            if 'true_peak' in raw_metrics:
                f.write(f"- True Peak: {raw_metrics['true_peak']} dBTP\n")
            
            if 'peak_level' in raw_metrics:
                f.write(f"- Peak Level: {raw_metrics['peak_level']} dB\n")
            
            if 'rms_level' in raw_metrics:
                f.write(f"- RMS Level: {raw_metrics['rms_level']} dB\n")
            
            if 'dc_offset' in raw_metrics:
                f.write(f"- DC Offset: {raw_metrics['dc_offset']}\n")
            
            f.write("\n")
            
            # Problems or success
            problems = interpreted.get('problems', [])
            if problems:
                f.write("**Problemas detectados:**\n")
                for problem in problems:
                    f.write(f"- {problem}\n")
            else:
                f.write("**✅ Sin problemas detectados**\n")
            
            f.write("\n")
    
    def _write_ab_section(self, f) -> None:
        """Write the A/B testing section."""
        ab_commands = []
        
        for result in self.successful_results:
            filename = result['filename']
            clean_name = result.get('clean_name', filename)
            ab_commands.append(f"afplay _analysis/_ab/{clean_name}.wav  # {filename}")
        
        ab_section = REPORT_AB_SECTION.format(
            ab_commands="\n".join(ab_commands)
        )
        
        f.write(ab_section)
        f.write("\n")
    
    def _get_recommended_file(self) -> str:
        """Get the filename of the recommended file."""
        if not self.successful_results:
            return None
        
        # Find file with highest score
        best_result = max(
            self.successful_results,
            key=lambda x: x.get('metrics', {}).get('overall_score', 0)
        )
        
        return best_result['filename']
    
    def generate_summary_text(self) -> str:
        """
        Generate a brief text summary of the analysis.
        
        Returns:
            Summary text string
        """
        if not self.successful_results:
            return "No successful analysis results available."
        
        recommended_file = self._get_recommended_file()
        if not recommended_file:
            return "No recommended file found."
        
        result = self.analysis_results[recommended_file]
        score = result.get('metrics', {}).get('overall_score', 0)
        
        total_files = len(self.analysis_results)
        successful_files = len(self.successful_results)
        
        summary = f"""Análisis completado:
- Archivos analizados: {successful_files}/{total_files}
- Archivo recomendado: {recommended_file}
- Puntuación: {score}/100
- Reporte completo: {self.output_dir / OUTPUT_FILES['quality_report']}"""
        
        return summary
    
    def print_console_summary(self) -> None:
        """Print a summary to the console."""
        print("\n" + "="*50)
        print("🎵 RESUMEN DEL ANÁLISIS")
        print("="*50)
        
        if not self.successful_results:
            print("❌ No se completó ningún análisis exitosamente")
            return
        
        recommended_file = self._get_recommended_file()
        if recommended_file:
            result = self.analysis_results[recommended_file]
            score = result.get('metrics', {}).get('overall_score', 0)
            
            print(f"📁 Archivo recomendado: {recommended_file}")
            print(f"⭐ Puntuación: {score}/100")
        
        print(f"📊 Archivos analizados: {len(self.successful_results)}/{len(self.analysis_results)}")
        print(f"📄 Reporte completo: {self.output_dir / OUTPUT_FILES['quality_report']}")
        print(f"🎧 Fragmentos A/B: {self.output_dir / OUTPUT_FILES['ab_fragments']}/")
        
        print("\n💡 Consejos:")
        print("• Revisa el reporte detallado para más información")
        print("• Escucha los fragmentos A/B para confirmar la decisión")
        print("• Usa el archivo con mayor puntuación para stem splitting")
        print("="*50)
