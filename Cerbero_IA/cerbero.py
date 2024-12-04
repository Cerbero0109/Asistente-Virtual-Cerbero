import pyttsx3 as px
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import pyautogui 
from pathlib import Path
import psutil
import random

# Configuración del motor de voz
engine = px.init()
voiceRate = 150
engine.setProperty('rate', voiceRate)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id) 

# Función para hablar
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Función para decir la hora
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    speak(f"La hora es: {current_time}")

# Función para decir la fecha
def tell_date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)

    months = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    speak("La fecha actual es:")
    speak(f"{day} de {months[month - 1]} del {year}")

# Función de saludo
def wishme():
    speak("Bienvenido Gabriel!")
    hour = datetime.datetime.now().hour

    if hour >= 6 and hour < 12:
        speak("Buenos días")
    elif hour >= 12 and hour < 18:
        speak("Buenas tardes")
    elif hour >= 18 and hour < 24:
        speak("Buenas noches")
    else:
        speak("Que tarde... ya es de madrugada")
    
    speak("Soy Cerbero, estoy a tu servicio. ¿Cómo puedo ayudarte?")

# Función para reconocer voz
def takeVoice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando el ruido ambiente...")
        r.adjust_for_ambient_noise(source)
        print("Escuchando...")
        audio = r.listen(source)
    
    try:
        print("Reconociendo...")
        return r.recognize_google(audio, language="es-ES")
    except sr.UnknownValueError:
        speak("No pude entender el audio. Por favor intenta de nuevo.")
        return None
    except sr.RequestError as e:
        speak(f"Hubo un error con el servicio de Google: {e}")
        return None

# Función para buscar en Wikipedia
def search_wikipedia(query):
    wikipedia.set_lang("es")  
    try:
        speak("Buscando en Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak("Esto es lo que encontré:")
        speak(result)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("El término es ambiguo. Intenta ser más específico.")
        options = ", ".join(e.options[:5]) 
        speak(f"Algunas opciones son: {options}")
    except wikipedia.exceptions.PageError:
        speak("No encontré información sobre eso. Asegúrate de que el término sea correcto.")
    except Exception as e:
        speak(f"Hubo un problema al conectarse a Wikipedia: {e}")


# Funcion para buscar en Google Chrome
def search_chrome(query):
    try:
        speak("¿Qué te gustaría buscar?")
        search_query = takeVoice()
        if search_query:
            url = f"https://www.google.com/search?q={search_query}"
            wb.open_new_tab(url)
            speak(f"Esto es lo que encontré sobre {search_query}")
        else:
            speak("No escuché nada. Por favor intenta de nuevo.")
    except Exception as e:
        speak(f"Hubo un error al abrir Google: {e}")

# Funcion Guardar Recuerdos
def remeber_that(query):
    speak("¿Qué quisieras que recordara?")
    data = takeVoice()
    speak("Me dijiste que recordara" + data)
    remeber = open("data.txt", "w")
    remeber.write(data)
    remeber.close()

# Funcion Decir Recuerdos
def tell_remeber():
    remeber = open("data.txt", "r")
    speak("Me dijiste lo siguiente: " + remeber.read())

# Funcion para tomar captura de pantalla 
def save_screenshot(img):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = Path(f"C:/Users/gglem/OneDrive/Escritorio/Cerbero_IA/capturas/ss_{timestamp}.png")
    img.save(path)
    print(f"Captura guardada en: {path}")

import psutil

# Función para ver el estado de la PC
def pc_status():
    usage = str(psutil.cpu_percent(interval=1)) 
    speak("El CPU está en uso al: " + usage + " por ciento")
    
    battery = psutil.sensors_battery()
    if battery:
        speak(f"La batería está al {battery.percent} por ciento")
        if battery.power_plugged:
            speak("El equipo está conectado a la corriente")
        else:
            speak("El equipo no está conectado a la corriente")
    else:
        speak("No se detectó batería en este dispositivo")

# Funcion para contar chistes
def tell_joke():
    jokes = [
        "¿Por qué no hay chistes de computadoras? Porque se cuelgan.",
        "¿Qué le dice un jardinero a otro? ¡Disfrutemos mientras podamos!",
        "¿Cómo se despiden los químicos? ¡Ácido un placer!",
        "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!",
        "¿Por qué el libro de matemáticas estaba triste? Porque tenía demasiados problemas.",
        "¿Qué le dijo una impresora a otra? ¿Esa hoja es tuya o es una impresión mía?",
        "¿Por qué los pájaros no usan Facebook? Porque ya tienen Twitter.",
        "¿Qué hace un perro con un taladro? ¡Taladrando!",
        "¿Qué le dijo una pared a otra? ¡Nos vemos en la esquina!",
        "¿Qué hace un pez en el gimnasio? Nada.",
        "¿Cómo se llama un boomerang que no vuelve? ¡Un palo!",
        "¿Qué hace un café en el gimnasio? Se pone espresso.",
        "¿Qué le dice un semáforo a otro? No me mires, me estoy cambiando.",
        "¿Qué hace una vaca estudiando? ¡Saca leche-datos!",
        "¿Por qué las gallinas no usan celular? Porque tienen miedo de los pollos entrantes.",
        "¿Qué hace un leñador en el gimnasio? ¡Madera de campeón!",
        "¿Cómo se llama un dinosaurio dormilón? ¡Dino-sueño!",
        "¿Por qué los gatos no juegan a las cartas? Porque temen a las trampas.",
        "¿Qué le dice un cubo a otro cubo? Nos vemos en la esquina.",
        "¿Cómo se despide una tostada? ¡Hasta el pan, hermano!"
    ]
    joke = random.choice(jokes)
    speak(joke)

# Main
if __name__ == "__main__":
    wishme()

    while True:
        query = takeVoice()
        if not query:
            continue
        query = query.lower()
        print(f"Comando reconocido: {query}")
        
        if "hora" in query:
            tell_time()
        elif "fecha" in query:
            tell_date()
        elif "wikipedia" in query:
            query = query.replace("wikipedia", "").strip()
            if query:
                search_wikipedia(query)
            else:
                speak("Por favor, dime qué deseas buscar en Wikipedia.")
        elif "google" in query:
            search_chrome(query)
        elif "recuerda" in query:
            remeber_that(query)
        elif "recuerdo" in query:
            tell_remeber()
        elif "captura de pantalla" in query:
            img = pyautogui.screenshot()
            save_screenshot(img)
            speak("Listo!")
        elif "estado cpu" in query:
            pc_status()
        elif "chiste" in query:
            tell_joke()
        elif "apagarse" in query:
            speak("Apagándome, hasta luego Gabriel.")
            quit()
