#!/usr/bin/env python3
"""
Script para decodificar tile_data de Godot y mostrar la matriz de Tile IDs
"""

# Datos del TileMap extraídos del archivo scenes/Nivel1.tscn
tile_data = [
    -65540, 0, 0, -65539, 1, 0, -65538, 2, 0, -65537, 4, 0, -131072, 5, 0, -131071, 6, 0, -131070, 5, 0, -131069, 6, 0, 
    -4, 8, 0, -3, 9, 0, -2, 10, 0, -1, 13, 0, -65536, 13, 0, -65535, 13, 0, -65534, 14, 0, -65533, 15, 0, 
    65532, 20, 0, 65533, 17, 0, 65534, 18, 0, 65535, 20, 0, 0, 19, 0, 1, 20, 0, 2, 20, 0, 3, 19, 0, 
    131068, 19, 0, 131069, 21, 0, 131070, 34, 0, 131071, 35, 0, 65536, 58, 0, 65537, 19, 0, 65538, 21, 0, 65539, 19, 0, 
    196604, 48, 0, 196605, 48, 0, 196606, 42, 0, 196607, 43, 0, 131072, 58, 0, 131073, 58, 0, 131074, 53, 0, 131075, 54, 0, 
    262140, 56, 0, 262141, 56, 0, 262142, 44, 0, 262143, 51, 0, 196608, 58, 0, 196609, 58, 0, 196610, 58, 0, 196611, 62, 0
]

def signed_to_coords(signed_pos):
    """Convierte posición signed int a coordenadas x,y según formato de Godot"""
    # Godot usa formato: y en bits altos, x en bits bajos
    # Convertir de signed a unsigned para manipulación de bits
    if signed_pos < 0:
        unsigned = signed_pos + 2**32
    else:
        unsigned = signed_pos
    
    # Extraer x (16 bits bajos) e y (16 bits altos)
    x = unsigned & 0xFFFF
    y = (unsigned >> 16) & 0xFFFF
    
    # Convertir a signed 16-bit si es necesario
    if x >= 32768:
        x = x - 65536
    if y >= 32768:
        y = y - 65536
    
    return x, y

# Procesar tile_data (cada 3 elementos: posición, tile_id, flags)
tiles = {}
min_x = min_y = float('inf')
max_x = max_y = float('-inf')

for i in range(0, len(tile_data), 3):
    signed_pos = tile_data[i]
    tile_id = tile_data[i + 1]
    flags = tile_data[i + 2]  # No usado para la matriz
    
    x, y = signed_to_coords(signed_pos)
    tiles[(x, y)] = tile_id
    
    min_x = min(min_x, x)
    max_x = max(max_x, x)
    min_y = min(min_y, y)
    max_y = max(max_y, y)

print(f"Rango del mapa: x({min_x} a {max_x}), y({min_y} a {max_y})")
print(f"Dimensiones: {max_x - min_x + 1}x{max_y - min_y + 1}")
print()

# Crear matriz
print("MATRIZ DE TILE IDs:")
print("=" * 50)

# Encabezado con coordenadas X
print("   Y\\X", end="")
for x in range(min_x, max_x + 1):
    print(f"{x:4d}", end="")
print()

# Filas de la matriz
for y in range(min_y, max_y + 1):
    print(f"{y:4d}: ", end="")
    for x in range(min_x, max_x + 1):
        if (x, y) in tiles:
            tile_id = tiles[(x, y)]
            print(f"{tile_id:4d}", end="")
        else:
            print("  --", end="")  # Celda vacía
    print()

print()
print("LEYENDA:")
print("-- = Celda vacía (Tile ID -1)")
print("Números = Tile ID en esa posición")