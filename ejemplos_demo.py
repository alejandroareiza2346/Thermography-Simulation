#!/usr/bin/env python3
"""
Script de ejemplo para demostrar el uso de la simulación termográfica.
Genera una imagen de muestra y la procesa con diferentes mapas de colores.
"""

import cv2
import numpy as np
import os
from termografia_simulation import TermografiaSimulator


def generar_imagen_ejemplo(variacion=True):
    """
    Genera una imagen de ejemplo con gradientes para simular diferentes temperaturas.
    
    Args:
        variacion (bool): Si True, genera patrones aleatorios. Si False, usa patrón fijo.
    
    Returns:
        str: Ruta a la imagen generada
    """
    # Crear una imagen de 400x400 píxeles
    altura, ancho = 400, 400
    imagen = np.zeros((altura, ancho), dtype=np.uint8)
    
    if variacion:
        # Generar patrones aleatorios
        print("Generando imagen con patrones aleatorios...")
        
        # Gradiente con dirección aleatoria
        direccion = np.random.choice(['horizontal', 'vertical', 'diagonal'])
        if direccion == 'horizontal':
            for x in range(ancho):
                intensidad = int(255 * x / ancho)
                imagen[:altura//4, x] = intensidad
        elif direccion == 'vertical':
            for y in range(altura//4):
                intensidad = int(255 * y / (altura//4))
                imagen[y, :] = intensidad
        else:  # diagonal
            for y in range(altura//4):
                for x in range(ancho):
                    intensidad = int(255 * (x + y) / (ancho + altura//4))
                    imagen[y, x] = min(255, intensidad)
        
        # Círculos aleatorios (3-7 círculos)
        num_circulos = np.random.randint(3, 8)
        for _ in range(num_circulos):
            centro_x = np.random.randint(50, ancho - 50)
            centro_y = np.random.randint(altura//4, altura - 50)
            radio = np.random.randint(20, 60)
            intensidad = np.random.randint(150, 255)
            cv2.circle(imagen, (centro_x, centro_y), radio, (intensidad, intensidad, intensidad), -1)
        
        # Formas geométricas aleatorias
        num_formas = np.random.randint(2, 5)
        for _ in range(num_formas):
            forma = np.random.choice(['rectangulo', 'elipse'])
            x1 = np.random.randint(0, ancho//2)
            y1 = np.random.randint(altura//2, altura - 100)
            x2 = x1 + np.random.randint(50, 150)
            y2 = y1 + np.random.randint(30, 100)
            intensidad = np.random.randint(100, 255)
            
            if forma == 'rectangulo':
                cv2.rectangle(imagen, (x1, y1), (x2, y2), int(intensidad), -1)
            else:  # elipse
                centro = ((x1 + x2) // 2, (y1 + y2) // 2)
                eje_mayor = abs(x2 - x1) // 2
                eje_menor = abs(y2 - y1) // 2
                cv2.ellipse(imagen, centro, (eje_mayor, eje_menor), 0, 0, 360, (int(intensidad), int(intensidad), int(intensidad)), -1)
        
        # Gradiente radial aleatorio
        centro_radial = (np.random.randint(ancho//4, 3*ancho//4), 
                        np.random.randint(altura//2, altura - 50))
        radio_max = np.random.randint(80, 150)
        intensidad_max = np.random.randint(200, 255)
        
        for y in range(altura):
            for x in range(ancho):
                distancia = np.sqrt((x - centro_radial[0])**2 + (y - centro_radial[1])**2)
                if distancia <= radio_max:
                    valor_actual = imagen[y, x]
                    nuevo_valor = max(valor_actual, int(intensidad_max * (1 - distancia / radio_max)))
                    imagen[y, x] = min(255, nuevo_valor)
        
        # Ruido más pronunciado para variación
        ruido = np.random.normal(0, 15, imagen.shape).astype(np.int16)
        imagen = np.clip(imagen.astype(np.int16) + ruido, 0, 255).astype(np.uint8)
        
    else:
        # Patrón fijo original (para consistencia en pruebas)
        print("Generando imagen con patrón fijo...")
        
        # Gradiente horizontal
        for x in range(ancho // 2):
            imagen[:altura//3, x] = int(255 * x / (ancho // 2))
        
        # Círculos con diferentes intensidades
        centros = [(100, 200), (300, 200), (200, 300)]
        radios = [40, 30, 50]
        intensidades = [180, 220, 255]
        
        for centro, radio, intensidad in zip(centros, radios, intensidades):
            cv2.circle(imagen, centro, radio, (intensidad, intensidad, intensidad), -1)
        
        # Rectángulo con gradiente
        for y in range(altura//3, 2*altura//3):
            for x in range(ancho//2, ancho):
                distancia = np.sqrt((x - ancho//2)**2 + (y - altura//2)**2)
                valor = max(0, 255 - int(distancia * 2))
                imagen[y, x] = valor
        
        # Ruido suave
        ruido = np.random.normal(0, 10, imagen.shape).astype(np.int16)
        imagen = np.clip(imagen.astype(np.int16) + ruido, 0, 255).astype(np.uint8)
    
    # Guardar la imagen
    ruta_imagen = os.path.join('ejemplos', 'imagen_ejemplo.jpg')
    cv2.imwrite(ruta_imagen, imagen)
    
    print(f"Imagen de ejemplo generada: {ruta_imagen}")
    return ruta_imagen


def demostrar_diferentes_mapas():
    """Demuestra el uso de diferentes mapas de colores."""
    
    # Generar imagen de ejemplo
    ruta_imagen = generar_imagen_ejemplo()
    
    # Mapas de colores a probar
    mapas = {
        'JET': cv2.COLORMAP_JET,
        'HOT': cv2.COLORMAP_HOT,
        'COOL': cv2.COLORMAP_COOL,
        'RAINBOW': cv2.COLORMAP_RAINBOW,
        'OCEAN': cv2.COLORMAP_OCEAN
    }
    
    print("\n=== DEMOSTRACIÓN DE MAPAS DE COLORES ===")
    
    for nombre_mapa, tipo_mapa in mapas.items():
        print(f"\nProcesando con mapa {nombre_mapa}...")
        
        # Crear simulador
        simulador = TermografiaSimulator()
        
        # Procesar imagen
        simulador.cargar_imagen(ruta_imagen)
        simulador.aplicar_mapa_termico(tipo_mapa)
        simulador.resaltar_zonas_calientes(umbral=200)
        
        # Guardar resultado
        archivo_salida = f'ejemplos/ejemplo_{nombre_mapa.lower()}.jpg'
        simulador.guardar_resultado(archivo_salida)
        
        print(f"Resultado guardado: {archivo_salida}")
    
    print("\n¡Demostración completada! Revisa la carpeta 'ejemplos' para ver los resultados.")


def ejemplo_interactivo():
    """Ejemplo interactivo que permite al usuario ajustar parámetros."""
    
    # Generar imagen si no existe
    ruta_imagen = os.path.join('ejemplos', 'imagen_ejemplo.jpg')
    if not os.path.exists(ruta_imagen):
        generar_imagen_ejemplo()
    
    print("\n=== EJEMPLO INTERACTIVO ===")
    print("Este ejemplo te permite experimentar con diferentes parámetros.")
    
    try:
        # Solicitar parámetros al usuario
        print(f"\nUsando imagen: {ruta_imagen}")
        
        print("\nMapas disponibles:")
        print("1. JET (azul-verde-amarillo-rojo)")
        print("2. HOT (negro-rojo-amarillo-blanco)")
        print("3. COOL (cian-magenta)")
        print("4. RAINBOW (espectro completo)")
        print("5. OCEAN (azules y verdes)")
        
        opcion_mapa = input("\nSelecciona un mapa (1-5, Enter para JET): ").strip()
        
        mapas_opciones = {
            '1': cv2.COLORMAP_JET,
            '2': cv2.COLORMAP_HOT,
            '3': cv2.COLORMAP_COOL,
            '4': cv2.COLORMAP_RAINBOW,
            '5': cv2.COLORMAP_OCEAN,
            '': cv2.COLORMAP_JET
        }
        
        tipo_mapa = mapas_opciones.get(opcion_mapa, cv2.COLORMAP_JET)
        
        umbral_input = input("Umbral para zonas calientes (0-255, Enter para 200): ").strip()
        umbral = int(umbral_input) if umbral_input.isdigit() else 200
        
        resaltar_input = input("¿Resaltar zonas calientes? (s/N): ").strip().lower()
        resaltar = resaltar_input in ['s', 'si', 'sí', 'y', 'yes']
        
        # Procesar imagen
        simulador = TermografiaSimulator()
        exito = simulador.procesar_imagen_completa(
            ruta_imagen=ruta_imagen,
            resaltar_calor=resaltar,
            umbral=umbral,
            tipo_mapa=tipo_mapa,
            mostrar=True,
            guardar=True,
            ruta_salida='ejemplos/resultado_interactivo.jpg'
        )
        
        if exito:
            print("\n¡Procesamiento completado exitosamente!")
        else:
            print("\nHubo un error en el procesamiento.")
            
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
    except Exception as e:
        print(f"\nError: {str(e)}")


def main():
    """Función principal del script de ejemplos."""
    
    print("=== EJEMPLOS DE SIMULACIÓN TERMOGRÁFICA ===")
    print("1. Generar imagen de ejemplo")
    print("2. Demostrar diferentes mapas de colores")
    print("3. Ejemplo interactivo")
    print("4. Ejecutar todo")
    
    try:
        opcion = input("\nSelecciona una opción (1-4): ").strip()
        
        if opcion == '1':
            generar_imagen_ejemplo()
        elif opcion == '2':
            demostrar_diferentes_mapas()
        elif opcion == '3':
            ejemplo_interactivo()
        elif opcion == '4':
            generar_imagen_ejemplo()
            demostrar_diferentes_mapas()
            ejemplo_interactivo()
        else:
            print("Opción no válida.")
            
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario.")
    except Exception as e:
        print(f"\nError: {str(e)}")


if __name__ == "__main__":
    main()
