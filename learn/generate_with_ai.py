import openai
from dotenv import load_dotenv
import tiktoken
import os

def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    num_tokens = len(encoding.encode(string))
    return num_tokens

load_dotenv()
def getStartingInformation(subtopic,subtopic_description):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = [
        {"role": "system", "content": "You are a teacher, you will teach me "+subtopic+", this is some description about the topic "+subtopic_description},
        {"role": "user", "content": "Generate a paragraph of around 100 words to teach me this topic"},
    ]
    input = ""
    for msg in messages:
        input +=  msg['content']
    print("tokens used: ",num_tokens_from_string(input))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = messages
    )
    return response['choices'][0]['message']['content']

def get_questions_related_to_information(subtopic,subtopic_description,info,count = 5):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = [
        {"role": "system", "content": "You are a teacher, you will teach me "+subtopic+", this is some description about the topic "+subtopic_description},
        {"role": "user", "content": "Generate "+str(count)+" questions, regarding this topic from the information "+info+ ", questions should only be from the above information, return the questions in JSON formatted List"},
    ]
    input = ""
    for msg in messages:
        input +=  msg['content']
    print("tokens used: ",num_tokens_from_string(input))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = messages
    )
    return response['choices'][0]['message']['content']

def is_this_answer_correct(subtopic,subtopic_description,question,answer):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    messages = [
        {"role": "system", "content": "You are a teacher, you will teach me "+subtopic+", this is some description about the topic "+subtopic_description},
        {"role": "user", "content": "Check if "+str(answer)+" is the correct answer to the question "+question+ ", return the answer with a yes or no and an explaination of 30 words"},
    ]
    input = ""
    for msg in messages:
        input +=  msg['content']
    print("tokens used: ",num_tokens_from_string(input))
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = messages
    )
    return response['choices'][0]['message']['content']