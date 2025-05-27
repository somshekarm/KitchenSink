import os
import json
import requests
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv(override=True)

def push(text):    
    requests.post("https://api.pushover.net/1/messages.json", data=
        {
        "user": os.getenv("PUSHOVER_USER_KEY"), 
        "token": os.getenv("PUSH_OVER_API_KEY"), 
        "message": text
        })
    
    
def record_user_detail(email, name="unknown name", message="unknown message"):
    push(f"Recording detail from {name} with email {email} has message : {message}")
    return {"recorded":"ok"}


def record_user_question(question):
    push(f"Recording {question} that was asked to me and I am not able to answer it.")
    return {"recorded": "ok"}   

record_user_detail_json = {
    "name":"record_user_detail",
    "description":"Provides user details with name, email and notes",
    "parameters": {
        "type": "object",
        "properties":{
            "email": {
                "type": "string",
                "description": "email of the user"
            },
            "name":{
                "type": "string",
                "description": "name of the user"
            },
            "message":{
                "type": "string",
                "description": "message provided by user"
            }
        },
        "required": ["email"],
        "additionalProperties": False                
    }
}

record_user_question_json = {
    "name": "record_user_question",
    "description": "Records a question or notes from user",
    "parameters": {
        "type": "object",
        "properties":{
            "question":{
            "type": "string",
            "description": "Question or notes from a user"
        },                    
        },        
    },
    "required":["question"],
    "additionalProperties": False
}

tools = [
    {"type": "function", "function": record_user_detail_json},
    {"type": "function", "function": record_user_question_json}
]



class Me:
    def __init__(self):
        self.openai = OpenAI()
        self.name = "Soma"
        self.my_profile = ""
        reader = PdfReader("me/Somashekhar_Muniyappa_TX.pdf")
        for pages in reader.pages:
            text = pages.extract_text()
            if text:
                self.my_profile += text
        with open("me/Somashekhar_Muniyappa_TX_summary.txt", "r", encoding="utf-8") as s:
            self.summary = s.read()
    
    def handle_tool_calls(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name        
            arguments = json.loads(tool_call.function.arguments) 
            print(f"Tool Called -> {tool_name}")
            print(f"Arguments -> {arguments}")
            if tool_name == "record_user_question":
                result = record_user_question(**arguments)
            elif tool_name == "record_user_detail":
                result = record_user_detail(**arguments)                          
            
            results.append({"role":"tool", "content": json.dumps(result, default=str), "tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
            particularly questions related to {self.name}'s career, background, skills and experience. \
            Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
            You are given a summary of {self.name}'s background and resume which you can use to answer questions. \
            Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
            If you don't know the answer to any question, use your record_user_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
            Respond to user saying {self.name} is alerted about this question and stop conversation by adding stop to finish_reason\
            If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email, name and a message to record it using your record_user_detail tool. \
            Respond to user saying {self.name} is alerted with your email and stop conversation by adding stop to finish_reason"

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## Resume:\n{self.my_profile}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        max_iteration = 1
        iteration = 0
        print(f"Dumps--->  {json.dumps(tools)}") 
        while not done and iteration <= max_iteration: 
            print("Starting---->")       
            response = self.openai.chat.completions.create(model= "gpt-4o-mini", messages= messages, tools = tools)
            print("Got response -->>")
            finish_reason = response.choices[0].finish_reason 
            print(f"Finish Reason -> {finish_reason}")      
            iteration += 1
            if finish_reason=="tool_calls":            
                message = response.choices[0].message            
                tool_calls = message.tool_calls
                results = self.handle_tool_calls(tool_calls)
                messages.append(message)
                messages.extend(results) 
            else:
                done = True   
        return response.choices[0].message.content
        

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()
