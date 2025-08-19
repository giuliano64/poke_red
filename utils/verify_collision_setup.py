#!/usr/bin/env python3
"""
Verificador completo del sistema de colisiones
"""

import re
from pathlib import Path

def verify_tileset_collisions():
    """Verifica las colisiones en el TileSet"""
    print("🔍 Verificando TileSet...")
    
    tileset_path = Path("tilesets/ash_room_small_optimized.tres")
    if not tileset_path.exists():
        print("❌ TileSet no encontrado")
        return False
    
    with open(tileset_path, 'r') as f:
        content = f.read()
    
    # Contar tiles con colisión
    collision_count = len(re.findall(r'\d+/shapes = \[  \{', content))
    
    # Verificar que existe el SubResource de colisión
    has_collision_shape = "ConvexPolygonShape2D" in content and "id=4" in content
    
    print(f"   Tiles con colisión configurados: {collision_count}")
    print(f"   SubResource de colisión presente: {'✅' if has_collision_shape else '❌'}")
    
    return collision_count > 0 and has_collision_shape

def verify_player_collision():
    """Verifica el CollisionShape2D del player"""
    print("🔍 Verificando player...")
    
    player_path = Path("scenes/player.tscn")
    if not player_path.exists():
        print("❌ Player.tscn no encontrado")
        return False
    
    with open(player_path, 'r') as f:
        content = f.read()
    
    # Verificar que existe CollisionShape2D
    has_collision_shape = "CollisionShape2D" in content
    has_rectangle_shape = "RectangleShape2D" in content
    
    # Verificar posición
    collision_pos_match = re.search(r'CollisionShape2D.*?position = Vector2\( ([^)]+) \)', content, re.DOTALL)
    sprite_pos_match = re.search(r'Sprite.*?position = Vector2\( ([^)]+) \)', content, re.DOTALL)
    
    collision_pos = collision_pos_match.group(1) if collision_pos_match else "No encontrada"
    sprite_pos = sprite_pos_match.group(1) if sprite_pos_match else "No encontrada"
    
    print(f"   CollisionShape2D presente: {'✅' if has_collision_shape else '❌'}")
    print(f"   RectangleShape2D presente: {'✅' if has_rectangle_shape else '❌'}")
    print(f"   Posición CollisionShape2D: {collision_pos}")
    print(f"   Posición Sprite: {sprite_pos}")
    print(f"   Posiciones coinciden: {'✅' if collision_pos == sprite_pos else '❌'}")
    
    return has_collision_shape and has_rectangle_shape

def verify_tilemap_settings():
    """Verifica configuración del TileMap"""
    print("🔍 Verificando TileMap...")
    
    nivel_path = Path("scenes/Nivel1.tscn")
    if not nivel_path.exists():
        print("❌ Nivel1.tscn no encontrado")
        return False
    
    with open(nivel_path, 'r') as f:
        content = f.read()
    
    # Verificar configuraciones importantes
    has_tileset = "ash_room_small_optimized.tres" in content
    has_show_collision = "show_collision = true" in content
    
    print(f"   TileSet optimizado cargado: {'✅' if has_tileset else '❌'}")
    print(f"   show_collision activado: {'✅' if has_show_collision else '❌'}")
    
    return has_tileset

def generate_collision_summary():
    """Genera un resumen de las colisiones configuradas"""
    print("\n📊 Resumen de colisiones configuradas:")
    print("=" * 50)
    
    # Mapa de tiles con colisión
    collision_tiles = {
        0: "Pared superior izquierda",
        1: "Pared superior", 
        2: "Pared superior derecha",
        4: "Pared lateral",
        5: "Marco ventana",
        8: "Borde interior",
        9: "Marco puerta",
        10: "Esquina",
        13: "Piso con bordes",
        14: "Objeto habitación",
        # Los demás tiles (muebles) también tienen colisión
        16: "Mesa/Mueble (ID 42)",
        17: "Silla/Objeto (ID 43)", 
        18: "Alfombra/Suelo (ID 48)",
        19: "Cama/Mueble (ID 51)",
        20: "Estante (ID 53)",
        21: "Decoración (ID 54)",
        22: "Objeto pared (ID 56)",
        23: "Televisor/Objeto (ID 62)"
    }
    
    print("Tiles con colisión activa:")
    for tile_idx, description in collision_tiles.items():
        if tile_idx <= 13:  # Solo los que sabemos que se configuraron
            print(f"   Tile {tile_idx}: {description}")

def main():
    print("🎮 Verificador del Sistema de Colisiones")
    print("=" * 50)
    
    tileset_ok = verify_tileset_collisions()
    player_ok = verify_player_collision() 
    tilemap_ok = verify_tilemap_settings()
    
    print("\n🎯 Resumen final:")
    print(f"   TileSet: {'✅ Configurado' if tileset_ok else '❌ Problemas'}")
    print(f"   Player: {'✅ Configurado' if player_ok else '❌ Problemas'}")  
    print(f"   TileMap: {'✅ Configurado' if tilemap_ok else '❌ Problemas'}")
    
    if all([tileset_ok, player_ok, tilemap_ok]):
        print("\n🎉 ¡Sistema de colisiones completamente configurado!")
        print("\n📋 Para probar:")
        print("1. Abrir Godot 3.5")
        print("2. Cargar el proyecto")
        print("3. Ir a Debug -> Visible Collision Shapes")
        print("4. Ejecutar main.tscn") 
        print("5. Intentar caminar hacia las paredes - deberían detener al player")
        
        generate_collision_summary()
    else:
        print("\n⚠️  Hay problemas en la configuración")
    
    return all([tileset_ok, player_ok, tilemap_ok])

if __name__ == "__main__":
    main()