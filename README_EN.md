# Pokemon Red - Godot 3.5

Pokemon Red recreation project using Godot 3.5, with optimized TileSet and complete utilities system.

## 🎮 Current Status

- **Engine**: Godot 3.5
- **Status**: ✅ Functional and optimized (August 2025)
- **Level**: Ash's room completely playable
- **TileSet**: Optimized (24 unique tiles, 100% efficiency)

## 🚀 How to Play

1. Open Godot 3.5
2. Import project from `project.godot`
3. Run `main.tscn`
4. Use keyboard arrows to move the player

## 📁 Project Structure

```
PokemonRed/
├── main.tscn               # Main scene
├── game.gd                 # Main game logic
├── scenes/
│   ├── Nivel1.tscn        # Ash's room (main level)
│   └── player.tscn        # Player with animations
├── tilesets/
│   ├── ash_room_small_optimized.tres  # Optimized TileSet ⭐
│   └── Ash_room_sharp.png             # Source sprite
├── sprites/               # Player sprites
├── utils/                 # 🛠️ Utility scripts (19 scripts)
│   └── README.md         # Complete documentation
└── README_COLISIONES.md  # Collision guide (ℹ️ see note below)
```

## ⚡ Features

### Movement System
- **Grid-based**: Precise 16x16 pixel movement
- **Automatic snap**: Perfectly aligns to grid
- **Animations**: Walking in 4 directions

### Technical Optimizations
- **Reconstructed TileSet**: 63 tiles → 24 unique tiles (61.9% reduction)
- **Eliminated duplicates**: Automatic visual analysis
- **100% efficiency**: Only necessary tiles

## 🛠️ Development Tools

The `utils/` folder contains **19 specialized scripts**:

### 🔍 For Analysis:
```bash
cd utils
python3 decode_tilemap.py          # View map structure
python3 analyze_spawn_system.py    # Understand positioning system
```

### ⚙️ For Optimization:
```bash
cd utils  
python3 analyze_sprite_for_unique_tiles.py  # Find duplicates
python3 extract_tileset_config.py           # Optimize TileSet
```

See `utils/README.md` for complete guide.

## 📊 Optimization Statistics

| Metric | Original | Optimized | Improvement |
|---------|----------|------------|--------|
| TileSet tiles | 63 tiles | 24 tiles | **-61.9%** |
| Visual duplicates | 5 | 0 | **-100%** |
| Usage efficiency | 46.0% | 100.0% | **+54.0%** |
| Functionality | ✅ Complete | ✅ Complete | **Preserved** |

## 🎯 Implemented Systems

- ✅ **Grid-based movement** with automatic snap
- ✅ **Spawn/player system** with coordinate reference  
- ✅ **Optimized TileMap** with unique tiles
- ✅ **Player animations** (4 directions)
- ✅ **Modular architecture** (main → game → level → player)
- ✅ **Robust collision system** with room boundaries
- ✅ **Safe snap-to-grid** that prevents accidental escapes

## ⚠️ Important Notes

### About README_COLISIONES.md
This file contains useful collision documentation, but **is outdated**:
- ❌ Mentions tiles 64-67 that were eliminated in optimization
- ❌ References unoptimized TileSet
- ✅ Collision concepts remain valid

### File Status
- **Current TileSet**: `tilesets/ash_room_small_optimized.tres`
- **Previous TileSet**: `tilesets/ash_room_small.tres` (unoptimized)
- **Backups**: Created automatically when using scripts

## 🔄 For Developers

### Restore Previous TileSet (if needed):
```bash
# Backups are in tilesets/ash_room_small.tres.backup_*
cp tilesets/ash_room_small.tres.backup_* tilesets/ash_room_small.tres
```

### Apply Optimization to Other Levels:
```bash
cd utils
python3 analyze_sprite_for_unique_tiles.py  # Analysis
python3 extract_tileset_config.py           # Optimization
```

## 🎮 Controls

- **↑↓←→**: Move player
- **X**: Interact with objects
- **C**: Close dialogs
- **Grid-based**: Precise tile-by-tile movement

## 🛡️ Collision System

### Features:
- **Physical boundaries**: 4 invisible walls (Top, Left, Right, Bottom)
- **Specific objects**: Bed, TV/furniture with individual collisions
- **Pre-detection**: Checks collision before moving
- **Safe snap**: Only repositions if new position is valid
- **Automatic recovery**: Player never gets "stuck"

### Room Boundaries:
- **TopWall**: Position (0, -40) - Blocks upper exit
- **LeftWall**: Position (-80, 16) - Blocks left exit
- **RightWall**: Position (80, 16) - Blocks right exit  
- **BottomWall**: Position (0, 72) - Blocks lower exit

### Objects with Collision:
- **🛏️ Bed (6 tiles)**: Positions (-64,-31) to (-32,-15) - Upper left corner
- **📺 TV/Furniture (4 tiles)**: Positions (32,-31) to (48,-15) - Upper right corner
- **Total**: 14 CollisionShape2D implemented

### Debug Messages:
- `"Collision detected [direction] - player stays in position"`
- `"Player snapped to: (x, y)"` - Successful snap
- `"Snap cancelled - maintain at: (x, y)"` - Snap blocked by safety

## 🎮 Implemented Interaction System

### ✅ Completed Functionalities
- **X and C keys**: Configured for interaction (A/B buttons from Game Boy)
- **Object detection**: PC and TV/console with specific messages
- **Dialog system**: Functional with authentic Pokemon Red sprite
- **Game pause**: During dialogs
- **Pokemon font**: Authentic from original Pokemon Red

### 🔧 Current Status - COMPLETELY OPTIMIZED
- **Functional interaction**: Player can interact with PC and TV
- **Optimized dialog system**: 3-line pagination, dynamic positioning, X/C controls
- **Dynamic positioning**: Dialog correctly follows player within game area
- **Optimized typography**: 5px font with adjusted spacing, full space utilization
- **Efficient messages**: Up to 3 lines per page, significantly fewer pages

See `DIALOGS_IMPLEMENTATION_EN.md` for complete documentation.

## 🚀 Next Steps

- [x] Basic interaction system
- [x] **Pokemon Red dialog system** (complete with pagination and typewriter)
- [x] **Dynamic dialog positioning** (follows player)
- [x] **Complete text optimization** (3 lines, 5px font, optimized spacing)
- [ ] Add more interactive objects
- [ ] Room transition system
- [ ] Gameplay mechanics (NPCs, objects, combat)

---

*Optimized and documented project - August 2025*  
*Use scripts in `utils/` for analysis and maintenance*