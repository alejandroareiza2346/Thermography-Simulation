#!/usr/bin/env python3
"""
Script de prueba para verificar que todas las dependencias están instaladas correctamente.
"""

import sys

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas correctamente."""
    
    dependencias_requeridas = [
        ('cv2', 'opencv-python'),
        ('numpy', 'numpy'),
        ('argparse', 'argparse'),
        ('pathlib', 'pathlib')
    ]
    
    print("=== VERIFICACIÓN DE DEPENDENCIAS ===")
    
    errores = []
    
    for modulo, paquete in dependencias_requeridas:
        try:
            __import__(modulo)
            print(f"✅ {paquete}: OK")
        except ImportError as e:
            print(f"❌ {paquete}: ERROR - {str(e)}")
            errores.append(paquete)
    
    if errores:
        print(f"\n❌ Se encontraron {len(errores)} errores:")
        for paquete in errores:
            print(f"   - {paquete}")
        print("\nPara instalar las dependencias faltantes:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("\n✅ Todas las dependencias están instaladas correctamente!")
        return True

def verificar_opencv():
    """Verifica funcionalidades específicas de OpenCV."""
    try:
        import cv2
        import numpy as np
        
        print("\n=== VERIFICACIÓN DE OPENCV ===")
        print(f"Versión de OpenCV: {cv2.__version__}")
        
        # Crear una imagen de prueba
        imagen_prueba = np.zeros((100, 100), dtype=np.uint8)
        imagen_prueba[25:75, 25:75] = 255
        
        # Probar aplicación de mapa de colores
        imagen_termica = cv2.applyColorMap(imagen_prueba, cv2.COLORMAP_JET)
        
        print("✅ OpenCV funciona correctamente")
        print(f"   - Imagen de prueba creada: {imagen_prueba.shape}")
        print(f"   - Mapa de colores aplicado: {imagen_termica.shape}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con OpenCV: {str(e)}")
        return False

def main():
    """Función principal."""
    print("Verificando instalación del proyecto de simulación termográfica...\n")
    
    # Verificar Python
    print(f"Versión de Python: {sys.version}")
    
    # Verificar dependencias
    deps_ok = verificar_dependencias()
    
    # Verificar OpenCV específicamente
    opencv_ok = verificar_opencv()
    
    print("\n" + "="*50)
    
    if deps_ok and opencv_ok:
        print("✅ INSTALACIÓN COMPLETA Y FUNCIONAL")
        print("\nPuedes ejecutar el simulador con:")
        print("python termografia_simulation.py --help")
        print("python ejemplos_demo.py")
    else:
        print("❌ PROBLEMAS ENCONTRADOS")
        print("\nResolve los errores mostrados arriba antes de continuar.")
    
    print("="*50)

if __name__ == "__main__":
    main()
