





# import os
# import json
# import subprocess
# import asyncio
# import streamlit as st
# from dotenv import dotenv_values

# # Import backend modules
# from backend.Model import FirstLayerDMM
# from backend.RealTimeSeachEngine import RealtimeSearchEngine
# from backend.Automation import Automation  # This is async
# from backend.SpeechToText import SpeechRecognition
# from backend.TextToSpeech import TextToSpeech
# from backend.Chatbot import ChatBot

# # Utility functions (simulate GUI status setters for Streamlit)
# def set_assistant_status(status):
#     st.session_state.assistant_status = status

# def get_assistant_status():
#     return st.session_state.get("assistant_status", "Available...")

# def set_microphone_status(status):
#     st.session_state.microphone_status = status

# def get_microphone_status():
#     return st.session_state.get("microphone_status", "False")

# # Paths and names
# env_vars = dotenv_values(".env")
# Username = env_vars.get("Username", "User")
# Assistantname = env_vars.get("Assistantname", "Assistant")

# TempDirectoryPath = r'C:\Users\LENOVO\Desktop\c++\jarvis\Frontend\Files'
# DefaultMessage = f"{Username}: Hello {Assistantname}, How are you?\n{Assistantname}: Welcome {Username}. I am doing well. How may I help you?"

# # Initialize chat log JSON path
# chat_log_path = 'Data/ChatLog.json'

# # Functions for chat management
# def initialize_chat_log():
#     if not os.path.exists(chat_log_path) or os.path.getsize(chat_log_path) < 5:
#         os.makedirs(os.path.dirname(chat_log_path), exist_ok=True)
#         with open(os.path.join(TempDirectoryPath, 'Database.data'), 'w', encoding='utf-8') as file:
#             file.write("")
#         with open(os.path.join(TempDirectoryPath, 'Responses.data'), 'w', encoding='utf-8') as file:
#             file.write(DefaultMessage)
#         with open(chat_log_path, 'w', encoding='utf-8') as file:
#             json.dump([], file)

# def read_chat_log():
#     try:
#         with open(chat_log_path, 'r', encoding='utf-8') as file:
#             return json.load(file)
#     except Exception:
#         return []

# def chat_log_integration():
#     json_data = read_chat_log()
#     formatted_chatlog = ""
#     for entry in json_data:
#         role = Username if entry["role"] == "user" else Assistantname
#         formatted_chatlog += f"{role}: {entry['content']}\n"
#     with open(os.path.join(TempDirectoryPath, 'Database.data'), 'w', encoding='utf-8') as file:
#         file.write(formatted_chatlog)

# def show_chats_on_gui():
#     try:
#         with open(os.path.join(TempDirectoryPath, 'Database.data'), "r", encoding="utf-8") as file:
#             return file.read()
#     except Exception:
#         return ""

# # Initialize session state variables
# if "assistant_status" not in st.session_state:
#     set_assistant_status("Available...")

# if "microphone_status" not in st.session_state:
#     set_microphone_status("False")

# if 'clear_input' not in st.session_state:
#     st.session_state.clear_input = False

# # Clear input if flag is set before widget creation
# if st.session_state.clear_input:
#     st.session_state.user_input = ""
#     st.session_state.clear_input = False

# initialize_chat_log()
# chat_log_integration()

# # Streamlit UI Start
# st.title(f"{Assistantname} - Your Virtual Assistant")
# st.markdown(
#     "Interact with your assistant by typing below or using the microphone (if implemented). "
#     "**For the web version, the mic option is not working; kindly type your query.** "
#     "**If you refresh, you can retype your query.**"
# )

# # Display Assistant Status
# st.markdown(f"**Assistant Status:** {get_assistant_status()}")

# # Microphone toggle (simulate)
# mic_toggle = st.checkbox("Microphone On/Off", value=(get_microphone_status() == "True"))
# set_microphone_status("True" if mic_toggle else "False")

# # Container for videos and GitHub link with layout to position videos close to border left and right
# video_container = st.container()
# with video_container:
#     col1, midspace, col2 = st.columns([12,1,12], gap="medium")

#     with col1:
#         st.markdown("### Actual Model Demo Video")
#         st.video("https://youtu.be/f1s8T5eC1AY", format="video/mp4", start_time=0)
#     with col2:
#         st.markdown("### Explanation of Project")
#         st.video("https://youtu.be/edf8hZT0mxk", format="video/mp4", start_time=0)

# st.markdown(
#     "[GitHub Repository](https://github.com/your_github_repo_link)  \n"
#     "_Click the link above to view the project source code._"
# )

