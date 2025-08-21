extends Control

export(int) var min_rows = 2
export(float) var chars_per_sec = 60.0   # velocidad del efecto typewriter
export(int) var padding_px = 6
# Tamaño del área jugable lógica
export(int) var playable_width = 160
export(int) var playable_height = 112
# Altura del cuadro como % del alto jugable
export(float) var height_ratio = 0.30
# Margen lateral/inferior
export(int) var margin_px = 4
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
	# Auto-layout basado en área jugable real
	_resize_to_playable()
	get_viewport().connect("size_changed", self, "_resize_to_playable")

func show_dialog(full_text: String) -> void:
	_pages = _paginate_text_exact(full_text)
	print("=== DEBUG PAGINACION ===")
	print("Texto completo length: ", full_text.length())
	print("Número de páginas creadas: ", _pages.size())
	for i in range(_pages.size()):
		print("Página ", i, ": '", _pages[i], "'")
	print("========================")
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

func _paginate_text(full_text: String) -> Array:
	# Paginación basada en caracteres por línea y líneas máximas
	var pages = []
	var words = full_text.split(" ")
	var current_page = ""
	var current_line = ""
	var lines_in_page = 0
	var chars_per_line = _estimate_chars_per_line()
	
	for word in words:
		var test_line = current_line
		if test_line != "":
			test_line += " "
		test_line += word
		
		# Si la línea se pasa del límite de caracteres
		if test_line.length() > chars_per_line:
			# Añadir la línea actual a la página y empezar nueva línea
			if current_page != "":
				current_page += "\n"
			current_page += current_line
			lines_in_page += 1
			
			# Si ya llegamos al máximo de líneas, crear nueva página
			if lines_in_page >= min_rows:
				pages.append(current_page.strip_edges())
				current_page = ""
				lines_in_page = 0
			
			current_line = word  # La palabra que no cabía empieza la nueva línea
		else:
			current_line = test_line  # La palabra cabe en la línea actual
	
	# Añadir la última línea a la página actual
	if current_line != "":
		if current_page != "":
			current_page += "\n"
		current_page += current_line
	
	# Añadir la última página si tiene contenido
	if current_page != "":
		pages.append(current_page.strip_edges())
	
	return pages

func _estimate_chars_per_line() -> int:
	# Calcular caracteres basado en el área jugable menos márgenes
	var dialog_width = playable_width - (margin_px * 2)  # Ancho total del diálogo
	var text_width = dialog_width - 16  # Menos márgenes internos del NinePatchRect
	var font_width_approx = 5  # Ancho por carácter con fuente Pokemon de 8px (más preciso)
	var chars = int(text_width / font_width_approx)
	
	print("=== CHARS PER LINE DEBUG ===")
	print("Playable width: ", playable_width)
	print("Dialog width: ", dialog_width)
	print("Text width: ", text_width) 
	print("Calculated chars per line: ", chars)
	print("===========================")
	
	return int(max(chars, 20))  # Usar todo el ancho disponible, mínimo 20

func _paginate_text_fallback(full_text: String) -> Array:
	# Fallback: paginación por palabras (más conservadora)
	var pages = []
	var words = full_text.split(" ")
	var words_per_line = 4  # Más conservador
	var current_page = ""
	var word_count = 0
	
	for word in words:
		if word_count >= words_per_line * min_rows:
			pages.append(current_page.strip_edges())
			current_page = word
			word_count = 1
		else:
			if current_page == "":
				current_page = word
			else:
				current_page += " " + word
			word_count += 1
	
	if current_page != "":
		pages.append(current_page.strip_edges())
	
	return pages

func _resize_to_playable():
	var vr = get_viewport().get_visible_rect()
	var center = vr.position + vr.size * 0.5
	var playable_pos = center - Vector2(playable_width, playable_height) * 0.5
	var playable_rect = Rect2(playable_pos, Vector2(playable_width, playable_height))

	var dialog_h = int(playable_rect.size.y * height_ratio)
	var dialog_w = int(playable_rect.size.x) - margin_px * 2

	anchor_left = 0
	anchor_right = 0
	anchor_top = 0
	anchor_bottom = 0

	rect_position = Vector2(
		playable_rect.position.x + margin_px,
		playable_rect.position.y + playable_rect.size.y - dialog_h - margin_px
	)
	rect_size = Vector2(dialog_w, dialog_h)

	if panel:
		panel.anchor_left = 0
		panel.anchor_top = 0
		panel.anchor_right = 1
		panel.anchor_bottom = 1
		panel.margin_left = 0
		panel.margin_top = 0
		panel.margin_right = 0
		panel.margin_bottom = 0

	print("=== DEBUG PLAYABLE AREA ===")
	print("Visible rect: ", vr)
	print("Playable rect: ", playable_rect)
	print("Dialog position: ", rect_position)
	print("Dialog size: ", rect_size)
	print("=============================")

func _paginate_text_exact(full_text: String) -> Array:
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
		var page_text = ""
		for j in range(page_lines.size()):
			if j > 0:
				page_text += "\n"
			page_text += page_lines[j]
		pages.append(page_text)
	return pages

func _get_text_area_size() -> Vector2:
	var size = panel.rect_size
	return Vector2(
		max(0, size.x - padding_px * 2),
		max(0, size.y - padding_px * 2)
	)

func _word_wrap_to_cols(text: String, cols: int) -> PoolStringArray:
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



