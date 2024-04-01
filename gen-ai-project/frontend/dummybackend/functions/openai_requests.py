import openai

#import custom functions
from functions.database import get_recent_messages

#get env variables
openai.organization="org-B2yqYB2USBVaJDDvulebKrlP"
openai.api_key="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"

#open ai - whisper - audio to text

def convert_audio_to_text(audio_file):
    try:
        transcript = openai.Audio.transcribe("whisper-1",audio_file)
        message_text= transcript["text"]
        return message_text
    except Exception as e:
        print(e)
        return
    

#open ai- chat gpt - get response to our message
def get_chat_response(message_input):
    messages = get_recent_messages()
    user_message = {
        "role":"user",
        "content": message_input
    }
    messages.append(user_message)

    print(f"\nThis is messages\n\n{messages}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        
        message_text = response["choices"][0]["message"]["content"]

        return message_text
    except Exception as e:
        print(e)
        return
    
