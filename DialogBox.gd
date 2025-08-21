extends Control

export(int) var max_lines_per_page = 2   # Pokémon clásico suele usar 2
export(float) var chars_per_sec = 60.0   # velocidad del efecto typewriter
# Dimensiones específicas del área jugable de Ash's room
export(int) var playable_width := 160   # -80 to +80
export(int) var playable_height := 112  # -40 to +72  
export(int) var dialog_height := 28     # Altura fija
export(int) var margin_px := 12         # Margen grande para estar completamente dentro
onready var label = $Panel/Text
onready var next_icon = $Panel/NextIcon
onready var panel := $Panel

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
	# Auto-layout proporcional al viewport
	_resize_to_viewport()
	get_viewport().connect("size_changed", self, "_resize_to_viewport")

func show_dialog(full_text: String) -> void:
	_pages = _paginate_text(full_text)
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
			if lines_in_page >= max_lines_per_page:
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
		if word_count >= words_per_line * max_lines_per_page:
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

func _resize_to_viewport():
	var vs := get_viewport_rect().size
	
	# EL CUARTO ESTÁ CENTRADO - USAR EL MÉTODO QUE FUNCIONABA
	var center_x = vs.x / 2
	var center_y = vs.y / 2
	
	# Área jugable centrada (160x112) 
	var playable_left = center_x - (playable_width / 2)
	var playable_top = center_y - (playable_height / 2)
	
	# Dimensiones del diálogo
	var dialog_w = playable_width - (margin_px * 2)
	var dialog_h = dialog_height
	
	# POSICIÓN FIJA AL PIE DEL ÁREA JUGABLE
	anchor_left = 0
	anchor_right = 0 
	anchor_top = 0
	anchor_bottom = 0
	
	rect_position.x = playable_left + margin_px
	rect_position.y = playable_top + playable_height - dialog_h - margin_px
	rect_size = Vector2(dialog_w, dialog_h)
	
	print("=== DEBUG CENTRADO ===")
	print("Viewport size: ", vs)
	print("Dialog position: ", rect_position)
	print("Dialog size: ", rect_size)
	print("======================")



