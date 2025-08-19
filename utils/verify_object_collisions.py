#!/usr/bin/env python3
"""
Verifica que las colisiones de objetos están correctamente implementadas
"""

def verify_object_collisions():
    print("=== VERIFICACIÓN DE COLISIONES DE OBJETOS ===\n")
    
    # Leer el archivo Nivel1.tscn para verificar colisiones
    with open('../scenes/Nivel1.tscn', 'r') as f:
        content = f.read()
    
    # Verificar que se agregaron los SubResource necesarios
    print("✅ VERIFICANDO SUBRESOURCES:")
    for i in range(5, 15):  # SubResource 5-14 para objetos
        if f"[sub_resource type=\"RectangleShape2D\" id={i}]" in content:
            print(f"  ✓ SubResource {i} encontrado")
        else:
            print(f"  ✗ SubResource {i} FALTANTE")
    
    # Verificar colisiones de la cama
    print("\n🛏️ VERIFICANDO COLISIONES DE LA CAMA:")
    bed_collisions = [
        ("Bed1", "Vector2( -64, -31 )"),
        ("Bed2", "Vector2( -48, -31 )"),
        ("Bed3", "Vector2( -32, -31 )"),
        ("Bed4", "Vector2( -64, -15 )"),
        ("Bed5", "Vector2( -48, -15 )"),
        ("Bed6", "Vector2( -32, -15 )")
    ]
    
    for bed_name, expected_pos in bed_collisions:
        if f'[node name="{bed_name}" type="CollisionShape2D"' in content:
            if expected_pos in content:
                print(f"  ✓ {bed_name} en posición {expected_pos}")
            else:
                print(f"  ✗ {bed_name} posición incorrecta")
        else:
            print(f"  ✗ {bed_name} FALTANTE")
    
    # Verificar colisiones del TV
    print("\n📺 VERIFICANDO COLISIONES DEL TV:")
    tv_collisions = [
        ("TV1", "Vector2( 32, -31 )"),
        ("TV2", "Vector2( 48, -31 )"),
        ("TV3", "Vector2( 32, -15 )"),
        ("TV4", "Vector2( 48, -15 )")
    ]
    
    for tv_name, expected_pos in tv_collisions:
        if f'[node name="{tv_name}" type="CollisionShape2D"' in content:
            if expected_pos in content:
                print(f"  ✓ {tv_name} en posición {expected_pos}")
            else:
                print(f"  ✗ {tv_name} posición incorrecta")
        else:
            print(f"  ✗ {tv_name} FALTANTE")
    
    # Verificar el load_steps
    print("\n⚙️ VERIFICANDO LOAD_STEPS:")
    if "[gd_scene load_steps=16 format=2]" in content:
        print("  ✓ load_steps actualizado a 16")
    else:
        print("  ✗ load_steps no actualizado correctamente")
    
    # Contar total de colisiones
    collision_count = content.count('type="CollisionShape2D"')
    print(f"\n📊 TOTAL DE COLISIONES: {collision_count}")
    print("  - 4 paredes de habitación")
    print("  - 6 tiles de cama")
    print("  - 4 tiles de TV/mueble")
    print("  = 14 colisiones esperadas")
    
    if collision_count == 14:
        print("  ✅ CORRECTO: Todas las colisiones implementadas")
    else:
        print(f"  ⚠️  ATENCIÓN: Se esperaban 14, encontradas {collision_count}")
    
    print("\n=== COORDINADAS FINALES IMPLEMENTADAS ===\n")
    
    print("🛏️ CAMA (6 tiles):")
    for bed_name, pos in bed_collisions:
        print(f"  {bed_name}: {pos}")
    
    print("\n📺 TV/MUEBLE (4 tiles):")
    for tv_name, pos in tv_collisions:
        print(f"  {tv_name}: {pos}")
    
    print("\n🎮 PARA PROBAR:")
    print("1. Abre Godot 3.5")
    print("2. Ejecuta main.tscn")
    print("3. Intenta caminar hacia la cama y el TV")
    print("4. El player debería detenerse al tocar estos objetos")
    
    return collision_count == 14

if __name__ == "__main__":
    result = verify_object_collisions()
    print(f"\n{'✅ VERIFICACIÓN EXITOSA' if result else '❌ VERIFICACIÓN FALLIDA'}")