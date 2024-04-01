import json
import random


#get recent messages

def get_recent_messages():

    #define the file name and learn instruction
    file_name="stored_data"
    learn_instruction = {
        "role" : "system",
        "content" : "Your name is John. You are teaching me on topics that I ask you about as I am student. You have a lot of knowledge in general, and also about dengue disease. Answer in short answers that are relevant to the question. Keep your answer under 30 words"
    }

    #initialize messages
    messages = []

    #append instruction to message
    messages.append(learn_instruction)

    #get last messages
    try:
        with open(file_name) as user_file:
            data=json.load(user_file)

            # Append last 5 items of data
            if data:
                if len(data)<5:
                    for item in data:
                        messages.append(item)
                else:
                    for item in data[-5:]:
                        messages.append(item)

    except Exception as e:
        print(e)
        pass

    #return messsages
    return messages

#store messages in stored_data.json file
def store_messages(request_message, response_message):

    #define file name
    file_name="stored_data.json"

    # get recent messages
    #first system messages is always being added so we start from second one
    messages = get_recent_messages()[1:]

    #add messages to data
    user_message = {"role" : "user", "content" : request_message}
    assistant_message = {"role" : "assistant", "content" : response_message}
    messages.append(user_message)
    messages.append(assistant_message)


    #save the updated file
    with open(file_name, "w") as f:
        json.dump(messages,f)

# reset messages
def reset_messages():

    #overwrite current file with nothing
    open("stored_data.json","w")

