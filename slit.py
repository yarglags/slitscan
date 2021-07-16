from subprocess import check_output
import json

def getData(vid):
    cmd = 'ffprobe -i |infile| -v error -show_entries stream -of json'
    cmd = cmd.replace('|infile|', vid)
    print (cmd)
    a = check_output(cmd, shell=True).decode()
    return (a)


def vidSlice(sourceVid, start, end, step, width):
    w = end + 2
    end *= 2
    picNo = 0
    for frameNo in range(start, end, step):
        #cmd = 'ffmpeg -y -ss 0.0 -i |sourceVid|  -t 8.5 -an -vf "crop=2:1280:|frameNo|:0, tile=1360x1" |picNo|.bmp' # tile=1024x1, hflip
        cmd = 'ffmpeg -y -ss 0.0 -i |sourceVid|  -t 8.5 -an -vf "crop=2:1280:|frameNo|:0, tile=648x1" |picNo|.bmp' # tile=1024x1, hflip
        # ffmpeg -y -i vid.mp4 -t 8.5 -an -vf "transpose=0, crop=1280:2:0:0, tile=1x1024, transpose=1" 0000.bmp
        # 'ffmpeg -y -i |sourceVid| -t 8.5 -an -vf "crop=1280:2:|frameNo|:0, transpose=2, tile=1024x1" |picNo|.bmp'
        # cmd = 'ffmpeg -y -i |sourceVid| -an -vf "crop=2:|width|:|frameNo|:0, tile=|frames|x1" |picNo|.bmp'
        cmd = cmd.replace('|sourceVid|', sourceVid)
        cmd = cmd.replace('|width|', width)
        cmd = cmd.replace('|frameNo|', str(frameNo))
        cmd = cmd.replace('|frames|', str(w))
        cmd = cmd.replace('|picNo|', ('0000' + str(picNo))[-4:])
        picNo += 1
        print(int(frameNo/step)+1, 'of', int(end/step), cmd)
        a = check_output(cmd, shell=True).decode()


def getAudio(vid, duration, newDuration):
    scale = duration/newDuration
    print ('Duration:', duration)
    print ('newDuration:', newDuration)
    print ('Scale:', scale)
    doublers = 0
    while((newDuration * pow(2,doublers)) <= duration):
        print ('newDuration * pow(2,doublers):', newDuration * pow(2,doublers))
        doublers += 1
        print ('Doublers:', doublers)
    print ('Power:', pow(2,doublers))
    final = scale / pow(2,doublers)
    print ('Final:', final)
    scaler = 'atempo=2.0, ' * doublers + 'atempo=|final|'.replace('|final|', str(final)[:5])
    cmd = 'ffmpeg -y -i |vid| -filter:a "volume=20dB, |scaler|" -vn audio.wav'
    cmd = cmd.replace('|vid|', vid)
    cmd = cmd.replace('|scaler|', scaler)
    print (cmd)
    a = check_output(cmd, shell=True).decode()
    return (a)


def makeVid(outFile, inFiles, frameRate, width, height):
    cmd = 'ffmpeg -r |frameRate| -start_number 0 -i |inFiles| -s |width|x|height| -c:v libx264 -crf 23 -profile:v baseline -level 3.0 -pix_fmt yuv420p -movflags faststart -y |outFile|'
    cmd = cmd.replace('|frameRate|', str(frameRate))
    cmd = cmd.replace('|inFiles|', inFiles)
    cmd = cmd.replace('|width|', width)
    cmd = cmd.replace('|height|', height)
    cmd = cmd.replace('|outFile|', outFile)
    print (cmd)
    a = check_output(cmd, shell=True).decode()
    return (a)


def makeVidWithAudio(outFile, inFiles, frameRate, width, height):
    cmd = 'ffmpeg -i audio.wav -r |frameRate| -start_number 0 -i |inFiles| -s |width|x|height| -c:v libx264 -crf 23 -profile:v baseline -level 3.0 -pix_fmt yuv420p -movflags faststart  -c:a aac -ac 2 -b:a 128k -strict -2  -shortest -y |outFile|'
    # cmd = 'ffmpeg -i audio.wav -r |frameRate| -start_number 0 -i |inFiles| -s |width|x|height| -c:v libx264 -crf 23 -profile:v baseline -level 3.0 -pix_fmt yuv420p -movflags faststart  -c:a aac -ac 2 -b:a 128k -strict -2  -shortest -y  -vf reverse -af areverse |outFile|'
    cmd = cmd.replace('|frameRate|', str(frameRate))
    cmd = cmd.replace('|inFiles|', inFiles)
    cmd = cmd.replace('|width|', width)
    cmd = cmd.replace('|height|', height)    
    cmd = cmd.replace('|outFile|', outFile)
    print (cmd)
    a = check_output(cmd, shell=True).decode()
    return (a)


sourceVid = 'vid.mp4'   #   <<<<<<<<<<<<<<<<<<<<<<<<< Your file goes here
# sourceVid = 'VID_20191113_171811.mp4'   
vidData = json.loads(getData(sourceVid))
astream = 1
vstream = 0
width = str((vidData['streams'][vstream]['width']))
height = str(vidData['streams'][vstream]['height'])
frames = int(vidData['streams'][vstream]['nb_frames'])
duration = float(vidData['streams'][vstream]['duration'])
framRate = (vidData['streams'][vstream]['r_frame_rate']) # avg_frame_rate
framRate = int(framRate.split('/')[vstream]) / int(framRate.split('/')[astream])
framRate = int(framRate)
audDuration = float(vidData['streams'][1]['duration'])

print ('Frames:',frames)
print ('Duration:',duration, 's')
print ('width:',width)
print ('height:',height)
print ('framRate:',framRate)
print ('audDuration:',audDuration)


start = 0
end = int(int(height)/ 2)+ int(start/2) # frames
step = 2
#vidSlice(sourceVid, start, end, step, width) # width

makeVid('out.mp4', '0%03d.bmp', 60, width, height)

newVidData = json.loads(getData('out.mp4'))
newDuration = float(vidData['streams'][0]['duration'])
print ('New Duration:',newDuration, 's')
getAudio(sourceVid, duration, newDuration)
makeVidWithAudio('AVout.mp4', '0%03d.bmp', 30, width, height)

"""
Join AV
ffmpeg -i .\out.mp4 -i audio.wav -c:v libx264 -crf 23 -profile:v baseline -level 3.0 -pix_fmt yuv
420p -c:a aac -ac 2 -b:a 128k -strict -2 -movflags faststart av.mp4
"""
