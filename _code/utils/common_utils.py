from playsound import playsound
from pathlib import Path

class Notifier:
    def __init__(self) -> None:
        pass
    def done(self):
        try : 
            playsound('./assets/audio/done.wav')
        except Exception as e:
            print(e)    