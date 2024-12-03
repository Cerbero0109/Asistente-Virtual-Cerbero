import pyttsx3 as px

engine = px.init()
voiceRate = 150
engine.setProperty('rate', voiceRate)

# Obtener todas las voces disponibles de nuestra PC
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id) 

# Función para hablar
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Probar la voz
speak("Hola, soy Cerbero y esta es mi primera prueba para hablar en español.")
