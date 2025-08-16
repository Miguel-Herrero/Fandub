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

## Comando Flexible de Preprocesamiento

### **Preprocesador Flexible** ✅ (Implementado)
```bash
./03_preprocesar_audio/preprocess_audio -i audio.mp3 -o output.wav [opciones]
```

**Opciones de procesamiento disponibles:**
- `--high-pass` - Filtro de altas frecuencias (80 Hz, 2 poles)
- `--remove-hiss` - Elimina siseo de fondo (8 dB reducción conservadora)
- `--remove-hum` - Elimina zumbido eléctrico (50/100/150 Hz)
- `--denoise` - Reducción general de ruido (RNNoise si disponible)
- `--normalize` - Normalización EBU R128 (-23 LUFS)

**Opciones de testing:**
- `--from TIME --to TIME` - Procesar solo un segmento (formato: mm:ss o hh:mm:ss)
- `--auto-detect-noise` - Analizar audio y sugerir filtros
- `--dry-run` - Mostrar qué se procesaría sin crear archivo

**Trazabilidad:**
- **Comando FFmpeg completo** - Se muestra en pantalla para referencia
- **Log de procesamiento** - Se guarda automáticamente como `archivo.log`

**Resultado:** Control total sobre el procesamiento en una sola pasada de FFmpeg para máxima calidad con trazabilidad completa.

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

## Uso del Preprocesador Flexible

### **1. Auto-detección de Ruido (Recomendado para empezar)**
```bash
# Analizar audio y obtener sugerencias
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/output.wav \
  --auto-detect-noise

# Salida ejemplo:
# 🔍 Audio Analysis Results:
# • Analyzed: 3 distributed segments (beginning, middle, end)
# • Total analysis time: ~30 seconds from 51:58 file
# • Suggested parameters: --high-pass --remove-hiss --normalize
```

**¿Cómo funciona la auto-detección?**
- Analiza **3 segmentos de 10 segundos** distribuidos por el archivo
- **Inicio** (0-10s), **medio** (centro del archivo), **final** (últimos 10s)
- **Total: 30 segundos** de análisis para archivos de cualquier duración
- **Más representativo** que analizar solo el inicio

### **2. Uso Básico (Casos Limpios)**
```bash
# Solo high-pass y normalización
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav \
  --high-pass --normalize
```

### **3. Casos con Ruido de Fondo**
```bash
# Para audio con siseo de fondo
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav \
  --high-pass --remove-hiss --normalize

# Para audio con zumbido eléctrico
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav \
  --high-pass --remove-hum --normalize

# Para casos muy ruidosos
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav \
  --high-pass --remove-hiss --remove-hum --denoise --normalize
```

### **4. Testing en Segmentos**
```bash
# Probar en un segmento pequeño primero
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/test_segment.wav \
  --high-pass --remove-hiss --normalize \
  --from 1:30 --to 1:45

# Si suena bien, procesar archivo completo
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav \
  --high-pass --remove-hiss --normalize
```

### **5. Dry-run para Verificar**
```bash
# Ver qué se procesaría sin crear archivo
./03_preprocesar_audio/preprocess_audio \
  -i samples/sherlock_episode1.mp3 \
  -o processed/output.wav \
  --high-pass --normalize --dry-run
```

## Trazabilidad del Procesamiento

### **Comando FFmpeg Completo**
El script siempre muestra el comando FFmpeg exacto que se ejecuta:

```bash
📋 FFmpeg Command:
ffmpeg -ss 90.0 -t 5.0 -i samples/audio.mp3 -acodec pcm_s16le -ar 48000 -ac 2 -af highpass=f=80:poles=2,loudnorm=I=-23:TP=-2:LRA=7 processed/output.wav
```

**Ventajas:**
- ✅ **Reproducibilidad** - Puedes ejecutar el comando manualmente si es necesario
- ✅ **Debugging** - Verificar exactamente qué filtros se aplicaron
- ✅ **Documentación** - Copiar y pegar para referencia futura

### **Log de Procesamiento Automático**
Se crea automáticamente un archivo `.log` junto al archivo procesado:

```bash
# Si procesas: processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav
# Se crea:     processed/SherlockHolmes_EN_MIX_preprocessed_v01.log
```

