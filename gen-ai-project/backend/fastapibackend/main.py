from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from deep_translator import GoogleTranslator
import os
from gtts import gTTS
from openai import OpenAI
from rag import *
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
import json
import requests
# import librosa
import base64
from pydub import AudioSegment
import shutil
from transformers import pipeline


load_dotenv()

OPENAI_API = os.getenv('OPENAI_API_KEY')
PINECONE_API = os.getenv('PINECONE_API_KEY')

app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.post("/getpdf/")
# async def get_pdf(pdf_file: UploadFile = File(...)):
#     try:
#         if pdf_file:
#             current_script_dir = os.path.dirname(os.path.abspath(__file__))
#             directory_path = os.path.join(current_script_dir, 'data')
#             if not os.path.exists(directory_path):
#                 os.makedirs(directory_path)
#             file_path = os.path.join( directory_path, 'data.pdf')
#             with open(file_path, "wb") as file_object:
#                 file_object.write(await pdf_file.read())
#             print('PDF file saved successfully')
#             process_pinecone()
#             return JSONResponse(content={"success": True, "message": "PDF received and saved successfully"}, status_code=200)
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         return JSONResponse(content={"success": False, "message": f"Error processing PDF: {str(e)}"}, status_code=500)


# @app.get("/resetpinecone/")
# async def reset_pinecone():
#     reset_the_pinecone()




# def sentimemt(text):
#     classifier = pipeline(task="text-classification", model="SamLowe/roberta-base-go_emotions", top_k=None)
#     sentences = [text]

#     model_outputs = classifier(sentences)
#     print ("emotion", model_outputs[0][0]['label'])
#     return model_outputs[0][0]['label']







def mp3_to_text(input_lang, data):
    client = OpenAI(api_key=OPENAI_API)
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=data,
        language=input_lang,
        response_format="text"
    )
    print(f"This is MP3 :\n\n{transcript}")
    return transcript




def base64_to_mp3(base64_string):
    print("generating audio")
    decoded_data = base64.b64decode(base64_string)
    with NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(decoded_data)
        tmp_path = tmp.name
    return tmp_path



