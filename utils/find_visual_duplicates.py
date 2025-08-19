#!/usr/bin/env python3
"""
Script para encontrar tiles duplicados basándose en la región visual (coordenadas del sprite)
"""

import re

def analyze_visual_duplicates(tileset_path):
    """Analiza el TileSet para encontrar tiles con la misma región visual"""
    
    with open(tileset_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Diccionario para agrupar tiles por región
    regions = {}  # region -> [tile_ids]
    tile_info = {}  # tile_id -> {name, region, texture}
    
    current_tile_id = None
    
    for line in lines:
        # Detectar tile ID
        tile_match = re.match(r'^(\d+)/name = "([^"]*)"', line)
        if tile_match:
            current_tile_id = int(tile_match.group(1))
            tile_name = tile_match.group(2)
            tile_info[current_tile_id] = {'name': tile_name}
            continue
        
        if current_tile_id is not None:
            # Detectar región
            region_match = re.match(r'^' + str(current_tile_id) + r'/region = Rect2\( ([0-9]+), ([0-9]+), ([0-9]+), ([0-9]+) \)', line)
            if region_match:
                x = int(region_match.group(1))
                y = int(region_match.group(2))
                w = int(region_match.group(3))
                h = int(region_match.group(4))
                region = (x, y, w, h)
                
                tile_info[current_tile_id]['region'] = region
                
                # Agrupar por región
                if region not in regions:
                    regions[region] = []
                regions[region].append(current_tile_id)
                continue
            
            # Detectar textura
            texture_match = re.match(r'^' + str(current_tile_id) + r'/texture = ExtResource\( (\d+) \)', line)
            if texture_match:
                texture_id = int(texture_match.group(1))
                tile_info[current_tile_id]['texture'] = texture_id
    
    return regions, tile_info

def find_true_duplicates(regions, tile_info, used_tiles):
    """Encuentra duplicados verdaderos considerando textura y si están en uso"""
    
    print("=== ANÁLISIS DE DUPLICADOS VISUALES ===")
    print()
    
    duplicates = []
    
    for region, tile_ids in regions.items():
        if len(tile_ids) > 1:
            # Verificar que usen la misma textura
            textures = set()
            for tile_id in tile_ids:
                if 'texture' in tile_info[tile_id]:
                    textures.add(tile_info[tile_id]['texture'])
            
            if len(textures) == 1:  # Misma textura
                # Separar en usados y no usados
                used = [tid for tid in tile_ids if tid in used_tiles]
                unused = [tid for tid in tile_ids if tid not in used_tiles]
                
                print(f"🔍 REGIÓN {region} (Texture {list(textures)[0]}):")
                for tile_id in sorted(tile_ids):
                    status = "🎯 USADO" if tile_id in used_tiles else "⚫ NO USADO"
                    name = tile_info[tile_id].get('name', 'Sin nombre')
                    print(f"   Tile {tile_id:2d}: {name} {status}")
                
                if len(used) > 1:
                    print(f"   ⚠️  PROBLEMA: {len(used)} tiles USADOS con misma región!")
                    print(f"   📝 Tiles usados: {used}")
                elif len(used) == 1 and len(unused) > 0:
                    print(f"   ✅ OPTIMIZABLE: Eliminar tiles no usados {unused}")
                    duplicates.extend(unused)
                elif len(used) == 0:
                    # Ninguno usado, mantener el de menor ID
                    keep = min(tile_ids)
                    remove = [tid for tid in tile_ids if tid != keep]
                    print(f"   💡 Mantener tile {keep}, eliminar {remove}")
                    duplicates.extend(remove)
                
                print()
    
    return duplicates

def main():
    tileset_path = "tilesets/ash_room_small.tres"
    
    # Tiles utilizados en el TileMap
    used_tiles = {0, 1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15, 17, 18, 19, 20, 21, 34, 35, 42, 43, 44, 48, 51, 53, 54, 56, 58, 62}
    
    print("=== DETECTOR DE DUPLICADOS VISUALES ===")
    print(f"Analizando: {tileset_path}")
    print(f"Tiles utilizados en TileMap: {len(used_tiles)}")
    print()
    
    regions, tile_info = analyze_visual_duplicates(tileset_path)
    duplicates_to_remove = find_true_duplicates(regions, tile_info, used_tiles)
    
    print("=== RESUMEN ===")
    print(f"Tiles duplicados seguros para eliminar: {len(duplicates_to_remove)}")
    print(f"Lista: {sorted(duplicates_to_remove)}")
    
    if duplicates_to_remove:
        print()
        print("💡 RECOMENDACIÓN:")
        print("Estos tiles son duplicados visuales seguros para eliminar")
        print("(no están siendo utilizados en el TileMap o son duplicados de tiles utilizados)")

if __name__ == "__main__":
    main()