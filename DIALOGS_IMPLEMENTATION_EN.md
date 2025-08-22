# Dialog System - Pokemon Red Godot 3.5

## Current Project Status

### ✅ Completed Functionalities

1. **Interaction System with X and C Keys**
   - Keys configured in `project.godot`
   - X = A Button (interact/confirm)
   - C = B Button (cancel/close)

2. **Interactive Object Detection**
   - PC at position (-45, -18) adjusted by TileMap offset
   - TV/Console at positions (-9, 26) and (-9, 39)
   - Prioritization system: PC > TV when both are in range
   - Detection based on minimum distance from player

3. **Functional Dialog System**
   - Shows/hides dialogs correctly
   - Pauses game during dialog
   - Closes with X or C
   - Uses authentic Pokemon Red sprite (`GUI/text.png`)
   - Authentic Pokemon font (`Fonts/Pokemon X and Y.ttf`)

### ❌ Previous Problem (SOLVED)

**Dialog appeared OUTSIDE the game area** instead of inside like in the original Pokemon Red.

## System Architecture

### File Structure
```
PokemonRed/
├── main.tscn                 # Main scene with GUI
├── game.gd                   # Main script 
├── player.gd                 # Player logic + interaction system
├── scenes/
│   ├── Dialogo.tscn         # Dialog scene
│   ├── player.tscn          # Player with animations
│   └── Nivel1.tscn          # Level with collisions
├── GUI/
│   └── text.png             # Dialog sprite (copied from reference)
├── Fonts/
│   └── Pokemon X and Y.ttf  # Authentic font (copied from reference)
└── dialogo.gd               # Dialog script
```

### Interaction Flow

1. **Player presses X** → `player.gd::_physics_process()`
2. **Interaction position calculated** → `get_interaction_position()`
3. **Distance to objects verified** → `check_interaction()`
4. **PC prioritized over TV** → `if pc_distance_min <= 50` logic
5. **Dialog displayed** → `show_dialog()` accesses `GUI/Dialogo`

## Step by Step Implementation

### Step 1: Configure Input Keys

In `project.godot`, add:
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

### Step 2: GUI Structure in main.tscn

```gdscript
[node name="main" type="Node2D"]
[node name="GUI" type="Node2D" parent="." groups=["gui"]]
[node name="Dialogo" parent="GUI" instance=ExtResource( 4 )]
```

### Step 3: Create Dialog Scene (Dialogo.tscn)

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

### Step 4: Dialog Script (dialogo.gd)

```gdscript
extends Node2D

func show_dialog(text: String):
    # Show sprite and text
    $bkg_txt.visible = true
    $txt.visible = true
    $txt.text = text
    
    # Pause game
    get_tree().paused = true
    pause_mode = Node.PAUSE_MODE_PROCESS

func hide_dialog():
    # Hide and unpause
    $bkg_txt.visible = false
    $txt.visible = false
    get_tree().paused = false
```

### Step 5: Interaction System in player.gd

```gdscript
# In _physics_process()
if Input.is_action_just_pressed("tecla_x"):
    check_interaction()

func check_interaction():
    # Calculate positions and distances
    var pc_distance = player_position.distance_to(Vector2(-45, -18))
    
    # Prioritize PC over TV
    if pc_distance <= 50:
        show_dialog("PC message")

func show_dialog(text: String):
    # Access GUI
    var gui = get_tree().get_nodes_in_group("gui")[0]
    var dialogo = gui.get_node("Dialogo") 
    dialogo.show_dialog(text)
```

## Reference Solution Configuration

### Exact Reference Values
- **bkg_txt position**: `Vector2( 258.053, 424 )`
- **bkg_txt scale**: `Vector2( 1.61006, 1.68421 )`
- **txt margins**: `left=16, top=376, right=496, bottom=472`
- **Font size**: `24`

### Game Sizes
- **Cell size**: 16x16 pixels
- **Game area**: Approximately 160x144 pixels
- **Dialog should be**: ~64-80 pixels wide (4-5 tiles)

## 🎉 COMPLETED AND OPTIMIZED SYSTEM - August 2025

### ✅ Completely Optimized Pokemon Red System

A complete production-ready Pokemon Red style dialog system was implemented and optimized:

#### **Final Architecture:**
1. **CanvasLayer UI:** Stable dialog independent from game world
2. **Optimized pagination:** Text divided into pages with 3 lines maximum and full space utilization
3. **Dynamic positioning:** Dialog correctly follows player within game area
4. **Typewriter effect:** Characters appear gradually (60 chars/sec)
5. **Pokemon controls:** X advances/completes, C closes immediately
6. **Game pause:** Player doesn't move during dialogs
7. **Visual indicator:** Arrow ▶ shows when there's more content
8. **Optimized typography:** 5px font with adjusted spacing for maximum readability

#### **Created/Modified Files:**
- `DialogBox.gd`: Complete script with pagination and typewriter
- `main.tscn`: CanvasLayer with DialogRoot (75% width x 28% height)
- `player.gd`: Integration with new system + input cycling prevention
- `game.gd`: PlayArea persistence and dynamic recalculation
- `project.godot`: Input mapping ui_accept (X key)

#### **Technical Components:**
- **DialogRoot (Control):** Main container positioned relatively
- **Panel (NinePatchRect):** Using authentic Pokemon Red sprite
- **Text (Label):** With manual wrapping and authentic Pokemon font (size=5)
- **NextIcon (Label):** ▶ indicator for more content

### 🔧 Solved Problems
1. ✅ Dialog appears within game area (dynamically positioned)
2. ✅ Proportional size using relative positioning (75% width x 28% height)
3. ✅ Automatic pagination for long texts
4. ✅ Typewriter effect with configurable speed
5. ✅ X/C controls working correctly
6. ✅ Input prevention during active dialog
7. ✅ Automatic game pause/resume
8. ✅ GDScript 3.5 compatibility (without := operators)
9. ✅ Dynamic positioning following player movement
10. ✅ Optimized typography with maximum space utilization

### 🛠️ Recent Major Improvements
- **Dynamic positioning:** Dialog follows player movement correctly
- **Text optimization:** Font reduced to 5px with adjusted spacing
- **3 lines per page:** Significant reduction in number of pages
- **Space optimization:** 75% width dialog, full area utilization
- **autowrap fix:** Disabled to prevent interference with manual wrapping

### 🎮 Implemented Example Messages

```gdscript
// PC (with automatic pagination)
"You turned on the PC. It's an incredibly powerful machine that will allow you to completely manage your Pokemon team. In the future you'll be able to store all your captured Pokemon here. You'll also be able to access the Pokemon storage system that connects to the Pokemon Center. This will be your most important tool for organizing your adventure."

// TV/Console (with automatic pagination)  
"There's a very interesting program on television about a young trainer who is beginning his Pokemon adventure. He's exploring different regions and capturing incredible Pokemon. But you better follow your own path to greatness."
```

### 🧪 Testing Completed
1. ✅ PC/TV interaction functional
2. ✅ Automatic pagination for long texts
3. ✅ Typewriter effect working
4. ✅ X/C controls operational
5. ✅ Game pause during dialogs
6. ✅ Dialog appears in correct position
7. ✅ Dynamic positioning following player
8. ✅ Optimized text layout with full space utilization

## Status: ✅ FULLY OPTIMIZED AND OPERATIONAL

🎮 Dialog system is completely implemented and functional  
📱 Dialog appears correctly within game area and follows player  
⌨️ Pokemon Red controls implemented (X advances, C closes)  
📄 Automatic pagination for long texts operational  
🎨 Optimized typography with maximum space efficiency