@app.post("/getaudio/")
async def get_audio(jd: str = Form(...),exp: str = Form(...),language: str = Form(...), audio: UploadFile = File(...)):
    try:

        # Save the uploaded audio file
        with open(audio.filename, "wb") as buffer:
            buffer.write(audio.file.read())
        audio_input = open(audio.filename,"rb")
        print(audio.filename)


        # mp3_data = await audio.read()
        # base64_encoded_data = base64.b64encode(mp3_data).decode('utf-8')
       
        if language == 'hindi':
            # input_lang = "hi"
            # sst_ind = await asr2(input_lang, base64_encoded_data)   # audio to indic text
            # print("sst_ind", sst_ind)
            # tt_eng = indic_to_english_text(input_lang, sst_ind)    # indic text to eng text
            # print(tt_eng)
            # emotion = sentimemt(tt_eng)
            # text_query_pdf = starting_point(tt_eng, emotion)  # query
            # print(text_query_pdf)
            # tt_ind = english_to_indic_text(input_lang, text_query_pdf)  # eng reply to indic text
            # print(tt_ind)
            # tts_b64 = tts(input_lang, tt_ind)
            # tts_ind = base64_to_mp3(tts_b64)    #indic text to voice

            input_lang="hi"
            sst_ind = mp3_to_text(input_lang, audio_input)
            tt_eng = indic_to_english_text(input_lang, sst_ind)
            emotion = sentimemt(tt_eng)
            text_query_pdf = starting_point(tt_eng, emotion)
            tt_ind = english_to_indic_text(input_lang, text_query_pdf)
            tts_b64 = tts(input_lang, tt_ind)
            tts_ind = base64_to_mp3(tts_b64)
            def iterfile():
                with open(tts_ind, "rb") as audio_file:
                    yield from audio_file
                os.remove(tts_ind)
            return StreamingResponse(iterfile(),media_type="application/octet-stream")
        elif language == 'marathi':
            input_lang="mr"
            sst_ind = mp3_to_text(input_lang, audio_input)
            tt_eng = indic_to_english_text(input_lang, sst_ind)
            emotion = sentimemt(tt_eng)
            text_query_pdf = starting_point(tt_eng, emotion)
            tt_ind = english_to_indic_text(input_lang, text_query_pdf)
            tts_b64 = tts(input_lang, tt_ind)
            tts_ind = base64_to_mp3(tts_b64)
            def iterfile():
                with open(tts_ind, "rb") as audio_file:
                    yield from audio_file
                os.remove(tts_ind)
            return StreamingResponse(iterfile(),media_type="application/octet-stream")
        elif language == 'tamil':
            input_lang="ta"
            sst_ind = mp3_to_text(input_lang, audio_input)
            tt_eng = indic_to_english_text(input_lang, sst_ind)
            emotion = sentimemt(tt_eng)
            text_query_pdf = starting_point(tt_eng, emotion)
            tt_ind = english_to_indic_text(input_lang, text_query_pdf)
            tts_b64 = tts(input_lang, tt_ind)
            tts_ind = base64_to_mp3(tts_b64)
            def iterfile():
                with open(tts_ind, "rb") as audio_file:
                    yield from audio_file
                os.remove(tts_ind)
            return StreamingResponse(iterfile(),media_type="application/octet-stream")
        elif language == 'Kannada':
            input_lang="kn"
            sst_ind = mp3_to_text(input_lang, audio_input)
            tt_eng = indic_to_english_text(input_lang, sst_ind)
            emotion = sentimemt(tt_eng)
            text_query_pdf = starting_point(tt_eng, emotion)
            tt_ind = english_to_indic_text(input_lang, text_query_pdf)
            tts_b64 = tts(input_lang, tt_ind)
            tts_ind = base64_to_mp3(tts_b64)
            def iterfile():
                with open(tts_ind, "rb") as audio_file:
                    yield from audio_file
                os.remove(tts_ind)
            return StreamingResponse(iterfile(),media_type="application/octet-stream")
        elif language == 'Urdu':
            input_lang="ur"
            sst_ind = mp3_to_text(input_lang, audio_input)
            tt_eng = indic_to_english_text(input_lang, sst_ind)
            emotion = sentimemt(tt_eng)
            text_query_pdf = starting_point(tt_eng, emotion)
            tt_ind = english_to_indic_text(input_lang, text_query_pdf)
            tts_b64 = tts(input_lang, tt_ind)
            tts_ind = base64_to_mp3(tts_b64)
            def iterfile():
                with open(tts_ind, "rb") as audio_file:
                    yield from audio_file
                os.remove(tts_ind)
            return StreamingResponse(iterfile(),media_type="application/octet-stream")
        elif language == 'Nepali':
            input_lang="ne"
            sst_ind = mp3_to_text(input_lang, audio_input)
            tt_eng = indic_to_english_text(input_lang, sst_ind)
            emotion = sentimemt(tt_eng)
            text_query_pdf = starting_point(tt_eng, emotion)
            tt_ind = english_to_indic_text(input_lang, text_query_pdf)
            tts_b64 = tts(input_lang, tt_ind)
            tts_ind = base64_to_mp3(tts_b64)
            def iterfile():
                with open(tts_ind, "rb") as audio_file:
                    yield from audio_file
                os.remove(tts_ind)
            return StreamingResponse(iterfile(),media_type="application/octet-stream")  
        else:
            input_lang = "en"
            sst_ind = mp3_to_text(input_lang, audio_input)
            text_query_pdf = starting_point(sst_ind, jd, exp)
            tts_b64 = tts(input_lang, text_query_pdf)
            tts_ind = base64_to_mp3(tts_b64)
            def iterfile():
                with open(tts_ind, "rb") as audio_file:
                    yield from audio_file
                os.remove(tts_ind)
            return StreamingResponse(iterfile(),media_type="application/octet-stream")

    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"success": False, "message": "Error processing audio"}, status_code=500)
    


input_lang = ""

