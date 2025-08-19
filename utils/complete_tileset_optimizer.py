#!/usr/bin/env python3
"""
Script para optimización completa del TileSet.
Elimina tanto tiles duplicados como tiles no utilizados.
"""

import re
import os

# Tiles utilizados en el TileMap
USED_TILES = [0, 1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15, 17, 18, 19, 20, 21, 34, 35, 42, 43, 44, 48, 51, 53, 54, 56, 58, 62]

# Tiles duplicados que sabemos que podemos eliminar (de análisis anterior)
DUPLICATE_TILES = [64, 65, 66, 67]  # Duplican tiles 0, 1, 2, 3 respectivamente

def optimize_tileset_complete(tileset_path):
    """
    Optimización completa: elimina tiles duplicados y no utilizados del final
    """
    print(f"🔧 Optimizando TileSet: {tileset_path}")
    
    # Calcular todos los tiles a eliminar
    highest_used = max(USED_TILES)
    
    # Tiles no utilizados del final (después del tile con mayor ID utilizado)
    unused_end_tiles = []
    for tile_id in range(highest_used + 1, 100):  # Buscar hasta el 100 para estar seguros
        unused_end_tiles.append(tile_id)
    
    # Combinar duplicados y tiles del final no utilizados
    all_tiles_to_remove = set(DUPLICATE_TILES + unused_end_tiles)
    
    print(f"Tiles duplicados a eliminar: {DUPLICATE_TILES}")
    print(f"Tiles no utilizados del final: {unused_end_tiles}")
    print(f"Total de tiles a eliminar: {len(all_tiles_to_remove)}")
    
    # Leer archivo actual
    with open(tileset_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    optimized_lines = []
    tiles_removed = 0
    current_tile_id = None
    skip_until_next_tile = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Detectar definición de tile
        tile_match = re.match(r'^(\d+)/name = "', line)
        if tile_match:
            current_tile_id = int(tile_match.group(1))
            should_remove = current_tile_id in all_tiles_to_remove
            
            if should_remove:
                print(f"  Eliminando tile {current_tile_id}...")
                tiles_removed += 1
                
                # Saltar todas las líneas de este tile hasta el siguiente tile
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    # Si encontramos otro tile, parar
                    next_tile_match = re.match(r'^(\d+)/', next_line)
                    if next_tile_match and int(next_tile_match.group(1)) != current_tile_id:
                        # No incrementar i aquí porque queremos procesar esta línea
                        break
                    i += 1
                continue
        
        # Si llegamos aquí, la línea debe ser mantenida
        optimized_lines.append(line)
        i += 1
    
    # Escribir archivo optimizado
    optimized_content = '\n'.join(optimized_lines)
    with open(tileset_path, 'w', encoding='utf-8') as f:
        f.write(optimized_content)
    
    print(f"✅ Eliminados {tiles_removed} tiles del TileSet")
    return tiles_removed

def verify_optimization_complete(tileset_path):
    """Verificación completa de la optimización"""
    
    with open(tileset_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar todos los tiles definidos
    tile_pattern = r'^(\d+)/name = "'
    tiles_found = []
    
    for line in content.split('\n'):
        match = re.match(tile_pattern, line)
        if match:
            tiles_found.append(int(match.group(1)))
    
    tiles_found.sort()
    
    print(f"\n=== VERIFICACIÓN COMPLETA ===")
    print(f"Tiles restantes en TileSet: {len(tiles_found)}")
    if tiles_found:
        print(f"Rango: {min(tiles_found)} a {max(tiles_found)}")
        print(f"Lista: {tiles_found}")
    
    # Verificar que todos los tiles utilizados están presentes
    missing_tiles = [tile for tile in USED_TILES if tile not in tiles_found]
    if missing_tiles:
        print(f"❌ ERROR: Tiles utilizados que faltan: {missing_tiles}")
        return False
    
    # Verificar que tiles duplicados fueron eliminados
    remaining_duplicates = [tile for tile in DUPLICATE_TILES if tile in tiles_found]
    if remaining_duplicates:
        print(f"⚠️  Tiles duplicados que aún existen: {remaining_duplicates}")
    
    # Verificar eficiencia
    efficiency = (len(USED_TILES) / len(tiles_found)) * 100 if tiles_found else 0
    print(f"📊 Eficiencia final: {efficiency:.1f}% ({len(USED_TILES)}/{len(tiles_found)} tiles utilizados)")
    
    print("✅ Todos los tiles utilizados están presentes")
    return True

def main():
    tileset_path = "tilesets/ash_room_small.tres"
    
    if not os.path.exists(tileset_path):
        print(f"❌ Error: No se encontró el archivo {tileset_path}")
        return
    
    print("=== OPTIMIZACIÓN COMPLETA DEL TILESET ===")
    print(f"Tiles utilizados: {len(USED_TILES)} -> {USED_TILES}")
    print(f"Tiles duplicados conocidos: {DUPLICATE_TILES}")
    print()
    
    # Realizar optimización
    tiles_removed = optimize_tileset_complete(tileset_path)
    
    if tiles_removed > 0:
        # Verificar resultado
        if verify_optimization_complete(tileset_path):
            print("\n✅ OPTIMIZACIÓN COMPLETA EXITOSA")
            print("   TileSet optimizado al máximo de forma segura")
        else:
            print("\n❌ ERROR EN LA OPTIMIZACIÓN")
            print("   Se recomienda restaurar backup")

if __name__ == "__main__":
    main()