**Contenido del log:**
```
# Audio Preprocessing Log
# Generated: 2025-08-16 21:43:19

## Input File
File: samples/audio.mp3
Codec: mp3
Sample Rate: 48000 Hz
Channels: 2
Duration: 51:58 (3118.1s)
Bit Rate: 320000 bps

## Processing Options
High-pass filter (80 Hz): Yes
Remove hiss: No
Remove hum (50/100/150 Hz): No
General denoise: No
Normalize (-23 LUFS): Yes

## Time Range
Start: 01:30
End: 01:35

## Output File
File: processed/test.wav
Format: WAV (48kHz, 16-bit, stereo)
Status: Success

## FFmpeg Command
ffmpeg -ss 90.0 -t 5.0 -i samples/audio.mp3 -acodec pcm_s16le -ar 48000 -ac 2 -af highpass=f=80:poles=2,loudnorm=I=-23:TP=-2:LRA=7 processed/test.wav
```

**Ventajas del log:**
- ✅ **Historial completo** - Qué se procesó, cuándo y cómo
- ✅ **Configuración exacta** - Todos los parámetros utilizados
- ✅ **Troubleshooting** - Información para resolver problemas
- ✅ **Auditoría** - Trazabilidad para proyectos profesionales

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

## Flujo de Trabajo Optimizado

### **Flujo Recomendado (Con Auto-detección Distribuida)**
```bash
# 1. Analizar calidad (Paso 2)
./02_analizar_audios/audio_analyzer -i samples

# 2. Auto-detectar ruido con análisis distribuido (3 segmentos)
./03_preprocesar_audio/preprocess_audio \
  -i samples/audio_recomendado.mp3 \
  -o processed/output.wav \
  --auto-detect-noise

# Salida: "Suggested parameters: --high-pass --remove-hiss --normalize"

# 3. Probar en segmento con parámetros sugeridos
./03_preprocesar_audio/preprocess_audio \
  -i samples/audio_recomendado.mp3 \
  -o processed/test.wav \
  --high-pass --remove-hiss --normalize \
  --from 1:30 --to 1:45

# 4. Procesar archivo completo si el test suena bien
./03_preprocesar_audio/preprocess_audio \
  -i samples/audio_recomendado.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav \
  --high-pass --remove-hiss --normalize

# 5. Stem splitting (Paso 4)
./04_separar_pistas/stem_splitter -i processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav
```

### **Flujo Rápido (Para Audio Conocido)**
```bash
# Si ya sabes qué filtros necesitas
./03_preprocesar_audio/preprocess_audio \
  -i samples/audio_recomendado.mp3 \
  -o processed/SherlockHolmes_EN_MIX_preprocessed_v01.wav \
  --high-pass --normalize
```

### **Ventajas del Enfoque Flexible:**
- ✅ **Control granular** - Solo aplicas lo que necesitas
- ✅ **Testing fácil** - Pruebas en segmentos antes del procesamiento completo
- ✅ **Auto-detección** - El sistema sugiere qué filtros usar
- ✅ **Una sola pasada** - Máxima calidad sin re-encoding múltiple
- ✅ **Orden correcto automático** - Los filtros se aplican en secuencia óptima

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

- ✅ **preprocess_audio** - Comando flexible completado y probado
- ✅ **Conversión a WAV** - Siempre aplicada (48kHz, 16-bit, estéreo)
- ✅ **Filtro de altas frecuencias** - Opcional (--high-pass, 80 Hz, 2 poles)
- ✅ **Eliminación de siseo** - Opcional (--remove-hiss, 8 dB reducción conservadora)
- ✅ **Eliminación de zumbido** - Opcional (--remove-hum, 50/100/150 Hz)
- ✅ **Reducción general de ruido** - Opcional (--denoise, RNNoise si disponible)
- ✅ **Normalización** - Opcional (--normalize, -23 LUFS conservador)
- ✅ **Procesamiento por segmentos** - Implementado (--from/--to para testing)
- ✅ **Auto-detección de ruido** - Implementado (--auto-detect-noise con análisis distribuido)
- ✅ **Una sola pasada FFmpeg** - Máxima calidad sin re-encoding
- ✅ **Trazabilidad completa** - Comando FFmpeg mostrado + log automático
- ✅ **Logs de procesamiento** - Archivo .log con todos los detalles
