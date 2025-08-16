# Paso 1: Crear Estructura de Carpetas

## Objetivo

Este paso crea la estructura de carpetas estandarizada para proyectos de edición de audio, específicamente diseñada para flujos de trabajo de doblaje con Reaper y separación de pistas mediante IA.

## Descripción

El script `create_project_structure.py` genera automáticamente:

- **Estructura completa de directorios** organizada en 6 categorías principales (00-06)
- **README.txt** con documentación detallada de cada carpeta y su propósito
- **Convenciones de nomenclatura** consistentes para archivos y versiones
- **Flujo de trabajo recomendado** paso a paso

## Estructura Generada

```
Proyecto_<TITULO>_<FPSDEST>_<SR>/
├─ 00_sources/          # Archivos originales (solo lectura)
│  ├─ video/
│  └─ audio/
├─ 01_preproc/          # Preprocesamiento antes de IA
├─ 02_stems/            # Resultados de separación IA
│  ├─ EN/
│  └─ ES/
├─ 03_reaper/           # Proyecto Reaper
│  ├─ Media/
│  └─ Backups/
├─ 04_intermediate/     # Ediciones post-IA
├─ 05_renders/          # Mezclas finales
│  ├─ audio/
│  └─ video_mux/
└─ 06_docs/             # Documentación y checksums
```

## Uso

### Ejecución Básica

```bash
./01_crear_estructura/create_project_structure "/ruta/al/proyecto"
```

### Ejemplos

```bash
# Crear estructura para película
./01_crear_estructura/create_project_structure "/Users/usuario/Proyectos/Sherlock_Holmes_23976_48k"

# Crear estructura en directorio actual
./01_crear_estructura/create_project_structure "./Mi_Proyecto_25fps_48k"

# Crear estructura con ruta absoluta
./01_crear_estructura/create_project_structure "/Volumes/Disco_Externo/Proyectos/Pelicula_TITULO_23976_48k"
```

## Características del Script

### Funcionalidades

- ✅ **Creación automática** de toda la estructura de directorios
- ✅ **Manejo robusto de errores** con mensajes informativos
- ✅ **Soporte para rutas con espacios** y caracteres especiales
- ✅ **Generación automática** del README.txt con documentación completa
- ✅ **Verificación de permisos** antes de crear directorios
- ✅ **Compatibilidad multiplataforma** (macOS, Linux, Windows)

### Validaciones

- Verifica que el directorio destino sea accesible
- Crea directorios padre si no existen
- Maneja conflictos con directorios existentes
- Proporciona feedback detallado del proceso

## Convenciones de Nomenclatura

### Formato Recomendado para Proyecto

```
Pelicula_<TITULO>_<FPSDEST>_<SR>
```

**Ejemplos:**
- `Sherlock_Holmes_23976_48k`
- `Matrix_Reloaded_25fps_48k`
- `Avengers_Endgame_24fps_48k`

### Elementos del Nombre

- **TITULO**: Nombre de la película/proyecto (sin espacios, usar guiones bajos)
- **FPSDEST**: Frame rate destino (`23976`, `25fps`, `24fps`)
- **SR**: Sample rate (`48k` para 48kHz)

## Requisitos del Sistema

### Software Necesario

- **Python 3.6+** (incluido en macOS por defecto)
- **Permisos de escritura** en el directorio destino

### Compatibilidad

- ✅ **macOS** (10.12+)
- ✅ **Linux** (cualquier distribución moderna)
- ✅ **Windows** (10+)

## Flujo de Trabajo Posterior

Una vez creada la estructura:

1. **Copiar archivos fuente** a `00_sources/`
2. **Seguir el flujo** descrito en `README.txt`
3. **Proceder al Paso 2** (análisis de audios candidatos)

## Solución de Problemas

### Errores Comunes

**Error de permisos:**
```bash
# Verificar permisos del directorio padre
ls -la /ruta/al/directorio/padre

# Cambiar permisos si es necesario
chmod 755 /ruta/al/directorio/padre
```

**Directorio ya existe:**
- El script respeta directorios existentes
- Solo crea los que faltan
- No sobrescribe contenido existente

**Caracteres especiales en rutas:**
- Usar comillas dobles alrededor de la ruta
- Evitar caracteres especiales en nombres de proyecto

### Verificación de Instalación

```bash
# Verificar Python
python3 --version

# Probar el script
./01_crear_estructura/create_project_structure --help
```

## Notas Importantes

- El script **NO sobrescribe** directorios existentes
- Se recomienda usar **rutas absolutas** para evitar confusiones
- El **README.txt generado** contiene la documentación completa del flujo de trabajo
- Mantener la **estructura intacta** es crucial para el funcionamiento correcto de Reaper

## Siguiente Paso

Una vez completado este paso, proceder al **Paso 2: Análisis de Audios Candidatos** para evaluar la calidad de los archivos fuente.
