# import google.generativeai as genai
# import textwrap
# from IPython.display import display
# from IPython.display import Markdown


# genai.configure(api_key="AIzaSyAHiCu34AQ9yabPeDkAAq4VE2fDqRnAZlA")
# model = genai.GenerativeModel('gemini-pro')
# def TextGenerator(full_prompt):
#     response = model.generate_content(full_prompt)
#     print(full_prompt)
#     return response.text

import google.generativeai as genai
from IPython.display import display, Markdown

genai.configure(api_key="AIzaSyAHiCu34AQ9yabPeDkAAq4VE2fDqRnAZlA")
model = genai.GenerativeModel('gemini-pro')

def TextGenerator(question):
    prompt = f"User: {question}\nChatbot:"
    response = model.generate_content(prompt)
    print(prompt)
    return response.text



# subject = "cricket"
# question = "who won the ICC cricket World cup in 2019 ?"
# performance = "Basic"

# def generate_prompt(subject, question , performace):
#     prompt = f"User: In the subject of {subject}, I have a question.\n"
#     prompt += f"User: {question}\n"
#     prompt += f"User: My understanding level is {performace} .write the answer in html code\n"
#     prompt += "Chatbot:"
    
#     return prompt

# full_prompt = generate_prompt(subject,question,performance)

# text= TextGenerator(full_prompt)

# print(text)