import os
import winsound

from .types import SoundType


class Player:
    _folder_path = "sounds"

    _names = {
        SoundType.Failure: "failure.wav",
        SoundType.Move: "move.wav",
        SoundType.Success: "success.wav",
    }

    @classmethod
    def play(cls, sound_type: SoundType):
        if not cls._names.get(sound_type):
            return

        base_dir = os.path.dirname(__file__)
        file_name = os.path.join(base_dir, cls._folder_path, cls._names[sound_type])
        winsound.PlaySound(file_name, winsound.SND_ASYNC)
