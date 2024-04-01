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


@app.post("/getpdf/")
async def get_pdf(pdf_file: UploadFile = File(...)):
    try:
        if pdf_file:
            current_script_dir = os.path.dirname(os.path.abspath(__file__))
            directory_path = os.path.join(current_script_dir, 'data')
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            file_path = os.path.join( directory_path, 'data.pdf')
            with open(file_path, "wb") as file_object:
                file_object.write(await pdf_file.read())
            print('PDF file saved successfully')
            process_pinecone()
            return JSONResponse(content={"success": True, "message": "PDF received and saved successfully"}, status_code=200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"success": False, "message": f"Error processing PDF: {str(e)}"}, status_code=500)


@app.get("/resetpinecone/")
async def reset_pinecone():
    reset_the_pinecone()



def mp3_to_text_hindi(data):
    client = OpenAI(api_key=OPENAI_API)
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=data,
        language="hi",
        response_format="text"
    )
    print(f"This is MP3 Hindi:\n\n{transcript}")
    return transcript

def english_to_hindi(english_text):
    translated = GoogleTranslator(source='en',target='hi').translate(english_text)
    print(f"This is english to hindi:\n\n{translated}")
    return translated


def hindi_text_to_mp3(text):
    print("generating audio")
    language = 'hi'
    speed = False
    tts = gTTS(text=text, lang=language, slow=speed)
    with NamedTemporaryFile(delete=False) as tmp:
        tts.save(tmp.name)
        tmp_path = tmp.name
    return tmp_path

def mp3_to_text_english(data):
    client = OpenAI(api_key=OPENAI_API)
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=data,
        language="en",
        response_format="text"
    )
    print(f"This is MP3 English:\n\n{transcript}")
    return transcript



def english_text_to_mp3(text):
    print("generating audio")
    language = 'en'
    speed = False
    tts = gTTS(text=text, lang=language, slow=speed)
    with NamedTemporaryFile(delete=False) as tmp:
        tts.save(tmp.name)
        tmp_path = tmp.name
    return tmp_path


def mp3_to_text_marathi(data):
    client = OpenAI(api_key=OPENAI_API)
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=data,
        language="mr",
        response_format="text"
    )
    print(f"This is MP3 Marathi:\n\n{transcript}")
    return transcript


def english_to_marathi(english_text):
    translated = GoogleTranslator(source='en',target='mr').translate(english_text)
    print(f"This is English text to Marathi:\n\n{translated}")
    return translated


def marathi_text_to_mp3(text):
    print("generating audio")
    language = 'mr'
    speed = False
    tts = gTTS(text=text, lang=language, slow=speed)
    with NamedTemporaryFile(delete=False) as tmp:
        tts.save(tmp.name)
        tmp_path = tmp.name
    return tmp_path

def mp3_to_text_tamil(data):
    client = OpenAI(api_key=OPENAI_API)
    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=data,
        language="ta",
        response_format="text"
    )
    print(f"This is MP3 Tamil:\n\n{transcript}")
    return transcript

def english_to_tamil(english_text):
    translated = GoogleTranslator(source='en',target='ta').translate(english_text)
    print(f"This is english to tamil:\n\n{translated}")
    return translated


def tamil_text_to_mp3(text):
    print("generating audio")
    language = 'ta'
    speed = False
    tts = gTTS(text=text, lang=language, slow=speed)
    with NamedTemporaryFile(delete=False) as tmp:
        tts.save(tmp.name)
        tmp_path = tmp.name
    return tmp_path


def hindi_to_english(english_text):
    translated = GoogleTranslator(source='hi',target='en').translate(english_text)
    print(f"This is hindi to english:\n\n{translated}")
    return translated


def marathi_to_english(english_text):
    translated = GoogleTranslator(source='mr',target='en').translate(english_text)
    print(f"This is Marathi to english:\n\n{translated}")
    return translated  


def tamil_to_english(english_text):
    translated = GoogleTranslator(source='ta',target='en').translate(english_text)
    print(f"This is tamil to english:\n\n{translated}")
    return translated  


