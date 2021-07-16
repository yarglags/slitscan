from subprocess import check_output
import json

### Get Video Data ###

def getData(vid):
    cmd = 'ffprobe -i '
    cmd += vid
    cmd += ' -v error -show_entries stream -of json'
    print (cmd)
    a = check_output(cmd, shell=True).decode()
    return (a)

sourceVid = 'vid.mp4'

vidData = json.loads(getData(sourceVid))

if vidData['streams'][0]['codec_type'] == 'video':
    audio = 1
    video = 0

width = vidData['streams'][video]['width']
print ('Video Width:\t',width, 'px')
height = vidData['streams'][video]['height']
print ('Video Height:\t',height, 'px')
frames = int(vidData['streams'][video]['nb_frames'])
print ('Total Frames:\t',frames)
duration = float(vidData['streams'][video]['duration'])
print ('Video Duration:\t',duration, 's')
frameRate = (vidData['streams'][video]['r_frame_rate']) # avg_frame_rate
frameRate = int(frameRate.split('/')[video]) / int(frameRate.split('/')[audio])
#frameRate = int(frameRate)
print ('Frame Rate:\t',frameRate, 'f/s')
audDuration = float(vidData['streams'][1]['duration'])
print ('Audio Duration:\t',audDuration, 's')


### Convert the video into sliced images ###

def vidSlice(sourceVid, start, end, step, width, frames):
    startTime = 0.0 # seconds
    duration = 9.5  # seconds 
    if frames % 2 != 0:
        frames += 1 # round up frames to an even number
    end *= 2
    
    picNo = 0
    for frameNo in range(start, end, step):
        cmd = 'ffmpeg -y -ss ' + str(startTime)
        cmd += ' -i ' + sourceVid
        cmd += ' -t ' + str(duration)
        cmd += ' -an -vf "crop=2:'
        cmd += '1280'
        cmd += ':'
        cmd += str(frameNo)
        cmd += ':0, tile='
        cmd += str(frames)
        cmd += 'x1" '
        cmd += ('0000' + str(picNo))[-4:]
        cmd += '.bmp' # tile=1024x1, hflip

        cmd = cmd.replace('|width|', str(width))

        picNo += 1
        print(int(frameNo/step)+1, 'of', int(end/step), cmd)
        a = check_output(cmd, shell=True).decode()

start = 0
end = int(int(height)/ 2)+ int(start/2) # frames
step = 2
vidSlice(sourceVid, start, end, step, width, frames) # width
