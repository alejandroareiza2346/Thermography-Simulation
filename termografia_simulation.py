#!/usr/bin/env python3
"""
Simulación de Termografía con Python y OpenCV
Descripción: Script que convierte imágenes en escala de grises a simulaciones térmicas
utilizando mapas de colores de OpenCV.

Autor: [Tu nombre]
Fecha: Mayo 2025
"""

import cv2
import numpy as np
import os
import argparse
from pathlib import Path


class TermografiaSimulator:
    """Clase para simular imágenes termográficas a partir de imágenes en escala de grises."""
    
    def __init__(self):
        """Inicializa el simulador de termografía."""
        self.imagen_original = None
        self.imagen_termica = None
        self.imagen_grises = None
        
    def cargar_imagen(self, ruta_imagen):
        """
        Carga una imagen desde el disco.
        
        Args:
            ruta_imagen (str): Ruta al archivo de imagen
            
        Returns:
            bool: True si la imagen se cargó correctamente, False en caso contrario
        """
        try:
            # Verificar que el archivo existe
            if not os.path.exists(ruta_imagen):
                print(f"Error: El archivo {ruta_imagen} no existe.")
                return False
            
            # Cargar la imagen original
            self.imagen_original = cv2.imread(ruta_imagen)
            
            if self.imagen_original is None:
                print(f"Error: No se pudo cargar la imagen {ruta_imagen}")
                return False
            
            # Convertir a escala de grises
            self.imagen_grises = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2GRAY)
            
            print(f"Imagen cargada exitosamente: {ruta_imagen}")
            print(f"Dimensiones: {self.imagen_original.shape[:2]}")
            
            return True
            
        except Exception as e:
            print(f"Error al cargar la imagen: {str(e)}")
            return False
    
    def aplicar_mapa_termico(self, tipo_mapa=cv2.COLORMAP_JET):
        """
        Aplica un mapa de color térmico a la imagen en escala de grises.
        
        Args:
            tipo_mapa: Tipo de mapa de color de OpenCV (por defecto COLORMAP_JET)
            
        Returns:
            bool: True si se aplicó correctamente, False en caso contrario
        """
        try:
            if self.imagen_grises is None:
                print("Error: No hay imagen cargada para procesar.")
                return False
            
            # Aplicar el mapa de color térmico
            self.imagen_termica = cv2.applyColorMap(self.imagen_grises, tipo_mapa)
            
            print("Mapa térmico aplicado exitosamente.")
            return True
            
        except Exception as e:
            print(f"Error al aplicar el mapa térmico: {str(e)}")
            return False
    
    def resaltar_zonas_calientes(self, umbral=200):
        """
        Resalta las zonas con "temperaturas altas" (valores de píxeles altos).
        
        Args:
            umbral (int): Valor umbral para considerar una zona como "caliente" (0-255)
        """
        try:
            if self.imagen_termica is None:
                print("Error: No hay imagen térmica para procesar.")
                return False
            
            # Crear una máscara para los píxeles "calientes"
            if self.imagen_grises is None:
                print("Error: La imagen en escala de grises no está disponible.")
                return False
            
            mascara_caliente = self.imagen_grises > umbral
            
            # Crear una copia de la imagen térmica
            imagen_resaltada = self.imagen_termica.copy()
            
            # Resaltar las zonas calientes con un contorno blanco
            contornos, _ = cv2.findContours(
                mascara_caliente.astype(np.uint8), 
                cv2.RETR_EXTERNAL, 
                cv2.CHAIN_APPROX_SIMPLE
            )
            
            # Dibujar contornos en las zonas calientes
            cv2.drawContours(imagen_resaltada, contornos, -1, (255, 255, 255), 2)
            
            # Actualizar la imagen térmica con las zonas resaltadas
            self.imagen_termica = imagen_resaltada
            
            print(f"Zonas calientes resaltadas (umbral: {umbral})")
            print(f"Se encontraron {len(contornos)} zonas calientes")
            
            return True
            
        except Exception as e:
            print(f"Error al resaltar zonas calientes: {str(e)}")
            return False
    
    def mostrar_imagenes(self):
        """Muestra la imagen original y la imagen termográfica en ventanas separadas."""
        try:
            if self.imagen_original is None or self.imagen_termica is None:
                print("Error: Imágenes no disponibles para mostrar.")
                return False
            
            # Mostrar imagen original
            cv2.imshow('Imagen Original', self.imagen_original)
            
            # Mostrar imagen en escala de grises
            if self.imagen_grises is not None:
                cv2.imshow('Imagen en Escala de Grises', self.imagen_grises)
            else:
                print("Error: La imagen en escala de grises no está disponible.")
            
            # Mostrar imagen termográfica
            cv2.imshow('Simulación Termográfica', self.imagen_termica)
            
            print("Presiona cualquier tecla para cerrar las ventanas...")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            return True
            
        except Exception as e:
            print(f"Error al mostrar las imágenes: {str(e)}")
            return False
    
    def guardar_resultado(self, ruta_salida='termografia_resultado.jpg'):
        """
        Guarda la imagen termográfica en disco.
        
        Args:
            ruta_salida (str): Ruta donde guardar el resultado
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            if self.imagen_termica is None:
                print("Error: No hay imagen térmica para guardar.")
                return False
            
            # Guardar la imagen
            exito = cv2.imwrite(ruta_salida, self.imagen_termica)
            
            if exito:
                print(f"Imagen termográfica guardada en: {ruta_salida}")
                return True
            else:
                print("Error al guardar la imagen.")
                return False
                
        except Exception as e:
            print(f"Error al guardar la imagen: {str(e)}")
            return False
    
    def procesar_imagen_completa(self, ruta_imagen, resaltar_calor=True, umbral=200, 
                                tipo_mapa=cv2.COLORMAP_JET, mostrar=True, 
                                guardar=True, ruta_salida='termografia_resultado.jpg'):
        """
        Procesa una imagen completa aplicando todos los pasos de la simulación térmica.
        
        Args:
            ruta_imagen (str): Ruta a la imagen de entrada
            resaltar_calor (bool): Si resaltar zonas calientes
            umbral (int): Umbral para zonas calientes
            tipo_mapa: Tipo de mapa de color
            mostrar (bool): Si mostrar las imágenes
            guardar (bool): Si guardar el resultado
            ruta_salida (str): Ruta de salida
            
        Returns:
            bool: True si el procesamiento fue exitoso
        """
        print("=== INICIANDO SIMULACIÓN DE TERMOGRAFÍA ===")
        
        # 1. Cargar imagen
        if not self.cargar_imagen(ruta_imagen):
            return False
        
        # 2. Aplicar mapa térmico
        if not self.aplicar_mapa_termico(tipo_mapa):
            return False
        
        # 3. Resaltar zonas calientes (opcional)
        if resaltar_calor:
            self.resaltar_zonas_calientes(umbral)
        
        # 4. Mostrar imágenes (opcional)
        if mostrar:
            self.mostrar_imagenes()
        
        # 5. Guardar resultado (opcional)
        if guardar:
            self.guardar_resultado(ruta_salida)
        
        print("=== SIMULACIÓN COMPLETADA ===")
        return True


def main():
    """Función principal del programa."""
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description='Simulador de Termografía con OpenCV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python termografia_simulation.py imagen.jpg
  python termografia_simulation.py imagen.png --umbral 180 --no-mostrar
  python termografia_simulation.py imagen.jpg --salida mi_termografia.jpg --no-resaltar
        """
    )
    
    parser.add_argument('imagen', help='Ruta a la imagen de entrada (.jpg o .png)')
    parser.add_argument('--umbral', type=int, default=200, 
                       help='Umbral para zonas calientes (0-255, default: 200)')
    parser.add_argument('--salida', default='termografia_resultado.jpg',
                       help='Archivo de salida (default: termografia_resultado.jpg)')
    parser.add_argument('--no-resaltar', action='store_true',
                       help='No resaltar zonas calientes')
    parser.add_argument('--no-mostrar', action='store_true',
                       help='No mostrar ventanas de imágenes')
    parser.add_argument('--no-guardar', action='store_true',
                       help='No guardar el resultado')
    parser.add_argument('--mapa', choices=['jet', 'hot', 'cool', 'rainbow', 'ocean'],
                       default='jet', help='Tipo de mapa de color (default: jet)')
    
    args = parser.parse_args()
    
    # Mapear nombres de mapas a constantes de OpenCV
    mapas_color = {
        'jet': cv2.COLORMAP_JET,
        'hot': cv2.COLORMAP_HOT,
        'cool': cv2.COLORMAP_COOL,
        'rainbow': cv2.COLORMAP_RAINBOW,
        'ocean': cv2.COLORMAP_OCEAN
    }
    
    # Crear instancia del simulador
    simulador = TermografiaSimulator()
    
    # Procesar la imagen
    exito = simulador.procesar_imagen_completa(
        ruta_imagen=args.imagen,
        resaltar_calor=not args.no_resaltar,
        umbral=args.umbral,
        tipo_mapa=mapas_color[args.mapa],
        mostrar=not args.no_mostrar,
        guardar=not args.no_guardar,
        ruta_salida=args.salida
    )
    
    if not exito:
        print("Error: No se pudo completar el procesamiento.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