@app.post("/getaudio/")
async def get_audio(language: str = Form(...), audio: UploadFile = File(...)):
    try:
        # Save the uploaded audio file
        with open(audio.filename, "wb") as buffer:
            buffer.write(audio.file.read())
        audio_input = open(audio.filename,"rb")

        

        if language == 'hindi':

            # input_lang = "hi"
            # print("base64 :" ,base64_input)
            # query = indic_to_english_voice(input_lang, base64_input)
            # print(query)
            # answer_eng = starting_point(query)
            # # print(answer_eng)
            # base64_output = english_to_indic_voice(input_lang, answer_eng)
            # final_output = convert_to_mp3(base64_output)


            input_lang = "hi"

            stt_hin = mp3_to_text_hindi(audio_input)
            tt_hin_eng = indic_to_english_text(input_lang, stt_hin)
            text_query_pdf = starting_point(tt_hin_eng)
            tt_eng_hin = english_to_indic_text(input_lang, text_query_pdf)
            tts_hin = hindi_text_to_mp3(tt_eng_hin)    
            def iterfile():
                with open(tts_hin, "rb") as audio_file:
                    yield from audio_file
                os.remove(tts_hin)
            return StreamingResponse(iterfile(),media_type="application/octet-stream")
        elif language == 'marathi':

            input_lang = "mr"
            stt_mar = mp3_to_text_marathi(audio_input)
            tt_mar_eng = indic_to_english_text(input_lang, stt_mar)
            text_query_pdf = starting_point(tt_mar_eng)
            tt_eng_mar = english_to_indic_text(input_lang, text_query_pdf)
            tts_mar = marathi_text_to_mp3(tt_eng_mar)
            def iterfile():
                with open(tts_mar, "rb") as audio_file:
                    yield from audio_file
                os.remove(tts_mar)
            return StreamingResponse(iterfile(),media_type="application/octet-stream")
        elif language == 'tamil':

            input_lang="ta"
            stt_tam = mp3_to_text_tamil(audio_input)
            tt_tam_eng = indic_to_english_text(input_lang, stt_tam)
            text_query_pdf = starting_point(tt_tam_eng)
            tt_eng_tam = english_to_indic_text(input_lang, text_query_pdf)
            tts_tam = tamil_text_to_mp3(tt_eng_tam)
            def iterfile():
                with open(tts_tam, "rb") as audio_file:
                    yield from audio_file
                os.remove(tts_tam)
            return StreamingResponse(iterfile(),media_type="application/octet-stream")
        else:
            stt_eng = mp3_to_text_english(audio_input)
            text_query_pdf = starting_point(stt_eng)
            tts_eng = english_text_to_mp3(text_query_pdf)
            print("english_output")
            print(  type(tts_eng))
            def iterfile():
                with open(tts_eng, "rb") as audio_file:
                    yield from audio_file
                os.remove(tts_eng)
            return StreamingResponse(iterfile(),media_type="application/octet-stream")

    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"success": False, "message": "Error processing audio"}, status_code=500)
    


input_lang = ""

@app.post("/gettext/")
async def get_text(text: str = Form(...), language: str = Form(...)):
    try:
        if language == 'hindi':
            input_lang = "hi"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)    # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'marathi':
            input_lang = "mr"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)      # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'tamil':
            input_lang = "ta"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'gom':
            input_lang = "gom"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'kannada':
            input_lang = "kn"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'dogri':
            input_lang = "doi"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'bodo':
            input_lang = "brx"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'urdu':
            input_lang = "ur"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'kashmiri':
            input_lang = "ks"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'assamese':
            input_lang = "as"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'bengali':
            input_lang = "bn"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'sindhi':
            input_lang = "sd"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'maithili':
            input_lang = "mai"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'punjabi':
            input_lang = "pa"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'malayalam':
            input_lang = "ml"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'manipuri':
            input_lang = "mni"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'telugu':
            input_lang = "te"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'sanskrit':
            input_lang = "sa"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'nepali':
            input_lang = "ne"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'santali':
            input_lang = "sat"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'gujarati':
            input_lang = "gu"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        elif language == 'odia':
            input_lang = "or"
            input_to_query = indic_to_english_text(input_lang, text)
            answer_to_indic = starting_point(input_to_query)        # change to conv chain
            final_answer = english_to_indic_text(input_lang, answer_to_indic)
            response_text = final_answer
        else:
            text_query_pdf = starting_point(text)       # change to conv chain
            response_text = text_query_pdf
        return JSONResponse(content={"text": response_text, "success": True}, status_code=200)
    except Exception as e:
        print(f"Error: {str(e)}")
        return JSONResponse(content={"success": False, "message": "Error processing text"}, status_code=500)



def indic_to_english_text(input_lang, input_text):
    url1 = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

    headers1 = {
        "Content-Type": "application/json",
        "ulcaApiKey": "3653475f10-336b-4d31-b3d3-713cf1b0d48a",
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
        # print("Translated text:", translated_text)
    else:
        print("Error:", response.status_code, response.text)


    output_text = translated_text['pipelineResponse'][0]['output'][0]['target']
    return output_text

def english_to_indic_text(input_lang, input_text):
    url1 = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

    headers1 = {
        "Content-Type": "application/json",
        "ulcaApiKey": "3653475f10-336b-4d31-b3d3-713cf1b0d48a",
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
        translated_text = response.json()
        # print("Translated text:", translated_text)
    else:
        print("Error:", response.status_code, response.text)


    output_text = translated_text['pipelineResponse'][0]['output'][0]['target']
    return output_text




def indic_to_english_voice(input_lang, input_audio_base64):
  url1 = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

  headers1 = {
      "Content-Type": "application/json",
      "ulcaApiKey": "3653475f10-336b-4d31-b3d3-713cf1b0d48a",
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
      "ulcaApiKey": "3653475f10-336b-4d31-b3d3-713cf1b0d48a",
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

