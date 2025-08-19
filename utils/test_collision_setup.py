#!/usr/bin/env python3
"""
Script para verificar que las colisiones están bien configuradas
"""

from pathlib import Path
import re

def check_collision_setup():
    print("🔍 Verificando configuración de colisiones...")
    
    # Verificar Nivel1.tscn
    nivel_path = Path("scenes/Nivel1.tscn")
    with open(nivel_path, 'r') as f:
        nivel_content = f.read()
    
    # Verificar player.tscn
    player_path = Path("scenes/player.tscn")
    with open(player_path, 'r') as f:
        player_content = f.read()
    
    # Contar elementos clave
    static_bodies = nivel_content.count("StaticBody2D")
    collision_shapes = nivel_content.count("CollisionShape2D")
    rectangle_shapes = nivel_content.count("RectangleShape2D")
    
    player_kinematic = player_content.count("KinematicBody2D")
    player_collision = player_content.count("CollisionShape2D")
    
    print(f"\n📋 Nivel1.tscn:")
    print(f"   StaticBody2D: {static_bodies}")
    print(f"   CollisionShape2D: {collision_shapes}")
    print(f"   RectangleShape2D: {rectangle_shapes}")
    
    print(f"\n🤖 player.tscn:")
    print(f"   KinematicBody2D: {player_kinematic}")
    print(f"   CollisionShape2D: {player_collision}")
    
    # Extraer posiciones de colisión
    positions = re.findall(r'position = Vector2\( ([^)]+) \)', nivel_content)
    if len(positions) >= 3:
        print(f"\n📍 Posiciones de colisión encontradas:")
        walls = ["TopWall", "LeftWall", "RightWall"]
        for i, pos in enumerate(positions[-3:]):  # Las últimas 3 posiciones
            if i < len(walls):
                print(f"   {walls[i]}: {pos}")
    
    success = (static_bodies >= 1 and collision_shapes >= 3 and 
               player_kinematic >= 1 and player_collision >= 1)
    
    if success:
        print(f"\n✅ ¡Configuración correcta!")
        print(f"\n🎮 Para probar:")
        print(f"1. Abre Godot 3.5")
        print(f"2. Ve a Debug -> Visible Collision Shapes")
        print(f"3. Ejecuta main.tscn")
        print(f"4. Las flechas deberían chocar con paredes invisibles")
    else:
        print(f"\n❌ Hay problemas en la configuración")
    
    return success

if __name__ == "__main__":
    check_collision_setup()