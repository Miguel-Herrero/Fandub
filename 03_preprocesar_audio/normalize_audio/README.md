# Normalizador de Audio para Preprocesamiento

## Objetivo

Normalizar los niveles de audio usando el estándar EBU R128 con configuración conservadora optimizada para preprocesamiento antes de stem splitting. Preserva las dinámicas naturales mientras proporciona niveles estables.

## ¿Por Qué Normalizar Antes del Stem Splitting?

### **Problemas con Niveles Inconsistentes**
- **Niveles muy bajos** - El algoritmo puede no detectar componentes débiles
- **Niveles muy altos** - Puede causar clipping y distorsión
- **Dinámicas extremas** - Dificulta la separación consistente
- **Variaciones de volumen** - Afecta la calidad de la separación

### **Solución: Normalización Conservadora**
- **Niveles estables** - Optimiza el rango de trabajo del stem splitter
- **Preserva dinámicas** - Mantiene las diferencias naturales entre instrumentos/voces
- **Evita artefactos** - Procesamiento mínimo para no introducir distorsión
- **Estándar profesional** - Usa EBU R128 (-23 LUFS) para consistencia

## Configuración Utilizada

### **Parámetros EBU R128 Conservadores**
```bash
ffmpeg -i input.wav -af loudnorm output.wav
```

**Valores por defecto (optimizados para preprocesamiento):**
- **Integrated Loudness**: -23 LUFS (conservador, preserva dinámicas)
- **True Peak**: -2 dBFS (headroom seguro)
- **Loudness Range**: 7 LU (mantiene variaciones naturales)

### **¿Por Qué -23 LUFS y No -16 LUFS?**

| Aspecto | -23 LUFS (Usado) | -16 LUFS (Broadcast) |
|---------|------------------|----------------------|
| **Dinámicas** | ✅ Preservadas | ❌ Comprimidas |
| **Separación** | ✅ Óptima | ⚠️ Puede degradarse |
| **Artefactos** | ✅ Mínimos | ⚠️ Más procesamiento |
| **Uso** | Preprocesamiento | Entrega final |

## Uso

### **Uso Básico**
```bash
# Normalización simple
./03_preprocesar_audio/normalize_audio/normalize_audio -i audio.wav -o normalized.wav
```

### **Uso Profesional (Recomendado)**
```bash
# Con naming automático siguiendo convenciones
./03_preprocesar_audio/normalize_audio/normalize_audio \
  -i processed/SherlockHolmes_EN_MIX_wav_v01.wav \
  -o processed/ \
  --auto-name \
  --project SherlockHolmes \
  --language EN \
  --type MIX \
  --version v01

# Resultado: processed/SherlockHolmes_EN_MIX_normalized_v01.wav
```

### **Análisis y Testing**
```bash
# Ver niveles actuales antes de normalizar
./03_preprocesar_audio/normalize_audio/normalize_audio -i audio.wav -o normalized.wav --verbose

# Saltar análisis para procesamiento más rápido
./03_preprocesar_audio/normalize_audio/normalize_audio -i audio.wav -o normalized.wav --no-analyze

# Probar normalización sin crear archivo (útil para archivos largos)
./03_preprocesar_audio/normalize_audio/normalize_audio -i audio.wav -o normalized.wav --dry-run
```

## Parámetros Disponibles

### **Argumentos Requeridos**
- `-i, --input` - Archivo de audio de entrada (preferiblemente WAV)
- `-o, --output` - Archivo de salida o directorio (para auto-naming)

### **Argumentos Opcionales**
- `--overwrite` - Sobrescribir archivo de salida si existe
- `--no-analyze` - Saltar análisis inicial (procesamiento más rápido)
- `--dry-run` - Probar normalización sin crear archivo de salida
- `--verbose` - Logging detallado

