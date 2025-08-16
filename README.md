# Sistema de Mezcla de Audio para Doblaje

Este proyecto contiene un conjunto completo de herramientas para mezclar voces de un idioma con la música y efectos de otro, optimizado para flujos de trabajo de doblaje profesional.

## 🎯 Flujo de Trabajo

El sistema está organizado en pasos secuenciales, cada uno con su propia herramienta especializada:

### **Paso 1: Crear Estructura del Proyecto**
```bash
./01_crear_estructura/create_project_structure "/ruta/al/proyecto"
```
Crea la estructura de carpetas estandarizada para el proyecto de doblaje.

### **Paso 2: Análisis de Calidad de Audio**
```bash
./02_analizar_audios/audio_analyzer -i samples -t 30 -s 00:00:10
```
Analiza múltiples archivos de audio candidatos y recomienda el mejor para stem splitting.

### **Paso 3: Preprocesamiento de Audio**
```bash
./03_preprocesar_audio/convert_to_wav -i audio.mp3 -o audio.wav
```
Convierte el audio a WAV de alta calidad y aplica optimizaciones para stem splitting.

### **Paso 4: Separación de Pistas (Stem Splitting)**
```bash
# (En desarrollo)
./04_separar_pistas/stem_splitter -i audio.wav -o stems/
```
Extrae las pistas de música y efectos (M&E) y voces (VOX) por separado.

### **Paso 5: Mezcla de Audio**
```bash
# (En desarrollo)
./05_mezclar_audio/audio_mixer -v voces_es.wav -m music_en.wav -o final.wav
```
Combina las voces del nuevo idioma con la música y efectos originales.

### **Paso 6: Exportación Final**
```bash
# (En desarrollo)
./06_exportar_final/audio_exporter -i mixed.wav -o final_master.wav
```
Genera el audio final masterizado y listo para distribución.

## 🚀 Inicio Rápido

```bash
# 1. Crear proyecto
./01_crear_estructura/create_project_structure "/ruta/mi_proyecto"

# 2. Copiar archivos fuente a 00_sources/

# 3. Analizar calidad de audio
./02_analizar_audios/audio_analyzer -i 00_sources/audio

# 4. Preprocesar el archivo recomendado
./03_preprocesar_audio/convert_to_wav -i 00_sources/audio/archivo_recomendado.mp3 -o 01_preproc/audio.wav

# 5. Continuar con el flujo según recomendaciones
```

## 📋 Requisitos del Sistema

- **macOS** (probado en macOS actual)
- **Python 3.6+** (incluido en macOS)
- **FFmpeg** (para análisis de audio)
- **Permisos de escritura** en directorios de trabajo

## 🛠️ Instalación de Dependencias

```bash
# Instalar FFmpeg (requerido para análisis de audio)
brew install ffmpeg

# Verificar instalación
ffmpeg -version
```

## 📁 Estructura del Proyecto

```
proyecto_doblaje/
├── 01_crear_estructura/     # Herramienta de creación de estructura
├── 02_analizar_audios/      # Sistema de análisis de calidad (v2.0)
├── 03_preprocesar_audio/    # Preprocesamiento de audio (v1.0)
├── 04_separar_pistas/       # (En desarrollo)
├── 05_mezclar_audio/        # (En desarrollo)
├── 06_exportar_final/       # (En desarrollo)
└── README.md               # Esta documentación
```

## 🎵 Estado Actual

- ✅ **Paso 1**: Creación de estructura - **Completado**
- ✅ **Paso 2**: Análisis de audio - **Completado (v2.0)**
- ✅ **Paso 3**: Preprocesamiento - **Completado (v1.0)**
- 🚧 **Paso 4**: Separación de pistas - En desarrollo
- 🚧 **Paso 5**: Mezcla de audio - En desarrollo
- 🚧 **Paso 6**: Exportación final - En desarrollo

## 📖 Documentación Detallada

Cada paso incluye su propia documentación completa:

- [Paso 1: Crear Estructura](01_crear_estructura/README.md)
- [Paso 2: Análisis de Audio](02_analizar_audios/README.md)
- [Paso 3: Preprocesamiento](03_preprocesar_audio/README.md)

## 🤝 Contribución

Este es un sistema en desarrollo activo. Cada herramienta está diseñada para ser modular y extensible.
