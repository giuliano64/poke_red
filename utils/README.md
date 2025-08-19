# Scripts de Utilidades - Pokemon Red Godot

Esta carpeta contiene scripts de Python creados para el análisis, optimización y mantenimiento del proyecto Pokemon Red en Godot.

## 📁 Organización por Categorías

### 🔍 **ANÁLISIS Y DECODIFICACIÓN**

#### `decode_tilemap.py`
- **Propósito**: Decodifica los datos binarios del TileMap de Godot a una matriz legible
- **Uso**: `python3 decode_tilemap.py`
- **Output**: Muestra matriz 8x6 con Tile IDs en formato visual
- **Cuándo usar**: Para visualizar qué tiles se están usando y dónde

#### `analyze_tileset.py`
- **Propósito**: Analiza un TileSet para identificar duplicados obvios
- **Uso**: `python3 analyze_tileset.py`
- **Output**: Lista duplicados encontrados (ej. tiles 64-67)
- **Cuándo usar**: Primera verificación rápida de duplicados

#### `analyze_used_tiles.py`
- **Propósito**: Identifica qué tiles del TileSet están siendo utilizados realmente
- **Uso**: `python3 analyze_used_tiles.py`
- **Output**: Estadísticas de uso y eficiencia del TileSet
- **Cuándo usar**: Antes de hacer optimizaciones para saber qué eliminar

#### `analyze_sprite_for_unique_tiles.py`
- **Propósito**: Analiza el sprite original para encontrar duplicados visuales
- **Uso**: `python3 analyze_sprite_for_unique_tiles.py`
- **Output**: Mapeo de tiles únicos y archivo `tile_mapping.txt`
- **Cuándo usar**: Para reconstruir TileSet desde cero con solo tiles únicos

### 🎯 **SISTEMAS DEL JUEGO**

#### `analyze_spawn_system.py`
- **Propósito**: Analiza el sistema de spawn y posicionamiento del player
- **Uso**: `python3 analyze_spawn_system.py`
- **Output**: Explicación completa del sistema spawn-player
- **Cuándo usar**: Para entender cómo funciona el posicionamiento

#### `analyze_positions.py`
- **Propósito**: Analiza posiciones exactas de elementos en el juego
- **Uso**: `python3 analyze_positions.py`
- **Output**: Coordenadas precisas de spawn, player, TileMap
- **Cuándo usar**: Para debug de posicionamiento

#### `analyze_main_flow.py`
- **Propósito**: Valida el flujo completo desde main.tscn hasta el juego
- **Uso**: `python3 analyze_main_flow.py`
- **Output**: Verificación de conexiones entre escenas
- **Cuándo usar**: Para verificar integridad del proyecto

### ⚙️ **OPTIMIZACIÓN**

#### `identify_safe_duplicates.py`
- **Propósito**: Identifica tiles duplicados seguros para eliminar
- **Uso**: `python3 identify_safe_duplicates.py`
- **Output**: Lista de tiles que se pueden eliminar sin problemas
- **Cuándo usar**: Antes de optimizaciones conservadoras

#### `advanced_tileset_optimizer.py`
- **Propósito**: Optimizador conservativo que elimina tiles del final
- **Uso**: `python3 advanced_tileset_optimizer.py`
- **Output**: TileSet optimizado eliminando tiles seguros
- **Cuándo usar**: Para optimización sin remapeo del TileMap

#### `complete_tileset_optimizer.py`
- **Propósito**: Optimizador completo que elimina duplicados y no utilizados
- **Uso**: `python3 complete_tileset_optimizer.py`
- **Output**: TileSet con máxima optimización posible
- **Cuándo usar**: Para optimización agresiva

#### `extract_tileset_config.py`
- **Propósito**: Extrae configuraciones del TileSet y crea versión optimizada
- **Uso**: `python3 extract_tileset_config.py` (requiere `tile_mapping.txt`)
- **Output**: TileSet reconstruido + script de actualización
- **Cuándo usar**: Para reconstrucción completa manteniendo funcionalidad

#### `update_tilemap.py`
- **Propósito**: Actualiza el TileMap para usar IDs de TileSet optimizado
- **Uso**: `python3 update_tilemap.py` (generado automáticamente)
- **Output**: TileMap actualizado con nuevos IDs
- **Cuándo usar**: Después de crear TileSet optimizado

