#!/usr/bin/env python3
"""
Debug del mapa actual con datos optimizados
"""

# Datos actuales del TileMap optimizado
tile_data = [
    -65540, 0, 0, -65539, 1, 0, -65538, 2, 0, -65537, 3, 0, -131072, 4, 0, -131071, 3, 0, -131070, 4, 0, -131069, 3, 0, 
    -4, 5, 0, -3, 6, 0, -2, 7, 0, -1, 8, 0, -65536, 8, 0, -65535, 8, 0, -65534, 9, 0, -65533, 10, 0, 
    65532, 13, 0, 65533, 11, 0, 65534, 12, 0, 65535, 13, 0, 0, 13, 0, 1, 13, 0, 2, 13, 0, 3, 13, 0, 
    131068, 13, 0, 131069, 13, 0, 131070, 14, 0, 131071, 15, 0, 65536, 13, 0, 65537, 13, 0, 65538, 13, 0, 65539, 13, 0, 
    196604, 18, 0, 196605, 18, 0, 196606, 16, 0, 196607, 17, 0, 131072, 13, 0, 131073, 13, 0, 131074, 20, 0, 131075, 21, 0, 
    262140, 22, 0, 262141, 22, 0, 262142, 13, 0, 262143, 19, 0, 196608, 13, 0, 196609, 13, 0, 196610, 13, 0, 196611, 23, 0
]

def signed_to_coords(signed_pos):
    """Convierte posición signed int a coordenadas x,y según formato de Godot"""
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

# Procesar tile_data
tiles = {}
min_x = min_y = float('inf')
max_x = max_y = float('-inf')

for i in range(0, len(tile_data), 3):
    signed_pos = tile_data[i]
    tile_id = tile_data[i + 1]
    flags = tile_data[i + 2]
    
    x, y = signed_to_coords(signed_pos)
    tiles[(x, y)] = tile_id
    
    min_x = min(min_x, x)
    max_x = max(max_x, x)
    min_y = min(min_y, y)
    max_y = max(max_y, y)

print(f"MAPA ACTUAL OPTIMIZADO:")
print(f"Rango: x({min_x} a {max_x}), y({min_y} a {max_y})")
print(f"Dimensiones: {max_x - min_x + 1}x{max_y - min_y + 1}")
print()

print("MATRIZ OPTIMIZADA:")
print("=" * 60)
print("   Y\\X", end="")
for x in range(min_x, max_x + 1):
    print(f"{x:4d}", end="")
print()

for y in range(min_y, max_y + 1):
    print(f"{y:4d}: ", end="")
    for x in range(min_x, max_x + 1):
        if (x, y) in tiles:
            tile_id = tiles[(x, y)]
            print(f"{tile_id:4d}", end="")
        else:
            print("  --", end="")
    print()

print()
print("🔍 ANÁLISIS:")
print(f"- Mapa va desde x={min_x} hasta x={max_x}")
print(f"- Si el debug se detiene en x=3, entonces X=4 debería estar FUERA")
print(f"- Pero si visualmente ves tiles en X=4+, hay un problema de alineación")