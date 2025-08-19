#!/usr/bin/env python3
"""
Script para analizar duplicados en el TileSet y mapear las regiones de sprites
"""
import re

# Leer el archivo de tileset
with open('tilesets/ash_room_small.tres', 'r') as f:
    content = f.read()

# Extraer todas las regiones de tiles
tile_regions = {}
pattern = r'(\d+)/region = Rect2\(\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\)'
matches = re.findall(pattern, content)

for match in matches:
    tile_id = int(match[0])
    x, y, w, h = map(int, match[1:])
    tile_regions[tile_id] = (x, y, w, h)

# Buscar regiones duplicadas
regions_to_tiles = {}
for tile_id, region in tile_regions.items():
    if region in regions_to_tiles:
        regions_to_tiles[region].append(tile_id)
    else:
        regions_to_tiles[region] = [tile_id]

# Mostrar información
print("ANÁLISIS DEL TILESET:")
print("=" * 50)
print(f"Total de tiles definidos: {len(tile_regions)}")
print()

print("REGIONES DUPLICADAS (mismo sprite, diferentes Tile IDs):")
print("-" * 50)
duplicates_found = False
for region, tile_ids in regions_to_tiles.items():
    if len(tile_ids) > 1:
        duplicates_found = True
        x, y, w, h = region
        print(f"Región ({x},{y},{w},{h}): Tile IDs {tile_ids}")

if not duplicates_found:
    print("No se encontraron regiones duplicadas.")

print()
print("TILES USADOS EN EL MAPA (de la matriz):")
print("-" * 50)
# Tiles que aparecen en nuestra matriz
used_tiles = {0, 1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15, 17, 18, 19, 20, 21, 34, 35, 42, 43, 44, 48, 51, 53, 54, 56, 58, 62}

print("Tile IDs usados en el mapa y sus regiones:")
for tile_id in sorted(used_tiles):
    if tile_id in tile_regions:
        region = tile_regions[tile_id]
        x, y, w, h = region
        print(f"Tile ID {tile_id:2d}: región ({x:3d},{y:3d},{w:2d},{h:2d})")
    else:
        print(f"Tile ID {tile_id:2d}: NO ENCONTRADO EN TILESET")

print()
print("ANÁLISIS DE POSIBLES SUELOS:")
print("-" * 50)
# Analizar tiles que podrían ser suelo (rango Y=0 a Y=-1 en la matriz)
floor_candidates = {5, 6, 13, 14, 15, 17, 18, 19, 20}
print("Tiles que aparecen en las filas Y=0 y Y=-1 (posibles suelos):")
for tile_id in sorted(floor_candidates):
    if tile_id in tile_regions:
        region = tile_regions[tile_id]
        x, y, w, h = region
        # Calcular posición en la imagen dividiendo por el tamaño del tile
        grid_x = x // 16
        grid_y = y // 16
        print(f"Tile ID {tile_id:2d}: región ({x:3d},{y:3d}) = posición en grid ({grid_x},{grid_y})")