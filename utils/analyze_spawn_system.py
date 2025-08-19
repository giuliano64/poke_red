#!/usr/bin/env python3
"""
Script para analizar el sistema de spawn y su relación con el Player
"""

import re

print("ANÁLISIS DEL SISTEMA DE SPAWN:")
print("=" * 40)

# Leer archivos relevantes
with open('player.gd', 'r') as f:
    player_content = f.read()

with open('game.gd', 'r') as f:
    game_content = f.read()

with open('scenes/Nivel1.tscn', 'r') as f:
    nivel1_content = f.read()

print("1. DEFINICIÓN DEL SPAWN:")
print("-" * 25)

# Buscar definición del spawn
spawn_match = re.search(r'\[node name="spawn_player".*?\].*?(?=\[node|\Z)', nivel1_content, re.DOTALL)
if spawn_match:
    spawn_def = spawn_match.group(0)
    print("✅ Spawn encontrado en scenes/Nivel1.tscn:")
    print(f"   - Tipo: Position2D")
    print(f"   - Nombre: spawn_player")
    print(f"   - Grupo: spawn")
    
    # Buscar posición específica
    pos_match = re.search(r'position = Vector2\((.*?)\)', spawn_def)
    if pos_match:
        position = pos_match.group(1)
        print(f"   - Posición: Vector2({position})")
    else:
        print("   - Posición: Vector2(0, 0) [por defecto]")
        
    # Buscar otras propiedades
    if "show_behind_parent = true" in spawn_def:
        print("   - show_behind_parent: true")
else:
    print("❌ No se encontró definición del spawn")

print("\n2. USO EN EL JUEGO (game.gd):")
print("-" * 30)

# Analizar game.gd
spawn_usage_game = re.search(r'new_player\.global_position = get_tree\(\)\.get_nodes_in_group\("spawn"\)\[0\]\.global_position', game_content)
if spawn_usage_game:
    print("✅ Inicialización del player:")
    print("   1. Se instancia el nivel (nivel1)")
    print("   2. Se instancia el player")
    print("   3. Se posiciona el player en el spawn:")
    print("      new_player.global_position = get_tree().get_nodes_in_group('spawn')[0].global_position")
else:
    print("❌ No se encontró uso del spawn en game.gd")

print("\n3. USO EN EL MOVIMIENTO (player.gd):")
print("-" * 35)

# Analizar player.gd
snap_logic = re.search(r'var global_pos_x.*?global_position = Vector2.*?\)', player_content, re.DOTALL)
if snap_logic:
    print("✅ Sistema de 'snap to grid' al finalizar animación:")
    print("   1. Obtiene posición del spawn:")
    print("      var global_pos_x = get_tree().get_nodes_in_group('spawn')[0].global_position.x")
    print("      var global_pos_y = get_tree().get_nodes_in_group('spawn')[0].global_position.y")
    print("   2. Calcula posición alineada al grid:")
    print("      global_position = Vector2(")
    print("         (round(round(global_position.x - global_pos_x)/vel_desp)*vel_desp)+global_pos_x,")
    print("         (round(round(global_position.y - global_pos_y)/vel_desp)*vel_desp)+global_pos_y")
    print("      )")
else:
    print("❌ No se encontró lógica de snap en player.gd")

print("\n4. PROPÓSITO DEL SISTEMA:")
print("-" * 25)
print("🎯 El spawn sirve como:")
print("   • Punto de aparición inicial del jugador")
print("   • Punto de referencia para el sistema de grid")
print("   • Origen de coordenadas para el movimiento tile-by-tile")

print("\n5. CÓMO FUNCIONA:")
print("-" * 20)
print("📍 Inicialización:")
print("   - El game.gd instancia el nivel y el player")
print("   - Posiciona el player exactamente en el spawn")

print("\n🎮 Durante el juego:")
print("   - El player se mueve libremente durante las animaciones")
print("   - Al terminar cada animación de movimiento:")
print("     1. Calcula la diferencia entre su posición actual y el spawn")
print("     2. Redondea esta diferencia a múltiplos de 16 píxeles (vel_desp)")
print("     3. Reposiciona al player en la grid más cercana")

print("\n⚡ Resultado:")
print("   - Movimiento suave durante animaciones")
print("   - Posicionamiento exacto en tiles al finalizar")
print("   - Consistencia en el sistema de grid")

print("\n6. FÓRMULA DE ALINEACIÓN:")
print("-" * 25)
print("nueva_pos = (round(round(pos_actual - pos_spawn) / 16) * 16) + pos_spawn")
print("   - pos_actual: Posición actual del player")
print("   - pos_spawn: Posición del spawn (punto de referencia)")
print("   - 16: Tamaño del tile (vel_desp)")
print("   - El doble round() asegura precisión en el cálculo")