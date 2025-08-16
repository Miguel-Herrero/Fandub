# Eliminador de Ruido de Baja Frecuencia

## Objetivo

Eliminar ruido de baja frecuencia (aire acondicionado, golpes de micrófono, rumble) usando un filtro de altas frecuencias optimizado para preprocesamiento de diálogos antes de stem splitting.

## ¿Por Qué Eliminar Frecuencias Bajas?

### **Problemas Típicos en Grabaciones de Series/TV**
- **Aire acondicionado** (20-60 Hz) - Ruido constante de fondo
- **Golpes de micrófono** (<50 Hz) - Impactos subsónicos
- **Rumble de tráfico** (10-80 Hz) - Vibraciones externas
- **Ruido eléctrico** (50/60 Hz) - Interferencias de la red eléctrica
- **Vibraciones de equipos** - Cámaras, focos, etc.

### **Beneficios para Stem Splitting de Diálogos**
- **Mejor separación VOX/MNE** - Algoritmo se enfoca en contenido útil
- **Menos interferencias** - Elimina ruidos que confunden al AI
- **Voces más claras** - Preserva todo el rango vocal (>80 Hz)
- **Procesamiento más eficiente** - Menos datos irrelevantes

## Configuración Utilizada

### **Filtro High-Pass Optimizado para Diálogos**
```bash
ffmpeg -i input.wav -af "highpass=f=80:poles=2" output.wav
```

**Parámetros fijos (optimizados para diálogos):**
- **Frecuencia de corte**: 80 Hz (elimina ruido, preserva voces)
- **Poles**: 2 (pendiente suave, mínimos artefactos)

### **¿Por Qué 80 Hz?**

| Contenido | Frecuencia | ¿Se Preserva? |
|-----------|------------|---------------|
| **Ruido subsónico** | 0-40 Hz | ❌ Eliminado |
| **Aire acondicionado** | 20-60 Hz | ❌ Eliminado |
| **Rumble/golpes** | 10-80 Hz | ❌ Eliminado |
| **Voces masculinas** | 85-180 Hz | ✅ Preservado |
| **Voces femeninas** | 165-265 Hz | ✅ Preservado |
| **Inteligibilidad** | 300-3000 Hz | ✅ Intacto |

## Uso

### **Uso Básico**
```bash
# Filtrado simple
./03_preprocesar_audio/remove_low_frequency_noise/remove_low_frequency_noise -i audio.wav -o filtered.wav
```

### **Uso Profesional (Recomendado)**
```bash
# Con naming automático siguiendo convenciones
./03_preprocesar_audio/remove_low_frequency_noise/remove_low_frequency_noise \
  -i processed/SherlockHolmes_EN_MIX_normalized_v01.wav \
  -o processed/ \
  --auto-name \
  --project SherlockHolmes \
  --language EN \
  --type MIX \
  --version v01

# Resultado: processed/SherlockHolmes_EN_MIX_filtered_v01.wav
```

### **Testing**
```bash
# Probar filtrado sin crear archivo (útil para archivos largos)
./03_preprocesar_audio/remove_low_frequency_noise/remove_low_frequency_noise -i audio.wav -o filtered.wav --dry-run
```

## Parámetros Disponibles

### **Argumentos Requeridos**
- `-i, --input` - Archivo de audio de entrada (preferiblemente WAV)
- `-o, --output` - Archivo de salida o directorio (para auto-naming)

### **Argumentos Opcionales**
- `--overwrite` - Sobrescribir archivo de salida si existe
- `--dry-run` - Probar filtrado sin crear archivo de salida
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

# 2. Eliminar ruido de baja frecuencia (este paso)
./03_preprocesar_audio/remove_low_frequency_noise/remove_low_frequency_noise -i processed/audio.wav -o processed/filtered.wav

# 3. Normalizar para stem splitting
./03_preprocesar_audio/normalize_audio/normalize_audio -i processed/filtered.wav -o processed/normalized.wav

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

# Paso 2: Filtrado de frecuencias bajas
./03_preprocesar_audio/remove_low_frequency_noise/remove_low_frequency_noise \
  -i processed/SherlockHolmes_EN_MIX_wav_v01.wav \
  -o processed/ \
  --auto-name \
  --project SherlockHolmes \
  --language EN \
  --type MIX \
  --version v01

# Paso 3: Normalización
./03_preprocesar_audio/normalize_audio/normalize_audio \
  -i processed/SherlockHolmes_EN_MIX_filtered_v01.wav \
  -o processed/ \
  --auto-name \
  --project SherlockHolmes \
  --language EN \
  --type MIX \
  --version v01