@app.post("/gettext/")
async def get_text(jd: str = Form(...),exp: str = Form(...), text: str = Form(...), language: str = Form(...)):
    try:
        if language == 'hindi':
            input_lang = "hi"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)    # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'marathi':
            input_lang = "mr"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)      # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'tamil':
            input_lang = "ta"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'gom':
            input_lang = "gom"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'kannada':
            input_lang = "kn"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'dogri':
            input_lang = "doi"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'bodo':
            input_lang = "brx"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'urdu':
            input_lang = "ur"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'kashmiri':
            input_lang = "ks"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'assamese':
            input_lang = "as"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'bengali':
            input_lang = "bn"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'sindhi':
            input_lang = "sd"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'maithili':
            input_lang = "mai"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'punjabi':
            input_lang = "pa"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'malayalam':
            input_lang = "ml"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'manipuri':
            input_lang = "mni"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'telugu':
            input_lang = "te"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'sanskrit':
            input_lang = "sa"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'nepali':
            input_lang = "ne"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'santali':
            input_lang = "sat"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'gujarati':
            input_lang = "gu"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'odia':
            input_lang = "or"
            input_to_query = indic_to_english_text(input_lang, text)
            emotion = sentimemt(input_to_query)
            answer_to_indic = starting_point(input_to_query,emotion)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        else:
            # emotion = sentimemt(text)
            text_query_pdf = starting_point(text, jd, exp)       # change to conv chain
            response_text = text_query_pdf
        return JSONResponse(content={"text": response_text, "success": True}, status_code=200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"success": False, "message": "Error processing text"}, status_code=500)




































def indic_to_english_text(input_lang, input_text):
    url1 = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

    headers1 = {
        "Content-Type": "application/json",
        "ulcaApiKey": "167642c261-1283-4816-9309-9767b0a1ea26",
        "userID": "1930b643ca2d4589b2bf9157cb2d7f3d"
    }

    payload1 = {
        "pipelineTasks": [{
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": input_lang,
                    "targetLanguage": "en"
                }
            }
        }],


        "pipelineRequestConfig": {
            "pipelineId": "64392f96daac500b55c543cd"
        }
    }

    response = requests.post(url1, json=payload1, headers=headers1)

    if response.status_code == 200:
        # Parsing the response JSON
        response_data = response.json()
        # print("Success:", response_data)
    else:
        print("Error:", response.status_code, response.text)
        

    compute_url = response_data['pipelineInferenceAPIEndPoint']['callbackUrl']
    header_name = response_data['pipelineInferenceAPIEndPoint']['inferenceApiKey']['name']
    header_value = response_data['pipelineInferenceAPIEndPoint']['inferenceApiKey']['value']
    payload_serviceID = response_data['pipelineResponseConfig'][0]['config'][0]['serviceId']
    payload_modelId = response_data['pipelineResponseConfig'][0]['config'][0]['modelId']



    url2 = compute_url

    headers2 = {
        header_name : header_value
    }

    payload2 = {
        "pipelineTasks": [
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": input_lang,
                        "targetLanguage": "en"
                    },
                    "serviceId": payload_serviceID,
                    "modelId": payload_modelId
                }
            }
        ],
        "inputData": {
            "input": [
                {
                    "source": input_text
                }
            ]
        }
    }


    response = requests.post(url2, json=payload2, headers=headers2)

    if response.status_code == 200:
        translated_text = response.json()
    else:
        print("Error:", response.status_code, response.text)


    output_text = translated_text['pipelineResponse'][0]['output'][0]['target']
    return output_text

