# Guía Completa: Sistema de Diálogos Pokemon Red en Godot 3.5

## 📋 Índice
1. [Estructura General](#estructura-general)
2. [Configuración del Proyecto](#configuración-del-proyecto)
3. [Implementación paso a paso](#implementación-paso-a-paso)
4. [Scripts Completos](#scripts-completos)
5. [Testing y Debug](#testing-y-debug)

---

## 1. Estructura General

### Arquitectura del Sistema
```
main.tscn (Node2D)
├── game.gd (instancia nivel + player)
├── UI (CanvasLayer)
│   └── DialogRoot (Control)
│       ├── DialogBox.gd (script principal)
│       └── Panel (NinePatchRect)
│           ├── Text (Label)
│           └── NextIcon (Label)
└── [Nivel y Player se instancian dinámicamente]
```

### Flujo de Interacción
1. **Player presiona X** → `player.gd::_physics_process()`
2. **Calcula posición de interacción** → `get_interaction_position()`
3. **Verifica distancia a objetos** → `check_interaction()`
4. **Prioriza PC sobre TV** → lógica de distancias
5. **Muestra diálogo** → `show_dialog()` → `DialogRoot.show_dialog()`

---

## 2. Configuración del Proyecto

### Input Map (project.godot)
```ini
[input]

tecla_x={
"deadzone": 0.5,
"events": [ Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":0,"alt":false,"shift":false,"control":false,"meta":false,"command":false,"pressed":false,"scancode":88,"unicode":0,"echo":false,"script":null) ]
}

tecla_c={
"deadzone": 0.5,
"events": [ Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":0,"alt":false,"shift":false,"control":false,"meta":false,"command":false,"pressed":false,"scancode":67,"unicode":0,"echo":false,"script":null) ]
}

ui_accept={
"deadzone": 0.5,
"events": [ Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":0,"alt":false,"shift":false,"control":false,"meta":false,"command":false,"pressed":false,"scancode":88,"unicode":0,"echo":false,"script":null) ]
}
```

### Assets Necesarios
- `GUI/text.png` - Sprite auténtico del diálogo Pokemon Red
- `Fonts/Pokemon X and Y.ttf` - Fuente original Pokemon

---

## 3. Implementación paso a paso

### Paso 1: Crear la estructura de escena en main.tscn

```
main (Node2D)
├── game.gd
├── UI (CanvasLayer)
│   └── DialogRoot (Control)
│       ├── Panel (NinePatchRect)
│       │   ├── texture = "res://GUI/text.png"
│       │   ├── region_enabled = true
│       │   ├── region_rect = Rect2(187.25, 169.984, 318.75, 76.4837)
│       │   ├── patch_margin_left/top/right/bottom = 8
│       │   └── rect_clip_content = true
│       ├── Text (Label)
│       │   ├── anchor_right = 1.0, anchor_bottom = 1.0
│       │   ├── margin_left = 6, margin_top = 6
│       │   ├── margin_right = -30, margin_bottom = -6
│       │   ├── custom_fonts/font = DynamicFont (size=8, Pokemon font)
│       │   ├── custom_colors/font_color = Color(0,0,0,1)
│       │   └── autowrap = true
│       └── NextIcon (Label)
│           ├── visible = false
│           ├── anchor_left/top/right/bottom = 1.0
│           ├── margin_left = -20, margin_top = -20
│           ├── margin_right = -8, margin_bottom = -8
│           ├── text = "▶"
│           └── align/valign = 1
```

### Paso 2: Crear game.gd (Instanciado dinámico)

```gdscript
extends Node2D

export (PackedScene) var player
export (PackedScene) var nivel1

func _ready():
    var new_level = nivel1.instance()
    add_child(new_level)
    var new_player = player.instance()
    add_child(new_player)
    new_player.global_position = get_tree().get_nodes_in_group("spawn")[0].global_position
```

### Paso 3: Sistema de Interacción en player.gd

#### Variables clave:
```gdscript
extends KinematicBody2D

var current_dialog = null
var can_interact = true  # prevención input cíclico
```

#### Detección de input:
```gdscript
func _physics_process(delta):
    # No procesar input si el juego está pausado (por diálogos)
    if get_tree().paused:
        return
        
    # Manejo de interacciones solo si no hay dialogo activo
    if can_interact and current_dialog == null and not get_tree().paused and Input.is_action_just_pressed("tecla_x"):
        check_interaction()
        can_interact = false  # bloquea re-abrir hasta soltar
    
    # Re-habilitar tras soltar tecla
    if current_dialog == null and not get_tree().paused and Input.is_action_just_released("tecla_x"):
        can_interact = true
```

#### Sistema de interacción:
```gdscript
func check_interaction():
    var player_position = global_position
    var interaction_position = get_interaction_position()
    
    # Posiciones de objetos (ajustadas por offset del TileMap)
    var pc_pos = Vector2(-45, -18)
    var tv1_pos = Vector2(-9, 26)
    var tv2_pos = Vector2(-9, 39)
    
    # Calcular distancias mínimas
    var pc_distance_min = min(player_position.distance_to(pc_pos), interaction_position.distance_to(pc_pos))
    var tv1_distance_min = min(player_position.distance_to(tv1_pos), interaction_position.distance_to(tv1_pos))
    var tv2_distance_min = min(player_position.distance_to(tv2_pos), interaction_position.distance_to(tv2_pos))
    
    # Priorizar PC sobre TV si ambos están en rango
    if pc_distance_min <= 50:
        show_dialog("Mensaje del PC aquí...")
    elif tv1_distance_min <= 45 or tv2_distance_min <= 60:
        show_dialog("Mensaje del TV aquí...")

func get_interaction_position():
    # Obtener posición frente al player basado en la dirección
    var direction = Vector2()
    var stick_rotation = $stick/Position.rotation_degrees
    
    if stick_rotation == 0:      # Mirando arriba
        direction = Vector2(0, -16)
    elif stick_rotation == 90:   # Mirando derecha
        direction = Vector2(16, 0)
    elif stick_rotation == 180:  # Mirando abajo
        direction = Vector2(0, 16)
    elif stick_rotation == 270:  # Mirando izquierda
        direction = Vector2(-16, 0)
    else:
        direction = Vector2(0, 16)  # Default abajo
    
    return global_position + direction

func show_dialog(text):
    # Acceder al DialogRoot en CanvasLayer
    var dialog_root = get_tree().get_root().get_node("main/UI/DialogRoot")
    if dialog_root == null:
        print("ERROR: No se encontró DialogRoot")
        return
    
    dialog_root.show_dialog(text)
```

### Paso 4: Sistema de Diálogos (DialogBox.gd)

#### Variables de configuración:
```gdscript
extends Control

export(int) var min_rows = 2
export(float) var chars_per_sec = 60.0   # velocidad typewriter
export(int) var padding_px = 6
export(int) var playable_width = 160     # área jugable lógica
export(int) var playable_height = 112
export(float) var height_ratio = 0.30    # % del alto jugable
export(int) var margin_px = 4            # margen lateral/inferior

onready var label = $Panel/Text
onready var next_icon = $Panel/NextIcon
onready var panel = $Panel

var _pages = []
var _page_idx = 0
var _typing = false
var _type_timer = 0.0
var _typed_chars = 0
var _current_text = ""
```

#### Inicialización:
```gdscript
func _ready():
    hide()
    if next_icon:
        next_icon.hide()
    
    # Configuración del Label
    label.autowrap = true
    label.valign = Label.VALIGN_TOP
    
    # Funcionar cuando el juego está pausado
    pause_mode = Node.PAUSE_MODE_PROCESS
    
    # Layout automático
    _resize_to_playable()
    get_viewport().connect("size_changed", self, "_resize_to_playable")
```

#### Sistema de paginación:
```gdscript
func show_dialog(full_text):
    _pages = _paginate_text_exact(full_text)
    _page_idx = 0
    _show_page(_page_idx)

func _show_page(idx):
    if idx >= _pages.size():
        hide()
        get_tree().paused = false
        return
    
    show()
    get_tree().paused = true
    
    if next_icon:
        next_icon.hide()
    
    _current_text = _pages[idx]
    label.text = _current_text
    
    # Iniciar efecto typewriter
    _typing = true
    _typed_chars = 0
    _type_timer = 0.0
    label.visible_characters = 0
    set_process(true)
```

#### Efecto typewriter:
```gdscript
func _process(delta):
    if not _typing:
        return
    
    _type_timer += delta
    var target = int(_type_timer * chars_per_sec)
    
    if target > _typed_chars:
        _typed_chars = target
        var total_chars = _current_text.length()
        label.visible_characters = clamp(_typed_chars, 0, total_chars)
        
        if label.visible_characters >= total_chars:
            _typing = false
            if next_icon:
                next_icon.show()
```

#### Controles:
```gdscript
func _input(event):
    if not visible:
        return
    
    if (event.is_action_pressed("ui_accept") or event.is_action_pressed("tecla_x") or event.is_action_pressed("tecla_c")) and not event.is_echo():
        get_tree().set_input_as_handled()  # evita que suba al Player
        _advance_or_close()

func _advance_or_close():
    if _typing:
        # Completar texto inmediatamente
        _typing = false
        label.visible_characters = _current_text.length()
        if next_icon:
            next_icon.show()
    else:
        # Verificar si hay más páginas
        if _page_idx + 1 < _pages.size():
            _page_idx += 1
            _show_page(_page_idx)
        else:
            # Cerrar diálogo
            hide()
            get_tree().paused = false
```

#### Paginación automática:
```gdscript
func _paginate_text_exact(full_text):
    var text_area_size = _get_text_area_size()
    var fnt = label.get_font("font")
    var line_h = fnt.get_height()
    var char_w = max(1, fnt.get_string_size("M").x)

    var cols = int(floor(text_area_size.x / char_w))
    var rows = max(min_rows, int(floor(text_area_size.y / line_h)))
    if cols < 4:
        cols = 4

    var wrapped_lines = _word_wrap_to_cols(full_text, cols)

    var pages = []
    var i = 0
    while i < wrapped_lines.size():
        var page_lines = []
        for r in range(rows):
            if i >= wrapped_lines.size():
                break
            page_lines.append(wrapped_lines[i])
            i += 1
        
        # Concatenar líneas (sin Array.join() para Godot 3.5)
        var page_text = ""
        for j in range(page_lines.size()):
            if j > 0:
                page_text += "\\n"
            page_text += page_lines[j]
        pages.append(page_text)
    
    return pages

func _word_wrap_to_cols(text, cols):
    var words = text.split(" ")
    var lines = []
    var cur = ""
    
    for w in words:
        var test = ""
        if cur == "":
            test = w
        else:
            test = cur + " " + w
            
        if test.length() <= cols:
            cur = test
        else:
            if cur == "":
                # Palabra más larga que columnas: partir
                lines.append(w.substr(0, cols))
                var rest = w.substr(cols, w.length() - cols)
                while rest.length() > cols:
                    lines.append(rest.substr(0, cols))
                    rest = rest.substr(cols, rest.length() - cols)
                if rest != "":
                    cur = rest
                else:
                    cur = ""
            else:
                lines.append(cur)
                cur = w
    
    if cur != "":
        lines.append(cur)
    
    return lines

func _get_text_area_size():
    var size = panel.rect_size
    return Vector2(
        max(0, size.x - padding_px * 2),
        max(0, size.y - padding_px * 2)
    )
```

#### Posicionamiento:
```gdscript
func _resize_to_playable():
    var vr = get_viewport().get_visible_rect()
    var center = vr.position + vr.size * 0.5
    var playable_pos = center - Vector2(playable_width, playable_height) * 0.5
    var playable_rect = Rect2(playable_pos, Vector2(playable_width, playable_height))

    var dialog_h = int(playable_rect.size.y * height_ratio)
    var dialog_w = int(playable_rect.size.x) - margin_px * 2

    # Anchors en 0 para evitar conflictos
    anchor_left = 0; anchor_right = 0; anchor_top = 0; anchor_bottom = 0

    rect_position = Vector2(
        playable_rect.position.x + margin_px,
        playable_rect.position.y + playable_rect.size.y - dialog_h - margin_px
    )
    rect_size = Vector2(dialog_w, dialog_h)

    if panel:
        panel.anchor_left = 0; panel.anchor_top = 0
        panel.anchor_right = 1; panel.anchor_bottom = 1
        panel.margin_left = 0; panel.margin_top = 0
        panel.margin_right = 0; panel.margin_bottom = 0
```

---

## 4. Scripts Completos

### game.gd completo:
```gdscript
extends Node2D

export (PackedScene) var player
export (PackedScene) var nivel1

func _ready():
    var new_level = nivel1.instance()
    add_child(new_level)
    var new_player = player.instance()
    add_child(new_player)
    new_player.global_position = get_tree().get_nodes_in_group("spawn")[0].global_position
```

### player.gd (fragmentos clave):
```gdscript
extends KinematicBody2D

var vel_actual = Vector2()
var vel_desp = 16
var dialog_scene = preload("res://scenes/Dialogo.tscn")
var current_dialog = null
var can_interact = true

func _physics_process(delta):
    if get_tree().paused:
        return
        
    # Sistema de interacción
    if can_interact and current_dialog == null and not get_tree().paused and Input.is_action_just_pressed("tecla_x"):
        check_interaction()
        can_interact = false
    
    if current_dialog == null and not get_tree().paused and Input.is_action_just_released("tecla_x"):
        can_interact = true
    
    # [Resto del código de movimiento...]

func check_interaction():
    var player_position = global_position
    var interaction_position = get_interaction_position()
    
    var pc_pos = Vector2(-45, -18)
    var tv1_pos = Vector2(-9, 26)
    var tv2_pos = Vector2(-9, 39)
    
    var pc_distance_min = min(player_position.distance_to(pc_pos), interaction_position.distance_to(pc_pos))
    var tv1_distance_min = min(player_position.distance_to(tv1_pos), interaction_position.distance_to(tv1_pos))
    var tv2_distance_min = min(player_position.distance_to(tv2_pos), interaction_position.distance_to(tv2_pos))
    
    if pc_distance_min <= 50:
        show_dialog("Encendiste la PC. Es una máquina increíblemente poderosa...")
    elif tv1_distance_min <= 45 or tv2_distance_min <= 60:
        show_dialog("En la televisión hay un programa muy interesante...")

func get_interaction_position():
    var direction = Vector2()
    var stick_rotation = $stick/Position.rotation_degrees
    
    if stick_rotation == 0:
        direction = Vector2(0, -16)
    elif stick_rotation == 90:
        direction = Vector2(16, 0)
    elif stick_rotation == 180:
        direction = Vector2(0, 16)
    elif stick_rotation == 270:
        direction = Vector2(-16, 0)
    else:
        direction = Vector2(0, 16)
    
    return global_position + direction

func show_dialog(text):
    var dialog_root = get_tree().get_root().get_node("main/UI/DialogRoot")
    if dialog_root == null:
        print("ERROR: No se encontró DialogRoot")
        return
    
    dialog_root.show_dialog(text)
```

---

## 5. Testing y Debug

### Verificaciones importantes:
1. **Input Map**: Verificar que `tecla_x`, `tecla_c` y `ui_accept` están configurados
2. **Assets**: Verificar que `GUI/text.png` y `Fonts/Pokemon X and Y.ttf` existen
3. **Rutas**: Verificar que `main/UI/DialogRoot` es accesible desde player
4. **Anchors**: DialogRoot debe tener anchors en 0, no "Full Rect"
5. **CanvasLayer**: UI debe ser CanvasLayer, no seguir viewport

### Debug útil:
```gdscript
# En player.gd
func check_interaction():
    print("Tecla X presionada - iniciando check_interaction")
    print("Posición del player: ", global_position)
    print("Distancias - PC: ", pc_distance_min, " TV: ", tv_distance_min)

# En DialogBox.gd
func _resize_to_playable():
    print("=== DEBUG PLAYABLE AREA ===")
    print("Visible rect: ", vr)
    print("Dialog position: ", rect_position)
    print("Dialog size: ", rect_size)
```

### Problemas comunes:
1. **Diálogo no aparece**: Verificar ruta `main/UI/DialogRoot`
2. **Input cíclico**: Usar `can_interact` y `get_tree().set_input_as_handled()`
3. **Posición incorrecta**: Verificar que anchors están en 0
4. **Texto cortado**: Ajustar `padding_px` y márgenes del Label
5. **Sin paginación**: Verificar que `_paginate_text_exact` se llama correctamente

---

## 🎯 Resultado Final

Con esta implementación obtienes:
- ✅ **Sistema de diálogos Pokemon Red auténtico**
- ✅ **Paginación automática** para textos largos
- ✅ **Efecto typewriter** configurable
- ✅ **Controles X/C** como el Game Boy original
- ✅ **Pausa de juego** durante diálogos
- ✅ **Prevención de input cíclico**
- ✅ **Posicionamiento correcto** dentro del área jugable
- ✅ **Interacción basada en distancia** con priorización
- ✅ **Compatible 100% con Godot 3.5**

El sistema es modular, reutilizable y escalable para agregar más objetos interactivos o mejoras adicionales.