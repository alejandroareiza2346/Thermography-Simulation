# Simulación de Termografía con Python y OpenCV

Este proyecto implementa un simulador de imágenes termográficas que convierte imágenes en escala de grises a simulaciones térmicas usando mapas de colores de OpenCV.

## Características

- ✅ Carga imágenes en formato JPG o PNG
- ✅ Convierte automáticamente a escala de grises
- ✅ Aplica mapas de colores térmicos (JET, HOT, COOL, RAINBOW, OCEAN)
- ✅ Resalta zonas con "temperaturas altas"
- ✅ Muestra imagen original y resultado térmico
- ✅ Guarda el resultado en disco
- ✅ Interfaz de línea de comandos con múltiples opciones

## Requisitos

- Python 3.7+
- OpenCV
- NumPy

## Instalación

1. Clona o descarga este proyecto
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso Básico

### Uso Simple
```bash
python termografia_simulation.py ejemplos\imagen_ejemplo.jpg
```

### Uso Avanzado
```bash
# Cambiar umbral para zonas calientes
python termografia_simulation.py imagen.jpg --umbral 180

# Usar mapa de color diferente
python termografia_simulation.py imagen.jpg --mapa hot

# Guardar con nombre personalizado
python termografia_simulation.py imagen.jpg --salida mi_termografia.jpg

# No mostrar ventanas (modo batch)
python termografia_simulation.py imagen.jpg --no-mostrar

# No resaltar zonas calientes
python termografia_simulation.py imagen.jpg --no-resaltar
```

## Opciones de Línea de Comandos

| Opción | Descripción | Default |
|--------|-------------|---------|
| `imagen` | Ruta a la imagen de entrada | Requerido |
| `--umbral` | Umbral para zonas calientes (0-255) | 200 |
| `--salida` | Archivo de salida | termografia_resultado.jpg |
| `--mapa` | Tipo de mapa (jet, hot, cool, rainbow, ocean) | jet |
| `--no-resaltar` | No resaltar zonas calientes | False |
| `--no-mostrar` | No mostrar ventanas | False |
| `--no-guardar` | No guardar resultado | False |

## Mapas de Color Disponibles

- **JET**: Clásico azul-verde-amarillo-rojo
- **HOT**: Negro-rojo-amarillo-blanco (como hierro caliente)
- **COOL**: Cian-magenta
- **RAINBOW**: Espectro completo de colores
- **OCEAN**: Tonos azules y verdes

## Estructura del Proyecto

```
termografic/
├── termografia_simulation.py    # Script principal
├── requirements.txt            # Dependencias
├── README.md                  # Este archivo
├── ejemplos/                  # Imágenes de ejemplo
│   ├── imagen_ejemplo.jpg
│   └── resultado_ejemplo.jpg
└── 
```

## Cómo Funciona

1. **Carga de Imagen**: Lee la imagen original y la convierte a escala de grises
2. **Aplicación de Mapa Térmico**: Usa `cv2.applyColorMap()` para aplicar colores
3. **Detección de Zonas Calientes**: Identifica píxeles con valores altos
4. **Resaltado**: Dibuja contornos alrededor de zonas "calientes"
5. **Visualización**: Muestra original, escala de grises y resultado térmico
6. **Guardado**: Exporta el resultado como archivo de imagen

## Personalización

La clase `TermografiaSimulator` puede usarse programáticamente:

```python
from termografia_simulation import TermografiaSimulator

# Crear simulador
sim = TermografiaSimulator()

# Cargar y procesar imagen
sim.cargar_imagen('mi_imagen.jpg')
sim.aplicar_mapa_termico(cv2.COLORMAP_HOT)
sim.resaltar_zonas_calientes(umbral=180)
sim.mostrar_imagenes()
sim.guardar_resultado('resultado.jpg')
```

## Ejemplos de Resultados

Las imágenes procesadas mostrarán:
- Zonas frías en azul/púrpura
- Zonas templadas en verde/amarillo  
- Zonas calientes en naranja/rojo
- Contornos blancos alrededor de zonas muy calientes

## Solución de Problemas

### Error: "No module named cv2"
```bash
pip install opencv-python
```

### Error: "No se pudo cargar la imagen"
- Verifica que la ruta sea correcta
- Asegúrate de que el archivo sea JPG o PNG válido
- Comprueba los permisos de lectura del archivo

### Ventanas no se muestran
- En sistemas Linux, instala: `sudo apt-get install python3-tk`
- En sistemas headless, usa `--no-mostrar`

## Autor

Alejandro Areiza Alzate

## Licencia

Este proyecto es de uso educativo y demostrativo.
