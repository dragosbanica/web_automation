import pyaudio
import wave


filename= "output.wav"
sound  = True

#set the chunk size of 1024 samples
CHUNK = 1024

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = 2,
                frames_per_buffer=CHUNK)

print('Recording...')
frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
 
print('Finished recording.')

#stop and close stream
stream.stop_stream()
stream.close()

#terminate pyaudio object
p.terminate()

#save audio file
#open the file in 'write bytes' modes
wf = wave.open(filename, 'wb')

#set the channels
wf.setnchannels(CHANNELS)

#set the sample format
wf.setsampwidth(p.get_sample_size(FORMAT))

#set the sample rate
wf.setframerate(RATE)

# write the frames as bytes
wf.writeframes(b''.join(frames))

# close the file
wf.close()