def english_to_indic_text(input_lang, input_text):
    url1 = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

    headers1 = {
        "Content-Type": "application/json",
        "ulcaApiKey": "167642c261-1283-4816-9309-9767b0a1ea26",
        "userID": "1930b643ca2d4589b2bf9157cb2d7f3d"
    }

    payload1 = {
        "pipelineTasks": [{
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": "en",
                    "targetLanguage": input_lang
                }
            }
        }],


        "pipelineRequestConfig": {
            "pipelineId": "64392f96daac500b55c543cd"
        }
    }

    response = requests.post(url1, json=payload1, headers=headers1)

    if response.status_code == 200:
        # Parsing the response JSON
        response_data = response.json()
        # print("Success:", response_data)
    else:
        print("Error:", response.status_code, response.text)
        

    compute_url = response_data['pipelineInferenceAPIEndPoint']['callbackUrl']
    header_name = response_data['pipelineInferenceAPIEndPoint']['inferenceApiKey']['name']
    header_value = response_data['pipelineInferenceAPIEndPoint']['inferenceApiKey']['value']
    payload_serviceID = response_data['pipelineResponseConfig'][0]['config'][0]['serviceId']
    payload_modelId = response_data['pipelineResponseConfig'][0]['config'][0]['modelId']



    url2 = compute_url

    headers2 = {
        header_name : header_value
    }

    payload2 = {
        "pipelineTasks": [
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": "en",
                        "targetLanguage": input_lang
                    },
                    "serviceId": payload_serviceID,
                    "modelId": payload_modelId
                }
            }
        ],
        "inputData": {
            "input": [
                {
                    "source": input_text
                }
            ]
        }
    }


    response = requests.post(url2, json=payload2, headers=headers2)

    if response.status_code == 200:
        translated = response.json()
    else:
        print("Error:", response.status_code, response.text)


    output_text = translated['pipelineResponse'][0]['output'][0]['target']
    return output_text




def indic_to_english_voice(input_lang, input_audio_base64):
  url1 = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

  headers1 = {
      "Content-Type": "application/json",
      "ulcaApiKey": "167642c261-1283-4816-9309-9767b0a1ea26",
      "userID": "1930b643ca2d4589b2bf9157cb2d7f3d"
  }

  payload1 = {
      "pipelineTasks" : [
        {
              "taskType": "asr",
              "config": {
                  "language": {
                      "sourceLanguage": input_lang
                  }
              }
          },
        {
          "taskType": "translation",
          "config": {
              "language": {
                  "sourceLanguage": input_lang,
                  "targetLanguage": "en"
              }
          }
      }
      ],

      "pipelineRequestConfig": {
          "pipelineId": "64392f96daac500b55c543cd"
      }
  }

  response = requests.post(url1, json=payload1, headers=headers1)

  if response.status_code == 200:
      data = response.json()
  else:
      print("Error:", response.status_code, response.text)

  service_id_1 = data["pipelineResponseConfig"][0]["config"][0]["serviceId"]
  service_id_2 = data["pipelineResponseConfig"][1]["config"][0]["serviceId"]
  callback_url = data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
  header_name = data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["name"]
  header_value = data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"]


  url2 = callback_url  # Replace with the actual URL

    # Your API key or token for authentication, if required
  headers2 = {
        header_name : header_value
  }

  null = "null"



  payload2 = {
        "pipelineTasks": [
            {
                "taskType": "asr",
                "config": {
                    "language": {
                        "sourceLanguage": input_lang
                    },
                    "serviceId": service_id_1,
                    "audioFormat": "mp3",
                    "samplingRate": 48000
                }
            },
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": input_lang,
                        "targetLanguage": "en"
                    },
                    "serviceId": service_id_2
                }
            }
        ],
        "inputData": {
            "input": [
                {
                    "source": null
                }
            ],
            "audio": [
                {
                    "audioContent": input_audio_base64
                }
            ]
        }
    }

  response = requests.post(url2, json=payload2, headers=headers2)

  if response.status_code == 200:
      data = response.json()
  else:
      print("Error : ", response.status_code, response.text)

  translation_output = data["pipelineResponse"][1]["output"][0]["target"]
  print(translation_output)
  return translation_output



