from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests


app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


languages = {
    "Hindi": "hi", #hindi
    "Gom": "gom", #Gom
    "Kannade": "kn", #Kannada
    "Dogri": "doi", #Dogri    
    "Bodo": "brx", #Bodo 
    "Urdu": "ur",  #Urdu
    "Tamil": "ta",  #Tamil
    "Kashmiri": "ks",  #Kashmiri
    "Assamese": "as",  #Assamese
    "Bengali": "bn", #Bengali
    "Marathi": "mr", #Marathi
    "Sindhi": "sd", #Sindhi
    "Maihtili": "mai",#Maithili
    "Punjabi": "pa", #Punjabi
    "Malayalam": "ml", #Malayalam
    "Manipuri": "mni",#Manipuri
    "Telugu": "te", #Telugu
    "Sanskrit": "sa", #Sanskrit
    "Nepali": "ne", #Nepali
    "Santali": "sat",#Santali
    "Gujarati": "gu", #Gujarati
    "Oriya": "or", #Oriya
    "English": "en",#English
}



@app.post("/gettext/")
async def get_text(text: str = Form(...), language: str = Form(...)):
    try:
        
        input_lang = languages['language']
        input_to_firebase = indic_to_english_text(input_lang, text)

        # send to firebase user1

        # get from firebase and send to user 2


        emotion = sentimemt(input_to_query)
        answer_to_indic = starting_point(input_to_query,emotion)    # change to conv chain
        final_answer = english_to_indic_text(input_lang, answer_to_indic)
        response_text = final_answer
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


