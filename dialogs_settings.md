# Configuración de Diálogos - Centrado en Área Jugable

## 🎯 **¿Cómo Funciona el Sistema?**

El sistema centra los diálogos **SOLO en el área donde se juega**, no en toda la pantalla. Esto evita que aparezcan en zonas grises (letterbox) o fuera del mapa.

---

## 📐 **Proceso Técnico**

### **Paso 1: Calcular Área Jugable Real**
`PlayArea.gd` analiza el TileMap y calcula exactamente qué parte de la pantalla ocupa:

```gdscript
# Convierte tiles usados → píxeles del mundo → píxeles de pantalla
var used = tm.get_used_rect()     # Ej: 10x9 tiles
var cell = tm.cell_size           # Ej: 16x16 píxeles por tile

# Resultado: Rectángulo exacto del área jugable
rect_screen = Rect2(50, 30, 160, 144)  # pos(50,30) + tamaño(160x144)
```

### **Paso 2: Posicionar Diálogo Dentro de Esa Área**
`DialogBox.gd` usa **SOLO** el área jugable para calcular posición y tamaño:

```gdscript
# Tamaño del diálogo = % del área jugable (NO del viewport)
var box_w = int(area_jugable.width * width_ratio)   # 160 * 0.66 = 105px
var box_h = int(area_jugable.height * height_ratio) # 144 * 0.22 = 31px

# Centrar DENTRO del área jugable
var pos_x = area_jugable.x + int((area_jugable.width - box_w) / 2)
var pos_y = area_jugable.y + area_jugable.height - box_h - margen
```

---

## 🎮 **Comparación Visual**

### **❌ Antes (Sistema Malo):**
```
┌─────────────────────────────────┐ ← Viewport completo
│ ████████████████████████████████ │
│ ┌─────────────────────────────┐ │
│ │                             │ │
│ │     ÁREA DE JUEGO           │ │
│ │                             │ │
│ └─────────────────────────────┘ │
│ [Diálogo centrado en viewport]  │ ← MAL: fuera del juego
│ ████████████████████████████████ │
└─────────────────────────────────┘
```

### **✅ Ahora (Sistema Correcto):**
```
┌─────────────────────────────────┐
│ ████████████████████████████████ │
│ ┌─────────────────────────────┐ │
│ │                             │ │
│ │     ÁREA DE JUEGO           │ │
│ │                             │ │
│ │    [Diálogo centrado]       │ │ ← BIEN: dentro del juego
│ └─────────────────────────────┘ │
│ ████████████████████████████████ │
└─────────────────────────────────┘
```

---

## ⚙️ **Configuración de Diálogos**

### **Variables Principales** (en `DialogBox.gd`):

```gdscript
export(float) var width_ratio  = 0.66   # % del ancho del área jugable
export(float) var height_ratio = 0.22   # % del alto del área jugable
export(int)   var h_align      = 0      # Alineación horizontal
export(int)   var bottom_px    = 6      # Margen inferior
export(int)   var margin_px    = 6      # Margen lateral
```

### **Valores de `h_align`:**
- **0** = Izquierda (estilo Game Boy)
- **1** = Centrado
- **2** = Derecha

---

## 🔧 **Cómo Personalizar**

### **Para Centrar el Diálogo:**
```gdscript
export(int) var h_align = 1    # Cambiar a centrado
```

### **Para Hacerlo Más Ancho:**
```gdscript
export(float) var width_ratio = 0.80   # 80% del ancho (era 66%)
```

### **Para Hacerlo Más Alto (más líneas):**
```gdscript
export(float) var height_ratio = 0.30  # 30% del alto (era 22%)
```

### **Para Estilo Game Boy Original:**
```gdscript
export(float) var width_ratio = 0.70   # Más ancho
export(int) var h_align = 0            # Alineado a la izquierda
export(int) var bottom_px = 8          # Más separación
```

### **Para Estilo Moderno Centrado:**
```gdscript
export(float) var width_ratio = 0.75   # Equilibrado
export(int) var h_align = 1            # Centrado
export(int) var bottom_px = 12         # Más espacio
```

---

## 📝 **Ejemplos de Configuración**

### **Configuración 1: Estilo Pokemon Red Original**
```gdscript
export(float) var width_ratio = 0.66
export(float) var height_ratio = 0.22
export(int) var h_align = 0        # Izquierda
export(int) var bottom_px = 6
```
**Resultado:** Diálogo angosto, alineado a la izquierda, 2 líneas

### **Configuración 2: Estilo Moderno Centrado**
```gdscript
export(float) var width_ratio = 0.75
export(float) var height_ratio = 0.25
export(int) var h_align = 1        # Centrado
export(int) var bottom_px = 10
```
**Resultado:** Diálogo más ancho, centrado, ligeramente más alto

### **Configuración 3: Diálogo Compacto**
```gdscript
export(float) var width_ratio = 0.60
export(float) var height_ratio = 0.20
export(int) var h_align = 1        # Centrado
export(int) var bottom_px = 8
```
**Resultado:** Diálogo pequeño y compacto, centrado

---

## 🛠️ **Implementación Técnica**

### **Archivos Involucrados:**

1. **`PlayArea.gd`** - Calcula área jugable
2. **`DialogBox.gd`** - Posiciona diálogo dentro del área
3. **`game.gd`** - Coordina el sistema

### **Flujo de Ejecución:**
```
1. game.gd encuentra TileMap
    ↓
2. PlayArea.set_from_tilemap(tm) calcula rect_screen
    ↓
3. DialogBox.refresh_layout() usa PlayArea.rect_screen
    ↓
4. Diálogo aparece centrado en área jugable
```

### **Debugging:**
Para ver valores en consola, busca estos prints:
```
=== PLAYAREA CALCULADA ===
Rect screen: (50, 30, 160, 144)

=== DIALOG LAYOUT (AREA JUGABLE) ===
Dialog position: (72, 137)
Dialog size: (105, 31)
```

---

## 🎯 **Puntos Clave**

- ✅ **Nunca usa viewport completo** - Solo área jugable
- ✅ **Respeta zoom y cámara** - Canvas transform automático
- ✅ **Proporcional al mapa** - Se adapta al tamaño del TileMap
- ✅ **Configurable fácilmente** - Variables export editables
- ✅ **Fallback seguro** - Si no hay PlayArea, usa viewport

---

## 🔄 **Recalculo Automático**

El sistema se actualiza automáticamente cuando:
- Cambia el tamaño de ventana
- Se carga un nuevo nivel
- Cambia el zoom de cámara

**No necesitas hacer nada manual** - el diálogo siempre queda bien posicionado.

---

## 📋 **Checklist de Configuración**

Para personalizar tu diálogo:

1. **Abrir `DialogBox.gd`**
2. **Modificar variables export al inicio del archivo**
3. **Guardar archivo**
4. **Ejecutar juego para ver cambios**
5. **Ajustar valores hasta obtener el resultado deseado**

**¡El diálogo se redimensiona automáticamente dentro del área jugable!**