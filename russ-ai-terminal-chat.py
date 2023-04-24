#CHAT WITH AI ON THE TERMINAL.  MAKE SURE openai-key.txt has your api key.

#does not do voice but requires almost no packages.  chat on the terminal with openai. great for rpi zero projects with tiny screens.

#cd /folder/filepath/
#python3 russ_ai_terminal_chat.py

import requests
import json

#load api key from file
file_path = "openai-key.txt"

def load_string_from_file():
    with open(file_path, 'r') as file:
        content = file.read().strip()
    return content

content = load_string_from_file()

#see if the content is 50 characters (always reads as 51...fail)

length = len(content)
if length -1 != 50:  #string length is always one char too big for some reason.
    print("Error: Api Key was the wrong number of characters: " +  str(length - 1) + " (should be 50)")
    print("please check for white spaces or extra digits.   this check can be removed from the script by editing it.")
    print("the key hasnt been checked if it works with openai.com, we're just checking it's length and there's a problem.")
    sys.exit()


API_KEY = content

def send_message_to_openai(message):
#    API_URL = "https://api.openai.com/v1/engines/gpt-3.5-turbo/completions"
    API_URL = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    data = {
             "messages":[
                {"role":"system","content": "You are a helpful assistant"},
                {"role":"user", "content": message}
                ],
            "model": "gpt-3.5-turbo"
#            "max_tokens":50,
#            "temperature": 0.7
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    #response = response['choices'][0]['message']['content']
    if response.status_code == 200:
        response_json = response.json()
        #return response_json["choices"][0]["text"].strip()
        return response_json['choices'][0]['message']['content']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def main():
    print("Welcome to the OpenAI chat!")
    print("Type 'exit' to end the conversation.")

    history = ""

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break


        #history += f"User: {user_input}\nAI: "

        #prompt = f"{history}{{response}}"
        response = send_message_to_openai(user_input)

        if response is not None:
            print(f"AI: {response}")
            history += f"{response}\n"

if __name__ == "__main__":
    main()
