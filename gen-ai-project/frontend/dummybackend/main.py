#main imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import openai

#custom function imports
from functions.text_to_speech import convert_text_to_speech
from functions.database import store_messages, reset_messages
from functions.openai_requests import convert_audio_to_text, get_chat_response


#initiate app
app = FastAPI()

#cors - origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:4174",
    "http://localhost:3000"
]

#cors - middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def check_health():
    return {"message": "Healthy"}

#reset the messages
@app.get("/reset")
async def reset_convo():
    reset_messages()
    return {"message": "convo reset"}

# #post bot response, not in browser
# @app.post("/post-audio")
# async def post_audio(file: UploadFile = File(...)):
#     print("hello")

#get route for now
@app.post("/post-audio")
async def post_audio(file: UploadFile = File(...)):

    #get saved audio
    # audio_input = open("voice.mp3","rb")

    #save file from frontend
    with open(file.filename,"wb") as buffer:
        buffer.write(file.file.read())
    audio_input= open(file.filename,"rb")


    #decode audio
    message_decoded=convert_audio_to_text(audio_input)

    print(f"This is message_decoded: \n\n{message_decoded}")

    #get chatgpt response 

    chat_response = get_chat_response(message_decoded)

    if not chat_response:
        return HTTPException(status_code=400,detail="failed to get chat response")
    print(f"This is chat_response: \n\n{chat_response}")

    #store messages
    store_messages(message_decoded,chat_response)

    audio_output = convert_text_to_speech(chat_response)
    if not audio_output:
        return HTTPException(status_code=400,detail="failed to get 11 lab audio")
    
    #create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    #return audio file
    return StreamingResponse(iterfile(),media_type="application/octet-stream")




@app.get("/post-audio-get")
async def get_audio():

    #get saved audio
    audio_input = open("voice.mp3","rb")

    #save file from frontend
    # with open(file.filename,"wb") as buffer:
    #     buffer.write(file.file.read())
    # audio_input= open(file.filename,"rb")


    #decode audio
    message_decoded=convert_audio_to_text(audio_input)

    print(f"This is message_decoded: \n\n{message_decoded}")

    #get chatgpt response 

    chat_response = get_chat_response(message_decoded)

    print(f"This is chat_response: \n\n{chat_response}")

    #store messages
    store_messages(message_decoded,chat_response)
    
    audio_output = convert_text_to_speech(chat_response)
    if not audio_output:
        return HTTPException(status_code=400,detail="failed to get 11 lab audio")
    #create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    #return audio file
    
    
    return StreamingResponse(iterfile(),media_type="audio/mpeg")

