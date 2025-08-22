# PlayArea.gd (Godot 3.5) - Singleton para área jugable
extends Node

var rect_screen = Rect2()  # Rect jugable en coordenadas de pantalla
var width  = 0
var height = 0
var origin = Vector2()  # top-left en pantalla

func _ready():
	add_to_group("play_area")

func set_from_tilemap(tm):
	if tm == null:
		rect_screen = Rect2()
		width = 0
		height = 0
		origin = Vector2()
		print("PlayArea: TileMap es null, usando valores vacíos")
		return

	var used = tm.get_used_rect()     # en celdas
	var cell = tm.cell_size

	# top-left y bottom-right en MUNDO (px)
	var world_tl = tm.to_global(Vector2(used.position.x * cell.x, used.position.y * cell.y))
	var world_br = tm.to_global(Vector2((used.position.x + used.size.x) * cell.x,
										(used.position.y + used.size.y) * cell.y))

	# transformar a PANTALLA (toma cámara/zoom/viewport)
	var ct = tm.get_viewport().get_canvas_transform()
	var screen_tl = ct.xform(world_tl)
	var screen_br = ct.xform(world_br)

	rect_screen = Rect2(screen_tl, screen_br - screen_tl)
	origin = rect_screen.position
	width  = rect_screen.size.x
	height = rect_screen.size.y
	
	print("=== PLAYAREA CALCULADA ===")
	print("Used rect (celdas): ", used)
	print("Cell size: ", cell)
	print("World TL: ", world_tl)
	print("World BR: ", world_br)
	print("Screen TL: ", screen_tl)
	print("Screen BR: ", screen_br)
	print("Rect screen: ", rect_screen)
	print("Origin: ", origin)
	print("Width x Height: ", width, " x ", height)
	print("============================")
