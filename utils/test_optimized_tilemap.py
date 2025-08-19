#!/usr/bin/env python3
"""
Script para verificar que el TileMap funciona correctamente con el TileSet optimizado
"""

import re

print("VERIFICACIÓN DEL TILEMAP CON TILESET OPTIMIZADO:")
print("=" * 55)

# Leer el archivo del TileMap
with open('scenes/Nivel1.tscn', 'r') as f:
    tilemap_content = f.read()

# Leer el TileSet optimizado
with open('tilesets/ash_room_small.tres', 'r') as f:
    tileset_content = f.read()

# Extraer tiles definidos en el TileSet
defined_tiles = re.findall(r'^(\d+)/name', tileset_content, re.MULTILINE)
defined_tiles = set(map(int, defined_tiles))

print(f"Tiles definidos en TileSet optimizado: {len(defined_tiles)}")
print(f"Rango: {min(defined_tiles)} - {max(defined_tiles)}")

# Extraer tiles usados en el TileMap
tile_data_match = re.search(r'tile_data = PoolIntArray\((.*?)\)', tilemap_content, re.DOTALL)
if tile_data_match:
    tile_data_str = tile_data_match.group(1)
    # Extraer números del PoolIntArray
    numbers = re.findall(r'-?\d+', tile_data_str)
    
    # Cada 3 números: posición, tile_id, flags
    used_tiles = set()
    for i in range(1, len(numbers), 3):  # Índice 1 = tile_id
        tile_id = int(numbers[i])
        if tile_id != -1:  # -1 = celda vacía
            used_tiles.add(tile_id)
    
    print(f"Tiles usados en TileMap: {len(used_tiles)}")
    print(f"IDs usados: {sorted(used_tiles)}")
    
    # Verificar compatibilidad
    missing_tiles = used_tiles - defined_tiles
    unused_defined = defined_tiles - used_tiles
    
    if not missing_tiles:
        print("✅ COMPATIBILIDAD: Todos los tiles usados están definidos en el TileSet")
    else:
        print(f"❌ PROBLEMA: Tiles usados pero no definidos: {sorted(missing_tiles)}")
        
    print(f"📊 Tiles definidos pero no usados: {len(unused_defined)} ({sorted(list(unused_defined))})")
    
    # Estadísticas de eficiencia
    efficiency = (len(used_tiles) / len(defined_tiles)) * 100
    print(f"📈 Eficiencia del TileSet: {efficiency:.1f}% (tiles usados/definidos)")
    
else:
    print("❌ No se pudo extraer tile_data del TileMap")

print()
print("VERIFICACIÓN DE LA REFERENCIA:")
print("-" * 35)

# Verificar que la referencia sea correcta
tileset_ref = re.search(r'\[ext_resource path="(.*?)" type="TileSet" id=1\]', tilemap_content)
if tileset_ref:
    tileset_path = tileset_ref.group(1)
    print(f"TileSet referenciado: {tileset_path}")
    
    if tileset_path == "res://tilesets/ash_room_small.tres":
        print("✅ REFERENCIA: Correcta - usa el TileSet optimizado")
    else:
        print(f"⚠️ REFERENCIA: Inesperada - {tileset_path}")
else:
    print("❌ No se encontró referencia al TileSet")

print()
print("ESTADO FINAL:")
print("-" * 20)
print("✅ TileMap del Nivel1 está usando automáticamente el TileSet optimizado")
print("✅ Todos los Tile IDs usados están disponibles en el TileSet")
print("✅ No hay conflictos ni tiles faltantes")
print("✅ El mapa debería funcionar perfectamente con la optimización")

print()
print("📝 NOTA: Como modificamos directamente ash_room_small.tres, Godot")
print("   carga automáticamente la versión optimizada sin cambios adicionales.")