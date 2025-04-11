import cv2
import mediapipe as mp
import numpy as np

# Inicializamos MediaPipe para el seguimiento de manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)  # Permitimos reconocer hasta dos manos
mp_draw = mp.solutions.drawing_utils

# Definimos los objetos que vamos a usar (dos esferas y rectángulos)
# Esferas para los ojos
objects = {
    "left_eye": {"x": 250, "y": 150, "radius": 30, "dragging": False},  # Ojo izquierdo
    "right_eye": {"x": 390, "y": 150, "radius": 30, "dragging": False},  # Ojo derecho
    "mouth": {"x": 320, "y": 250, "width": 150, "height": 80, "dragging": False},  # Boca más grande
    "left_eyebrow": {"x": 230, "y": 100, "width": 120, "height": 20, "dragging": False},  # Cejas
    "right_eyebrow": {"x": 370, "y": 100, "width": 120, "height": 20, "dragging": False},  # Cejas
}

# Variable para saber qué objeto está siendo arrastrado
active_object = None

# Iniciamos la cámara
cap = cv2.VideoCapture(0)

# Función para verificar si se está haciendo el gesto de "agarrar"
def is_grabbing(thumb, index, w, h):
    thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h)
    index_x, index_y = int(index.x * w), int(index.y * h)

    # Calculamos la distancia entre los dedos pulgar e índice
    distance = np.hypot(index_x - thumb_x, index_y - thumb_y)
    
    # Hacemos que el umbral de "agarrar" dependa de la distancia relativa en la imagen
    grabbing_threshold = 50  # Umbral fijo para detectar el "agarrar"
    return distance < grabbing_threshold

# Función para verificar si los dedos están suficientemente separados (gesto de soltar)
def is_released(thumb, index, w, h):
    thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h)
    index_x, index_y = int(index.x * w), int(index.y * h)

    # Si los dedos están bastante separados
    distance = np.hypot(index_x - thumb_x, index_y - thumb_y)
    
    # Umbral de "soltar" más amplio
    release_threshold = 70
    return distance > release_threshold

while True:
    success, frame = cap.read()
    if not success:
        break
    
    frame = cv2.flip(frame, 1)  # Volteamos la imagen para una mejor experiencia
    h, w, _ = frame.shape  # Obtenemos las dimensiones del frame

    # Convertimos el frame a formato RGB, que es el que MediaPipe necesita
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    # Si se detectan manos en el frame
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            # Dibujamos las conexiones de la mano
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            # Extraemos las posiciones de los dedos pulgar e índice
            thumb = handLms.landmark[4]
            index = handLms.landmark[8]

            # Verificamos si se está haciendo el gesto de "agarrar"
            if is_grabbing(thumb, index, w, h):
                for obj_key in objects:
                    obj = objects[obj_key]
                    if active_object is None:  # Solo se puede agarrar un objeto si no hay uno activo
                        # Verificamos si el objeto es una esfera (ojo)
                        if obj_key == "left_eye" or obj_key == "right_eye":
                            distance = np.hypot(obj["x"] - int(thumb.x * w), obj["y"] - int(thumb.y * h))
                            if distance < obj["radius"]:  # Si la mano está cerca de la esfera
                                obj["dragging"] = True
                                active_object = obj_key  # Marcamos el objeto como activo
                        else:
                            # Verificamos si el objeto es un rectángulo (boca o ceja)
                            rect_center_x = obj["x"] + obj["width"] // 2
                            rect_center_y = obj["y"] + obj["height"] // 2
                            distance = np.hypot(rect_center_x - int(thumb.x * w), rect_center_y - int(thumb.y * h))
                            if distance < obj["width"] // 2:
                                obj["dragging"] = True
                                active_object = obj_key  # Marcamos el objeto como activo

            # Verificamos si se está haciendo el gesto de "soltar"
            if is_released(thumb, index, w, h):
                if active_object:
                    # Si el objeto está siendo arrastrado, lo soltamos
                    objects[active_object]["dragging"] = False
                    active_object = None  # Reiniciamos la variable del objeto activo

            # Si un objeto está siendo arrastrado, actualizamos su posición
            if active_object:
                obj = objects[active_object]
                obj["x"], obj["y"] = int(thumb.x * w), int(thumb.y * h)

    # Dibujamos los objetos en la pantalla
    for obj_key, obj in objects.items():
        if obj_key == "left_eye" or obj_key == "right_eye":
            # Dibujamos las esferas (ojos) con colores llamativos
            color = (255, 165, 0) if obj["dragging"] else (255, 0, 0)  # Naranja si está arrastrando, rojo si no
            cv2.circle(frame, (obj["x"], obj["y"]), obj["radius"], color, -1)
        elif obj_key == "mouth":
            # Dibujamos una boca sonriente más grande y nítida
            color = (255, 20, 147) if obj["dragging"] else (255, 105, 180)  # Deep Pink si está arrastrando, Hot Pink si no
            center = (obj["x"] + obj["width"] // 2, obj["y"] + obj["height"] // 2)
            axes = (obj["width"] // 2, obj["height"] // 2)
            angle = 0
            start_angle = 0
            end_angle = 180
            cv2.ellipse(frame, center, axes, angle, start_angle, end_angle, color, -1)
            # Añadimos un borde para mejorar la nitidez
            cv2.ellipse(frame, center, axes, angle, start_angle, end_angle, (255, 0, 0), 3)  # Borde azul
        elif obj_key == "left_eyebrow" or obj_key == "right_eyebrow":
            # Dibujamos los rectángulos para las cejas con colores brillantes
            color = (255, 69, 0) if obj["dragging"] else (255, 99, 71)  # Rojo anaranjado si está arrastrando, rojo si no
            cv2.rectangle(frame, (obj["x"], obj["y"]), (obj["x"] + obj["width"], obj["y"] + obj["height"]), color, -1)

    # Mostramos el frame con los objetos en pantalla
    cv2.imshow("Interacción con Manos - Cara", frame)
    
    # Si presionamos la tecla ESC, salimos del loop
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Cerramos la cámara y las ventanas cuando terminamos
cap.release()
cv2.destroyAllWindows()
