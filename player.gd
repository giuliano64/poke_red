extends KinematicBody2D

var vel_actual = Vector2()
var vel_desp = 16
var dialog_scene = preload("res://scenes/Dialogo.tscn")
var current_dialog = null
var can_interact := true  # supresor contra re-abrir en el mismo apretón

func _ready():
	$animationPlayer.play("idle_up")

func _physics_process(delta):
	# No procesar input si el juego está pausado (por diálogos)
	if get_tree().paused:
		return
		
	# Manejo de interacciones solo si no hay dialogo activo y el juego no está pausado
	if can_interact and current_dialog == null and not get_tree().paused and Input.is_action_just_pressed("tecla_x"):
		print("Tecla X presionada - iniciando check_interaction")
		print("Posición del player: ", global_position)
		print("Stick rotation: ", $stick/Position.rotation_degrees)
		check_interaction()
		can_interact = false  # bloquea re-abrir hasta soltar
	
	# cuando el diálogo no está abierto, re-habilitar sólo tras soltar
	if current_dialog == null and not get_tree().paused and Input.is_action_just_released("tecla_x"):
		can_interact = true
	
	if(!$animationPlayer.is_playing() and current_dialog == null):
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

func check_interaction():
	# Verificar interacción desde la posición del player y la casilla enfrente
	var player_position = global_position
	var interaction_position = get_interaction_position()
	var interaction_found = false
	
	print("Posición del player: ", player_position)
	print("Posición de interacción calculada: ", interaction_position)
	
	# Obtener referencia al nivel
	var nivel = get_tree().get_nodes_in_group("tile")[0]
	if nivel == null:
		print("No se encontró nivel en el grupo 'tile'")
		return
	
	# Posiciones de objetos (ajustadas por offset del TileMap)
	var pc_pos = Vector2(-45, -18)  # -19 + 1 por el offset del TileMap
	var tv1_pos = Vector2(-9, 26)   # 25 + 1 por el offset del TileMap
	var tv2_pos = Vector2(-9, 39)   # 38 + 1 por el offset del TileMap
	
	# Verificar interacción con PC desde player o posición de interacción
	var pc_distance_player = player_position.distance_to(pc_pos)
	var pc_distance_interaction = interaction_position.distance_to(pc_pos)
	print("PC - Distancia desde player: ", pc_distance_player, " - Desde interacción: ", pc_distance_interaction)
	
	# Verificar interacción con TV/consola
	var tv1_distance_player = player_position.distance_to(tv1_pos)
	var tv1_distance_interaction = interaction_position.distance_to(tv1_pos)
	var tv2_distance_player = player_position.distance_to(tv2_pos)
	var tv2_distance_interaction = interaction_position.distance_to(tv2_pos)
	print("TV1 - Player: ", tv1_distance_player, " - Interacción: ", tv1_distance_interaction)
	print("TV2 - Player: ", tv2_distance_player, " - Interacción: ", tv2_distance_interaction)
	
	# Verificar cuál objeto está más cerca y solo interactuar con ese
	var pc_distance_min = min(pc_distance_player, pc_distance_interaction)
	var tv1_distance_min = min(tv1_distance_player, tv1_distance_interaction)
	var tv2_distance_min = min(tv2_distance_player, tv2_distance_interaction)
	
	print("Distancias mínimas - PC: ", pc_distance_min, " TV1: ", tv1_distance_min, " TV2: ", tv2_distance_min)
	
	# Priorizar PC sobre TV si ambos están en rango
	if pc_distance_min <= 50:
		print("¡PC detectado!")
		show_dialog("Encendiste la PC. Es una máquina increíblemente poderosa que te permitirá gestionar completamente tu equipo Pokemon. En el futuro podrás almacenar todos tus Pokemon capturados aquí. También podrás acceder al sistema de almacenamiento Pokemon que conecta con el Centro Pokemon. Esta será tu herramienta más importante para organizar tu aventura.")
		interaction_found = true
	elif tv1_distance_min <= 45 or tv2_distance_min <= 60:
		print("¡TV/Consola detectada!")
		show_dialog("En la televisión hay un programa muy interesante sobre un joven entrenador que está comenzando su aventura Pokemon. Está explorando diferentes regiones y capturando Pokemon increíbles. Pero mejor sigues tu propio camino hacia la grandeza.")
		interaction_found = true
	
	if interaction_found:
		print("Interacción detectada")
	else:
		print("No se detectó interacción cerca")

func get_interaction_position():
	# Obtener posición frente al player basado en la dirección que está mirando
	var direction = Vector2()
	
	# Determinar dirección basada en la rotación del stick
	var stick_rotation = $stick/Position.rotation_degrees
	if stick_rotation == 0:      # Mirando arriba
		direction = Vector2(0, -16)
	elif stick_rotation == 90:   # Mirando derecha
		direction = Vector2(16, 0)
	elif stick_rotation == 180: # Mirando abajo
		direction = Vector2(0, 16)
	elif stick_rotation == 270: # Mirando izquierda
		direction = Vector2(-16, 0)
	else: # Default mirando abajo si no hay dirección clara
		direction = Vector2(0, 16)
	
	return global_position + direction

func is_near_position(pos1: Vector2, pos2: Vector2, threshold: float) -> bool:
	return pos1.distance_to(pos2) <= threshold

func show_dialog(text: String):
	print("=== MOSTRANDO DIALOGO CON SISTEMA POKEMON ===")
	print("Texto: ", text)
	
	# Acceder al nuevo DialogRoot en CanvasLayer
	var dialog_root = get_tree().get_root().get_node("main/UI/DialogRoot")
	if dialog_root == null:
		print("ERROR: No se encontró DialogRoot")
		return
	
	print("Llamando show_dialog en DialogRoot...")
	dialog_root.show_dialog(text)
	print("Diálogo mostrado con sistema Pokemon Red")

func _on_dialog_closed():
	current_dialog = null
	get_tree().paused = false
