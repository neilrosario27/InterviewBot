import requests


ELEVEN_LABS_API_KEY= "65eab46032a07ce4c74712066ae2221f"

#eleven labs - convert text to speech

def convert_text_to_speech(message):

    #define body to send to 11labs endpoint
    body = {
        "text" : message,
        "voice_settings": {
            "stability" : 0,
            "similarity_boost" : 0,
        }
    }

    #define voice
    voice_john = "29vD33N1CtxCmqQRPOHJ"

    #headers and endpoint 
    headers = {"xi-api-key" : ELEVEN_LABS_API_KEY, "Content-Type" : "application/json", "accept" : "audio/mpeg"}
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_john}"

    #send request
    try:
        response = requests.post(endpoint,json=body,headers=headers)
    except Exception as e:
        print("could not get audio")
        return

    #handle response
    if response.status_code == 200:
        print(response.content)
        return response.content
    else:
        print(response.status_code)
        print("sorry cant do")
        print(response)
        return
    
        