```

### **Procesamiento por Lotes**
```bash
# Filtrar múltiples archivos
for file in processed/*_normalized_*.wav; do
  ./03_preprocesar_audio/remove_low_frequency_noise/remove_low_frequency_noise -i "$file" -o "${file%.*}_filtered.wav"
done
```

## Interpretación de Resultados

### **Antes del Filtrado**
```
Input: pcm_s16le | 48000Hz | 2 channels | 3118.1s
```

### **Después del Filtrado**
```
✅ High-pass filtering successful!
Output: processed/SherlockHolmes_EN_MIX_filtered_v01.wav
Size: 52.1 MB
```

**Nota:** El tamaño del archivo debería ser similar al original - el filtro no comprime, solo elimina frecuencias.

## Verificación de Resultados

### **Comprobar Espectro de Frecuencias**
```bash
# Generar espectrograma para verificar el filtrado
ffmpeg -i filtered.wav -lavfi showspectrumpic=s=1024x512:legend=1 spectrum_filtered.png

# Comparar con el original
ffmpeg -i original.wav -lavfi showspectrumpic=s=1024x512:legend=1 spectrum_original.png
```

### **Escuchar Diferencias**
```bash
# Escuchar antes y después
afplay original.wav
afplay filtered.wav

# La diferencia debería ser sutil - menos "peso" en graves, voces más claras
```

### **Análisis Técnico**
```bash
# Ver información del archivo filtrado
ffprobe -v quiet -print_format json -show_streams filtered.wav
```

## Casos de Uso Específicos

### **Audio con Mucho Aire Acondicionado**
```bash
# El filtro eliminará el ruido constante de 20-60 Hz
./remove_low_frequency_noise -i noisy_audio.wav -o filtered.wav --verbose
```

### **Grabaciones con Golpes de Micrófono**
```bash
# Elimina impactos subsónicos sin afectar las voces
./remove_low_frequency_noise -i bumpy_audio.wav -o filtered.wav
```

### **Audio Ya Limpio**
```bash
# El filtro se aplica de forma conservadora, sin degradar calidad
./remove_low_frequency_noise -i clean_audio.wav -o filtered.wav
# Resultado: Mínima diferencia audible, mejor para stem splitting
```

### **Archivos Muy Largos**
```bash
# Usar dry-run primero para verificar que funciona
./remove_low_frequency_noise -i long_audio.wav -o filtered.wav --dry-run

# Luego procesar normalmente
./remove_low_frequency_noise -i long_audio.wav -o filtered.wav
```

## Solución de Problemas

### **Error: "FFmpeg not found or highpass filter not available"**
```bash
# Verificar FFmpeg
ffmpeg -version

# Verificar filtro highpass
ffmpeg -filters | grep highpass

# Instalar/actualizar FFmpeg si es necesario
brew install ffmpeg
```

### **Error: "Output file exists"**
```bash
# Usar flag --overwrite
./remove_low_frequency_noise -i audio.wav -o filtered.wav --overwrite
```

### **El Audio Suena "Delgado"**
**Esto es normal y esperado:**
- ✅ Se eliminaron frecuencias muy bajas (ruido)
- ✅ Las voces se mantienen intactas
- ✅ La inteligibilidad mejora
- ✅ El stem splitting funcionará mejor

### **No Se Nota Diferencia**
**Esto puede indicar:**
- ✅ El audio original ya estaba limpio
- ✅ El filtro funcionó correctamente
- ✅ El ruido eliminado era subsónico (no audible directamente)

## Flujo de Trabajo Recomendado

### **Orden de Preprocesamiento Actualizado**
```bash
# 1. Conversión a WAV (si es necesario)
./convert_to_wav -i audio.mp3 -o audio.wav

# 2. Filtrado de frecuencias bajas (este paso - NUEVO)
./remove_low_frequency_noise -i audio.wav -o filtered.wav

# 3. Normalización
./normalize_audio -i filtered.wav -o normalized.wav

# 4. Stem splitting
# ./stem_splitter -i normalized.wav
```

### **¿Por Qué Este Orden?**
1. **Filtrar antes de normalizar** - Los niveles se calculan sobre contenido limpio
2. **Eliminar ruido primero** - Evita que interfiera en pasos posteriores
3. **Preparar para stem splitting** - Audio optimizado para separación

## Requisitos del Sistema

- **FFmpeg** con filtro `highpass` (versión 2.8+)
- **Python 3.6+**
- **Espacio en disco** - Archivo de salida similar al de entrada
- **Tiempo de procesamiento** - Muy rápido (< tiempo real)

## Próximos Pasos

Una vez filtrado:

1. **Verificar resultado** - Escuchar el audio filtrado
2. **Aplicar normalización** - Para niveles óptimos
3. **Proceder al stem splitting** - Audio limpio y optimizado

## Estado del Desarrollo

- ✅ **remove_low_frequency_noise** - Completado y probado
- ✅ **80 Hz cutoff, 2 poles** - Configuración optimizada para diálogos
- ✅ **dry-run mode** - Implementado para testing
- 🚧 **enhance_voice** - Próximamente
- 🚧 **batch_preprocess** - Próximamente
