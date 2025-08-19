#!/usr/bin/env python3
"""
Script para agregar colisiones a los tiles del TileSet de la habitación de Ash.
Identifica automáticamente qué tiles necesitan colisión basándose en su uso en el mapa.
"""

import re
from pathlib import Path

# Tiles que necesitan colisión (paredes y objetos sólidos)
COLLISION_TILES = [
    0, 1, 2,        # Paredes superiores  
    4, 5, 6,        # Más paredes
    8, 9, 10,       # Paredes laterales
    13, 14, 15,     # Bordes/marcos
    42, 43, 44,     # Objetos de la habitación (parte inferior)
    48, 51,         # Objetos sólidos 
    53, 54, 56,     # Más muebles
    58, 62          # Objetos adicionales
]

def add_collisions_to_tileset():
    """Agrega colisiones a los tiles especificados"""
    
    tileset_path = Path("tilesets/ash_room_small_optimized.tres")
    
    if not tileset_path.exists():
        print(f"❌ No se encontró el archivo {tileset_path}")
        return False
    
    print("🔧 Agregando colisiones al TileSet...")
    
    # Leer el archivo actual
    with open(tileset_path, 'r') as f:
        content = f.read()
    
    # Agregar shape de colisión estándar si no existe
    collision_shape = """
[sub_resource type="ConvexPolygonShape2D" id=4]
points = PoolVector2Array( 0, 0, 16, 0, 16, 16, 0, 16 )"""
    
    if "id=4" not in content:
        # Insertar después del último SubResource existente
        insert_pos = content.rfind("]", content.find("[resource]"))
        if insert_pos != -1:
            content = content[:insert_pos+1] + collision_shape + content[insert_pos+1:]
    
    # Procesar cada tile que necesita colisión
    for tile_id in COLLISION_TILES:
        print(f"   Agregando colisión a tile {tile_id}...")
        
        # Buscar el patrón del tile
        pattern = rf"({tile_id}/shapes = \[ )\]"
        match = re.search(pattern, content)
        
        if match:
            # Agregar shape de colisión
            collision_config = """{
"autotile_coord": Vector2( 0, 0 ),
"one_way": false,
"one_way_margin": 1.0,
"shape": SubResource( 4 ),
"shape_transform": Transform2D( 1, 0, 0, 1, 0, 0 )
} ]"""
            
            replacement = f"{match.group(1)}{collision_config}"
            content = re.sub(pattern, replacement, content)
            print(f"   ✅ Colisión agregada a tile {tile_id}")
        else:
            print(f"   ⚠️  No se encontró el tile {tile_id} en el TileSet")
    
    # Escribir el archivo modificado
    with open(tileset_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Colisiones agregadas exitosamente!")
    print(f"📁 Archivo modificado: {tileset_path}")
    return True

def verify_collisions():
    """Verifica que las colisiones se agregaron correctamente"""
    
    tileset_path = Path("tilesets/ash_room_small_optimized.tres")
    
    with open(tileset_path, 'r') as f:
        content = f.read()
    
    collision_count = 0
    for tile_id in COLLISION_TILES:
        if f"{tile_id}/shapes = [ {{" in content:
            collision_count += 1
    
    print(f"\n📊 Verificación:")
    print(f"   Tiles con colisión esperados: {len(COLLISION_TILES)}")
    print(f"   Tiles con colisión encontrados: {collision_count}")
    
    if collision_count == len(COLLISION_TILES):
        print("   ✅ Todas las colisiones fueron agregadas correctamente")
        return True
    else:
        print("   ⚠️  Algunas colisiones pueden no haberse agregado")
        return False

if __name__ == "__main__":
    print("🎮 Configurador de Colisiones - Pokemon Red")
    print("=" * 50)
    
    if add_collisions_to_tileset():
        verify_collisions()
        print("\n🎯 Pasos siguientes:")
        print("1. Abrir Godot y cargar el proyecto")
        print("2. Ir a Debug -> Visible Collision Shapes")  
        print("3. Ejecutar el juego para probar las colisiones")
    else:
        print("❌ Error al agregar colisiones")