### **Naming Profesional**
- `--auto-name` - Generar nombre profesional automáticamente
- `--project` - Nombre del proyecto (ej: SherlockHolmes)
- `--language` - Código de idioma (ej: EN, ES, FR)
- `--type` - Tipo de audio (MIX, VOX, MNE, MUS, SFX)
- `--version` - Versión (ej: v01, v02)

## Ejemplos de Uso

### **Flujo Típico de Preprocesamiento**
```bash
# 1. Convertir a WAV (si no está ya)
./03_preprocesar_audio/convert_to_wav -i audio.mp3 -o processed/audio.wav

# 2. Probar normalización primero (para archivos largos)
./03_preprocesar_audio/normalize_audio/normalize_audio -i processed/audio.wav -o processed/normalized.wav --dry-run

# 3. Normalizar para stem splitting
./03_preprocesar_audio/normalize_audio/normalize_audio -i processed/audio.wav -o processed/normalized.wav

# 4. Proceder al stem splitting
# ./04_separar_pistas/stem_splitter -i processed/normalized.wav
```

### **Con Naming Profesional Completo**
```bash
# Paso 1: Conversión
./03_preprocesar_audio/convert_to_wav \
  -i samples/sherlock_episode1.mp3 \
  -o processed/ \
  --auto-name \
  --project SherlockHolmes \
  --language EN \
  --type MIX \
  --version v01

# Paso 2: Test de normalización
./03_preprocesar_audio/normalize_audio/normalize_audio \
  -i processed/SherlockHolmes_EN_MIX_wav_v01.wav \
  -o processed/ \
  --auto-name \
  --project SherlockHolmes \
  --language EN \
  --type MIX \
  --version v01 \
  --dry-run

# Paso 3: Normalización real
./03_preprocesar_audio/normalize_audio/normalize_audio \
  -i processed/SherlockHolmes_EN_MIX_wav_v01.wav \
  -o processed/ \
  --auto-name \
  --project SherlockHolmes \
  --language EN \
  --type MIX \
  --version v01
```

### **Procesamiento por Lotes**
```bash
# Probar normalización en múltiples archivos
for file in processed/*_wav_*.wav; do
  echo "Testing: $file"
  ./03_preprocesar_audio/normalize_audio/normalize_audio -i "$file" -o "${file%.*}_normalized.wav" --dry-run
done

# Normalizar múltiples archivos (después del test)
for file in processed/*_wav_*.wav; do
  ./03_preprocesar_audio/normalize_audio/normalize_audio -i "$file" -o "${file%.*}_normalized.wav" --no-analyze
done
```

## Interpretación de Resultados

### **Análisis de Loudness**
```
Current loudness: -18.5 LUFS | True Peak: -0.8 dBFS | LRA: 12.3 LU
```

**Interpretación:**
- **-18.5 LUFS** - Más alto que el objetivo (-23), se reducirá
- **-0.8 dBFS** - Cerca del clipping, se aplicará headroom
- **12.3 LU** - Rango dinámico amplio, se preservará en gran medida

### **Resultado de Dry Run**
```
✅ Dry run successful!
Normalization would create: processed/SherlockHolmes_EN_MIX_normalized_v01.wav
No output file was created (dry run mode)
```

### **Resultado Real**
```
✅ Normalization successful!
Output: processed/SherlockHolmes_EN_MIX_normalized_v01.wav
Size: 52.1 MB
```

## Verificación de Resultados

### **Comprobar Niveles Finales**
```bash
# Analizar archivo normalizado
ffprobe -v quiet -print_format json -show_streams normalized.wav

# Verificar loudness específicamente
ffmpeg -i normalized.wav -af loudnorm=print_format=json -f null - 2>&1 | grep -A 10 "{"
```

### **Comparar Antes y Después**
```bash
# Escuchar diferencias
afplay original.wav
afplay normalized.wav

# Comparar tamaños (deberían ser similares)
ls -lh original.wav normalized.wav
```

## Casos de Uso Específicos

