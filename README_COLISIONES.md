# Guía de Colisiones y Bordes en Pokemon Red (Godot 3.5)

## 📋 Resumen
Esta guía documenta cómo agregar bordes con colisión a un TileMap en Godot, incluyendo la creación de tiles personalizados y configuración de colisiones.

## 🔧 Proceso Completo

### 1. Backup de Archivos
**SIEMPRE hacer backup antes de modificar:**
```bash
mkdir backup_$(date +%Y%m%d_%H%M%S)
cp tilesets/ash_room_small.tres backup_*/
cp tilesets/Ash_room_sharp.png backup_*/
```

### 2. Crear Imagen de Bordes

#### Crear imagen con Python (64x16px = 4 tiles):
```python
from PIL import Image, ImageDraw

# Crear imagen de bordes (64x16px = 4 tiles de 16x16)
border_img = Image.new('RGBA', (64, 16), (0, 0, 0, 0))
draw = ImageDraw.Draw(border_img)

# Colores Pokemon Red
wall_color = (64, 64, 64, 255)      # Gris oscuro
wall_top = (96, 96, 96, 255)        # Gris más claro

# Tile 0: Pared sólida
draw.rectangle([0, 0, 15, 15], fill=wall_color, outline=wall_top)

# Tile 1: Pared con borde superior
draw.rectangle([16, 0, 31, 15], fill=wall_color)
draw.rectangle([16, 0, 31, 2], fill=wall_top)

# Tile 2: Pared lateral izquierda
draw.rectangle([32, 0, 47, 15], fill=wall_color)
draw.rectangle([32, 0, 34, 15], fill=wall_top)

# Tile 3: Pared esquina
draw.rectangle([48, 0, 63, 15], fill=wall_color)
draw.rectangle([48, 0, 63, 2], fill=wall_top)
draw.rectangle([48, 0, 50, 15], fill=wall_top)

border_img.save('tilesets/borders.png')
```

### 3. Modificar TileSet (.tres)

#### Agregar nueva textura:
```gdscript
# Cambiar load_steps de 2 a 3
[gd_resource type="TileSet" load_steps=3 format=2]

# Agregar resource de bordes
[ext_resource path="res://tilesets/Ash_room_sharp.png" type="Texture" id=1]
[ext_resource path="res://tilesets/borders.png" type="Texture" id=2]
```

#### Agregar SubResources para colisiones:
```gdscript
[sub_resource type="ConvexPolygonShape2D" id=1]
points = PoolVector2Array( 0, 0, 16, 0, 16, 16, 0, 16 )

[sub_resource type="ConvexPolygonShape2D" id=2]
points = PoolVector2Array( 0, 0, 16, 0, 16, 16, 0, 16 )

[sub_resource type="ConvexPolygonShape2D" id=3]
points = PoolVector2Array( 0, 0, 16, 0, 16, 16, 0, 16 )
```

#### Agregar tiles de borde (IDs 64-67):
```gdscript
64/name = "Wall_Solid"
64/texture = ExtResource( 2 )
64/region = Rect2( 0, 0, 16, 16 )
64/tile_mode = 0
64/shapes = [ {
"autotile_coord": Vector2( 0, 0 ),
"one_way": false,
"one_way_margin": 1.0,
"shape": SubResource( 1 ),
"shape_transform": Transform2D( 1, 0, 0, 1, 0, 0 )
} ]

# Repetir para tiles 65, 66, 67 con sus respectivas regiones y shapes
```

### 4. Configurar Player para Colisiones

#### En player.tscn, agregar CollisionShape2D:
```gdscript
[sub_resource type="RectangleShape2D" id=7]
extents = Vector2( 7, 7 )  # Tamaño apropiado

[node name="CollisionShape2D" type="CollisionShape2D" parent="."]
position = Vector2( -56, 16 )  # MISMA posición que el Sprite
shape = SubResource( 7 )
```

### 5. Usar Bordes en el Mapa

#### Desde Godot IDE:
1. Abrir escena con TileMap
2. Seleccionar nodo TileMap
3. Panel inferior → Paleta de tiles
4. Seleccionar tiles 64-67 (bordes)
5. Pintar en el mapa donde necesites

#### Programáticamente:
```gdscript
func add_borders_to_map():
    var tilemap = $TileMap
    var border_tile = 64  # Wall_Solid
    var map_width = 8
    var map_height = 8
    
    # Bordes alrededor del mapa
    for x in range(map_width):
        tilemap.set_cell(x, 0, border_tile)              # Arriba
        tilemap.set_cell(x, map_height-1, border_tile)   # Abajo
    
    for y in range(map_height):
        tilemap.set_cell(0, y, border_tile)              # Izquierda
        tilemap.set_cell(map_width-1, y, border_tile)    # Derecha
```

## 🎯 Tiles Creados

| ID | Nombre | Descripción | Región |
|----|---------|-------------|---------|
| 64 | Wall_Solid | Pared sólida gris | (0,0,16,16) |
| 65 | Wall_Top | Pared con borde superior | (16,0,16,16) |
| 66 | Wall_Left | Pared con borde izquierdo | (32,0,16,16) |
| 67 | Wall_Corner | Pared esquina | (48,0,16,16) |

## ✅ Verificación

### Para confirmar que funciona:
1. **Debug** → **Visible Collision Shapes** (debe mostrar rectángulos azules)
2. **Ejecutar juego** → Player no debe poder atravesar bordes
3. **TileMap** → Debe mostrar tiles 64-67 en la paleta

## ⚠️ Problemas Comunes

### Player atraviesa bordes:
- ❌ Falta CollisionShape2D en player
- ❌ CollisionShape2D en posición incorrecta
- ❌ Shape no definido en CollisionShape2D

### No se ven bordes en paleta:
- ❌ Archivo borders.png no existe
- ❌ Error en sintaxis del .tres
- ❌ load_steps incorrecto

### Colisiones no funcionan:
- ❌ Falta SubResource para shapes
- ❌ shapes = [ ] vacío en tile
- ❌ Player no es KinematicBody2D

## 🔄 Para Revertir
```bash
# Restaurar desde backup
cp backup_FECHA/* tilesets/
```

## 📝 Notas Técnicas

- **TileMap automáticamente** crea StaticBody2D para tiles con colisión
- **KinematicBody2D + CollisionShape2D** detecta colisiones con StaticBody2D
- **Posición del CollisionShape2D** debe coincidir con la del Sprite
- **Extents** del CollisionShape2D debe ser menor que el sprite (ej: 7x7 para sprite 16x16)