def english_to_indic_voice(output_lang, input_text):

  url1 = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

  headers1 = {
      "Content-Type": "application/json",
      "ulcaApiKey": "167642c261-1283-4816-9309-9767b0a1ea26",
      "userID": "1930b643ca2d4589b2bf9157cb2d7f3d"
  }

  payload1 = {
      "pipelineTasks": [{
          "taskType": "translation",
          "config": {
              "language": {
                  "sourceLanguage": "en",
                  "targetLanguage": output_lang
                  }
          }
      },
      {
          "taskType": "tts",
          "config": {
                  "language": {
                      "sourceLanguage": output_lang
                  }
              }
      }],

      "pipelineRequestConfig": {
          "pipelineId": "64392f96daac500b55c543cd"
      }
  }



  response = requests.post(url1, json=payload1, headers=headers1)

  if response.status_code == 200:
      data = response.json()
      # print(data)
  else:
      print("Error:", response.status_code, response.text)


  service_id_1 = data["pipelineResponseConfig"][0]["config"][0]["serviceId"]
  service_id_2 = data["pipelineResponseConfig"][1]["config"][0]["serviceId"]

  callback_url = data["pipelineInferenceAPIEndPoint"]["callbackUrl"]

  header_name = data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["name"]
  header_value = data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"]

  url2 = callback_url

  headers2 = { 
      header_name : header_value
  }
  null = "null"

  payload2 = {
      "pipelineTasks": [
          {
              "taskType": "translation",
              "config": {
                  "language": {
                      "sourceLanguage": "en",
                      "targetLanguage": output_lang
                  },
                  "serviceId": service_id_1
              }
          },
          {
              "taskType": "tts",
              "config": {
                  "language": {
                      "sourceLanguage": output_lang
                  },
                  "serviceId": service_id_2,
                  "gender": "male"
              }
          }
      ],
      "inputData": {
          "input": [
              {
                  "source": input_text
              }
          ],
          "audio": [
              {
                  "audioContent": null
              }
          ]
      }
  }

  response = requests.post(url2, json=payload2, headers=headers2)

  if response.status_code == 200:
      data = response.json()
      # print(data)
  else:
      print("Error:", response.status_code, response.text)

  return data['pipelineResponse'][1]['audio'][0]['audioContent']



async def asr(input_lang, base64_input):

    url_config = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

    headers_config = {
        "Content-Type": "application/json",
        "ulcaApiKey": "167642c261-1283-4816-9309-9767b0a1ea26",
        "userID": "1930b643ca2d4589b2bf9157cb2d7f3d"
    }

    payload_config = {
        "pipelineTasks": [
            {
                "taskType": "asr",
                "config": {
                    "language": {
                        "sourceLanguage": input_lang
                    }
                }
            }],


        "pipelineRequestConfig": {
            "pipelineId": "64392f96daac500b55c543cd"
        }
    }


    response = requests.post(url_config, json=payload_config, headers=headers_config)

    if response.status_code == 200:
        response_data = response.json()
    else:
        print("Error asr1:", response.status_code, response.text)


    compute_url = response_data['pipelineInferenceAPIEndPoint']['callbackUrl']
    header_name = response_data['pipelineInferenceAPIEndPoint']['inferenceApiKey']['name']
    header_value = response_data['pipelineInferenceAPIEndPoint']['inferenceApiKey']['value']
    payload_serviceID = response_data['pipelineResponseConfig'][0]['config'][0]['serviceId']
    payload_modelId = response_data['pipelineResponseConfig'][0]['config'][0]['modelId']


    url_compute = compute_url
    null = "null"

    headers_compute = {
        header_name : header_value
    }



    payload_compute = {
        "pipelineTasks": [
            {
                "taskType": "asr",
                "config": {
                    "language": {
                        "sourceLanguage": input_lang
                    },
                    "serviceId": payload_serviceID,
                    "audioFormat": "wav",
                    "samplingRate": 48000
                }
            }
        ],
        "inputData": {
            "input": [
                {
                    "source": null
                }
            ],
            "audio": [
                {
                    "audioContent": base64_input
                }
            ]
        }
    }

    response = requests.post(url_compute, json=payload_compute, headers=headers_compute)
    
    if response.status_code == 200:
        ans = response.json()
        # print("Translated text:", asr)
    else:
        print("Error asr2:", response.status_code, response.text)


    asr_output = ans['pipelineResponse'][0]['output'][0]['source']

    return asr_output


