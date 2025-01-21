import os
import time
import random
import datetime
import winsound
import subprocess as sub
import pyttsx3 as px
import pywhatkit
import pyautogui
import psutil
import wikipedia
import webbrowser as wb
from pathlib import Path
import speech_recognition as sr


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
        return r.recognize_google(audio, language="es-ES,en-US")
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
        speak("Claro! ¿Qué te gustaria buscar en Wikipedia?")
        query = takeVoice()
        speak("Buscando en Wikipedia...")
        result = wikipedia.summary(query, sentences=1)
        speak("Esto es lo que encontré:")
        print(result)
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
def search_chrome():
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


# Funcion para Reproducir Videos en YT
def search_videos():
    speak("Por supuesto ¿Qué te gustaria escuchar?")
    rec = takeVoice()
    music = rec.replace("reproduce" , "")
    print("Reproduciendo..." + music)
    pywhatkit.playonyt(music)


# Funcion de Alarma
def set_alarm():
    try:
        speak("Por favor, dime la hora para la alarma en formato de 24 horas.")
        alarm_time = takeVoice() 
        alarm_time = alarm_time.strip()
        
        if ":" not in alarm_time:
            speak("Formato de hora no válido. Asegúrate de usar el formato HH:MM.")
            return

        hour, minute = map(int, alarm_time.split(":")) 
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            speak("La hora ingresada no es válida. Por favor, inténtalo de nuevo.")
            return

        speak(f"Alarma configurada para las {hour}:{minute}. Te avisaré cuando sea el momento.")
        while True:
            now = datetime.datetime.now()
            if now.hour == hour and now.minute == minute:
                speak("Es hora. La alarma está sonando.")
                for _ in range(5):  
                    winsound.Beep(1000, 500) 
                break
            time.sleep(10)  
    except ValueError:
        speak("Hubo un error configurando la alarma. Inténtalo de nuevo.")


# Diccionario de Paginas 
sites = {
        'UNICAES' : "https://plataforma.catolica.edu.sv/login/index.php",
        'Google' : "https://www.google.com/",
        'Facebook' : "https://www.facebook.com/",
        'YouTube' : "https://www.youtube.com/"
}

# Funcion buscar abrir sitios web
def search_websites():
    speak("¿Que sitio web deseas que abra?")
    command = takeVoice()
    if not command:
        speak("No entendí el comando. Por favor, intenta nuevamente.")
        return
    
    for site in sites:
        if site in command:
            sub.call(f'start chrome.exe {sites[site]}', shell=True)
            speak(f"Abriendo {site}")
            break
    else:
        speak("No encontré un sitio correspondiente en la lista.")



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
        elif "recuerdes" in query:
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
        elif "reproduce" in query:
            search_videos()
        elif "alarma" in query:
            set_alarm()
        elif "abre" in query:
            search_websites()
        elif "repite" in query:
            speak("Ok di algo para repetir:")
            prueba = takeVoice()
            print(prueba)
            speak(prueba)
        elif "apagarse" in query:
            speak("Apagándome, hasta luego Gabriel.")
            quit()

