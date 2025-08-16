# Paso 3: Preprocesamiento Completo de Audio

## Objetivo

Preparar completamente el audio seleccionado del Paso 2 para el proceso de separación de pistas (stem splitting) mediante un único comando que realiza todos los pasos de optimización necesarios.

## ¿Qué Hace el Preprocesamiento Completo?

### **Problemas que Resuelve**
- **Formato comprimido** (MP3/AAC) - Convierte a WAV sin pérdidas
- **Ruido de baja frecuencia** - Elimina aire acondicionado, golpes de micro
- **Niveles inconsistentes** - Normaliza para stem splitting óptimo
- **Múltiples pasos manuales** - Todo en un solo comando

### **Resultado: Audio Optimizado**
- **Formato WAV** (48kHz, 16-bit, estéreo) - Estándar profesional
- **Sin ruido de graves** - Filtro 80 Hz elimina interferencias
- **Niveles perfectos** - Normalización -23 LUFS conservadora
- **Listo para stem splitting** - Sin procesamiento adicional necesario

## Comando Único de Preprocesamiento

### **Preprocesador Completo** ✅ (Implementado)
```bash
./03_preprocesar_audio/preprocess_audio -i audio.mp3 -o SherlockHolmes_EN_MIX_preprocessed_v01.wav
```

**Realiza automáticamente:**
1. **Conversión a WAV** (48kHz, 16-bit, estéreo)
2. **Filtro de altas frecuencias** (80 Hz, 2 poles) - elimina ruido de graves
3. **Normalización EBU R128** (-23 LUFS) - niveles óptimos para stem splitting

**Resultado:** Audio completamente optimizado y listo para stem splitting en un solo paso.

## Convenciones de Naming Profesional

### **¿Por Qué Importa el Naming?**
En doblaje profesional, el naming correcto es **crucial** para:
- ✅ **Trazabilidad** - Saber qué procesamiento se aplicó
- ✅ **Organización** - Mantener orden en proyectos complejos
- ✅ **Colaboración** - Equipos entienden inmediatamente el contenido
- ✅ **Versionado** - Control de versiones sin confusión

### **Estructura Estándar para Archivos Preprocesados**
```
[PROYECTO]_[IDIOMA]_[TIPO]_preprocessed_[VERSION].wav
```

### **Códigos de Idioma**
- `EN` = English (Inglés)
- `ES` = Español
- `FR` = Français (Francés)
- `DE` = Deutsch (Alemán)
- `IT` = Italiano
- `PT` = Português

### **Tipos de Audio**
- `MIX` = Mezcla completa (música + voces + efectos)
- `VOX` = Solo voces/diálogos
- `MNE` = Music & Effects (música y efectos sin voces)
- `MUS` = Solo música
- `SFX` = Solo efectos de sonido

### **Ejemplos de Naming**
```bash
# Archivo original
samples/sherlock_episode1.mp3

# Después del preprocesamiento completo
processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav

# Stems separados (después del paso 4)
stems/SherlockHolmes_EN_VOX_isolated_v01.wav
stems/SherlockHolmes_EN_MNE_isolated_v01.wav

# Mezcla final en español
final/SherlockHolmes_ES_MIX_final_v01.wav
```

## Uso del Preprocesador Completo

### **Uso Básico (Recomendado)**
```bash
# Preprocesamiento completo en un comando
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav
```

### **Uso con Testing**
```bash
# Probar primero sin crear archivo (para archivos largos)
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav \
  --dry-run

# Luego ejecutar realmente
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav
```

### **Sobrescribir Archivos Existentes**
```bash
# Si el archivo de salida ya existe
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav \
  --overwrite
```

### **Parámetros del Preprocesamiento**

El preprocesador usa configuraciones fijas optimizadas para doblaje:

#### **Formato de Salida (Fijo)**
- **Sample Rate:** 48000 Hz (estándar profesional de video)
- **Bit Depth:** 16 bits (suficiente para fuentes comprimidas)
- **Canales:** Estéreo (mantiene información espacial)

#### **Filtro de Altas Frecuencias (Fijo)**
- **Frecuencia de corte:** 80 Hz (elimina ruido, preserva voces)
- **Poles:** 2 (pendiente suave, mínimos artefactos)

#### **Normalización (Fija)**
- **Target:** -23 LUFS (conservador, preserva dinámicas)
- **True Peak:** -2 dBFS (headroom seguro)
- **LRA:** 7 LU (mantiene variaciones naturales)

## Casos de Uso

### **Para Doblaje de Series/Películas (Estándar)**
```bash
# Un solo comando hace todo
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav
```

### **Para Archivos Muy Grandes**
```bash
# Probar primero con dry-run
./03_preprocesar_audio/preprocess_audio \
  -i large_file.mp3 \
  -o processed/output.wav \
  --dry-run

# Luego procesar si todo está bien
./03_preprocesar_audio/preprocess_audio \
  -i large_file.mp3 \
  -o processed/output.wav
```

