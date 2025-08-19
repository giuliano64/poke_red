#!/usr/bin/env python3
"""
Script para analizar qué tiles del TileSet están siendo utilizados realmente
y crear una lista de tiles seguros para eliminar.
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

def analyze_used_tiles():
    """Analiza qué tiles están siendo utilizados en el TileMap"""
    
    # Extraer todos los Tile IDs utilizados
    used_tiles = set()
    for i in range(1, len(tile_data), 3):  # Cada 3er elemento es un tile_id
        tile_id = tile_data[i]
        used_tiles.add(tile_id)
    
    used_tiles = sorted(used_tiles)
    
    print("=== ANÁLISIS DE TILES UTILIZADOS ===")
    print(f"Tiles utilizados en el TileMap: {len(used_tiles)}")
    print(f"Lista de tiles utilizados: {used_tiles}")
    print()
    
    # Analizar el rango completo del TileSet (0-63 después de la optimización anterior)
    tileset_range = list(range(64))  # 0 a 63
    unused_tiles = [tile for tile in tileset_range if tile not in used_tiles]
    
    print("=== TILES NO UTILIZADOS ===")
    print(f"Tiles definidos en TileSet pero NO utilizados: {len(unused_tiles)}")
    print(f"Lista de tiles no utilizados: {unused_tiles}")
    print()
    
    # Calcular estadísticas
    efficiency_current = (len(used_tiles) / 64) * 100
    efficiency_optimized = 100  # Si solo dejamos los tiles utilizados
    reduction = len(unused_tiles)
    
    print("=== ESTADÍSTICAS ===")
    print(f"Eficiencia actual del TileSet: {efficiency_current:.1f}%")
    print(f"Eficiencia tras optimización avanzada: {efficiency_optimized:.1f}%")
    print(f"Tiles que se pueden eliminar: {reduction}")
    print(f"Reducción en tiles: {(reduction/64)*100:.1f}%")
    print()
    
    return used_tiles, unused_tiles

def verify_tile_continuity(used_tiles):
    """Verifica si los tiles utilizados tienen continuidad en los índices"""
    print("=== VERIFICACIÓN DE CONTINUIDAD ===")
    
    # Verificar si hay gaps en la secuencia
    gaps = []
    for i in range(len(used_tiles) - 1):
        current = used_tiles[i]
        next_tile = used_tiles[i + 1]
        if next_tile - current > 1:
            missing = list(range(current + 1, next_tile))
            gaps.extend(missing)
    
    if gaps:
        print(f"⚠️  HAY GAPS en la secuencia de tiles utilizados: {gaps}")
        print("Esto significa que necesitaremos remapear los Tile IDs en el TileMap")
        print("O mantener algunos tiles vacíos para preservar los índices")
    else:
        print("✅ Los tiles utilizados forman una secuencia continua")
    
    print()
    return gaps

if __name__ == "__main__":
    used_tiles, unused_tiles = analyze_used_tiles()
    gaps = verify_tile_continuity(used_tiles)
    
    print("=== RECOMENDACIÓN ===")
    if gaps:
        print("⚠️  CUIDADO: Eliminar tiles no utilizados requerirá remapear el TileMap")
        print("Opciones:")
        print("1. Crear un script de remapeo que actualice todos los Tile IDs")
        print("2. Mantener tiles vacíos para preservar índices existentes")
        print("3. Hacer optimización conservativa (solo eliminar tiles del final)")
    else:
        print("✅ SEGURO: Se pueden eliminar tiles sin remapear el TileMap")
    
    print(f"\nTiles seguros para eliminar: {unused_tiles}")