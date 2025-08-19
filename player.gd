extends KinematicBody2D

var vel_actual = Vector2()
var vel_desp = 16

func _ready():
	$animationPlayer.play("idle_up")

func _physics_process(delta):
	if(!$animationPlayer.is_playing()):
		# Resetear velocidad al inicio de cada frame
		vel_actual = Vector2(0, 0)
		
		if(Input.is_action_just_pressed("tecla_w")):
			# Probar movimiento antes de ejecutar
			var test_vel = Vector2(0, -vel_desp*delta/$animationPlayer.get_animation("walk_up").length)
			var collision = move_and_collide(test_vel, true, true, true)
			if not collision:
				vel_actual = test_vel
				$animationPlayer.play("walk_up")
				$stick/Position.rotation_degrees = 0
			else:
				print("Colisión detectada arriba - player se queda en posición")
				vel_actual = Vector2(0, 0)
		elif(Input.is_action_just_pressed("tecla_s")):
			var test_vel = Vector2(0, vel_desp*delta/$animationPlayer.get_animation("walk_down").length)
			var collision = move_and_collide(test_vel, true, true, true)
			if not collision:
				vel_actual = test_vel
				$animationPlayer.play("walk_down")
				$stick/Position.rotation_degrees = 180
			else:
				print("Colisión detectada abajo - player se queda en posición")
				vel_actual = Vector2(0, 0)
		elif(Input.is_action_just_pressed("tecla_a")):
			var test_vel = Vector2(-vel_desp*delta/$animationPlayer.get_animation("walk_left").length, 0)
			var collision = move_and_collide(test_vel, true, true, true)
			if not collision:
				vel_actual = test_vel
				$animationPlayer.play("walk_left")
				$stick/Position.rotation_degrees = 270
			else:
				print("Colisión detectada izquierda - player se queda en posición")
				vel_actual = Vector2(0, 0)
		elif(Input.is_action_just_pressed("tecla_d")):
			var test_vel = Vector2(vel_desp*delta/$animationPlayer.get_animation("walk_right").length, 0)
			var collision = move_and_collide(test_vel, true, true, true)
			if not collision:
				vel_actual = test_vel
				$animationPlayer.play("walk_right")
				$stick/Position.rotation_degrees = 90
			else:
				print("Colisión detectada derecha - player se queda en posición")
				vel_actual = Vector2(0, 0)
	
	if($animationPlayer.is_playing()):
		# Solo moverse si hay velocidad válida
		if vel_actual != Vector2(0, 0):
			var collision = move_and_collide(vel_actual)
			if collision:
				# Si colisiona durante el movimiento, detener animación
				$animationPlayer.stop()
				vel_actual = Vector2(0, 0)
				print("Colisión durante movimiento - deteniendo player")

func _on_animationPlayer_animation_finished(anim_name):
	vel_actual = Vector2(0,0)
	
	# Guardar posición actual antes del snap
	var previous_position = global_position
	
	# Calcular posición snapped
	var global_pos_x = get_tree().get_nodes_in_group("spawn")[0].global_position.x
	var global_pos_y = get_tree().get_nodes_in_group("spawn")[0].global_position.y
	var snapped_position = Vector2((round(round(global_position.x - global_pos_x)/vel_desp)*vel_desp)+global_pos_x,(round(round(global_position.y - global_pos_y)/vel_desp)*vel_desp)+global_pos_y)
	
	# Probar si la posición snapped es segura
	var test_collision = move_and_collide(snapped_position - global_position, true, true, true)
	
	if not test_collision:
		# Posición snapped es segura
		global_position = snapped_position
		print("Player snapped to: ", global_position)
	else:
		# Posición snapped causaría colisión, mantener posición actual
		global_position = previous_position
		print("Snap cancelado - mantener en: ", global_position)
