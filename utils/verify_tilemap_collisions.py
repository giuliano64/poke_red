#!/usr/bin/env python3
"""
Verificador de colisiones del TileMap
"""

import re
from pathlib import Path

def verify_tilemap_setup():
    """Verifica la configuración de colisiones en el TileMap"""
    
    print("🎮 Verificando Sistema de Colisiones del TileMap")
    print("=" * 50)
    
    nivel_path = Path("scenes/Nivel1.tscn")
    
    if not nivel_path.exists():
        print("❌ Archivo Nivel1.tscn no encontrado")
        return False
    
    with open(nivel_path, 'r') as f:
        content = f.read()
    
    # Verificar elementos clave
    has_static_body = "StaticBody2D" in content
    has_collision_shapes = "CollisionShape2D" in content
    has_rectangle_shapes = "RectangleShape2D" in content
    collision_count = len(re.findall(r'CollisionShape2D.*parent="Nivel/StaticBody2D"', content))
    
    print("📋 Configuración encontrada:")
    print(f"   StaticBody2D presente: {'✅' if has_static_body else '❌'}")
    print(f"   CollisionShape2D presente: {'✅' if has_collision_shapes else '❌'}")
    print(f"   RectangleShape2D presente: {'✅' if has_rectangle_shapes else '❌'}")
    print(f"   Número de colisiones: {collision_count}")
    
    # Extraer posiciones de las colisiones
    collision_positions = re.findall(r'position = Vector2\( ([^)]+) \)', content)
    if collision_positions:
        print(f"\n📍 Posiciones de colisión:")
        for i, pos in enumerate(collision_positions[-3:]):  # Solo las últimas 3 (las colisiones)
            wall_names = ["TopWall", "LeftWall", "RightWall"]
            if i < len(wall_names):
                print(f"   {wall_names[i]}: {pos}")
    
    return has_static_body and has_collision_shapes and collision_count >= 3

def verify_player_setup():
    """Verifica que el player tenga su CollisionShape2D"""
    
    player_path = Path("scenes/player.tscn")
    
    if not player_path.exists():
        print("❌ Archivo player.tscn no encontrado")
        return False
    
    with open(player_path, 'r') as f:
        content = f.read()
    
    has_kinematic_body = "KinematicBody2D" in content
    has_collision_shape = "CollisionShape2D" in content
    
    print(f"\n🤖 Player configuration:")
    print(f"   KinematicBody2D: {'✅' if has_kinematic_body else '❌'}")
    print(f"   CollisionShape2D: {'✅' if has_collision_shape else '❌'}")
    
    return has_kinematic_body and has_collision_shape

def show_testing_instructions():
    """Muestra instrucciones para probar las colisiones"""
    
    print(f"\n🎯 Instrucciones para probar:")
    print("1. Abre Godot 3.5")
    print("2. Carga el proyecto")
    print("3. Ve a Debug -> Visible Collision Shapes (para ver las colisiones)")
    print("4. Ejecuta main.tscn")
    print("5. Usa las flechas para mover al player")
    print("6. El player NO debe poder salir de la habitación por:")
    print("   - Arriba (pared superior)")
    print("   - Izquierda (pared izquierda)")  
    print("   - Derecha (pared derecha)")
    
    print(f"\n💡 Configuración actual:")
    print("   - TopWall: Bloquea salida por arriba")
    print("   - LeftWall: Bloquea salida por la izquierda")
    print("   - RightWall: Bloquea salida por la derecha")
    print("   - La parte inferior queda abierta (para futuras conexiones)")

def main():
    tilemap_ok = verify_tilemap_setup()
    player_ok = verify_player_setup()
    
    if tilemap_ok and player_ok:
        print("\n🎉 ¡Sistema de colisiones configurado correctamente!")
        show_testing_instructions()
    else:
        print("\n⚠️ Hay problemas en la configuración")
    
    return tilemap_ok and player_ok

if __name__ == "__main__":
    main()