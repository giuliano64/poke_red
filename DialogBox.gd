extends Control

export(int) var max_lines_per_page := 2   # Pokémon clásico suele usar 2
export(float) var chars_per_sec := 60.0   # velocidad del efecto typewriter
onready var label := $Panel/Text
onready var next_icon := $Panel/NextIcon

var _pages := []
var _page_idx := 0
var _typing := false
var _type_timer := 0.0
var _typed_chars := 0
var _current_text := ""

func _ready():
	hide()
	if next_icon:
		next_icon.hide()
	label.bbcode_enabled = true
	label.autowrap_mode = RichTextLabel.AUTOWRAP_WORD_SMART
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
	label.bbcode_text = _current_text
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
	var target := int(_type_timer * chars_per_sec)
	if target > _typed_chars:
		_typed_chars = target
		label.visible_characters = clamp(_typed_chars, 0, label.get_total_character_count())
		if label.visible_characters >= label.get_total_character_count():
			_typing = false
			if next_icon:
				next_icon.show()

func _input(event):
	if not visible:
		return
	if event.is_action_pressed("ui_accept"):
		if _typing:
			# Si está escribiendo, completar texto inmediatamente
			_typing = false
			label.visible_characters = label.get_total_character_count()
			if next_icon:
				next_icon.show()
		else:
			# Avanzar a siguiente página
			_page_idx += 1
			_show_page(_page_idx)

func _paginate_text(full_text: String) -> Array:
	# Pagina por líneas reales renderizadas con autowrap.
	var pages := []
	var words := full_text.split(" ")
	var working := ""
	var last_good := ""
	label.bbcode_text = ""
	label.visible_characters = -1  # sin recorte, queremos medir

	for w in words:
		var probe := ""
		if working == "":
			probe = w
		else:
			probe = working + " " + w
		label.bbcode_text = probe
		var lines := label.get_line_count()
		if lines <= max_lines_per_page:
			working = probe
			last_good = probe
		else:
			pages.append(last_good.strip_edges())
			working = w
			last_good = w
			label.bbcode_text = working

	if working != "":
		pages.append(working.strip_edges())

	return pages