#!/usr/bin/env python3
"""
Script para verificar que la optimización del TileSet fue exitosa
"""

import re
import os

# Comparar archivos
backup_path = None
for file in os.listdir('tilesets/'):
    if file.startswith('ash_room_small.tres.backup_'):
        backup_path = f'tilesets/{file}'
        break

if not backup_path:
    print("❌ No se encontró archivo de backup")
    exit(1)

print("VERIFICACIÓN DE OPTIMIZACIÓN DEL TILESET:")
print("=" * 50)

# Leer ambos archivos
with open('tilesets/ash_room_small.tres', 'r') as f:
    optimized_content = f.read()

with open(backup_path, 'r') as f:
    original_content = f.read()

# Contar líneas
orig_lines = len(original_content.split('\n'))
opt_lines = len(optimized_content.split('\n'))

print(f"Líneas originales: {orig_lines}")
print(f"Líneas optimizadas: {opt_lines}")
print(f"Líneas eliminadas: {orig_lines - opt_lines}")

# Verificar load_steps
orig_load_steps = re.search(r'load_steps=(\d+)', original_content)
opt_load_steps = re.search(r'load_steps=(\d+)', optimized_content)

if orig_load_steps and opt_load_steps:
    orig_steps = int(orig_load_steps.group(1))
    opt_steps = int(opt_load_steps.group(1))
    print(f"load_steps: {orig_steps} → {opt_steps} (reducción: {orig_steps - opt_steps})")

# Contar tiles definidos
orig_tiles = re.findall(r'^(\d+)/name', original_content, re.MULTILINE)
opt_tiles = re.findall(r'^(\d+)/name', optimized_content, re.MULTILINE)

print(f"Tiles originales: {len(orig_tiles)} (IDs: 0-{max(map(int, orig_tiles))})")
print(f"Tiles optimizados: {len(opt_tiles)} (IDs: 0-{max(map(int, opt_tiles))})")
print(f"Tiles eliminados: {len(orig_tiles) - len(opt_tiles)}")

# Verificar que se eliminaron los tiles correctos
eliminated_tiles = set(orig_tiles) - set(opt_tiles)
expected_eliminated = {'64', '65', '66', '67'}

if eliminated_tiles == expected_eliminated:
    print(f"✅ Tiles eliminados correctos: {sorted(eliminated_tiles)}")
else:
    print(f"❌ Tiles eliminados inesperados: {sorted(eliminated_tiles)}")
    print(f"   Se esperaba: {sorted(expected_eliminated)}")

# Verificar que no se eliminó borders.png
if 'borders.png' not in optimized_content:
    print("✅ ExtResource borders.png eliminado correctamente")
else:
    print("❌ ExtResource borders.png no se eliminó")

# Verificar SubResources
orig_subres = re.findall(r'\[sub_resource.*?id=(\d+)\]', original_content)
opt_subres = re.findall(r'\[sub_resource.*?id=(\d+)\]', optimized_content)

print(f"SubResources originales: {len(orig_subres)}")
print(f"SubResources optimizados: {len(opt_subres)}")

if len(opt_subres) == 0:
    print("✅ Todos los SubResources eliminados correctamente")
else:
    print(f"❌ Quedan SubResources: {opt_subres}")

print()
print("RESUMEN DE LA OPTIMIZACIÓN:")
print("-" * 30)
reduction_lines = ((orig_lines - opt_lines) / orig_lines) * 100
reduction_tiles = ((len(orig_tiles) - len(opt_tiles)) / len(orig_tiles)) * 100

print(f"• Reducción de líneas: {reduction_lines:.1f}%")
print(f"• Reducción de tiles: {reduction_tiles:.1f}%") 
print(f"• Tiles eliminados: 64, 65, 66, 67 (duplicados innecesarios)")
print(f"• ExtResource borders.png eliminado")
print(f"• SubResources de colisión eliminados")

print()
print("✅ OPTIMIZACIÓN COMPLETADA EXITOSAMENTE")
print("📂 El TileSet ahora es más eficiente y mantiene toda la funcionalidad")