#!/usr/bin/env python3
"""
Script para verificar que la optimización del tilemap mantiene la apariencia visual
"""

# Datos originales
original = [
    -65540, 0, 0, -65539, 1, 0, -65538, 2, 0, -65537, 4, 0, -131072, 5, 0, -131071, 6, 0, -131070, 5, 0, -131069, 6, 0, 
    -4, 8, 0, -3, 9, 0, -2, 10, 0, -1, 13, 0, -65536, 13, 0, -65535, 13, 0, -65534, 14, 0, -65533, 15, 0, 
    65532, 20, 0, 65533, 17, 0, 65534, 18, 0, 65535, 20, 0, 0, 19, 0, 1, 20, 0, 2, 20, 0, 3, 19, 0, 
    131068, 19, 0, 131069, 21, 0, 131070, 34, 0, 131071, 35, 0, 65536, 58, 0, 65537, 19, 0, 65538, 21, 0, 65539, 19, 0, 
    196604, 48, 0, 196605, 48, 0, 196606, 42, 0, 196607, 43, 0, 131072, 58, 0, 131073, 58, 0, 131074, 53, 0, 131075, 54, 0, 
    262140, 56, 0, 262141, 56, 0, 262142, 44, 0, 262143, 51, 0, 196608, 58, 0, 196609, 58, 0, 196610, 58, 0, 196611, 62, 0
]

# Datos optimizados
optimized = [
    -65540, 0, 0, -65539, 0, 0, -65538, 0, 0, -65537, 5, 0, -131072, 5, 0, -131071, 6, 0, -131070, 5, 0, -131069, 6, 0, 
    -4, 9, 0, -3, 9, 0, -2, 9, 0, -1, 13, 0, -65536, 13, 0, -65535, 13, 0, -65534, 13, 0, -65533, 13, 0, 
    65532, 20, 0, 65533, 18, 0, 65534, 18, 0, 65535, 20, 0, 0, 19, 0, 1, 20, 0, 2, 20, 0, 3, 19, 0, 
    131068, 19, 0, 131069, 21, 0, 131070, 35, 0, 131071, 35, 0, 65536, 58, 0, 65537, 19, 0, 65538, 21, 0, 65539, 19, 0, 
    196604, 51, 0, 196605, 51, 0, 196606, 43, 0, 196607, 43, 0, 131072, 58, 0, 131073, 58, 0, 131074, 54, 0, 131075, 54, 0, 
    262140, 58, 0, 262141, 58, 0, 262142, 43, 0, 262143, 51, 0, 196608, 58, 0, 196609, 58, 0, 196610, 58, 0, 196611, 58, 0
]

def signed_to_coords(signed_pos):
    if signed_pos < 0:
        unsigned = signed_pos + 2**32
    else:
        unsigned = signed_pos
    
    x = unsigned & 0xFFFF
    y = (unsigned >> 16) & 0xFFFF
    
    if x >= 32768:
        x = x - 65536
    if y >= 32768:
        y = y - 65536
    
    return x, y

def extract_tiles(data):
    tiles = {}
    for i in range(0, len(data), 3):
        signed_pos = data[i]
        tile_id = data[i + 1]
        x, y = signed_to_coords(signed_pos)
        tiles[(x, y)] = tile_id
    return tiles

# Mapeo de regiones (de analyze_tileset.py)
tile_regions = {
    0: (0, 0, 16, 16), 1: (16, 0, 16, 16), 2: (32, 0, 16, 16), 4: (64, 0, 16, 16),
    5: (80, 0, 16, 16), 6: (96, 0, 16, 16), 8: (0, 16, 16, 16), 9: (16, 16, 16, 16),
    10: (32, 16, 16, 16), 13: (80, 16, 16, 16), 14: (96, 16, 16, 16), 15: (112, 16, 16, 16),
    17: (16, 32, 16, 16), 18: (32, 32, 16, 16), 19: (48, 32, 16, 16), 20: (64, 32, 16, 16),
    21: (80, 32, 16, 16), 34: (32, 64, 16, 16), 35: (48, 64, 16, 16), 42: (32, 80, 16, 16),
    43: (48, 80, 16, 16), 44: (64, 80, 16, 16), 48: (0, 96, 16, 16), 51: (48, 96, 16, 16),
    53: (80, 96, 16, 16), 54: (96, 96, 16, 16), 56: (0, 112, 16, 16), 58: (32, 112, 16, 16),
    62: (96, 112, 16, 16)
}

original_tiles = extract_tiles(original)
optimized_tiles = extract_tiles(optimized)

print("VERIFICACIÓN DE LA OPTIMIZACIÓN:")
print("=" * 50)
print(f"Posiciones en mapa original: {len(original_tiles)}")
print(f"Posiciones en mapa optimizado: {len(optimized_tiles)}")
print()

# Verificar que todas las posiciones se mantienen
if set(original_tiles.keys()) == set(optimized_tiles.keys()):
    print("✅ Todas las posiciones se mantienen")
else:
    print("❌ Se perdieron o agregaron posiciones")

print()
print("CAMBIOS DETALLADOS:")
print("-" * 40)

changes_count = 0
potential_visual_changes = 0

for pos in sorted(original_tiles.keys()):
    orig_tile = original_tiles[pos]
    opt_tile = optimized_tiles[pos]
    
    if orig_tile != opt_tile:
        changes_count += 1
        x, y = pos
        
        # Obtener regiones para comparar si son visualmente diferentes
        orig_region = tile_regions.get(orig_tile, "UNKNOWN")
        opt_region = tile_regions.get(opt_tile, "UNKNOWN")
        
        if orig_region != opt_region:
            potential_visual_changes += 1
            status = "⚠️ VISUAL"
        else:
            status = "✅ OK"
            
        print(f"Pos({x:2d},{y:2d}): Tile {orig_tile:2d} → {opt_tile:2d} {status}")
        
        if orig_region != "UNKNOWN" and opt_region != "UNKNOWN":
            print(f"           Región {orig_region} → {opt_region}")

print()
print("RESUMEN:")
print("-" * 30)
print(f"Total de cambios: {changes_count}")
print(f"Cambios potencialmente visuales: {potential_visual_changes}")

if potential_visual_changes == 0:
    print("✅ La optimización no debería cambiar la apariencia visual")
else:
    print("⚠️ Algunos cambios podrían afectar la apariencia visual")

# Mostrar tiles únicos usados
print()
print("TILES ÚNICOS ANTES Y DESPUÉS:")
print("-" * 40)
orig_unique = set(original_tiles.values())
opt_unique = set(optimized_tiles.values())

print(f"Tiles únicos originales: {len(orig_unique)} - {sorted(orig_unique)}")
print(f"Tiles únicos optimizados: {len(opt_unique)} - {sorted(opt_unique)}")
print(f"Reducción: {len(orig_unique) - len(opt_unique)} tiles ({((len(orig_unique) - len(opt_unique))/len(orig_unique)*100):.1f}%)")

removed_tiles = orig_unique - opt_unique
added_tiles = opt_unique - orig_unique

if removed_tiles:
    print(f"Tiles eliminados: {sorted(removed_tiles)}")
if added_tiles:
    print(f"Tiles nuevos: {sorted(added_tiles)}")