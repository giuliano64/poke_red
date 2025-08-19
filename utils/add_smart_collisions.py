#!/usr/bin/env python3
"""
Script inteligente para agregar colisiones al TileSet optimizado.
Mapea los Tile IDs usados en el TileMap con los índices del TileSet optimizado.
"""

import re
from pathlib import Path

def get_tilemap_tile_ids():
    """Extrae los Tile IDs utilizados en el TileMap"""
    nivel_path = Path("scenes/Nivel1.tscn")
    
    if not nivel_path.exists():
        return []
    
    with open(nivel_path, 'r') as f:
        content = f.read()
    
    # Buscar tile_data
    tile_data_match = re.search(r'tile_data = PoolIntArray\( ([^)]+) \)', content)
    if not tile_data_match:
        return []
    
    tile_data = tile_data_match.group(1)
    
    # Extraer los Tile IDs (cada tercer número, empezando desde el segundo)
    numbers = [int(x.strip()) for x in tile_data.split(',')]
    tile_ids = set()
    
    # Formato: posición, tile_id, flip_flags
    for i in range(1, len(numbers), 3):
        if i < len(numbers):
            tile_ids.add(numbers[i])
    
    return sorted(list(tile_ids))

def get_tileset_mapping():
    """Obtiene el mapeo entre índices del TileSet y los Tile IDs originales"""
    tileset_path = Path("tilesets/ash_room_small_optimized.tres")
    
    if not tileset_path.exists():
        return {}
    
    with open(tileset_path, 'r') as f:
        content = f.read()
    
    mapping = {}
    
    # Buscar todos los tiles en el TileSet
    tile_pattern = r'(\d+)/name = "AshRoom_Small_(\d+)"'
    matches = re.findall(tile_pattern, content)
    
    for tileset_index, original_id in matches:
        mapping[int(original_id)] = int(tileset_index)
    
    return mapping

def identify_collision_tiles():
    """Identifica qué Tile IDs necesitan colisión basándose en el análisis visual"""
    
    # Tiles que representan paredes y objetos sólidos
    # Basado en la matriz del mapa y análisis visual
    wall_tiles = [0, 1, 2, 4, 5, 6]  # Paredes superiores
    object_tiles = [8, 9, 10, 13, 14, 15]  # Marcos y bordes  
    furniture_tiles = [42, 43, 44, 48, 51, 53, 54, 56, 58, 62]  # Muebles y objetos
    
    return wall_tiles + object_tiles + furniture_tiles

def add_collisions():
    """Agrega colisiones a los tiles apropiados"""
    
    # Obtener mapeos
    used_tile_ids = get_tilemap_tile_ids()
    tileset_mapping = get_tileset_mapping()
    collision_tile_ids = identify_collision_tiles()
    
    print("📊 Análisis del mapa:")
    print(f"   Tile IDs usados en el mapa: {used_tile_ids}")
    print(f"   Tiles que necesitan colisión: {collision_tile_ids}")
    
    # Filtrar solo los tiles que realmente existen y se usan
    tiles_to_process = []
    for tile_id in collision_tile_ids:
        if tile_id in used_tile_ids and tile_id in tileset_mapping:
            tileset_index = tileset_mapping[tile_id]
            tiles_to_process.append((tile_id, tileset_index))
    
    print(f"   Tiles a procesar: {[(f'ID{tid}->Idx{idx}') for tid, idx in tiles_to_process]}")
    
    if not tiles_to_process:
        print("❌ No se encontraron tiles para procesar")
        return False
    
    # Leer TileSet
    tileset_path = Path("tilesets/ash_room_small_optimized.tres")
    with open(tileset_path, 'r') as f:
        content = f.read()
    
    # Verificar que el SubResource de colisión existe
    if "id=4" not in content:
        print("🔧 Agregando SubResource de colisión...")
        # Insertar después del último SubResource
        insert_pos = content.rfind("[sub_resource")
        if insert_pos != -1:
            # Encontrar el final de ese SubResource
            insert_pos = content.find("\n", content.find("points = ", insert_pos))
            collision_shape = """
[sub_resource type="ConvexPolygonShape2D" id=4]
points = PoolVector2Array( 0, 0, 16, 0, 16, 16, 0, 16 )"""
            content = content[:insert_pos] + collision_shape + content[insert_pos:]
    
    # Agregar colisiones
    modified_count = 0
    for tile_id, tileset_index in tiles_to_process:
        print(f"🔧 Agregando colisión a Tile ID {tile_id} (índice {tileset_index})...")
        
        # Buscar el patrón del tile
        pattern = rf"({tileset_index}/shapes = \[  )\]"
        match = re.search(pattern, content)
        
        if match:
            # Configuración de colisión
            collision_config = """{
"autotile_coord": Vector2( 0, 0 ),
"one_way": false,
"one_way_margin": 1.0,
"shape": SubResource( 4 ),
"shape_transform": Transform2D( 1, 0, 0, 1, 0, 0 )
} ]"""
            
            replacement = f"{match.group(1)}{collision_config}"
            content = re.sub(pattern, replacement, content)
            modified_count += 1
            print(f"   ✅ Colisión agregada")
        else:
            print(f"   ❌ No se encontró el patrón para el índice {tileset_index}")
    
    # Escribir archivo modificado
    with open(tileset_path, 'w') as f:
        f.write(content)
    
    print(f"\n✅ Proceso completado!")
    print(f"   Tiles modificados: {modified_count}/{len(tiles_to_process)}")
    
    return modified_count > 0

if __name__ == "__main__":
    print("🎮 Configurador Inteligente de Colisiones")
    print("=" * 50)
    
    if add_collisions():
        print("\n🎯 Siguientes pasos:")
        print("1. Abrir Godot")
        print("2. Activar Debug -> Visible Collision Shapes") 
        print("3. Ejecutar el juego para probar")
    else:
        print("❌ No se pudieron agregar las colisiones")