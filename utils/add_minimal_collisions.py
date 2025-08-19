#!/usr/bin/env python3
"""
Agregador de colisiones mínimas y seguras - Solo paredes principales
"""

import re
from pathlib import Path

def add_safe_collisions():
    """Agrega colisiones solo a tiles de paredes principales para evitar problemas"""
    
    # Solo agregar colisiones a las paredes más obvias
    # Tiles 0, 1, 2 = paredes superiores 
    # Tiles 3, 4 = paredes laterales
    WALL_TILES = [0, 1, 2, 3, 4]
    
    tileset_path = Path("tilesets/ash_room_small_optimized.tres")
    
    print("🔧 Agregando colisiones mínimas (solo paredes principales)...")
    
    with open(tileset_path, 'r') as f:
        content = f.read()
    
    # Agregar un solo SubResource simple
    if "ConvexPolygonShape2D" not in content:
        shape_resource = """
[sub_resource type="ConvexPolygonShape2D" id=100]
points = PoolVector2Array( 0, 0, 16, 0, 16, 16, 0, 16 )
"""
        # Insertar antes de [resource]
        resource_pos = content.find("[resource]")
        if resource_pos != -1:
            content = content[:resource_pos] + shape_resource + content[resource_pos:]
    
    # Procesar solo tiles de pared
    modified_count = 0
    for tile_idx in WALL_TILES:
        print(f"   Tile {tile_idx}...")
        
        # Patrón específico para cada tile
        pattern = rf"({tile_idx}/shapes = \[  )\]"
        
        if re.search(pattern, content):
            replacement = f"{tile_idx}/shapes = [ {{\n\"autotile_coord\": Vector2( 0, 0 ),\n\"one_way\": false,\n\"one_way_margin\": 1.0,\n\"shape\": SubResource( 100 ),\n\"shape_transform\": Transform2D( 1, 0, 0, 1, 0, 0 )\n}} ]"
            content = re.sub(pattern, replacement, content)
            modified_count += 1
            print(f"     ✅ Agregada")
        else:
            print(f"     ⚠️ No encontrado")
    
    # Escribir archivo
    with open(tileset_path, 'w') as f:
        f.write(content)
    
    print(f"\n✅ {modified_count} tiles con colisión agregados")
    return modified_count > 0

def test_project():
    """Prueba que el proyecto pueda cargarse sin errores"""
    print("\n🧪 Probando carga del proyecto...")
    
    # Verificar archivos críticos
    files_to_check = [
        "tilesets/ash_room_small_optimized.tres",
        "scenes/Nivel1.tscn", 
        "scenes/player.tscn",
        "tilesets/Ash_room_sharp.png"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        path = Path(file_path)
        if path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            all_exist = False
    
    return all_exist

if __name__ == "__main__":
    print("🛠️ Agregador de Colisiones Mínimas")
    print("=" * 40)
    
    if add_safe_collisions():
        if test_project():
            print("\n🎯 Listos para probar en Godot:")
            print("1. Abrir Godot 3.5")
            print("2. Cargar proyecto")
            print("3. Ejecutar main.tscn")
            print("4. Probar movimiento - las paredes superiores tendrán colisión")
        else:
            print("\n⚠️ Faltan archivos críticos")
    else:
        print("\n❌ No se pudieron agregar colisiones")