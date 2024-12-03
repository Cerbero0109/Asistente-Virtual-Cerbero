import pyttsx3 as px
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb

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
        elif "apagarse" in query:
            speak("Apagándome, hasta luego Gabriel.")
            quit()
        elif "wikipedia" in query:
            query = query.replace("wikipedia", "").strip()
            if query:
                search_wikipedia(query)
            else:
                speak("Por favor, dime qué deseas buscar en Wikipedia.")
        elif "google" in query:
            search_chrome(query)


