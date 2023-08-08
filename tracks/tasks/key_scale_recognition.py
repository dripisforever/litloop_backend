# ref https://stackoverflow.com/questions/14734644/algorithm-to-get-the-key-and-scale-from-musical-notes

import music21
from celery import shared_task


transcribed_to_midi = transcribe(track)


@shared_task
def scale_recognition(self,):
    score = music21.converter.parse('filename.mid')
    key = score.analyze('key')
    print(key.tonic.name, key.mode)

    key1 = score.analyze('Krumhansl')
    key2 = score.analyze('AardenEssen')
    
