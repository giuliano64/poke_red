extends KinematicBody2D

var vel_actual = Vector2()
var vel_desp = 16

func _ready():
		  $animationPlayer.play("idle_up")

func _physics_process(delta):
	if(!$animationPlayer.is_playing()):
		if(Input.is_action_just_pressed("tecla_w")):
			vel_actual.y = -vel_desp*delta/$animationPlayer.get_animation("walk_up").length
			$animationPlayer.play("walk_up")
			$stick/Position.rotation_degrees = 0
		elif(Input.is_action_just_pressed("tecla_s")):
			vel_actual.y = vel_desp*delta/$animationPlayer.get_animation("walk_down").length
			$animationPlayer.play("walk_down")
			$stick/Position.rotation_degrees = 180
		elif(Input.is_action_just_pressed("tecla_a")):
			vel_actual.x = -vel_desp*delta/$animationPlayer.get_animation("walk_left").length
			$animationPlayer.play("walk_left")
			$stick/Position.rotation_degrees = 270
		elif(Input.is_action_just_pressed("tecla_d")):
			vel_actual.x = vel_desp*delta/$animationPlayer.get_animation("walk_right").length
			$animationPlayer.play("walk_right")
			$stick/Position.rotation_degrees = 90
	if($animationPlayer.is_playing()):
		var tilemap = get_tree().get_nodes_in_group("tile")[0]
		var adjusted_pos = global_position - tilemap.position
		var player_map_pos = tilemap.world_to_map(adjusted_pos)
		var n_tile = tilemap.get_cellv(player_map_pos)
		
		# Solo imprimir cuando hay un tile válido (para debug de mecánicas especiales)
		if n_tile != -1:
			print("Standing on special tile ID: ", n_tile, " at coords: ", player_map_pos)
		
		# Moverse siempre - las colisiones las manejan los StaticBody2D
		move_and_collide(vel_actual)

func _on_animationPlayer_animation_finished(anim_name):
	vel_actual = Vector2(0,0)
	var global_pos_x  = get_tree().get_nodes_in_group("spawn")[0].global_position.x
	var global_pos_y = get_tree().get_nodes_in_group("spawn")[0].global_position.y
	global_position = Vector2((round(round(global_position.x - global_pos_x)/vel_desp)*vel_desp)+global_pos_x,(round(round(global_position.y - global_pos_y)/vel_desp)*vel_desp)+global_pos_y)
