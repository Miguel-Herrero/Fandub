# Paso 2: Análisis de Calidad de Audio (Versión 2.0)

## Objetivo

Este paso analiza la calidad de archivos de audio candidatos para determinar cuál es el más adecuado para el proceso de separación de pistas (stem splitting) en flujos de trabajo de doblaje.

## Descripción

Sistema completo de análisis de calidad de audio reescrito en Python con arquitectura modular y mejorada. Proporciona:

- **Análisis técnico completo** usando FFmpeg/FFprobe
- **Mediciones EBU R128** (loudness, LRA, true peak)
- **Estadísticas avanzadas** (RMS, DC offset, rango dinámico)
- **Interpretación automática** con emojis y puntuaciones
- **Fragmentos A/B** para escucha comparativa
- **Reportes detallados** en Markdown
- **Procesamiento paralelo** para múltiples archivos

## Arquitectura del Sistema

```
02_analizar_audios/
├── __init__.py              # Inicialización del paquete
├── main.py                  # Interfaz CLI principal
├── audio_analyzer           # Script ejecutable
├── config.py               # Configuración y rangos de interpretación
├── utils.py                # Utilidades y llamadas a FFmpeg
├── metrics.py              # Extracción y procesamiento de métricas
├── interpreters.py         # Interpretación de valores con emojis
├── analyzer.py             # Lógica principal de análisis
├── reporters.py            # Generación de reportes
└── README.md               # Esta documentación
```

## Uso

### Interfaz Básica (Compatible)

```bash
# Analizar carpeta (mantiene compatibilidad con versión anterior)
./02_analizar_audios/audio_analyzer -i samples

# Con opciones personalizadas
./02_analizar_audios/audio_analyzer -i samples -t 45 -s 00:01:00 -o results
```

### Interfaz Avanzada

```bash
# Analizar archivos específicos
python3 -m 02_analizar_audios.main -f audio1.mp3 audio2.wav

# Análisis con configuración personalizada
python3 -m 02_analizar_audios.main -i samples -o analysis_results -t 60 --no-parallel

# Modo silencioso
python3 -m 02_analizar_audios.main -i samples --quiet

# Modo verbose para debugging
python3 -m 02_analizar_audios.main -i samples --verbose
```

## Opciones de Línea de Comandos

### Opciones de Entrada
- `-i, --input-dir`: Directorio con archivos de audio
- `-f, --files`: Archivos específicos a analizar

### Opciones de Salida
- `-o, --output`: Directorio de resultados (default: `_analysis`)

### Opciones de Fragmentos A/B
- `-t, --fragment-duration`: Duración en segundos (default: 30)
- `-s, --fragment-start`: Tiempo de inicio HH:MM:SS (default: 00:00:10)

### Opciones de Procesamiento
- `--no-parallel`: Deshabilitar procesamiento paralelo
- `--extensions`: Extensiones de archivo a incluir

### Opciones de Salida
- `--quiet`: Suprimir salida excepto errores
- `--verbose`: Habilitar logging detallado

## Formatos Soportados

**Audio:** MP3, WAV, FLAC, AAC, M4A  
**Video:** MP4, MKV, AVI, MOV (extrae audio automáticamente)

## Salida Generada

### Estructura de Resultados
```
_analysis/
├── quality_report.md        # Reporte principal
├── _ab/                     # Fragmentos para escucha A/B
│   ├── archivo1.wav
│   └── archivo2.wav
├── archivo1/                # Análisis detallado por archivo
│   ├── tech.txt            # Información técnica
│   ├── ffprobe.json        # Datos completos de ffprobe
│   ├── ebu128.txt          # Mediciones EBU R128
│   ├── astats.txt          # Estadísticas de audio
│   └── archivo1_spectrum.png  # Visualización del espectro (NUEVO)
└── archivo2/
    ├── tech.txt
    ├── ffprobe.json
    ├── ebu128.txt
    ├── astats.txt
    └── archivo2_spectrum.png  # Visualización del espectro (NUEVO)
```

### **Nueva Funcionalidad: Visualización del Espectro**

Se genera automáticamente una imagen del espectro de frecuencias para cada archivo:

- **Formato**: PNG de alta resolución (1920x1080)
- **Contenido**: Espectrograma completo del archivo de audio
- **Utilidad**: Visualizar ruido, frecuencias dominantes, calidad general
- **Ubicación**: Carpeta individual de cada archivo (`archivo_spectrum.png`)

