# Paso 3: Preprocesamiento de Audio

## Objetivo

Preparar el audio seleccionado del Paso 2 para el proceso de separación de pistas (stem splitting), optimizando su calidad y formato para obtener los mejores resultados posibles.

## ¿Por Qué Preprocesar?

### **Problema con MP3/AAC**
- **Compresión con pérdida** - Información eliminada permanentemente
- **Artefactos de compresión** - Pueden interferir con stem splitting
- **Formato no óptimo** - No ideal para edición profesional

### **Solución: WAV + Optimizaciones**
- **Sin compresión** - Conserva toda la información disponible
- **Formato estándar** - Compatible con todas las herramientas profesionales
- **Optimizaciones específicas** - Mejoras para separación de pistas

## Herramientas Disponibles

### **1. Conversión a WAV** ✅ (Implementado)
```bash
./03_preprocesar_audio/convert_to_wav -i audio.mp3 -o audio.wav
```
**Función:** Convierte cualquier formato de audio a WAV de alta calidad.

### **2. Normalización** ✅ (Implementado)
```bash
./03_preprocesar_audio/normalize_audio/normalize_audio -i audio.wav -o normalized.wav
```
**Función:** Ajusta el volumen a niveles óptimos para stem splitting usando EBU R128 conservador.

### **3. Eliminación de Ruido de Baja Frecuencia** ✅ (Implementado)
```bash
./03_preprocesar_audio/remove_low_frequency_noise/remove_low_frequency_noise -i audio.wav -o filtered.wav
```
**Función:** Elimina ruido de baja frecuencia (aire acondicionado, golpes de micro) con filtro 80 Hz.

### **4. Reducción de Ruido Avanzada** 🚧 (Próximamente)
```bash
./03_preprocesar_audio/remove_noise -i audio.wav -o clean.wav
```
**Función:** Elimina ruido de fondo complejo que puede interferir con la separación.

### **5. Realce de Voz** 🚧 (Próximamente)
```bash
./03_preprocesar_audio/enhance_voice -i audio.wav -o enhanced.wav
```
**Función:** Optimiza frecuencias de diálogo para mejor separación.

### **6. Procesamiento por Lotes** 🚧 (Próximamente)
```bash
./03_preprocesar_audio/batch_preprocess -i audio.wav -o processed.wav
```
**Función:** Aplica todos los pasos automáticamente.

## Convenciones de Naming Profesional

### **¿Por Qué Importa el Naming?**
En doblaje profesional, el naming correcto es **crucial** para:
- ✅ **Trazabilidad** - Saber qué procesamiento se aplicó
- ✅ **Organización** - Mantener orden en proyectos complejos
- ✅ **Colaboración** - Equipos entienden inmediatamente el contenido
- ✅ **Versionado** - Control de versiones sin confusión

### **Estructura Estándar**
```
[PROYECTO]_[IDIOMA]_[TIPO]_[PROCESAMIENTO]_[VERSION].wav
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
SherlockHolmes_EN_MIX_wav_v01.wav

# Después de normalización
SherlockHolmes_EN_MIX_normalized_v01.wav

# Stems separados
SherlockHolmes_EN_VOX_isolated_v01.wav
SherlockHolmes_EN_MNE_isolated_v01.wav

# Mezcla final en español
SherlockHolmes_ES_MIX_final_v01.wav
```

## Uso Detallado

### **Conversión a WAV (Paso Fundamental)**

#### **Uso Básico**
```bash
# Conversión simple
./03_preprocesar_audio/convert_to_wav -i samples/audio.mp3 -o processed/audio.wav
```

#### **Uso Profesional (Recomendado)**
```bash
# Naming automático siguiendo convenciones de doblaje
./03_preprocesar_audio/convert_to_wav \
  -i samples/audio.mp3 \
  -o processed/ \
  --auto-name \
  --project SherlockHolmes \
  --language EN \
  --type MIX \
  --version v01

# Resultado: processed/SherlockHolmes_EN_MIX_wav_v01.wav
```

#### **Configuración Avanzada**
```bash
# Control total de parámetros
./03_preprocesar_audio/convert_to_wav \
  -i samples/audio.mp3 \
  -o processed/ \
  --auto-name \
  --project MiPelicula \
  --language ES \
  --type MIX \
  --sample-rate 48000 \
  --bit-depth 16 \
  --overwrite
```

#### **Conversión a Mono**
```bash
# Para contenido que no necesita estéreo
./03_preprocesar_audio/convert_to_wav \
  -i samples/audio.mp3 \
  -o processed/audio_mono.wav \
  --channels 1
```

### **Parámetros Explicados**

#### **Sample Rate (Frecuencia de Muestreo)**
- **48000 Hz** ✅ **Recomendado** - Estándar profesional de video
- **44100 Hz** ⚠️ Aceptable - Estándar de CD
- **96000 Hz** ❌ Innecesario - Para fuentes MP3

#### **Bit Depth (Profundidad de Bits)**
- **16 bits** ✅ **Recomendado** - Suficiente para fuentes MP3
- **24 bits** ⚠️ Overkill - No mejora calidad desde MP3

#### **Canales**
- **Estéreo (2)** ✅ **Recomendado** - Mantiene información espacial
- **Mono (1)** ⚠️ Solo si es necesario - Pierde información espacial

## Configuraciones Recomendadas por Caso

