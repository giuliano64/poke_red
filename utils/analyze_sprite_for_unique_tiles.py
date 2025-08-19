#!/usr/bin/env python3
"""
Analizador de sprites para crear TileSet optimizado
Identifica tiles únicos necesarios basándose en los tiles utilizados en el TileMap
"""

import re
from PIL import Image
import hashlib

# Tiles utilizados en el TileMap actual
USED_TILES = [0, 1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15, 17, 18, 19, 20, 21, 34, 35, 42, 43, 44, 48, 51, 53, 54, 56, 58, 62]

def extract_current_tile_regions(tileset_path):
    """Extrae las regiones de los tiles utilizados del TileSet actual"""
    
    with open(tileset_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    tile_regions = {}  # tile_id -> (x, y, w, h)
    current_tile_id = None
    
    for line in content.split('\n'):
        # Detectar tile ID
        tile_match = re.match(r'^(\d+)/name = "([^"]*)"', line)
        if tile_match:
            current_tile_id = int(tile_match.group(1))
            continue
        
        # Detectar región solo para tiles utilizados
        if current_tile_id in USED_TILES:
            region_match = re.match(r'^' + str(current_tile_id) + r'/region = Rect2\( ([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+) \)', line)
            if region_match:
                x = int(region_match.group(1))
                y = int(region_match.group(2))
                w = int(region_match.group(3))
                h = int(region_match.group(4))
                tile_regions[current_tile_id] = (x, y, w, h)
    
    return tile_regions

def get_tile_image_hash(image, x, y, w, h):
    """Obtiene hash del contenido visual de un tile"""
    tile_img = image.crop((x, y, x + w, y + h))
    # Convertir a bytes y calcular hash
    img_bytes = tile_img.tobytes()
    return hashlib.md5(img_bytes).hexdigest()

def analyze_unique_tiles(sprite_path, tile_regions):
    """Analiza el sprite para encontrar tiles únicos"""
    
    print(f"🎨 Analizando sprite: {sprite_path}")
    
    try:
        image = Image.open(sprite_path)
        print(f"📏 Dimensiones del sprite: {image.size}")
        print()
    except Exception as e:
        print(f"❌ Error cargando imagen: {e}")
        return {}, {}
    
    unique_tiles = {}  # hash -> (x, y, w, h, first_tile_id)
    tile_hashes = {}   # tile_id -> hash
    duplicates = {}    # hash -> [tile_ids]
    
    print("🔍 Analizando tiles utilizados:")
    for tile_id in sorted(USED_TILES):
        if tile_id not in tile_regions:
            print(f"   ⚠️  Tile {tile_id}: No se encontró región")
            continue
        
        x, y, w, h = tile_regions[tile_id]
        tile_hash = get_tile_image_hash(image, x, y, w, h)
        
        tile_hashes[tile_id] = tile_hash
        
        if tile_hash not in unique_tiles:
            unique_tiles[tile_hash] = (x, y, w, h, tile_id)
            duplicates[tile_hash] = [tile_id]
            print(f"   ✅ Tile {tile_id:2d}: ÚNICO - región ({x:3d},{y:3d},{w:2d},{h:2d})")
        else:
            duplicates[tile_hash].append(tile_id)
            original_tile = unique_tiles[tile_hash][4]
            print(f"   🔄 Tile {tile_id:2d}: DUPLICADO de tile {original_tile} - región ({x:3d},{y:3d},{w:2d},{h:2d})")
    
    return unique_tiles, duplicates, tile_hashes

def generate_optimization_report(unique_tiles, duplicates):
    """Genera reporte de optimización"""
    
    print(f"\n=== REPORTE DE OPTIMIZACIÓN ===")
    print(f"Tiles utilizados analizados: {len(USED_TILES)}")
    print(f"Tiles únicos encontrados: {len(unique_tiles)}")
    print(f"Duplicados identificados: {len(USED_TILES) - len(unique_tiles)}")
    print(f"Reducción posible: {((len(USED_TILES) - len(unique_tiles)) / len(USED_TILES)) * 100:.1f}%")
    print()
    
    if len(unique_tiles) < len(USED_TILES):
        print("🎯 DUPLICADOS ENCONTRADOS:")
        for tile_hash, tile_list in duplicates.items():
            if len(tile_list) > 1:
                x, y, w, h, original = unique_tiles[tile_hash]
                print(f"   Región ({x:3d},{y:3d}): Tile {original} ← {tile_list[1:]}")
        print()
    
    print("💡 NUEVO TILESET OPTIMIZADO:")
    new_id = 0
    old_to_new_mapping = {}
    
    for tile_hash, (x, y, w, h, original_tile_id) in unique_tiles.items():
        # El tile original mantiene su posición, pero ahora con nuevo ID secuencial
        for old_tile_id in duplicates[tile_hash]:
            old_to_new_mapping[old_tile_id] = new_id
        
        print(f"   Nuevo ID {new_id:2d}: región ({x:3d},{y:3d}) ← tiles antiguos {duplicates[tile_hash]}")
        new_id += 1
    
    return old_to_new_mapping

def main():
    tileset_path = "tilesets/ash_room_small.tres"
    sprite_path = "tilesets/Ash_room_sharp.png"
    
    print("=== ANALIZADOR DE TILES ÚNICOS ===")
    print("Objetivo: Crear TileSet optimizado con solo tiles necesarios")
    print()
    
    # 1. Extraer regiones de tiles utilizados
    tile_regions = extract_current_tile_regions(tileset_path)
    print(f"📊 Tiles utilizados con regiones: {len(tile_regions)}")
    
    if not tile_regions:
        print("❌ No se pudieron extraer regiones del TileSet")
        return
    
    # 2. Analizar sprite para encontrar tiles únicos
    unique_tiles, duplicates, tile_hashes = analyze_unique_tiles(sprite_path, tile_regions)
    
    # 3. Generar reporte
    old_to_new_mapping = generate_optimization_report(unique_tiles, duplicates)
    
    # 4. Guardar mapeo para usar en siguiente paso
    print(f"\n📁 Guardando mapeo de tiles...")
    with open("tile_mapping.txt", "w") as f:
        for old_id, new_id in sorted(old_to_new_mapping.items()):
            f.write(f"{old_id} -> {new_id}\n")
    
    print("✅ Análisis completado. Usa tile_mapping.txt para el siguiente paso.")

if __name__ == "__main__":
    main()