# # Display chat history in a text area (read only)
# chat_history = show_chats_on_gui()
# st.text_area("Chat History", value=chat_history, height=300, disabled=True)

# # Select box for predefined query options plus free text input
# query_options = [
#     "Play music \"NAME\"",
#     "Generate image \"QUERY\"",
#     "Write a code of \"NAME\"",
#     "LinkedIn AI \"Name of Person\"",
#     "Other (Type your own query)"
# ]

# selected_query = st.selectbox("Select a query or choose Other to type your own:", query_options)
# user_input = ""

# if selected_query != "Other (Type your own query)":
#     user_input = selected_query
# else:
#     user_input = st.text_input("Your Query:", key="user_input")

# # Placeholder for responses
# response_placeholder = st.empty()

# # Processing logic for user input on submit button
# if st.button("Send") and user_input.strip():
#     set_assistant_status("Thinking...")
#     response_placeholder.text(f"{Username}: {user_input}")

#     Decision = FirstLayerDMM(user_input)
#     general_decisions = [i for i in Decision if i.startswith("general")]
#     realtime_decisions = [i for i in Decision if i.startswith("realtime")]
#     functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

#     image_generation_query = ""
#     image_execution = False
#     for q in Decision:
#         if "generate" in q:
#             image_generation_query = q.split("generate", 1)[1].strip()
#             image_execution = True

#     task_executed = False
#     if any(q.startswith(func) for q in Decision for func in functions) and not task_executed:
#         # Run async Automation in sync context
#         asyncio.run(Automation(list(Decision)))
#         task_executed = True

#     if image_execution:
#         try:
#             with open(os.path.join(TempDirectoryPath, 'ImageGeneration.data'), "w") as file:
#                 file.write(f"{image_generation_query},True")
#             p = subprocess.Popen(['python', r'Backend\\ImageGeneration.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
#             st.info("Image generation started... Check outputs.")
#         except Exception as e:
#             st.error(f"Error launching image generation: {e}")

#     merged_query = " and ".join([q.split(maxsplit=1)[1] if len(q.split(maxsplit=1)) > 1 else "" for q in Decision if q.startswith("general") or q.startswith("realtime")])

#     answer = ""
#     if general_decisions and realtime_decisions:
#         set_assistant_status("Searching...")
#         answer = RealtimeSearchEngine(merged_query)
#     else:
#         for q in Decision:
#             if "general" in q:
#                 set_assistant_status("Thinking...")
#                 query_final = q.replace("general", "")
#                 answer = ChatBot(query_final)
#                 break
#             elif "realtime" in q:
#                 set_assistant_status("Searching...")
#                 query_final = q.replace("realtime", "")
#                 answer = RealtimeSearchEngine(query_final)
#                 break
#             elif "exit" in q:
#                 answer = "Okay, Bye!"
#                 set_assistant_status("Answering...")
#                 response_placeholder.text(f"{Assistantname}: {answer}")
#                 TextToSpeech(answer)
#                 st.stop()

#     if answer:
#         set_assistant_status("Answering...")
#         response_placeholder.text(f"{Assistantname}: {answer}")
#         TextToSpeech(answer)

#         chat_log = read_chat_log()
#         chat_log.append({"role": "user", "content": user_input})
#         chat_log.append({"role": "assistant", "content": answer})
#         with open(chat_log_path, 'w', encoding='utf-8') as file:
#             json.dump(chat_log, file, indent=2)

#         chat_log_integration()

#     set_assistant_status("Available...")

#     # Set flag to clear input on next run
#     st.session_state.clear_input = True

# st.markdown("---")
# st.markdown("© Your Assistant powered by Streamlit")
import os
import json
import subprocess
import asyncio
import streamlit as st
from dotenv import dotenv_values

# 🔧 Commented Backend Modules for now
# from backend.Model import FirstLayerDMM
# from backend.RealTimeSeachEngine import RealtimeSearchEngine
# from backend.Automation import Automation
# from backend.SpeechToText import SpeechRecognition
# from backend.TextToSpeech import TextToSpeech
# from backend.Chatbot import ChatBot

# ✅ Debug message to confirm app loads
st.write("✅ App started... Streamlit is working!")

# --- Utility session state setup ---
def set_assistant_status(status):
    st.session_state.assistant_status = status

def get_assistant_status():
    return st.session_state.get("assistant_status", "Available...")

def set_microphone_status(status):
    st.session_state.microphone_status = status

def get_microphone_status():
    return st.session_state.get("microphone_status", "False")

