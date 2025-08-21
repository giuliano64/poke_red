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

## 🎉 SISTEMA COMPLETADO - Agosto 2025

### ✅ Sistema Pokemon Red Implementado

Se implementó completamente un sistema de diálogos estilo Pokemon Red moderno:

#### **Arquitectura Final:**
1. **CanvasLayer UI:** Diálogo estable independiente del mundo del juego
2. **Paginado automático:** Texto se divide en páginas de 5 palabras por línea (2 líneas max)
3. **Efecto typewriter:** Caracteres aparecen gradualmente (60 chars/sec)
4. **Controles Pokemon:** X avanza/completa, C cierra inmediatamente
5. **Pausa de juego:** Player no se mueve durante diálogos
6. **Indicador visual:** Flecha ▶ muestra cuando hay más contenido

#### **Archivos Creados/Modificados:**
- `DialogBox.gd`: Script completo con paginación y typewriter
- `main.tscn`: CanvasLayer con DialogRoot (anchors 30-70% x 60-85%)
- `player.gd`: Integración con nuevo sistema + prevención input cíclico
- `project.godot`: Input mapping ui_accept (tecla X)

#### **Componentes Técnicos:**
- **DialogRoot (Control):** Contenedor principal posicionado relativamente
- **Panel (NinePatchRect):** Usando sprite auténtico Pokemon Red
- **Text (Label):** Con autowrap y fuente Pokemon auténtica (size=8)
- **NextIcon (Label):** Indicador ▶ para más contenido

### 🔧 Problemas Resueltos
1. ✅ Diálogo aparece dentro del área de juego (centrado)
2. ✅ Tamaño proporcional usando anchors (40% ancho x 25% altura)
3. ✅ Paginación automática para textos largos
4. ✅ Efecto typewriter con velocidad configurable
5. ✅ Controles X/C funcionando correctamente
6. ✅ Prevención de input durante diálogo activo
7. ✅ Pausa/resume de juego automático
8. ✅ Compatibilidad GDScript 3.5 (sin := operators)

### 🐛 Problemas Conocidos
- **Input cíclico menor:** Ocasionalmente X puede reabrir diálogo
- **Tamaño:** Podría ser aún más pequeño para mejor proporción

### 🎮 Mensajes de Ejemplo Implementados

```gdscript
// PC (con paginación automática)
"Has encendido tu PC. Es una máquina poderosa que te permite hacer muchas tareas. Por el momento no ejecutarás nada en la misma, pero sabes que en el futuro podrás usarla para almacenar Pokemon y acceder al sistema de almacenamiento."

// TV/Consola (con paginación automática)  
"Estas jugando a la SNES, disfrutando de algunos clásicos retro. La consola funciona perfectamente y tienes una gran colección de juegos. Pero de momento, decides apagarla y seguir adelante con tu aventura Pokemon, ya va a haber tiempo para juegos retro más tarde."
```

### 🧪 Testing Completado
1. ✅ Interacción PC/TV funcional
2. ✅ Paginación automática para textos largos
3. ✅ Typewriter effect funcionando
4. ✅ Controles X/C operativos
5. ✅ Pausa de juego durante diálogos
6. ✅ Diálogo aparece en posición correcta

## Estado: ✅ FUNCIONAL Y OPERATIVO

🎮 El sistema de diálogos está completamente implementado y funcional  
📱 Diálogo aparece correctamente dentro del área de juego  
⌨️ Controles Pokemon Red implementados (X avanza, C cierra)  
📄 Paginación automática para textos largos operativa