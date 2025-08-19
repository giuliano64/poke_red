#!/usr/bin/env python3
# Script para actualizar el TileMap con los nuevos IDs de tiles optimizados

import re

TILE_MAPPING = {0: 0, 1: 1, 2: 2, 4: 3, 5: 4, 6: 3, 8: 5, 9: 6, 10: 7, 13: 8, 14: 9, 15: 10, 17: 11, 18: 12, 19: 13, 20: 13, 21: 13, 34: 14, 35: 15, 42: 16, 43: 17, 44: 13, 48: 18, 51: 19, 53: 20, 54: 21, 56: 22, 58: 13, 62: 23}

def update_tilemap_data():
    tilemap_file = "scenes/Nivel1.tscn"
    
    with open(tilemap_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if line.startswith('tile_data = PoolIntArray('):
            print("🔄 Actualizando tile_data...")
            data_match = re.search(r'tile_data = PoolIntArray\( (.+) \)', line)
            if data_match:
                data_str = data_match.group(1)
                data_parts = [int(x.strip()) for x in data_str.split(',') if x.strip()]
                
                updated_data = []
                for i in range(0, len(data_parts), 3):
                    if i + 2 < len(data_parts):
                        pos = data_parts[i]
                        old_tile_id = data_parts[i + 1]
                        flags = data_parts[i + 2]
                        
                        new_tile_id = TILE_MAPPING.get(old_tile_id, old_tile_id)
                        updated_data.extend([pos, new_tile_id, flags])
                        
                        if old_tile_id != new_tile_id:
                            print(f"   Mapeando tile {old_tile_id} → {new_tile_id}")
                
                data_str_new = ', '.join(map(str, updated_data))
                new_line = f"tile_data = PoolIntArray( {data_str_new} )"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    with open(tilemap_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print("✅ TileMap actualizado exitosamente")
    return True

if __name__ == "__main__":
    print("=== ACTUALIZADOR DE TILEMAP ===")
    update_tilemap_data()
