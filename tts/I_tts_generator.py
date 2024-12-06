from abc import ABC

class ITtsGenerator(ABC):
    """
    Interface for the TTS strategy pattern generator
    """

    def generate_tts(self, script:str, tema:str):
        """Generates a tts given a script and a topic

        Args:
            script (str): El script para procesar el tts
            tema (str): El tema sobre lo que se trata el script. Para ponerle nombre
        """
        pass