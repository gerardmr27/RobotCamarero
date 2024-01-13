# RobotCamarero
Proyecto de robot camarero usando el turtlebot y una interfaz de usuario creada en Matlab App Designer

FICHEROS:
1. labmap.yaml: carga el fichero pgm del mapa
2. labmap1.pgm: mapa del laboratorio refinado
3. labmap.world: fichero del mapa para la simulación en stage
4. interfaz.mlapp: fichero de la interfaz de usuario
5. robot_camarero.py: fichero que crea el nodo de ROS para ejecutar el código

REQUISITOS:
1. Tener instalado Matlab junto con la librería de ROS
2. Tener instalado el simulador de turtlebot_stage
3. Tener instalado el map_server (únicamente si se va a probar en el turtlebot real)

INSTRUCCIONES PARA SIMULACIÓN:
- Descargar todos los ficheros de los mapas y el del nodo de ROS donde se tenga instalado ROS
- Descargar el fichero de la interfaz en Windows (aunque también se podría ejecutar desde Linux)
- Ejecutar el siguiente comando en Linux: roslaunch turtlebot_stage turtlebot_in_stage.launch map_file:=ruta_al_fichero_yaml world_file:=ruta_al_fichero_world
- Lanzar el turtlebot teleop
- Indicar donde se encuentra el robot utilizando el 2D Pose Estimate de RViZ y hacer girar al robot hasta que las partículas se concentren en un punto
- Cerrar el teleop
- Lanzar el fichero robot_camarero.py (python robot_camarero.py)
- Abrir el código de la interfaz y en propiedades cambiar la variable ipAdress por la de vuestro equipo en el que se está ejecutando ROS
- Ejecutar la interfaz, pulsar en conectar y esperar a que la luz se ponga en verde
- Escribir algún plato en cualquiera de los campos de texto de las mesas (simulan las comandas que se reciben) y pulsar en el botón de la mesa correspondiente. Una vez pulsado el robot comenzará a moverse hacia la mesa, esperará 15s para que los clientes recojan el plato y luego retornará al punto Home, situado en el pasillo

INSTRUCCIONES PARA EL TURTLEBOT REAL:
- Configurar las variables de entorno de ROS para conectarse al turtlebot
- Lanzar en una terminal del turtlebot los comandos: roslaunch turtlebot_bringup minimal.launch, roslaunch turtlebot_bringup hokuyo_ust10x.launch, roslaunch turtlebot_navigation amcl_demo.launch
- Lanzar en una terminal del usuario el comando_ rosrun map_server map_server labmap.yaml
- Lanzar RVIZ (rosrun rviz rviz) y añadir un mapa (topic /map) y un particle cloud (topic /particlecloud)
- Ejecutar en una terminal del robot el teleop y girar el robot hasta que las partículas se concentren en un punto
- Cerrar el teleop
- Abrir el código de la interfaz y modificar la variable ipAdress a la del turtlebot que se esté utilizando
- Ejecutar la interfaz, pulsar en conectar y esperar a que se ponga la luz en verde
- Escribir algún plato en cualquiera de los campos de texto de las mesas (simulan las comandas que se reciben) y pulsar en el botón de la mesa correspondiente. Una vez pulsado el robot comenzará a moverse hacia la mesa, esperará 15s (mientras emite sonido) para que los clientes recojan el plato y luego retornará al punto Home, situado en el pasillo
  
