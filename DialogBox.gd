# DialogRoot.gd (Godot 3.5) - Usa SOLO el área jugable real
extends Control

export(float) var width_ratio  = 0.66    # % del ancho del cuarto
export(float) var height_ratio = 0.22    # % del alto del cuarto (2 líneas aprox)
export(int)   var margin_px    = 6       # margen lateral dentro del cuarto
export(int)   var bottom_px    = 6       # separación desde "piso" del cuarto
export(int)   var h_align      = 0       # 0=izq (GB), 1=centro, 2=dcha
export(int)   var padding_px   = 7       # padding interno
export(float) var chars_per_sec = 60.0  # velocidad del efecto typewriter

onready var label = $Panel/Text
onready var next_icon = $Panel/NextIcon
onready var panel = $Panel

var _pages = []
var _page_idx = 0
var _typing = false
var _type_timer = 0.0
var _typed_chars = 0
var _current_text = ""

func _ready():
	hide()
	if next_icon:
		next_icon.hide()
	# Configuración básica para Label
	label.autowrap = true
	label.valign = Label.VALIGN_TOP
	# Permitir que funcione cuando el juego está pausado
	pause_mode = Node.PAUSE_MODE_PROCESS
	# anclas absolutas
	anchor_left = 0; anchor_right = 0
	anchor_top  = 0; anchor_bottom = 0
	refresh_layout()
	# si no usas autorefresco desde game.gd, podrías conectar aquí size_changed
	
	# Actualizar posición cada frame si está visible
	set_process(true)

func refresh_layout():
	var rr = Rect2()
	var have_room = false
	
	# Acceder al singleton por grupo
	var play_area_nodes = get_tree().get_nodes_in_group("play_area")
	if play_area_nodes.size() > 0:
		var play_area = play_area_nodes[0]
		rr = play_area.rect_screen
		have_room = rr.size != Vector2()
	
	# fallback: si por algún motivo no hay room aún, usar visible rect
	var ref_rect = rr
	if not have_room:
		ref_rect = get_viewport().get_visible_rect()

	# dimensiones del cuadro en función del ROOM (no del viewport)
	var box_w = int(ref_rect.size.x * width_ratio)
	var box_h = int(ref_rect.size.y * height_ratio)

	# limitar ancho para no tocar paredes
	var max_w = int(ref_rect.size.x) - margin_px * 2
	box_w = min(box_w, max_w)

	# posicionar dentro del ROOM (X y Y)
	var pos_x = 0
	if h_align == 0:
		pos_x = ref_rect.position.x + margin_px
	elif h_align == 1:
		pos_x = ref_rect.position.x + int((ref_rect.size.x - box_w) / 2)
	else:
		pos_x = ref_rect.position.x + ref_rect.size.x - box_w - margin_px

	# OJO: Y anclado al borde INFERIOR del ROOM
	var pos_y = ref_rect.position.y + ref_rect.size.y - box_h - bottom_px

	rect_position = Vector2(pos_x, pos_y)
	rect_size     = Vector2(box_w, box_h)

	if panel:
		panel.anchor_left = 0; panel.anchor_top = 0
		panel.anchor_right = 1; panel.anchor_bottom = 1
		panel.margin_left = 0; panel.margin_top = 0
		panel.margin_right = 0; panel.margin_bottom = 0
	
	print("=== DIALOG LAYOUT (AREA JUGABLE) ===")
	print("PlayArea rect_screen: ", rr)
	print("Have room: ", have_room)
	print("Ref rect usado: ", ref_rect)
	print("Dialog position: ", rect_position)
	print("Dialog size: ", rect_size)
	print("====================================")

func show_dialog(full_text):
	# Recalcular posición ANTES de mostrar el diálogo
	refresh_layout()
	
	_pages = paginate_two_lines(full_text)
	print("=== DEBUG PAGINACION 2 LINEAS ===")
	print("Texto completo length: ", full_text.length())
	print("Número de páginas creadas: ", _pages.size())
	var i = 0
	while i < _pages.size():
		print("Página ", i, ": '", _pages[i], "'")
		i += 1
	print("=================================")
	_page_idx = 0
	_show_page(_page_idx)

func _show_page(idx: int) -> void:
	if idx >= _pages.size():
		hide()
		# Despausar el juego cuando termine el diálogo
		get_tree().paused = false
		return
	
	show()
	# Pausar el juego mientras hay diálogo
	get_tree().paused = true
	
	if next_icon:
		next_icon.hide()
	_current_text = _pages[idx]
	label.text = _current_text
	
	# Mostrar progreso de páginas en debug
	print("Mostrando página ", idx + 1, " de ", _pages.size())
	
	# preparar typewriter
	_typing = true
	_typed_chars = 0
	_type_timer = 0.0
	label.visible_characters = 0
	set_process(true)

func _process(delta: float) -> void:
	# Actualizar posición del diálogo si está visible
	if visible:
		refresh_layout()
	
	# Efecto typewriter
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

func _input(event):
	if not visible:
		return
	if (event.is_action_pressed("ui_accept") or event.is_action_pressed("tecla_x") or event.is_action_pressed("tecla_c")) and not event.is_echo():
		get_tree().set_input_as_handled()  # evita que suba al Player
		_advance_or_close()

func _advance_or_close():
	if _typing:
		# Si está escribiendo, completar texto inmediatamente
		_typing = false
		label.visible_characters = _current_text.length()
		if next_icon:
			next_icon.show()
	else:
		# Verificar si hay más páginas
		if _page_idx + 1 < _pages.size():
			# Avanzar a siguiente página
			_page_idx += 1
			_show_page(_page_idx)
		else:
			# Es la última página, cerrar diálogo
			hide()
			get_tree().paused = false

# PAGINADO FIJO EN EXACTAMENTE 2 LÍNEAS (GODOT 3.5)
func paginate_two_lines(full_text):
	var area = _get_text_area()
	var fnt = label.get_font("font")   # DynamicFont/BitmapFont
	var line_h = fnt.get_height()
	var char_w = max(1, fnt.get_string_size("M").x)

	var cols = max(4, int(floor(area.x / char_w)))
	var rows = 2  # ← exactamente 2 líneas por página

	var wrapped = _wrap_cols(full_text, cols)

	var pages = []
	var i = 0
	while i < wrapped.size():
		var page_text = wrapped[i]
		i += 1
		if i < wrapped.size():
			page_text += "\n" + wrapped[i]
			i += 1
		pages.append(page_text)
	return pages

func _get_text_area():
	var s = panel.rect_size
	return Vector2(
		max(0, s.x - padding_px * 2),
		max(0, s.y - padding_px * 2)
	)

func _wrap_cols(t, cols):
	var words = t.split(" ")
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
			if cur != "":
				lines.append(cur)
				cur = w
			else:
				# palabra más larga que cols → partir
				var rest = w
				while rest.length() > cols:
					lines.append(rest.substr(0, cols))
					rest = rest.substr(cols, rest.length() - cols)
				if rest != "":
					cur = rest
	if cur != "":
		lines.append(cur)
	return lines