# --- Environment setup ---
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")
# Deployment-safe relative path
BASE_DIR = os.path.dirname(__file__)
TempDirectoryPath = os.path.join(BASE_DIR, 'Frontend', 'Files')
DefaultMessage = f"{Username}: Hello {Assistantname}, How are you?\n{Assistantname}: Welcome {Username}. I am doing well. How may I help you?"

chat_log_path = 'Data/ChatLog.json'

# --- Chat management ---
def initialize_chat_log():
    if not os.path.exists(chat_log_path) or os.path.getsize(chat_log_path) < 5:
        os.makedirs(os.path.dirname(chat_log_path), exist_ok=True)
        with open(os.path.join(TempDirectoryPath, 'Database.data'), 'w', encoding='utf-8') as file:
            file.write("")
        with open(os.path.join(TempDirectoryPath, 'Responses.data'), 'w', encoding='utf-8') as file:
            file.write(DefaultMessage)
        with open(chat_log_path, 'w', encoding='utf-8') as file:
            json.dump([], file)

def read_chat_log():
    try:
        with open(chat_log_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        return []

def chat_log_integration():
    json_data = read_chat_log()
    formatted_chatlog = ""
    for entry in json_data:
        role = Username if entry["role"] == "user" else Assistantname
        formatted_chatlog += f"{role}: {entry['content']}\n"
    with open(os.path.join(TempDirectoryPath, 'Database.data'), 'w', encoding='utf-8') as file:
        file.write(formatted_chatlog)

def show_chats_on_gui():
    try:
        with open(os.path.join(TempDirectoryPath, 'Database.data'), "r", encoding="utf-8") as file:
            return file.read()
    except Exception:
        return ""

# --- Streamlit session states ---
if "assistant_status" not in st.session_state:
    set_assistant_status("Available...")

if "microphone_status" not in st.session_state:
    set_microphone_status("False")

if 'clear_input' not in st.session_state:
    st.session_state.clear_input = False

if st.session_state.clear_input:
    st.session_state.user_input = ""
    st.session_state.clear_input = False

initialize_chat_log()
chat_log_integration()

# --- Streamlit UI ---
st.title(f"{Assistantname} - Your Virtual Assistant")

st.markdown(
    "Interact with your assistant by typing below or using the microphone (if implemented). "
    "**For the web version, the mic option is not working; kindly type your query.** "
    "**If you refresh, you can retype your query.**"
)

st.markdown(f"**Assistant Status:** {get_assistant_status()}")

mic_toggle = st.checkbox("Microphone On/Off", value=(get_microphone_status() == "True"))
set_microphone_status("True" if mic_toggle else "False")

video_container = st.container()
with video_container:
    col1, _, col2 = st.columns([12,1,12], gap="medium")

    with col1:
        st.markdown("### Actual Model Demo Video")
        st.video("https://youtu.be/f1s8T5eC1AY", format="video/mp4", start_time=0)
    with col2:
        st.markdown("### Explanation of Project")
        st.video("https://youtu.be/edf8hZT0mxk", format="video/mp4", start_time=0)

st.markdown(
    "[GitHub Repository](https://github.com/your_github_repo_link)  \n"
    "_Click the link above to view the project source code._"
)

chat_history = show_chats_on_gui()
st.text_area("Chat History", value=chat_history, height=300, disabled=True)

query_options = [
    "Play music \"NAME\"",
    "Generate image \"QUERY\"",
    "Write a code of \"NAME\"",
    "LinkedIn AI \"Name of Person\"",
    "Other (Type your own query)"
]

selected_query = st.selectbox("Select a query or choose Other to type your own:", query_options)
user_input = "" if selected_query == "Other (Type your own query)" else selected_query
if selected_query == "Other (Type your own query)":
    user_input = st.text_input("Your Query:", key="user_input")

response_placeholder = st.empty()

if st.button("Send") and user_input.strip():
    set_assistant_status("Thinking...")
    response_placeholder.text(f"{Username}: {user_input}")
    
    # ⚠️ Actual logic is disabled temporarily
    st.info("Backend modules are disabled right now. This is a test run.")

    assistant_reply = "This is a placeholder reply. Backend not active."
    set_assistant_status("Answering...")
    response_placeholder.text(f"{Assistantname}: {assistant_reply}")

    chat_log = read_chat_log()
    chat_log.append({"role": "user", "content": user_input})
    chat_log.append({"role": "assistant", "content": assistant_reply})
    with open(chat_log_path, 'w', encoding='utf-8') as file:
        json.dump(chat_log, file, indent=2)
    chat_log_integration()

    set_assistant_status("Available...")
    st.session_state.clear_input = True

st.markdown("---")
st.markdown("© Your Assistant powered by Streamlit")