### **Para Doblaje de Series/Películas (Flujo Completo Recomendado)**
```bash
# Paso 1: Conversión a WAV
./convert_to_wav -i audio.mp3 -o audio.wav --sample-rate 48000 --bit-depth 16

# Paso 2: Filtrar ruido de baja frecuencia (PRIMERO)
./remove_low_frequency_noise/remove_low_frequency_noise -i audio.wav -o filtered.wav

# Paso 3: Normalizar audio limpio
./normalize_audio/normalize_audio -i filtered.wav -o normalized.wav --no-analyze
```
- **Sample Rate:** 48000 Hz (estándar video)
- **Bit Depth:** 16 bits (suficiente)
- **Orden:** Filtrar → Normalizar (crucial para mejores resultados)

### **Para Contenido con Mucho Ruido**
```bash
# Paso 1: Convertir
./convert_to_wav -i audio.mp3 -o audio.wav

# Paso 2: Reducir ruido (cuando esté disponible)
# ./remove_noise -i audio.wav -o clean.wav
```

### **Para Archivos Muy Grandes**
```bash
# Usar 16 bits para ahorrar espacio
./convert_to_wav -i audio.mp3 -o audio.wav --bit-depth 16
```

## Flujo de Trabajo Recomendado

### **Flujo Básico (Mínimo)**
```bash
# 1. Analizar calidad (Paso 2)
./02_analizar_audios/audio_analyzer -i samples

# 2. Convertir el archivo recomendado
./03_preprocesar_audio/convert_to_wav -i samples/audio_recomendado.mp3 -o processed/audio.wav

# 3. Proceder al stem splitting (Paso 4)
```

### **Flujo Recomendado (Con Preprocesamiento)**
```bash
# 1. Analizar calidad
./02_analizar_audios/audio_analyzer -i samples

# 2. Convertir a WAV
./03_preprocesar_audio/convert_to_wav -i samples/audio_recomendado.mp3 -o processed/audio.wav

# 3. Eliminar ruido de baja frecuencia (PRIMERO - antes de normalizar)
./03_preprocesar_audio/remove_low_frequency_noise/remove_low_frequency_noise -i processed/audio.wav -o processed/filtered.wav

# 4. Normalizar audio limpio para stem splitting
./03_preprocesar_audio/normalize_audio/normalize_audio -i processed/filtered.wav -o processed/normalized.wav

# 5. Stem splitting
./04_separar_pistas/stem_splitter -i processed/normalized.wav
```

### **¿Por Qué Este Orden?**

**Filtrar ANTES de normalizar es crucial:**
- ✅ **Niveles más precisos** - La normalización se calcula sobre contenido limpio
- ✅ **Evita amplificar ruido** - El ruido de baja frecuencia no se potencia
- ✅ **Mejor stem splitting** - Audio optimizado desde el primer paso
- ✅ **Procesamiento eficiente** - Cada paso trabaja con datos más limpios

### **Flujo Completo (Futuro)**
```bash
# 1. Analizar calidad
./02_analizar_audios/audio_analyzer -i samples

# 2. Preprocesamiento completo
./03_preprocesar_audio/batch_preprocess -i samples/audio_recomendado.mp3 -o processed/audio_final.wav

# 3. Stem splitting
./04_separar_pistas/stem_splitter -i processed/audio_final.wav
```

## Verificación de Resultados

### **Comprobar Conversión**
```bash
# Ver información del archivo convertido
ffprobe -v quiet -print_format json -show_streams processed/audio.wav

# Escuchar el resultado
afplay processed/audio.wav
```

### **Comparar Tamaños**
```bash
# Ver tamaños de archivos
ls -lh samples/audio.mp3 processed/audio.wav

# Ejemplo típico:
# audio.mp3:  5.2 MB (comprimido)
# audio.wav: 52.1 MB (sin comprimir)
```

## Solución de Problemas

### **Error: "FFmpeg not found"**
```bash
# Instalar FFmpeg
brew install ffmpeg

# Verificar instalación
ffmpeg -version
```

### **Error: "Output file exists"**
```bash
# Usar flag --overwrite
./convert_to_wav -i audio.mp3 -o audio.wav --overwrite
```

### **Archivo muy grande**
```bash
# Verificar duración del audio
ffprobe -v quiet -show_entries format=duration -of csv=p=0 audio.mp3

# Si es muy largo, considerar recortar primero
ffmpeg -i audio.mp3 -ss 00:00:00 -t 01:00:00 audio_1hour.mp3
```

### **Calidad no mejora**
**Importante:** La conversión a WAV NO mejora la calidad del MP3 original. Solo:
- ✅ Evita re-compresión en pasos posteriores
- ✅ Proporciona formato óptimo para herramientas profesionales
- ✅ Elimina artefactos de decodificación repetida

## Próximos Pasos

Una vez convertido a WAV:

1. **Verificar calidad** - Escuchar el resultado
2. **Aplicar preprocesamiento adicional** - Cuando esté disponible
3. **Proceder al Paso 4** - Separación de pistas (stem splitting)

## Requisitos del Sistema

- **FFmpeg** (instalado y en PATH)
- **Python 3.6+** (incluido en macOS)
- **Espacio en disco** - WAV ocupa ~10x más que MP3
- **Tiempo de procesamiento** - Conversión rápida (tiempo real o menos)

## Estado del Desarrollo

- ✅ **convert_to_wav** - Completado y probado
- ✅ **normalize_audio** - Completado y probado
- ✅ **remove_low_frequency_noise** - Completado y probado
- 🚧 **remove_noise** - En desarrollo
- 🚧 **enhance_voice** - En desarrollo
- 🚧 **batch_preprocess** - En desarrollo
