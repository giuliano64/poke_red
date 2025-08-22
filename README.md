# Pokemon Red - Godot 3.5

Proyecto de recreación de Pokemon Red usando Godot 3.5, con TileSet optimizado y sistema completo de utilidades.

## 🎮 Estado Actual

- **Motor**: Godot 3.5
- **Estado**: ✅ Funcional y optimizado (Agosto 2025)
- **Nivel**: Ash's room completamente jugable
- **TileSet**: Optimizado (24 tiles únicos, 100% eficiencia)

## 🚀 Cómo Jugar

1. Abre Godot 3.5
2. Importa el proyecto desde `project.godot`
3. Ejecuta `main.tscn`
4. Usa flechas del teclado para mover al player

## 📁 Estructura del Proyecto

```
PokemonRed/
├── main.tscn               # Escena principal
├── game.gd                 # Lógica principal del juego
├── scenes/
│   ├── Nivel1.tscn        # Ash's room (nivel principal)
│   └── player.tscn        # Player con animaciones
├── tilesets/
│   ├── ash_room_small_optimized.tres  # TileSet optimizado ⭐
│   └── Ash_room_sharp.png             # Sprite fuente
├── sprites/               # Sprites del player
├── utils/                 # 🛠️ Scripts de utilidades (19 scripts)
│   └── README.md         # Documentación completa
└── README_COLISIONES.md  # Guía de colisiones (ℹ️ ver nota abajo)
```

## ⚡ Características

### Sistema de Movimiento
- **Grid-based**: Movimiento preciso de 16x16 píxeles
- **Snap automático**: Se alinea perfectamente al grid
- **Animaciones**: Caminar en 4 direcciones

### Optimizaciones Técnicas
- **TileSet reconstruido**: 63 tiles → 24 tiles únicos (61.9% reducción)
- **Duplicados eliminados**: Análisis visual automático
- **Eficiencia 100%**: Solo tiles necesarios

## 🛠️ Herramientas de Desarrollo

La carpeta `utils/` contiene **19 scripts** especializados:

### 🔍 Para Análisis:
```bash
cd utils
python3 decode_tilemap.py          # Ver estructura del mapa
python3 analyze_spawn_system.py    # Entender sistema de posicionamiento
```

### ⚙️ Para Optimización:
```bash
cd utils  
python3 analyze_sprite_for_unique_tiles.py  # Encontrar duplicados
python3 extract_tileset_config.py           # Optimizar TileSet
```

Ver `utils/README.md` para guía completa.

## 📊 Estadísticas de Optimización

| Métrica | Original | Optimizado | Mejora |
|---------|----------|------------|--------|
| Tiles en TileSet | 63 tiles | 24 tiles | **-61.9%** |
| Duplicados visuales | 5 | 0 | **-100%** |
| Eficiencia de uso | 46.0% | 100.0% | **+54.0%** |
| Funcionalidad | ✅ Completa | ✅ Completa | **Preservada** |

## 🎯 Sistemas Implementados

- ✅ **Movimiento grid-based** con snap automático
- ✅ **Sistema spawn/player** con referencia de coordenadas  
- ✅ **TileMap optimizado** con tiles únicos
- ✅ **Animaciones** del player (4 direcciones)
- ✅ **Arquitectura modular** (main → game → nivel → player)
- ✅ **Sistema de colisiones robusto** con límites de habitación
- ✅ **Snap-to-grid seguro** que previene escapes accidentales

## ⚠️ Notas Importantes

### Sobre README_COLISIONES.md
Este archivo contiene documentación útil sobre colisiones, pero **está desactualizado**:
- ❌ Menciona tiles 64-67 que fueron eliminados en la optimización
- ❌ Referencia TileSet sin optimizar
- ✅ Conceptos de colisión siguen siendo válidos

### Estado de Archivos
- **TileSet actual**: `tilesets/ash_room_small_optimized.tres`
- **TileSet anterior**: `tilesets/ash_room_small.tres` (no optimizado)
- **Backups**: Se crean automáticamente al usar scripts

## 🔄 Para Desarrolladores

### Restaurar TileSet Anterior (si necesario):
```bash
# Los backups están en tilesets/ash_room_small.tres.backup_*
cp tilesets/ash_room_small.tres.backup_* tilesets/ash_room_small.tres
```

### Aplicar Optimización a Otros Niveles:
```bash
cd utils
python3 analyze_sprite_for_unique_tiles.py  # Análisis
python3 extract_tileset_config.py           # Optimización
```

## 🎮 Controles

- **↑↓←→**: Mover player
- **Grid-based**: Movimiento preciso tile por tile

## 🛡️ Sistema de Colisiones

### Características:
- **Límites físicos**: 4 paredes invisibles (Top, Left, Right, Bottom)
- **Objetos específicos**: Cama, TV/mueble con colisiones individuales
- **Detección previa**: Verifica colisión antes de moverse
- **Snap seguro**: Solo reposiciona si la nueva posición es válida
- **Recuperación automática**: Nunca queda el player "colgado"

### Límites de Habitación:
- **TopWall**: Posición (0, -40) - Bloquea salida superior
- **LeftWall**: Posición (-80, 16) - Bloquea salida izquierda
- **RightWall**: Posición (80, 16) - Bloquea salida derecha  
- **BottomWall**: Posición (0, 72) - Bloquea salida inferior

### Objetos con Colisión:
- **🛏️ Cama (6 tiles)**: Posiciones (-64,-31) a (-32,-15) - Esquina superior izquierda
- **📺 TV/Mueble (4 tiles)**: Posiciones (32,-31) a (48,-15) - Esquina superior derecha
- **Total**: 14 CollisionShape2D implementados

### Mensajes de Debug:
- `"Colisión detectada [dirección] - player se queda en posición"`
- `"Player snapped to: (x, y)"` - Snap exitoso
- `"Snap cancelado - mantener en: (x, y)"` - Snap bloqueado por seguridad

## 🎮 Sistema de Interacción Implementado

### ✅ Funcionalidades Completadas
- **Teclas X y C**: Configuradas para interacción (A/B buttons del Game Boy)
- **Detección de objetos**: PC y TV/consola con mensajes específicos
- **Sistema de diálogos**: Funcional con sprite auténtico de Pokemon Red
- **Pausa del juego**: Durante los diálogos
- **Fuente Pokemon**: Auténtica del Pokemon Red original

### 🔧 Estado Actual - COMPLETAMENTE OPTIMIZADO
- **Interacción funcional**: El player puede interactuar con PC y TV
- **Sistema de diálogos optimizado**: Paginación a 3 líneas, posicionamiento dinámico, controles X/C
- **Posicionamiento dinámico**: Diálogo sigue al jugador correctamente dentro del área de juego
- **Tipografía optimizada**: Fuente 5px con espaciado ajustado, aprovechamiento total del espacio
- **Mensajes eficientes**: Hasta 3 líneas por página, significativamente menos páginas

Ver `DIALOGS_IMPLEMENTATION.md` para documentación completa.

## 🚀 Próximos Pasos

- [x] Sistema de interacción básico
- [x] **Sistema de diálogos Pokemon Red** (completo con paginación y typewriter)
- [x] **Posicionamiento dinámico del diálogo** (sigue al jugador)
- [x] **Optimización completa de texto** (3 líneas, fuente 5px, spacing optimizado)
- [ ] Añadir más objetos interactivos
- [ ] Sistema de transiciones entre habitaciones
- [ ] Mecánicas de gameplay (NPCs, objetos, combate)

---

*Proyecto optimizado y documentado - Agosto 2025*  
*Utiliza scripts en `utils/` para análisis y mantenimiento*