**Beneficios:**
- ✅ **Detección visual de ruido** - Ver patrones de interferencia
- ✅ **Comparación de calidad** - Diferencias entre archivos
- ✅ **Identificación de problemas** - Clipping, distorsión, ruido de fondo
- ✅ **Verificación de contenido** - Rango de frecuencias utilizado

### Reporte Principal

El `quality_report.md` incluye:

1. **Resumen Ejecutivo** - Archivo recomendado y puntuación
2. **Tabla Comparativa** - Métricas con emojis interpretativos
3. **Análisis Detallado** - Especificaciones y problemas por archivo
4. **Fragmentos A/B** - Comandos para escucha comparativa
5. **Imágenes de espectro** - Referencias a las visualizaciones generadas

## Interpretación de Métricas

### Emojis de Calidad
- ✅ **Excelente/Bueno** - Valores óptimos para doblaje
- ⚠️ **Aceptable/Cuidado** - Usable pero con limitaciones
- ❌ **Problemático/Malo** - Puede causar problemas

### Rangos de Interpretación

**Sample Rate:**
- ✅ ≥48kHz (óptimo)
- ✅ 44.1-47.9kHz (bueno)
- ⚠️ 32-44kHz (aceptable)
- ❌ <32kHz (problemático)

**Integrated Loudness (LUFS):**
- ✅ -16 a -18 LUFS (streaming)
- ✅ -19 a -23 LUFS (broadcast) ← **Rango típico**
- ✅ -24 a -27 LUFS (conservador)
- ⚠️ -14 a -16 LUFS (alto)
- ⚠️ -28 a -35 LUFS (bajo)
- ❌ >-14 o <-35 LUFS (extremo)

**True Peak:**
- ✅ ≤-3.0 dBFS (excelente margen)
- ✅ -3.0 a -1.0 dBFS (bueno)
- ⚠️ -1.0 a 0.0 dBFS (límite)
- ❌ >0.0 dBFS (clipping)

## Mejoras de la Versión 2.0

### Arquitectura
- ✅ **Código Python modular** - Más mantenible y extensible
- ✅ **Configuración centralizada** - Fácil ajuste de rangos
- ✅ **Manejo robusto de errores** - Mejor recuperación ante fallos
- ✅ **Logging estructurado** - Debugging más eficiente

### Funcionalidad
- ✅ **Procesamiento paralelo** - Análisis más rápido de múltiples archivos
- ✅ **Interpretación mejorada** - Rangos más precisos según la guía
- ✅ **Reportes más ricos** - Información más detallada y útil
- ✅ **Compatibilidad mantenida** - Misma interfaz que versión anterior

### Rendimiento
- ✅ **Llamadas FFmpeg optimizadas** - Menos overhead
- ✅ **Parsing más eficiente** - Procesamiento JSON nativo
- ✅ **Gestión de memoria** - Mejor manejo de archivos grandes

## Requisitos del Sistema

### Software Necesario
- **Python 3.6+** (incluido en macOS)
- **FFmpeg** con FFprobe
- **Permisos de escritura** en directorio de salida

### Verificación de Dependencias
```bash
# El script verifica automáticamente las dependencias
./02_analizar_audios/audio_analyzer -i samples
```

## Solución de Problemas

### Errores Comunes

**"FFmpeg not found":**
```bash
# Instalar FFmpeg en macOS
brew install ffmpeg

# Verificar instalación
ffmpeg -version
```

**"No audio files found":**
- Verificar que el directorio contiene archivos soportados
- Comprobar permisos de lectura
- Usar `--extensions` para especificar formatos

**Errores de análisis:**
- Usar `--verbose` para más información
- Verificar que los archivos no estén corruptos
- Comprobar espacio en disco para archivos temporales

### Debugging

```bash
# Modo verbose para información detallada
./02_analizar_audios/audio_analyzer -i samples --verbose

# Análisis secuencial para aislar problemas
./02_analizar_audios/audio_analyzer -i samples --no-parallel
```

## Migración desde Versión 1.0

La nueva versión mantiene **compatibilidad completa** con la interfaz anterior:

```bash
# Comando anterior (sigue funcionando)
./02_analizar_audios_old/audio_analyzer -i samples -t 30 -s 00:00:10

# Comando nuevo (misma funcionalidad, mejor rendimiento)
./02_analizar_audios/audio_analyzer -i samples -t 30 -s 00:00:10
```

## Siguiente Paso

Una vez completado el análisis, proceder al **Paso 3: Preprocesamiento de Audio** usando el archivo recomendado por el análisis.
