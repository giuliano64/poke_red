#!/usr/bin/env python3
"""
Identifica objetos específicos en la habitación de Ash para implementar colisiones
"""

def identify_room_objects():
    # Matriz actual del TileMap
    tilemap_matrix = [
        [ 0,  1,  2,  4,  5,  6,  5,  6], # Y=-2
        [ 8,  9, 10, 13, 13, 13, 14, 15], # Y=-1  
        [20, 17, 18, 20, 19, 20, 20, 19], # Y=0
        [19, 21, 34, 35, 58, 19, 21, 19], # Y=1
        [48, 48, 42, 43, 58, 58, 53, 54], # Y=2
        [56, 56, 44, 51, 58, 58, 58, 62]  # Y=3
    ]
    
    # Coordenadas: X(-4 a 3), Y(-2 a 3)
    x_coords = list(range(-4, 4))
    y_coords = list(range(-2, 4))
    
    print("=== ANÁLISIS DE OBJETOS EN LA HABITACIÓN DE ASH ===\n")
    
    # Basándome en la imagen del sprite, identifiquemos objetos específicos:
    
    print("🛏️ CAMA (esquina superior izquierda):")
    cama_positions = []
    for y_idx, y in enumerate(y_coords):
        for x_idx, x in enumerate(x_coords):
            if y_idx <= 1 and x_idx <= 2:  # Esquina superior izquierda
                tile_id = tilemap_matrix[y_idx][x_idx]
                world_x = x * 16
                world_y = y * 16 + 1  # +1 por posición del TileMap
                cama_positions.append((x, y, world_x, world_y, tile_id))
                print(f"  Grid({x}, {y}) -> World({world_x}, {world_y}) -> Tile ID: {tile_id}")
    
    print("\n📺 TV/MUEBLE (esquina superior derecha):")
    tv_positions = []
    for y_idx, y in enumerate(y_coords):
        for x_idx, x in enumerate(x_coords):
            if y_idx <= 1 and x_idx >= 6:  # Esquina superior derecha
                tile_id = tilemap_matrix[y_idx][x_idx]
                world_x = x * 16
                world_y = y * 16 + 1
                tv_positions.append((x, y, world_x, world_y, tile_id))
                print(f"  Grid({x}, {y}) -> World({world_x}, {world_y}) -> Tile ID: {tile_id}")
    
    print("\n🪑 ESCRITORIO/SILLA (centro-izquierda):")
    escritorio_positions = []
    for y_idx, y in enumerate(y_coords):
        for x_idx, x in enumerate(x_coords):
            if 2 <= y_idx <= 3 and 1 <= x_idx <= 3:  # Centro-izquierda
                tile_id = tilemap_matrix[y_idx][x_idx]
                world_x = x * 16
                world_y = y * 16 + 1
                if tile_id in [34, 35, 42, 43, 44, 51]:  # Tiles específicos de muebles
                    escritorio_positions.append((x, y, world_x, world_y, tile_id))
                    print(f"  Grid({x}, {y}) -> World({world_x}, {world_y}) -> Tile ID: {tile_id}")
    
    print("\n🌸 ALFOMBRA/DECORACIÓN (centro-derecha):")
    alfombra_positions = []
    for y_idx, y in enumerate(y_coords):
        for x_idx, x in enumerate(x_coords):
            if 2 <= y_idx <= 3 and 4 <= x_idx <= 7:  # Centro-derecha
                tile_id = tilemap_matrix[y_idx][x_idx]
                world_x = x * 16
                world_y = y * 16 + 1
                if tile_id in [58, 53, 54, 62]:  # Tiles específicos de alfombra
                    alfombra_positions.append((x, y, world_x, world_y, tile_id))
                    print(f"  Grid({x}, {y}) -> World({world_x}, {world_y}) -> Tile ID: {tile_id}")
    
    print("\n=== RECOMENDACIONES PARA COLISIONES ===\n")
    
    print("🛏️ CAMA - Objetos sólidos (no atravesables):")
    for pos in cama_positions:
        if pos[4] in [0, 1, 2, 8, 9, 10]:  # Tiles sólidos de la cama
            print(f"  Collision en World({pos[2]}, {pos[3]}) - Tile {pos[4]}")
    
    print("\n📺 TV/MUEBLE - Objetos sólidos:")
    for pos in tv_positions:
        if pos[4] in [5, 6, 14, 15]:  # Tiles sólidos del TV
            print(f"  Collision en World({pos[2]}, {pos[3]}) - Tile {pos[4]}")
    
    print("\n🪑 ESCRITORIO - Objetos sólidos:")
    for pos in escritorio_positions:
        print(f"  Collision en World({pos[2]}, {pos[3]}) - Tile {pos[4]}")
    
    print("\n💡 ÁREA LIBRE PARA CAMINAR:")
    walkable_area = []
    for y_idx, y in enumerate(y_coords):
        for x_idx, x in enumerate(x_coords):
            tile_id = tilemap_matrix[y_idx][x_idx]
            world_x = x * 16
            world_y = y * 16 + 1
            
            # Tiles de suelo/alfombra que son caminables
            if tile_id in [13, 19, 20, 21, 58]:
                walkable_area.append((x, y, world_x, world_y))
    
    print(f"  {len(walkable_area)} tiles caminables identificados")
    
    print("\n=== COORDENADAS ESPECÍFICAS PARA IMPLEMENTAR ===\n")
    
    # Objetos que definitivamente deben tener colisión
    collision_objects = [
        # Cama (esquina superior izquierda)
        {"name": "Bed", "positions": [(-64, -31), (-48, -31), (-32, -31), (-64, -15), (-48, -15), (-32, -15)]},
        
        # TV/Mueble (esquina superior derecha)  
        {"name": "TV", "positions": [(32, -31), (48, -31), (32, -15), (48, -15)]},
        
        # Escritorio y silla
        {"name": "Desk", "positions": [(-32, 17), (-16, 17)]},
        {"name": "Chair", "positions": [(-32, 33), (-16, 33)]}
    ]
    
    for obj in collision_objects:
        print(f"{obj['name']}:")
        for pos in obj['positions']:
            print(f"  Position({pos[0]}, {pos[1]})")
    
    return collision_objects

if __name__ == "__main__":
    identify_room_objects()