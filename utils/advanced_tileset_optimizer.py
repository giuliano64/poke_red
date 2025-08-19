#!/usr/bin/env python3
"""
Script para optimización avanzada y segura del TileSet.
Elimina tiles no utilizados de forma conservativa para evitar problemas de remapeo.
"""

import re
import os
from datetime import datetime

# Tiles utilizados en el TileMap
USED_TILES = [0, 1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15, 17, 18, 19, 20, 21, 34, 35, 42, 43, 44, 48, 51, 53, 54, 56, 58, 62]

def find_safe_tiles_to_remove(used_tiles, max_tile_id=63):
    """
    Encuentra tiles seguros para eliminar sin necesidad de remapeo.
    Estrategia conservativa: eliminar solo tiles del final que no están siendo utilizados.
    """
    # Encontrar el tile con mayor ID que está siendo utilizado
    highest_used = max(used_tiles)
    
    # Tiles que podemos eliminar safely (desde highest_used+1 hasta max_tile_id)
    safe_to_remove = []
    for tile_id in range(highest_used + 1, max_tile_id + 1):
        if tile_id not in used_tiles:
            safe_to_remove.append(tile_id)
    
    print(f"Tile con mayor ID utilizado: {highest_used}")
    print(f"Tiles seguros para eliminar (del final): {safe_to_remove}")
    print(f"Reducción segura: {len(safe_to_remove)} tiles")
    
    return safe_to_remove, highest_used

def optimize_tileset_conservative(tileset_path, safe_tiles_to_remove):
    """
    Optimiza el TileSet eliminando solo tiles seguros del final
    """
    if not safe_tiles_to_remove:
        print("❌ No hay tiles seguros para eliminar.")
        return False
    
    print(f"🔧 Optimizando TileSet eliminando tiles: {safe_tiles_to_remove}")
    
    # Leer archivo actual
    with open(tileset_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    optimized_lines = []
    tiles_removed = 0
    current_tile_id = None
    skip_until_next_tile = False
    
    for line in lines:
        # Detectar definición de tile
        tile_match = re.match(r'^(\d+)/name = "', line)
        if tile_match:
            current_tile_id = int(tile_match.group(1))
            skip_until_next_tile = current_tile_id in safe_tiles_to_remove
            
            if skip_until_next_tile:
                print(f"  Eliminando tile {current_tile_id}...")
                tiles_removed += 1
                continue
        
        # Si estamos saltando un tile, no agregar líneas hasta el siguiente
        if skip_until_next_tile:
            # Verificar si esta línea pertenece al tile actual o es una nueva sección
            next_tile_match = re.match(r'^(\d+)/', line)
            if next_tile_match and int(next_tile_match.group(1)) != current_tile_id:
                # Es un nuevo tile, dejar de saltar
                current_tile_id = int(next_tile_match.group(1))
                skip_until_next_tile = current_tile_id in safe_tiles_to_remove
                if not skip_until_next_tile:
                    optimized_lines.append(line)
            # Si no es un nuevo tile, seguir saltando
        else:
            optimized_lines.append(line)
    
    # Escribir archivo optimizado
    optimized_content = '\n'.join(optimized_lines)
    with open(tileset_path, 'w', encoding='utf-8') as f:
        f.write(optimized_content)
    
    print(f"✅ Optimización completada. Eliminados {tiles_removed} tiles.")
    return True

def verify_tileset_structure(tileset_path):
    """Verifica la estructura del TileSet después de la optimización"""
    
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
    
    print(f"\n=== VERIFICACIÓN POST-OPTIMIZACIÓN ===")
    print(f"Tiles encontrados en TileSet: {len(tiles_found)}")
    print(f"Rango de tiles: {min(tiles_found)} a {max(tiles_found)}")
    print(f"Lista de tiles: {tiles_found}")
    
    # Verificar que todos los tiles utilizados están presentes
    missing_tiles = [tile for tile in USED_TILES if tile not in tiles_found]
    if missing_tiles:
        print(f"❌ ERROR: Tiles utilizados que faltan: {missing_tiles}")
        return False
    else:
        print("✅ Todos los tiles utilizados están presentes")
        return True

def main():
    tileset_path = "tilesets/ash_room_small.tres"
    
    if not os.path.exists(tileset_path):
        print(f"❌ Error: No se encontró el archivo {tileset_path}")
        return
    
    print("=== OPTIMIZACIÓN AVANZADA DEL TILESET ===")
    print(f"Archivo objetivo: {tileset_path}")
    print(f"Tiles utilizados: {len(USED_TILES)}")
    print(f"Tiles utilizados: {USED_TILES}")
    print()
    
    # Encontrar tiles seguros para eliminar
    safe_tiles, highest_used = find_safe_tiles_to_remove(USED_TILES)
    
    if not safe_tiles:
        print("❌ No se encontraron tiles seguros para eliminar de forma conservativa.")
        print("   Todos los tiles del final están siendo utilizados.")
        return
    
    print(f"\n🎯 Se eliminarán {len(safe_tiles)} tiles del final (tiles {safe_tiles[0]}-{safe_tiles[-1]})")
    print(f"📊 Esto mejorará la eficiencia de {len(USED_TILES)}/64 = {(len(USED_TILES)/64)*100:.1f}% a {len(USED_TILES)}/{highest_used+1} = {(len(USED_TILES)/(highest_used+1))*100:.1f}%")
    
    # Confirmar optimización
    response = input("\n¿Proceder con la optimización? (s/n): ")
    if response.lower() != 's':
        print("❌ Optimización cancelada.")
        return
    
    # Realizar optimización
    success = optimize_tileset_conservative(tileset_path, safe_tiles)
    
    if success:
        # Verificar resultado
        if verify_tileset_structure(tileset_path):
            print("\n✅ OPTIMIZACIÓN EXITOSA")
            print("   El TileSet ha sido optimizado de forma segura.")
            print("   Todos los tiles utilizados están presentes.")
        else:
            print("\n❌ ERROR EN LA OPTIMIZACIÓN")
            print("   Restaurando backup...")
            
            # Buscar el backup más reciente
            backup_files = [f for f in os.listdir("tilesets/") if f.startswith("ash_room_small.tres.backup_before_advanced")]
            if backup_files:
                latest_backup = max(backup_files)
                os.system(f'cp "tilesets/{latest_backup}" "{tileset_path}"')
                print(f"   Backup restaurado desde: {latest_backup}")
    
    print(f"\n📁 Backup disponible en: tilesets/ash_room_small.tres.backup_before_advanced_optimization_*")

if __name__ == "__main__":
    main()