### 🧪 **VERIFICACIÓN Y TESTING**

#### `test_optimized_tilemap.py`
- **Propósito**: Verifica compatibilidad entre TileSet y TileMap
- **Uso**: `python3 test_optimized_tilemap.py`
- **Output**: Reporte de compatibilidad y tiles faltantes
- **Cuándo usar**: Después de cualquier optimización

#### `verify_optimization.py`
- **Propósito**: Verifica que los cambios de optimización son correctos
- **Uso**: `python3 verify_optimization.py`
- **Output**: Validación de integridad post-optimización
- **Cuándo usar**: Después de optimizaciones básicas

#### `verify_tileset_optimization.py`
- **Propósito**: Verificación específica de optimizaciones del TileSet
- **Uso**: `python3 verify_tileset_optimization.py`
- **Output**: Validación detallada del TileSet optimizado
- **Cuándo usar**: Para confirmar optimizaciones del TileSet

#### `verify_optimized_system.py`
- **Propósito**: Verificación completa del sistema TileSet+TileMap optimizado
- **Uso**: `python3 verify_optimized_system.py`
- **Output**: Reporte final completo con estadísticas
- **Cuándo usar**: Después de reconstrucción completa

### 🔧 **UTILIDADES ESPECIALIZADAS**

#### `find_visual_duplicates.py`
- **Propósito**: Encuentra duplicados basándose en regiones visuales
- **Uso**: `python3 find_visual_duplicates.py`
- **Output**: Análisis de duplicados por región de sprite
- **Cuándo usar**: Para identificar duplicados visuales específicos

#### `fix_tileset_removal.py`
- **Propósito**: Corrige problemas de eliminación de tiles específicos
- **Uso**: `python3 fix_tileset_removal.py`
- **Output**: TileSet con tiles problemáticos eliminados
- **Cuándo usar**: Cuando la eliminación automática falla

#### `optimize_tilemap.py`
- **Propósito**: Optimización directa del TileMap (no usado finalmente)
- **Uso**: `python3 optimize_tilemap.py`
- **Output**: TileMap optimizado
- **Cuándo usar**: Para optimización directa sin TileSet (experimental)

#### `optimization_summary.py`
- **Propósito**: Genera resumen de optimizaciones realizadas
- **Uso**: `python3 optimization_summary.py`
- **Output**: Reporte estadístico de mejoras
- **Cuándo usar**: Para documentar resultados de optimización

## 📋 **Flujos de Trabajo Recomendados**

### **Análisis Inicial del Proyecto**
```bash
cd utils
python3 decode_tilemap.py          # Ver estructura actual
python3 analyze_tileset.py         # Identificar duplicados obvios  
python3 analyze_used_tiles.py      # Ver eficiencia actual
```

### **Optimización Conservadora**
```bash
cd utils
python3 identify_safe_duplicates.py       # Identificar qué eliminar
python3 advanced_tileset_optimizer.py     # Aplicar optimización
python3 verify_optimization.py            # Verificar resultado
```

### **Reconstrucción Completa (Recomendada)**
```bash
cd utils
python3 analyze_sprite_for_unique_tiles.py    # Identificar tiles únicos
python3 extract_tileset_config.py             # Crear TileSet optimizado
python3 update_tilemap.py                     # Actualizar TileMap
python3 verify_optimized_system.py            # Verificar todo
```

### **Análisis de Sistemas del Juego**
```bash
cd utils  
python3 analyze_spawn_system.py       # Entender spawn system
python3 analyze_positions.py          # Ver posiciones exactas
python3 analyze_main_flow.py          # Validar flujo completo
```

## 📝 **Notas Importantes**

- **Backups**: Todos los scripts crean backups automáticos antes de modificar archivos
- **Compatibilidad**: Los scripts mantienen 100% compatibilidad con la funcionalidad existente
- **Orden**: Seguir los flujos recomendados para evitar problemas
- **Verificación**: Siempre ejecutar scripts de verificación después de optimizaciones

## 🎯 **Resultados Obtenidos**

Con estos scripts logramos:
- **TileSet**: 63 tiles → 24 tiles únicos (61.9% reducción)
- **Eficiencia**: 46.0% → 100.0% 
- **Duplicados**: Eliminados completamente
- **Funcionalidad**: 100% preservada

---

*Scripts creados el 19 de agosto 2025 para optimización del proyecto Pokemon Red en Godot 3.5*