def tts(input_lang, text_input):
    url_config = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

    headers_config = {
        "Content-Type": "application/json",
        "ulcaApiKey": "167642c261-1283-4816-9309-9767b0a1ea26",
        "userID": "1930b643ca2d4589b2bf9157cb2d7f3d"
    }

    payload_config = {
        "pipelineTasks": [{
            "taskType": "tts",
            "config": {
                    "language": {
                        "sourceLanguage": input_lang
                    }
                }
        }],


        "pipelineRequestConfig": {
            "pipelineId": "64392f96daac500b55c543cd"
        }
    }

    # Making the POST request to the API
    response = requests.post(url_config, json=payload_config, headers=headers_config)

    response_data = ""
    if response.status_code == 200:
        # Parsing the response JSON
        response_data = response.json()
    else:
        print("Error tts1:", response.status_code, response.text)

    #  used in compute call (? next step)

    compute_url = response_data['pipelineInferenceAPIEndPoint']['callbackUrl']
    header_name = response_data['pipelineInferenceAPIEndPoint']['inferenceApiKey']['name']
    header_value = response_data['pipelineInferenceAPIEndPoint']['inferenceApiKey']['value']
    payload_serviceID = response_data['pipelineResponseConfig'][0]['config'][0]['serviceId']
    payload_modelId = response_data['pipelineResponseConfig'][0]['config'][0]['modelId']

    url_compute = compute_url  # Replace with the actual URL

    gender_input = "male"

    # Your API key or token for authentication, if required
    headers_compute = {
        header_name : header_value
    }


    payload_compute = {
        "pipelineTasks": [
            {
                "taskType": "tts",
                "config": {
                    "language": {
                        "sourceLanguage": input_lang
                    },
                    "serviceId": payload_serviceID,
                    "gender": gender_input
                }
            }
        ],
        "inputData": {
            "input": [
                {
                    "source": text_input
                }
            ]
        }
    }

    # Making the POST request to the API
    response = requests.post(url_compute, json=payload_compute, headers=headers_compute)

    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the response JSON
        response_data = response.json()
    else:
        print("Error tts2:", response.status_code, response.text)

    base64_mp3_data = response_data['pipelineResponse'][0]['audio'][0]['audioContent']

    return base64_mp3_data


async def asr2(source_language, content):
    headers = {
        "Content-Type": "application/json",
        "ulcaApiKey": "167642c261-1283-4816-9309-9767b0a1ea26",
        "userID": "1930b643ca2d4589b2bf9157cb2d7f3d"
    }
    payload = {
        "pipelineTasks": [
            {
                "taskType": "asr",
                "config": {
                    "language": {
                        "sourceLanguage": source_language
                    }
                }
            }
        ],
        "pipelineRequestConfig": {
            "pipelineId" : "64392f96daac500b55c543cd"
        }
    }
    
    response = requests.post('https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline', json=payload, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        service_id = response_data["pipelineResponseConfig"][0]["config"][0]["serviceId"]

        compute_payload = {
            "pipelineTasks": [
                {
                    "taskType": "asr",
                    "config": {
                        "language": {
                            "sourceLanguage": source_language,
                        },
                        "serviceId": service_id
                    }
                }
            ],
            "inputData": {
                "audio": [
                    {
                        "audioContent": content
                    }
                ]
            }
        }

        callback_url = response_data["pipelineInferenceAPIEndPoint"]["callbackUrl"]
        
        headers2 = {
            response_data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["name"]:
            response_data["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"]
        }

        compute_response = requests.post(callback_url, json=compute_payload, headers=headers2)

        if compute_response.status_code == 200:
            compute_response_data = compute_response.json()
            transcribed_content = compute_response_data["pipelineResponse"][0]["output"][0]["source"]
            return {
                "status_code": 200,
                "message": "Translation successful",
                "transcribed_content": transcribed_content
            }
        else:
            return {
                "status_code": compute_response.status_code,
                "message": "Error in translation",
                "transcribed_content": None
            }
    else:
        return {
            "status_code": response.status_code,
            "message": "Error in translation request",
            "transcribed_content": None
        }