extends Node2D

export (PackedScene) var player
export (PackedScene) var nivel1
func _ready():
	var new_level = nivel1.instance()
	add_child(new_level)
	var new_player = player.instance()
	add_child(new_player)
	new_player.global_position = get_tree().get_nodes_in_group("spawn")[0].global_position


