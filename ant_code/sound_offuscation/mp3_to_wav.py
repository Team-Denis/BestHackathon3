from pydub import AudioSegment

mp3_file = AudioSegment.from_mp3("ant_code/sound_offuscation/data/oppa_input.mp3")
wav_file = mp3_file.export("ant_code/sound_offuscation/data/oppa_input.wav", format="wav")
