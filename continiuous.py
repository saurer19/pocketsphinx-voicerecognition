import os
from pocketsphinx import LiveSpeech
from threading import Timer
import commands


class VoiceRecognition:
    def __init__(self,model_path):
        self.Speech = LiveSpeech(
            # verbose = True,
            sampling_rate = 16000,
            buffer_size=2048,
            hmm=os.path.join(model_path, 'en-us-adapt'),
            lm=os.path.join(model_path, 'new.lm.bin'),
            dic=os.path.join(model_path, 'new.dict'),
            # kws=os.path.join(model_path, 'kws.list')
            # keyphrase='computer', kws_threshold=1e-30
            jsgf= os.path.join(model_path,'test.gram')

        )
        self.HotKey= 'computer'
        self.Active = False
        self.Found = False

    def tssCommand(self, tss):
        os.system('echo "{0}" | festival --tts'.format(tss))
        print(tss)

    def commandFound(self, tss):
        self.tssCommand(tss)
        self.Found = True

    def commandList(self, phrase):
        if(phrase == commands.MASTER_LIGHTS_ON):
            self.commandFound("Turning master lights on")
        elif(phrase == commands.MASTER_LIGHTS_OFF):
            self.commandFound("Turning master lights off")
        elif(phrase == commands.TV_ON):
            self.commandFound("Turning TV ON")
        elif(phrase == commands.TV_OFF):
            self.commandFound("Turning TV OFF")       

    def reactivate(self, timeout):
        timeout.cancel()

    def activate(self):
        self.Active = True
        timeout = Timer(10.0, self.deactivate)
        timeout.start()
        self.tssCommand("I'm Listening...")

    def deactivate(self):
        self.Active = False
        self.Found = False
        self.tssCommand("I'm deactivated")

    def commandListener(self):
        pass

    def run(self):
        for phrase in self.Speech:
            p = str(phrase).lower()
            print("you said: " +p)
            if(self.Active):
                print('act')
                self.commandList(p)
            elif(p==self.HotKey):
                print('here')
                self.activate()
            print('end')
    
def main():
    script_dir = os.path.dirname(__file__)
    model_path = os.path.join(script_dir,'model/')
    voice = VoiceRecognition(model_path)
    voice.run()


if __name__ == '__main__':
    main()
