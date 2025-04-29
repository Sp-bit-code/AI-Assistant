import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from Frontend.Graphics.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)


# Ab modules import karo
from backend.Model import FirstLayerDMM
from backend.RealTimeSeachEngine import RealtimeSearchEngine
from backend.Automation import Automation
from backend.SpeechToText import SpeechRecognition
from backend.TextToSpeech import TextToSpeech
from backend.Chatbot import ChatBot
from Frontend.Graphics.GUI import GraphicalUserInterface
from PyQt5.QtWidgets import QApplication
import time
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
import webbrowser
import requests


sys.path.append(r"C:\Users\LENOVO\Desktop\c++\jarvis\backend")
sys.path.append(r"C:\Users\LENOVO\Desktop\c++\jarvis\Frontend\Graphics")
sys.path.append(r"C:\Users\LENOVO\Desktop\c++\jarvis\backend\Model.py")
sys.path.append(r"C:\Users\LENOVO\Desktop\c++\jarvis\backend\RealTimeSeachEngine.py")
sys.path.append(r"C:\Users\LENOVO\Desktop\c++\jarvis\backend\Automation.py")
sys.path.append(r"C:\Users\LENOVO\Desktop\c++\jarvis\backend\SpeechToText.py")
sys.path.append(r"C:\Users\LENOVO\Desktop\c++\jarvis\backend\TextToSpeech.py")
sys.path.append(r"C:\Users\LENOVO\Desktop\c++\jarvis\backend\Chatbot.py")
sys.path.append(r"C:\Users\LENOVO\Desktop\c++\jarvis\Frontend\Graphics\GUI2.py")
TempDirectoryPath = r'C:\Users\LENOVO\Desktop\c++\jarvis\Frontend\Files'

env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")  # Default value if None
Assistantname = env_vars.get("Assistantname", "Assistant")  # Default value if None

DefaultMessage = f"{Username}: Hello {Assistantname}, How are you?\n{Assistantname}: Welcome {Username}. I am doing well. How may I help you?"

subprocesses = []
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]
def ShowDefaultChatIfNoChats():
    with open(r'Data\ChatLog.json', "r", encoding='utf-8') as file:
        if len(file.read()) < 5:
            with open(os.path.join(TempDirectoryPath, 'Database.data'), 'w', encoding='utf-8') as file:
                file.write("")
            with open(os.path.join(TempDirectoryPath, 'Responses.data'), 'w', encoding='utf-8') as file:
                file.write(DefaultMessage)

def ReadChatLogJson():
    with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User", Username)
    formatted_chatlog = formatted_chatlog.replace("Assistant", Assistantname)
    with open(os.path.join(TempDirectoryPath, 'Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    with open(os.path.join(TempDirectoryPath, 'Database.data'), "r", encoding="utf-8") as file:
        data = file.read()
    if len(str(data)) > 0:
        lines = data.split('\n')
        result = '\n'.join(lines)
    with open(os.path.join(TempDirectoryPath, 'Responses.data'), "w", encoding="utf-8") as file:
        file.write(result)

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

InitialExecution()

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""
    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    ShowTextToScreen(f"{Username}: {Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)
    print(f"\nDecision: {Decision}\n")
    
    G = [i for i in Decision if i.startswith("general")]
    R = [i for i in Decision if i.startswith("realtime")]
    Mearged_query = " and ".join(["".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")])
    
    for queries in Decision:
        if "generate" in queries:
            ImageGenerationQuery = queries.split("generate", 1)[1].strip()
            ImageExecution=True
    if not TaskExecution:
        if any(queries.startswith(func) for func in Functions):
            run(Automation(list(Decision)))
            TaskExecution = True
    if ImageExecution:
        try:
            with open(os.path.join(TempDirectoryPath, 'ImageGeneration.data'), "w") as file:
                file.write(f"{ImageGenerationQuery},True")
            p1 = subprocess.Popen(['python', r'Backend\ImageGeneration.py'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, 
                                  stdin=subprocess.PIPE, 
                                  shell=False)
            subprocesses.append(p1)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")


    
    if G and R:
        SetAssistantStatus("Searching...")
        Answer = RealtimeSearchEngine(QueryModifier(Mearged_query))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
        return True
    else:
        for Queries in Decision:
            if "general" in Queries:
                SetAssistantStatus("Thinking...")
                QueryFinal = Queries.replace("general", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            elif "realtime" in Queries:
                SetAssistantStatus("Searching...")
                QueryFinal = Queries.replace("realtime", "")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            elif "exit" in Queries:
                QueryFinal = "Okay, Bye!"
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                os._exit(1)

exit_flag = False  # Global flag to stop threads
subprocesses = []  # Store subprocess references

def FirstThread():
    global exit_flag
    while not exit_flag:
        CurrentStatus = GetMicrophoneStatus()
        if CurrentStatus == "True":
            MainExecution()
        else:
            AIStatus = GetAssistantStatus()
            if "Available..." in AIStatus:
                time.sleep(0.1)
            else:
                SetAssistantStatus("Available...")

if __name__ == "__main__":
    try:
        thread2 = threading.Thread(target=FirstThread, daemon=True)
        thread2.start()
        p1 = subprocess.Popen(
            ['python', r'Backend\ImageGeneration.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            shell=False
        )
        subprocesses.append(p1)
        app = QApplication([])
        GraphicalUserInterface()
        app.exec_()
    except KeyboardInterrupt:
        exit_flag = True 
        print("Exiting...")
    finally:
        for p in subprocesses:
            if p.poll() is None: 
                p.terminate()
                p.wait()
        print("All processes and threads stopped.")
