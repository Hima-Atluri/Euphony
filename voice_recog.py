import speech_recognition as sr
import pyttsx3 
def voice_recognizer():  
    # Initialize the recognizer 
    r = sr.Recognizer()
    
    # Loop infinitely for user to speak
    while(1):    
        try:    
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                  
                # wait for a second to let the recognizer adjust the energy threshold based on the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
                  
                #listens for the user's input 
                audio2 = r.listen(source2)
                  
                # Using ggogle to recognize audio
                MyText = r.recognize_google(audio2)
                #print(MyText)
                return MyText
                  
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
              
        except sr.UnknownValueError:
            print("unknown error occured")
