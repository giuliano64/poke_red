#!/usr/bin/env python3
"""
Extractor de configuraciones del TileSet actual
Preserva todas las propiedades importantes para el nuevo TileSet optimizado
"""

import re

# Tiles utilizados que necesitamos preservar
USED_TILES = [0, 1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15, 17, 18, 19, 20, 21, 34, 35, 42, 43, 44, 48, 51, 53, 54, 56, 58, 62]

def extract_tile_properties(tileset_path):
    """Extrae todas las propiedades de los tiles utilizados"""
    
    with open(tileset_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    # Extraer header (load_steps, resources, etc.)
    header_lines = []
    resource_start = False
    
    for line in lines:
        if line.startswith('[resource]'):
            resource_start = True
            break
        header_lines.append(line)
    
    # Extraer propiedades de tiles utilizados
    tile_properties = {}
    current_tile_id = None
    
    for line in lines:
        # Detectar tile ID
        tile_match = re.match(r'^(\d+)/(.+)', line)
        if tile_match:
            tile_id = int(tile_match.group(1))
            property_line = tile_match.group(2)
            
            if tile_id in USED_TILES:
                if tile_id not in tile_properties:
                    tile_properties[tile_id] = []
                tile_properties[tile_id].append(property_line)
    
    return header_lines, tile_properties

def load_tile_mapping():
    """Carga el mapeo de tiles antiguos a nuevos"""
    mapping = {}
    try:
        with open("tile_mapping.txt", "r") as f:
            for line in f:
                if " -> " in line:
                    old_id, new_id = line.strip().split(" -> ")
                    mapping[int(old_id)] = int(new_id)
    except FileNotFoundError:
        print("❌ Error: No se encontró tile_mapping.txt. Ejecuta primero analyze_sprite_for_unique_tiles.py")
        return None
    
    return mapping

def create_optimized_tileset_config(header_lines, tile_properties, tile_mapping):
    """Crea la configuración del TileSet optimizado"""
    
    print("🔧 Creando configuración del TileSet optimizado...")
    
    # Mapeo inverso para obtener el tile original representativo de cada nuevo ID
    new_to_representative = {}
    for old_id, new_id in tile_mapping.items():
        if new_id not in new_to_representative:
            new_to_representative[new_id] = old_id  # Primer tile que encontremos con este nuevo ID
    
    # Generar nuevo TileSet
    new_lines = header_lines + ['[resource]']
    
    print(f"📊 Generando {len(new_to_representative)} tiles únicos...")
    
    for new_id in sorted(new_to_representative.keys()):
        representative_old_id = new_to_representative[new_id]
        
        if representative_old_id in tile_properties:
            print(f"   Nuevo tile {new_id:2d} ← tile original {representative_old_id}")
            
            # Generar propiedades para el nuevo tile
            for property_line in tile_properties[representative_old_id]:
                # Reemplazar el ID en la línea de propiedad
                new_line = f"{new_id}/{property_line}"
                new_lines.append(new_line)
        else:
            print(f"   ⚠️  Tile {representative_old_id} no tiene propiedades guardadas")
    
    return new_lines

def generate_tilemap_update_script(tile_mapping):
    """Genera script para actualizar el TileMap"""
    
    script_content = f"""#!/usr/bin/env python3
# Script para actualizar el TileMap con los nuevos IDs de tiles optimizados

import re

TILE_MAPPING = {tile_mapping}

def update_tilemap_data():
    tilemap_file = "scenes/Nivel1.tscn"
    
    with open(tilemap_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\\n')
    new_lines = []
    
    for line in lines:
        if line.startswith('tile_data = PoolIntArray('):
            print("🔄 Actualizando tile_data...")
            data_match = re.search(r'tile_data = PoolIntArray\\( (.+) \\)', line)
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
                            print(f"   Mapeando tile {{old_tile_id}} → {{new_tile_id}}")
                
                data_str_new = ', '.join(map(str, updated_data))
                new_line = f"tile_data = PoolIntArray( {{data_str_new}} )"
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    
    with open(tilemap_file, 'w', encoding='utf-8') as f:
        f.write('\\n'.join(new_lines))
    
    print("✅ TileMap actualizado exitosamente")
    return True

if __name__ == "__main__":
    print("=== ACTUALIZADOR DE TILEMAP ===")
    update_tilemap_data()
"""
    
    with open("update_tilemap.py", "w", encoding='utf-8') as f:
        f.write(script_content)
    
    print("📁 Script generado: update_tilemap.py")

def main():
    tileset_path = "tilesets/ash_room_small.tres"
    
    print("=== EXTRACTOR DE CONFIGURACIONES ===")
    print(f"Analizando: {tileset_path}")
    print()
    
    # 1. Cargar mapeo de tiles
    tile_mapping = load_tile_mapping()
    if not tile_mapping:
        return
    
    print(f"📊 Mapeo cargado: {len(tile_mapping)} tiles")
    
    # 2. Extraer configuraciones existentes
    header_lines, tile_properties = extract_tile_properties(tileset_path)
    print(f"🎯 Propiedades extraídas de {len(tile_properties)} tiles")
    
    # 3. Crear configuración optimizada
    new_tileset_lines = create_optimized_tileset_config(header_lines, tile_properties, tile_mapping)
    
    # 4. Guardar nuevo TileSet
    new_tileset_path = "tilesets/ash_room_small_optimized.tres"
    with open(new_tileset_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_tileset_lines))
    
    print(f"\n📁 TileSet optimizado creado: {new_tileset_path}")
    
    # 5. Generar script de actualización del TileMap
    generate_tilemap_update_script(tile_mapping)
    
    print("\n✅ Configuraciones extraídas y TileSet optimizado generado")
    print("   Próximo paso: Ejecutar update_tilemap.py")

if __name__ == "__main__":
    main()