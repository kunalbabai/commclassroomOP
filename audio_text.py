#importing the dependecies 
import youtube_dl
import subprocess
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
#fisrt craeting a function to download the youtube video ----
def youTubeVide_downloader(link):
    you_out = {}
    with youtube_dl.YoutubeDL(you_out) as fl:
        fl.download([link])
#extracting the audio from video
def extract_audio(name_file,output_name):
    command = f'ffmpeg -i {name_file}.mkv -ab 160k -ar 44100 -vn {output_name}.wav'
    subprocess.call(command, shell=True)
#writing text file & clening IBM Audio Text Output Cleaning -
def process_text(data,name_output):
    text = [result['alternatives'][0]['transcript'].rstrip() + '.\n' for result in data['results']]
    text = [para[0].title() + para[1:] for para in text]
    transcript = ''.join(text)
    with open(f'{name_output}.txt', 'w') as out:
        out.writelines(transcript)
#audio to text setup & process
def audio_to_text(apikey,url,audio_file_name,text_file_name):
    authentication = IAMAuthenticator(apikey=apikey)
    speech_text = SpeechToTextV1(authenticator=authentication)
    speech_text.set_service_url(url)
    with open(audio_file_name+'.wav','rb') as f:
        result = speech_text.recognize(audio=f,content_type=audio_file_name+'/wav',model='en-AU_NarrowbandModel', continuous=True).get_result()
    process_text(result,text_file_name)

#main program 
try:
    global roll_back
    roll_back = "yes"
    while roll_back == True:
        link = input("Enter Youtube URL - ")
        youTubeVide_downloader(link=link.strip())
        roll_back = input("If you wnat to dowload any other video then type 'Yes' or prees 'No' if you are done -").lower()
    #calling the extracting audio function
    video_file_name = input("Enter the video file name -").strip()
    video_file_name_audio = input("Enter the audio file name -").strip()
    extract_audio(video_file_name,video_file_name_audio)
    #setup the STT Service from IBM watson
    apikey = input("Plaes Provide the IBM Api Key -").strip()
    authenticator_url = input("Enter Your Autheticator URL - ").strip()
    output_file_name = input("Enter Your output Fiile Name -").strip()
    audio_to_text(apikey=apikey,url=authenticator_url,audio_file_name=video_file_name_audio,text_file_name=output_file_name)
except Exception as Ex:
    print(Ex)
