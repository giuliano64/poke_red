#!/usr/bin/env python3
"""
Script para eliminar definitivamente los tiles no utilizados del TileSet
"""

import re

def remove_tiles_precise(tileset_path, tiles_to_remove):
    """Elimina tiles específicos del TileSet de forma precisa"""
    
    print(f"🔧 Eliminando tiles: {tiles_to_remove}")
    
    with open(tileset_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Buscar inicio de definición de tile
        tile_match = re.match(r'^(\d+)/name = "', line)
        if tile_match:
            tile_id = int(tile_match.group(1))
            
            if tile_id in tiles_to_remove:
                print(f"  Eliminando tile {tile_id}...")
                
                # Saltar todas las líneas de este tile
                i += 1
                while i < len(lines):
                    next_line = lines[i]
                    
                    # Si es otra línea del mismo tile (formato número/)
                    if re.match(rf'^{tile_id}/', next_line):
                        i += 1
                        continue
                    
                    # Si es el inicio de otro tile, salir del loop sin incrementar i
                    if re.match(r'^(\d+)/', next_line):
                        break
                    
                    # Si es una línea que no pertenece a ningún tile específico
                    # (como líneas vacías al final), salir
                    break
                continue
        
        # Si llegamos aquí, conservar la línea
        new_lines.append(line)
        i += 1
    
    # Escribir el archivo
    new_content = '\n'.join(new_lines)
    with open(tileset_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Tiles eliminados correctamente")

def verify_removal(tileset_path, removed_tiles):
    """Verificar que los tiles fueron eliminados"""
    
    with open(tileset_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    remaining_tiles = []
    for line in content.split('\n'):
        tile_match = re.match(r'^(\d+)/name = "', line)
        if tile_match:
            remaining_tiles.append(int(tile_match.group(1)))
    
    remaining_tiles.sort()
    
    print(f"\nTiles restantes: {len(remaining_tiles)}")
    print(f"Rango: {min(remaining_tiles) if remaining_tiles else 'N/A'} a {max(remaining_tiles) if remaining_tiles else 'N/A'}")
    
    # Verificar que los tiles eliminados ya no están
    still_present = [t for t in removed_tiles if t in remaining_tiles]
    if still_present:
        print(f"❌ ERROR: Estos tiles aún están presentes: {still_present}")
        return False
    else:
        print(f"✅ Tiles eliminados correctamente: {removed_tiles}")
        return True

def main():
    tileset_path = "tilesets/ash_room_small.tres"
    
    # Tiles a eliminar: duplicados (64-67) + tile no utilizado del final (63)
    tiles_to_remove = [63, 64, 65, 66, 67]
    
    print("=== ELIMINACIÓN PRECISA DE TILES ===")
    print(f"Archivo: {tileset_path}")
    print(f"Tiles a eliminar: {tiles_to_remove}")
    
    remove_tiles_precise(tileset_path, tiles_to_remove)
    
    if verify_removal(tileset_path, tiles_to_remove):
        print("\n✅ ELIMINACIÓN EXITOSA")
        print("TileSet optimizado correctamente")
    else:
        print("\n❌ FALLÓ LA ELIMINACIÓN")

if __name__ == "__main__":
    main()