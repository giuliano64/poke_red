# Sistema de Diálogos - Pokemon Red Godot 3.5

## Estado Actual del Proyecto

### ✅ Funcionalidades Completadas

1. **Sistema de Interacción con Teclas X y C**
   - Teclas configuradas en `project.godot`
   - X = Botón A (interactuar/confirmar)
   - C = Botón B (cancelar/cerrar)

2. **Detección de Objetos Interactivos**
   - PC en posición (-45, -18) ajustada por offset del TileMap
   - TV/Consola en posiciones (-9, 26) y (-9, 39)
   - Sistema de priorización: PC > TV cuando ambos están en rango
   - Detección basada en distancia mínima del player

3. **Sistema de Diálogos Funcional**
   - Muestra/oculta diálogos correctamente
   - Pausa el juego durante el diálogo
   - Se cierra con X o C
   - Usa sprite auténtico de Pokemon Red (`GUI/text.png`)
   - Fuente Pokemon auténtica (`Fonts/Pokemon X and Y.ttf`)

### ❌ Problema Pendiente

**El diálogo aparece FUERA del área de juego** en lugar de dentro como en el Pokemon Red original.

## Arquitectura del Sistema

### Estructura de Archivos
```
PokemonRed/
├── main.tscn                 # Escena principal con GUI
├── game.gd                   # Script principal 
├── player.gd                 # Lógica del player + sistema de interacción
├── scenes/
│   ├── Dialogo.tscn         # Escena del diálogo
│   ├── player.tscn          # Player con animaciones
│   └── Nivel1.tscn          # Nivel con colisiones
├── GUI/
│   └── text.png             # Sprite del diálogo (copiado de referencia)
├── Fonts/
│   └── Pokemon X and Y.ttf  # Fuente auténtica (copiada de referencia)
└── dialogo.gd               # Script del diálogo
```

### Flujo de Interacción

1. **Player presiona X** → `player.gd::_physics_process()`
2. **Se calcula posición de interacción** → `get_interaction_position()`
3. **Se verifica distancia a objetos** → `check_interaction()`
4. **Se prioriza PC sobre TV** → lógica de `if pc_distance_min <= 50`
5. **Se muestra diálogo** → `show_dialog()` accede a `GUI/Dialogo`

## Implementación Paso a Paso

### Paso 1: Configurar Teclas de Input

En `project.godot`, agregar:
```gdscript
tecla_x={
"deadzone": 0.5,
"events": [ Object(InputEventKey,"scancode":88) ]
}
tecla_c={
"deadzone": 0.5, 
"events": [ Object(InputEventKey,"scancode":67) ]
}
```

### Paso 2: Estructura de GUI en main.tscn

```gdscript
[node name="main" type="Node2D"]
[node name="GUI" type="Node2D" parent="." groups=["gui"]]
[node name="Dialogo" parent="GUI" instance=ExtResource( 4 )]
```

### Paso 3: Crear Escena de Diálogo (Dialogo.tscn)

```gdscript
[node name="Dialogo" type="Node2D"]
z_index = 100

[node name="bkg_txt" type="Sprite" parent="."]
texture = "res://GUI/text.png"
region_enabled = true
region_rect = Rect2( 187.25, 169.984, 318.75, 76.4837 )

[node name="txt" type="Label" parent="."]
custom_fonts/font = [Pokemon Font]
```

### Paso 4: Script del Diálogo (dialogo.gd)

```gdscript
extends Node2D

func show_dialog(text: String):
    # Mostrar sprite y texto
    $bkg_txt.visible = true
    $txt.visible = true
    $txt.text = text
    
    # Pausar juego
    get_tree().paused = true
    pause_mode = Node.PAUSE_MODE_PROCESS

func hide_dialog():
    # Ocultar y despausar
    $bkg_txt.visible = false
    $txt.visible = false
    get_tree().paused = false
```

### Paso 5: Sistema de Interacción en player.gd

```gdscript
# En _physics_process()
if Input.is_action_just_pressed("tecla_x"):
    check_interaction()

func check_interaction():
    # Calcular posiciones y distancias
    var pc_distance = player_position.distance_to(Vector2(-45, -18))
    
    # Priorizar PC sobre TV
    if pc_distance <= 50:
        show_dialog("Mensaje del PC")

func show_dialog(text: String):
    # Acceder a GUI
    var gui = get_tree().get_nodes_in_group("gui")[0]
    var dialogo = gui.get_node("Dialogo") 
    dialogo.show_dialog(text)
```

## Configuración de la Solución de Referencia

### Valores Exactos de la Referencia
- **bkg_txt position**: `Vector2( 258.053, 424 )`
- **bkg_txt scale**: `Vector2( 1.61006, 1.68421 )`
- **txt margins**: `left=16, top=376, right=496, bottom=472`
- **Font size**: `24`

### Tamaños del Juego
- **Cell size**: 16x16 píxeles
- **Área de juego**: Aproximadamente 160x144 píxeles
- **El diálogo debería ser**: ~64-80 píxeles de ancho (4-5 tiles)

## Próximos Pasos para Resolver el Problema

### Problema Principal
El diálogo aparece en coordenadas absolutas de pantalla en lugar de coordenadas relativas al área de juego.

### Soluciones a Probar

1. **Usar Camera2D como referencia**
   - Posicionar diálogo relativo a la cámara del player
   - `position = camera.global_position + Vector2(0, offset)`

2. **Crear diálogo como hijo del TileMap**
   - Que herede las coordenadas del mundo del juego
   - Posicionar en coordenadas del mundo, no de pantalla

3. **Ajustar escala basado en viewport**
   - Calcular escala dinámicamente según tamaño de ventana
   - Usar proporciones exactas de la referencia

### Mensajes de Diálogo Actuales

```gdscript
// PC
"Has encendido tu PC.\nPor el momento no ejecutaras\nnada en la misma."

// TV/Consola  
"Estas jugando a la SNES,\npero de momento, decides\napagarla y seguir adelante,\nya va a haber tiempo para\njuegos retro..."
```

## Debug y Testing

### Comandos de Debug Actuales
- `print("PC - Distancia desde player: ", distance)`
- `print("¡PC detectado!")` 
- `print("=== MOSTRANDO DIALOGO ===")`

### Cómo Testear
1. Ejecutar el juego
2. Caminar hasta el PC (esquina superior izquierda)
3. Presionar X
4. El diálogo debería aparecer DENTRO del área de juego
5. Presionar X o C para cerrarlo

## Estado: Funcional pero Mal Posicionado

✅ El sistema funciona correctamente  
❌ El diálogo aparece fuera del área de juego  
🔄 Necesita ajustes de posicionamiento para que aparezca dentro del mundo del juego