import cv2
import numpy as np
import serial
import time

# Cambia COM6 por tu puerto
arduino = serial.Serial('COM6', 9600)
time.sleep(2)  # Esperar conexion

# Camara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # ROJO
    rojo_bajo = np.array([0,120,70])
    rojo_alto = np.array([10,255,255])
    mask_rojo = cv2.inRange(hsv, rojo_bajo, rojo_alto)

    # VERDE
    verde_bajo = np.array([40,40,40])
    verde_alto = np.array([80,255,255])
    mask_verde = cv2.inRange(hsv, verde_bajo, verde_alto)

    # Contar pixeles
    rojo = np.sum(mask_rojo)
    verde = np.sum(mask_verde)

    # Apagar (opcional enviar nada)

    if rojo > 500000:
        print("Detectado ROJO")
        arduino.write(b'R')
        cv2.putText(frame, "ROJO", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    elif verde > 500000:
        print("Detectado VERDE")
        arduino.write(b'V')
        cv2.putText(frame, "VERDE", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    # Mostrar camara
    cv2.imshow("Camara", frame)

    # Salir con ESC
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