## Flujo de Trabajo Simplificado

### **Flujo Actual (Recomendado)**
```bash
# 1. Analizar calidad (Paso 2)
./02_analizar_audios/audio_analyzer -i samples

# 2. Preprocesamiento completo en un comando (Paso 3)
./03_preprocesar_audio/preprocess_audio \
  -i samples/audio_recomendado.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav

# 3. Stem splitting (Paso 4)
./04_separar_pistas/stem_splitter -i processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav
```

### **¿Qué Hace el Preprocesamiento Automáticamente?**

**Un solo comando realiza todos los pasos en el orden correcto:**
1. ✅ **Conversión a WAV** (48kHz, 16-bit, estéreo)
2. ✅ **Filtro de altas frecuencias** (80 Hz) - elimina ruido ANTES de normalizar
3. ✅ **Normalización** (-23 LUFS) - calcula niveles sobre audio limpio

**Ventajas del enfoque unificado:**
- ✅ **Simplicidad** - Un comando en lugar de tres
- ✅ **Orden correcto** - Procesamiento optimizado automáticamente
- ✅ **Menos errores** - No hay pasos intermedios que olvidar
- ✅ **Eficiencia** - Procesamiento en una sola pasada de FFmpeg

## Verificación de Resultados

### **Comprobar Audio Preprocesado**
```bash
# Ver información del archivo preprocesado
ffprobe -v quiet -print_format json -show_streams processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav

# Escuchar el resultado
afplay processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav
```

### **Comparar Antes y Después**
```bash
# Ver tamaños de archivos
ls -lh samples/sherlock_episode1.mp3 processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav

# Ejemplo típico:
# sherlock_episode1.mp3:     5.2 MB (comprimido)
# *_preprocessed_v01.wav:   52.1 MB (sin comprimir, filtrado, normalizado)
```

### **Verificar Procesamiento**
```bash
# El archivo debe tener estas características:
# - Formato: WAV, 48000 Hz, 16-bit, estéreo
# - Sin frecuencias <80 Hz (ruido eliminado)
# - Niveles normalizados (-23 LUFS aproximadamente)
```

## Solución de Problemas

### **Error: "FFmpeg not found" o "Missing filters"**
```bash
# Instalar FFmpeg con todos los filtros
brew install ffmpeg

# Verificar instalación y filtros
ffmpeg -version
ffmpeg -filters | grep -E "(highpass|loudnorm)"
```

### **Error: "Output file exists"**
```bash
# Usar flag --overwrite
./03_preprocesar_audio/preprocess_audio -i audio.mp3 -o output.wav --overwrite
```

### **Archivo muy grande o procesamiento lento**
```bash
# Usar dry-run primero para verificar
./03_preprocesar_audio/preprocess_audio -i large_file.mp3 -o output.wav --dry-run

# Verificar duración del audio
ffprobe -v quiet -show_entries format=duration -of csv=p=0 large_file.mp3

# Si es muy largo, considerar recortar primero
ffmpeg -i large_file.mp3 -ss 00:00:00 -t 01:00:00 segment.mp3
```

### **El audio no suena "mejor"**
**Importante:** El preprocesamiento NO mejora la calidad del audio original. Su objetivo es:
- ✅ **Optimizar para stem splitting** - Formato y niveles ideales
- ✅ **Eliminar interferencias** - Ruido que confunde algoritmos
- ✅ **Estandarizar formato** - WAV profesional consistente
- ✅ **Preparar para procesamiento** - Sin pasos adicionales necesarios

## Próximos Pasos

Una vez completado el preprocesamiento:

1. **Verificar resultado** - Escuchar el audio preprocesado
2. **Comprobar formato** - Debe ser WAV, 48kHz, 16-bit, estéreo
3. **Proceder al Paso 4** - Separación de pistas (stem splitting)

## Requisitos del Sistema

- **FFmpeg** con filtros `highpass` y `loudnorm` (versión 3.1+)
- **Python 3.6+** (incluido en macOS)
- **Espacio en disco** - WAV ocupa ~10x más que MP3
- **Tiempo de procesamiento** - Aproximadamente tiempo real para archivos normales

## Estado del Desarrollo

- ✅ **preprocess_audio** - Comando unificado completado y probado
- ✅ **Conversión a WAV** - Integrado (48kHz, 16-bit, estéreo)
- ✅ **Filtro de altas frecuencias** - Integrado (80 Hz, 2 poles)
- ✅ **Normalización** - Integrado (-23 LUFS conservador)
- 🚧 **Herramientas individuales** - Mantenidas para casos especiales
- 🚧 **Procesamiento avanzado** - Futuras mejoras según necesidades
