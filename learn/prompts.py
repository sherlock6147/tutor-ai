from topics.models import *
from learn.generate_with_ai import *
from learn.models import *
import json

def createHelpPrompt(subtopic:SubTopic,context,**kwargs):
    print("creating start asking questions prompt")
    chat_prompt = Chat()
    chat_prompt.learner = context['learner']
    chat_prompt.message = kwargs.get('message',"When you feel that you have learnt enough of the above information, you can use '/start' command to start answering questions to test your knowledge.")
    chat_prompt.msg_type = "info"
    chat_prompt.from_ai = True
    chat_prompt.subtopic = subtopic
    chat_prompt.save()

def createStartingInformationPrompt(subtopic:SubTopic,context):
    print("creating starting information prompt")
    start_prompt = getStartingInformation(subtopic.name,subtopic.description)
    chat_prompt = Chat()
    chat_prompt.learner = context['learner']
    chat_prompt.message = start_prompt
    chat_prompt.msg_type = "info"
    chat_prompt.from_ai = True
    chat_prompt.subtopic = subtopic
    chat_prompt.save()
    learning_info = LearningInformation()
    learning_info.chat = chat_prompt
    learning_info.information = start_prompt
    learning_info.save()
    createHelpPrompt(subtopic,context)

def createQuestions(subtopic:SubTopic,context,**kwargs):
    print("creating question prompt")
    response = get_questions_related_to_information(subtopic.name,subtopic.description,kwargs.get('info').information)
    try:
        questions = json.loads(response)
        questions_list = [q['question'] for q in questions]
        for question in questions_list:
            new_q = Question()
            new_q.content = question
            new_q.information = kwargs.get('info')
            new_q.save()
        print(questions_list)
    except:
        questions_list = []
    print(questions_list)
    return questions_list

def createQuestionPrompt(subtopic:SubTopic,context,**kwargs):
    print("creating question prompt")
    start_prompt = kwargs.get('question',"Dummy Question")
    chat_prompt = Chat()
    chat_prompt.learner = context['learner']
    chat_prompt.message = start_prompt
    chat_prompt.msg_type = "question"
    chat_prompt.from_ai = True
    chat_prompt.subtopic = subtopic
    chat_prompt.save()
    createHelpPrompt(subtopic,context,message="You can answer the question using the /answer prompt. After that your answer will be evaluated")

def createLearnerPrompt(subtopic:SubTopic,context,**kwargs):
    # msg prompt containing user's response / command
    print("creating Learner prompt")
    start_prompt = kwargs.get('input',"Default")
    chat_prompt = Chat()
    chat_prompt.learner = context['learner']
    chat_prompt.message = start_prompt
    chat_prompt.msg_type = "command_from_user"
    chat_prompt.from_ai = False
    chat_prompt.subtopic = subtopic
    chat_prompt.save()
    # createHelpPrompt(subtopic,context)


def createAnswerPrompt(subtopic:SubTopic,context,**kwargs):
    print("creating Answer prompt")
    start_prompt = kwargs.get('response',"Some error occurred")
    chat_prompt = Chat()
    chat_prompt.learner = context['learner']
    chat_prompt.message = start_prompt
    chat_prompt.msg_type = "answer"
    chat_prompt.from_ai = True
    chat_prompt.subtopic = subtopic
    chat_prompt.save()
    createHelpPrompt(subtopic,context,message="You can use the /start commmand to answer more questions or the /evaluate command to evaluate your progress")

def is_answer_correct_ques(subtopic:SubTopic,context,question:Question):
    response  = is_this_answer_correct(subtopic.name,subtopic.description,question.content,question.answer_response)
    print(response)
    if 'yes' in  str(response).lower():
        createAnswerPrompt(subtopic,context,response=response)
        return True
    createAnswerPrompt(subtopic,context,response=response)
    return False