### **Audio Muy Bajo (< -30 LUFS)**
```bash
# El normalizador aumentará significativamente el volumen
./normalize_audio -i quiet_audio.wav -o normalized.wav --verbose
```

### **Audio Muy Alto (> -10 LUFS)**
```bash
# El normalizador reducirá el volumen y aplicará headroom
./normalize_audio -i loud_audio.wav -o normalized.wav --verbose
```

### **Audio Ya Normalizado**
```bash
# Si está cerca de -23 LUFS, se aplicará normalización mínima
./normalize_audio -i already_good.wav -o normalized.wav
# Output: "Audio is already well-normalized (within 1 LUFS of target)"
```

### **Archivos Muy Largos**
```bash
# Usar dry-run primero para verificar que funciona
./normalize_audio -i long_audio.wav -o normalized.wav --dry-run

# Luego procesar sin análisis inicial para mayor velocidad
./normalize_audio -i long_audio.wav -o normalized.wav --no-analyze
```

## Solución de Problemas

### **Error: "FFmpeg not found or loudnorm filter not available"**
```bash
# Verificar FFmpeg
ffmpeg -version

# Verificar filtro loudnorm
ffmpeg -filters | grep loudnorm

# Instalar/actualizar FFmpeg si es necesario
brew install ffmpeg
```

### **Error: "Output file exists"**
```bash
# Usar flag --overwrite
./normalize_audio -i audio.wav -o normalized.wav --overwrite
```

### **Procesamiento Muy Lento**
```bash
# Usar dry-run para probar primero
./normalize_audio -i audio.wav -o normalized.wav --dry-run

# Saltar análisis inicial
./normalize_audio -i audio.wav -o normalized.wav --no-analyze

# Para archivos muy largos, considerar dividir primero
ffmpeg -i long_audio.wav -ss 00:00:00 -t 01:00:00 segment1.wav
```

### **Resultado No Suena Mejor**
**Importante:** La normalización NO mejora la calidad del audio original. Solo:
- ✅ Estabiliza los niveles para procesamiento posterior
- ✅ Optimiza el rango dinámico para stem splitting
- ✅ Previene clipping en pasos posteriores

## Flujo de Trabajo Recomendado

### **Orden de Preprocesamiento**
```bash
# 1. Conversión a WAV (si es necesario)
./convert_to_wav -i audio.mp3 -o audio.wav

# 2. Test de normalización (para archivos largos)
./normalize_audio -i audio.wav -o normalized.wav --dry-run

# 3. Normalización (este paso)
./normalize_audio -i audio.wav -o normalized.wav --no-analyze

# 4. Reducción de ruido (futuro, si es necesario)
# ./remove_noise -i normalized.wav -o clean.wav

# 5. Stem splitting
# ./stem_splitter -i normalized.wav
```

### **Verificación Entre Pasos**
```bash
# Después de cada paso, verificar:
ffprobe -v quiet -show_entries format=duration,stream=codec_name,sample_rate,channels normalized.wav
afplay normalized.wav  # Escuchar brevemente
```

## Requisitos del Sistema

- **FFmpeg** con filtro `loudnorm` (versión 3.1+)
- **Python 3.6+**
- **Espacio en disco** - Archivo de salida similar al de entrada
- **Tiempo de procesamiento** - Aproximadamente tiempo real (1x duración)

## Próximos Pasos

Una vez normalizado:

1. **Verificar resultado** - Escuchar el audio normalizado
2. **Aplicar reducción de ruido** - Si hay ruido de fondo significativo
3. **Proceder al stem splitting** - El audio está optimizado para separación

## Estado del Desarrollo

- ✅ **normalize_audio** - Completado y probado
- ✅ **dry-run mode** - Implementado para testing
- 🚧 **remove_noise** - Próximamente
- 🚧 **enhance_voice** - Próximamente
- 🚧 **batch_preprocess** - Próximamente
