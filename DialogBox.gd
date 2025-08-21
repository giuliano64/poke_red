extends Control

export(int) var max_lines_per_page = 2   # Pokémon clásico suele usar 2
export(float) var chars_per_sec = 60.0   # velocidad del efecto typewriter
onready var label = $Panel/Text
onready var next_icon = $Panel/NextIcon

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

func show_dialog(full_text: String) -> void:
	_pages = _paginate_text(full_text)
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
	if event.is_action_pressed("ui_accept") or event.is_action_pressed("tecla_c"):
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
	# Pagina por líneas reales renderizadas con autowrap.
	# Paginación simple basada en palabras por línea
	var pages = []
	var words = full_text.split(" ")
	var words_per_line = 5  # Palabras por línea, más conservador
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
