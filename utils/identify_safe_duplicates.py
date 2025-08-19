#!/usr/bin/env python3
"""
Script para identificar tiles duplicados seguros para eliminar del TileSet
"""

# Tiles usados en el mapa actual (de nuestro análisis anterior)
used_tiles = {0, 1, 2, 4, 5, 6, 8, 9, 10, 13, 14, 15, 17, 18, 19, 20, 21, 34, 35, 42, 43, 44, 48, 51, 53, 54, 56, 58, 62}

# Duplicados identificados (misma región)
duplicates = {
    # Formato: tile_original: [tile_duplicado1, tile_duplicado2, ...]
    0: [64],  # Región (0,0,16,16)
    1: [65],  # Región (16,0,16,16)  
    2: [66],  # Región (32,0,16,16)
    3: [67],  # Región (48,0,16,16)
}

print("ANÁLISIS DE TILES DUPLICADOS SEGUROS PARA ELIMINAR:")
print("=" * 60)

safe_to_remove = []
potentially_unsafe = []

for original, duplicates_list in duplicates.items():
    print(f"\nTile ID {original}:")
    print(f"  Región: mismo sprite que tiles {duplicates_list}")
    print(f"  Original usado en mapa: {'✅ SÍ' if original in used_tiles else '❌ NO'}")
    
    for dup in duplicates_list:
        used_in_map = dup in used_tiles
        print(f"  Duplicado {dup} usado en mapa: {'✅ SÍ' if used_in_map else '❌ NO'}")
        
        if not used_in_map:
            safe_to_remove.append(dup)
            print(f"    → ✅ SEGURO ELIMINAR (no se usa en mapa)")
        else:
            potentially_unsafe.append(dup)
            print(f"    → ⚠️ PELIGROSO ELIMINAR (se usa en mapa)")

print("\n" + "=" * 60)
print("RESUMEN:")
print(f"Tiles seguros para eliminar: {sorted(safe_to_remove)}")
print(f"Tiles peligrosos de eliminar: {sorted(potentially_unsafe)}")

if safe_to_remove:
    print(f"\n✅ Podemos eliminar {len(safe_to_remove)} tiles sin afectar el mapa")
else:
    print(f"\n❌ No hay tiles seguros para eliminar")

print("\nDETALLE DE LOS TILES A ELIMINAR:")
print("-" * 40)
for tile_id in sorted(safe_to_remove):
    print(f"Tile ID {tile_id}: Duplicado no usado - ELIMINAR")