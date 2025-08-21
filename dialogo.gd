extends Node2D

var is_dialog_active = false

onready var bkg_txt = $bkg_txt
onready var txt = $txt

func _ready():
	hide_dialog()
	# Posicionar relativo al player y área de juego
	position = Vector2(0, 0)  # Se ajustará dinámicamente

func show_dialog(text: String):
	print("=== MOSTRANDO DIALOGO CON SPRITE ORIGINAL ===")
	print("Texto: ", text)
	
	is_dialog_active = true
	
	# Configurar texto
	txt.text = text.replace("\\n", "\n")
	
	# Mostrar elementos usando el mismo patrón que la referencia
	bkg_txt.visible = true
	txt.visible = true
	visible = true
	
	print("Sprite y texto visibles")
	
	# Pausar juego
	get_tree().paused = true
	pause_mode = Node.PAUSE_MODE_PROCESS

func hide_dialog():
	print("=== OCULTANDO DIALOGO ===")
	is_dialog_active = false
	bkg_txt.visible = false
	txt.visible = false
	visible = false
	get_tree().paused = false

func _input(event):
	if is_dialog_active and visible:
		if Input.is_action_just_pressed("tecla_x") or Input.is_action_just_pressed("tecla_c"):
			print("Cerrando diálogo por input")
			hide_dialog()
