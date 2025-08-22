extends Node2D

export (PackedScene) var player
export (PackedScene) var nivel1

var current_tilemap = null  # Mantener referencia persistente

func _ready():
	var new_level = nivel1.instance()
	add_child(new_level)
	var new_player = player.instance()
	add_child(new_player)
	new_player.global_position = get_tree().get_nodes_in_group("spawn")[0].global_position

	# --- calcular el rect jugable en pantalla y refrescar el HUD
	current_tilemap = _find_tilemap_in(new_level)  # Guardar referencia
	var play_area = get_tree().get_nodes_in_group("play_area")
	if play_area.size() > 0:
		play_area[0].set_from_tilemap(current_tilemap)
	
	# Refrescar el DialogRoot si existe
	var dialog_root = get_node("UI/DialogRoot")
	if dialog_root and dialog_root.has_method("refresh_layout"):
		dialog_root.refresh_layout()
	else:
		print("ERROR: DialogRoot no encontrado o sin método refresh_layout")

	# si cambia tamaño de ventana, recalcular
	get_viewport().connect("size_changed", self, "_on_viewport_resized")

func _on_viewport_resized():
	# Usar la referencia guardada en lugar de buscar cada vez
	var play_area = get_tree().get_nodes_in_group("play_area")
	if play_area.size() > 0:
		play_area[0].set_from_tilemap(current_tilemap)
	
	var dialog_root = get_node("UI/DialogRoot")
	if dialog_root and dialog_root.has_method("refresh_layout"):
		dialog_root.refresh_layout()

func _find_tilemap_in(node):
	for c in node.get_children():
		if c is TileMap:
			return c
	return null


