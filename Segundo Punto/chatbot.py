import serial
import time
import speech_recognition as sr
import sys
import unicodedata

SERIAL_PORT = 'COM3'  
BAUD_RATE = 9600

def normalize_text(text: str) -> str:
    # Quita tildes: "habitación" -> "habitacion"
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

def initialize_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
        time.sleep(2)  # Arduino se reinicia al abrir el puerto
        ser.reset_input_buffer()
        print(f"--- Conectado a Arduino en {SERIAL_PORT} ---")
        return ser
    except Exception as e:
        print(f"Error al conectar al puerto serial: {e}")
        return None

def send_command(ser, command):
    if not ser:
        return "Error: No hay conexión Serial."

    try:
        ser.reset_input_buffer()                 # limpia basura anterior
        ser.write((command + '\n').encode())
        ser.flush()
        time.sleep(0.1)                          # da tiempo a responder
        response = ser.readline().decode('utf-8', errors='ignore').strip()
        return response if response else "(sin respuesta del Arduino)"
    except Exception as e:
        return f"Error enviando comando: {e}"

def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nEscuchando... Di algo:")
        r.adjust_for_ambient_noise(source, duration=0.8)
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="es-ES")
        print(f"Dijiste: {text}")
        return normalize_text(text)
    except sr.UnknownValueError:
        print("No entendí lo que dijiste.")
        return ""
    except sr.RequestError as e:
        print(f"Error con el servicio de reconocimiento: {e}")
        return ""

def process_input(user_input, ser):
    user_input = normalize_text(user_input)

    if "encender" in user_input or "prender" in user_input or "enciende" in user_input or "prende" in user_input:
        if "sala" in user_input or "luz 1" in user_input or "primer" in user_input or "led1" in user_input:
            print(send_command(ser, "LED1_ON"))
        elif "habitacion" in user_input or "luz 2" in user_input or "segundo" in user_input or "led2" in user_input:
            print(send_command(ser, "LED2_ON"))
        elif "todas" in user_input or "luces" in user_input:
            print(send_command(ser, "LED1_ON"))
            print(send_command(ser, "LED2_ON"))
            print("OK: Todas las luces encendidas.")
        else:
            print("Robot: ¿Cuál luz? (sala / habitacion / todas)")

    elif "apagar" in user_input or "apaga" in user_input:
        if "sala" in user_input or "luz 1" in user_input or "primer" in user_input or "led1" in user_input:
            print(send_command(ser, "LED1_OFF"))
        elif "habitacion" in user_input or "luz 2" in user_input or "segundo" in user_input or "led2" in user_input:
            print(send_command(ser, "LED2_OFF"))
        elif "todas" in user_input or "luces" in user_input:
            print(send_command(ser, "LED1_OFF"))
            print(send_command(ser, "LED2_OFF"))
            print("OK: Todas las luces apagadas.")
        else:
            print("Robot: ¿Cuál luz? (sala / habitacion / todas)")

    elif "temperatura" in user_input or "cuantos grados" in user_input or "grados" in user_input:
        temp = send_command(ser, "GET_TEMP")
        print(f"Robot: La temperatura actual es de {temp}°C")

    elif "salir" in user_input or "chau" in user_input or "adios" in user_input:
        print("Robot: ¡Adiós!")
        return False

    else:
        print("Robot: No entendí el comando. Prueba: 'encender sala', 'apagar habitacion', 'temperatura'.")

    return True

def main():
    print("--- INGENIERO DE TELECOMUNICACIONES: Chatbot IoT v1.0 ---")
    print("IMPORTANTE: Cierra el Monitor Serial antes de usar este programa.\n")

    ser = initialize_serial()
    if not ser:
        print("Asegúrate de conectar el Arduino y configurar el puerto COM correcto.")
        sys.exit(1)

    running = True
    while running:
        print("\nSelecciona entrada: [1] Texto | [2] Voz | [3] Salir")
        choice = input("Opción: ")

        if choice == '1':
            user_input = input("Tú (Texto): ")
            running = process_input(user_input, ser)
        elif choice == '2':
            user_input = recognize_speech()
            if user_input:
                running = process_input(user_input, ser)
        elif choice == '3':
            running = False
        else:
            print("Opción no válida.")

    ser.close()

if __name__ == "__main__":
    main()