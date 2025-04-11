# 🖐️ Mini Proyecto: Arrastrar y Soltar con Seguimiento de Manos

Este proyecto permite mover objetos virtuales en pantalla usando gestos con la mano, capturados en tiempo real con la cámara web. Se utiliza Python, OpenCV y MediaPipe para detectar la mano y permitir que el usuario "agarre", mueva y "suelte" elementos en pantalla de forma intuitiva.

---

###  Tecnologías
- Python 3
- OpenCV
- MediaPipe
- Git + GitHub

---

### ¿Cómo funciona?

1. **Captura de video:** El proyecto utiliza OpenCV para capturar el video de la cámara web en tiempo real.
2. **Detección de mano:** Se usa MediaPipe para identificar los puntos clave de la mano (landmarks). MediaPipe realiza el seguimiento de la mano a través de estos puntos, permitiendo la detección precisa de la posición de la mano y los dedos.
3. **Detección de gesto de agarre:** Al detectar la proximidad entre los dedos índice y pulgar (usando las coordenadas de los puntos clave), se interpreta que el usuario está "agarrando" el objeto.
4. **Arrastrar el objeto:** Mientras los dedos estén cerca, el objeto virtual sigue el movimiento de la mano, manteniéndose pegado al puntero de la mano.
5. **Soltar:** Cuando los dedos se separan, el objeto se queda en su nueva posición en la pantalla.

Este sistema simula un entorno interactivo, en el que no es necesario usar un mouse ni dispositivos adicionales, solo la mano frente a la cámara.

---

### 

El código principal se encuentra en el archivo `arrastrar_soltar.py`, que contiene la lógica para:

- **Configuración de la cámara:** Usamos OpenCV para acceder a la cámara web y mostrar el video en tiempo real.
- **Detección de manos con MediaPipe:** Utilizamos el modelo de detección de manos de MediaPipe para localizar los landmarks de la mano en la imagen capturada por la cámara.
- **Cálculo de distancia entre dedos:** Calculamos la distancia entre el dedo índice y el pulgar para determinar si están lo suficientemente cerca como para "agarrar" el objeto.
- **Movimiento del objeto:** Si el gesto de agarre es detectado, el objeto en pantalla se mueve con el seguimiento de la mano.
- **Interfaz gráfica (opcional):** Puedes integrar una interfaz gráfica usando Tkinter (si se prefiere) para una mayor interacción.

---

### 🎥 Video de demostración
👉 https://drive.google.com/file/d/1rXMHPBBMTZBYkMrh22B3rLzxSzq063CN/view?usp=sharing

