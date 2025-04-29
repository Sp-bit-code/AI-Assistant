from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
import webbrowser
import google.generativeai as genai

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")

# Retrieve environment variables for the chatbot configuration.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistant.name")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client with the provided API key.
client = Groq(api_key=GroqAPIKey)

# Define the system instructions for the chatbot.
System = f"""
Hello, I am {Username}. You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time access.
Provide answers in a professional way, making sure to use proper grammar, punctuation, and sentence structure.
Just answer the question from the provided data professionally.
"""

# Try to load the chat log from a JSON file, or create an empty one if it doesn't exist.
try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    messages = []
    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f)

# Function to perform a Google search and format the results.
def GoogleSearch(query):
    # Define titles to remove
    titles_to_remove = ["sir", "ma'am", "maam", "mr", "ms", "mrs", "dr", "professor", "teacher"]
    
    # Remove titles from the query
    for title in titles_to_remove:
        query = query.replace(title, "").strip()
    
    # Handle LinkedIn AI commands with case insensitivity
    if any(keyword in query.lower() for keyword in ["linkedin ai", "linkedin Ai", "LinkedIn ai", "LinkedIn Ai", "Linkedin ai", "Linkedin Ai"]):
        search_query = query.lower().replace("linkedin ai", "").strip()
        linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={'+'.join(search_query.split())}"
        try:
            webbrowser.open(linkedin_url)  # Open the LinkedIn URL in the browser
            return f"Results opened for LinkedIn search: {search_query}"  # Return a string message
        except Exception as e:
            return f"❌ Failed to open LinkedIn search: {e}"

    # For everything else, open Google search
    elif "google search" in query.lower():
        search_query = query.lower().replace("google search", "").strip()
        google_url = f"https://www.google.com/search?q={'+'.join(search_query.split())}"
        try:
            webbrowser.open(google_url)  # Open the Google search URL in the browser
            return f"Results opened for Google search: {search_query}"  # Return a string message
        except Exception as e:
            return f"❌ Failed to open Google search: {e}"

    else:
        return "Please say a valid command like 'Google search ...' or 'LinkedIn AI ...'."

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Function to get real-time information like the current date and time.
def Information():
    data = ""
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    
    return data

# Function to handle real-time search and response generation.
def RealtimeSearchEngine(prompt):
    global messages
    
    # Load the chat log from the JSON file.
    with open(r"Data/ChatLog.json", "r") as f:
        messages = load(f)
    
    messages.append({"role": "user", "content": f"{prompt}"})
    
    # Check if the prompt is for LinkedIn or Google search
    if "linkedin ai" in prompt.lower() or "google search" in prompt.lower():
        search_result = GoogleSearch(prompt)  # Handle the search directly
        return search_result  # Return the search result directly without API call

    # If not a search query, proceed with API call
    SystemChatBot = [
        {"role": "system", "content": System},
        {"role": "user", "content": prompt}
    ]
    
    SystemChatBot.append({"role": "system", "content": "Processing your request..."})
    
    # Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )
    
    Answer = ""
    # Concatenate response chunks from the streaming output.
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content
            Answer = Answer.strip().replace("</s>", "")
    
    messages.append({"role": "assistant", "content": Answer})
    
    # Save the updated chat log back to the JSON file.
    with open(r"Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)
    
    return AnswerModifier(Answer=Answer)

# genai.configure(api_key="AIzaSyA8ytWEsTbt-gkOFeovJjsH3MLjryp31bo")

# # Load the Gemini model (choose version accordingly)
# client = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-1.5-pro

# def RealtimeSearchEngine(prompt):
#     global messages

#     # Load chat history
#     with open(r"Data/ChatLog.json", "r") as f:
#         messages = load(f)

#     # Add user's prompt to messages
#     messages.append({"role": "user", "content": f"{prompt}"})

#     # Check if the prompt is for a search query (LinkedIn or Google search)
#     if "linkedin ai" in prompt.lower() or "google search" in prompt.lower():
#         search_result = GoogleSearch(prompt)  # Make sure GoogleSearch function is defined elsewhere
#         return search_result  # Return the search result directly without calling the API

#     # Prepare the system and user context for Gemini model
#     SystemChatBot = [
#         {"role": "system", "content": "System initialization..."},
#         {"role": "user", "content": prompt},
#         {"role": "system", "content": "Processing your request..."}
#     ]

#     # Convert all messages into a prompt string for Gemini
#     prompt_text = ""
#     for message in SystemChatBot + [{"role": "system", "content": "Information Request"}] + messages:
#         role = message.get("role", "user")
#         content = message.get("content", "")
#         prompt_text += f"{role}: {content}\n"

#     # Generate response from the Gemini model
#     completion = client.generate_content(
#         prompt_text,
#         generation_config=genai.types.GenerationConfig(
#             temperature=0.7,
#             max_output_tokens=2048,
#             top_p=1.0,
#             stop_sequences=[]
#         )
#     )

#     Answer = completion.text.strip().replace("</s>", "")  # Clean the response

#     # Append the assistant's reply to the messages list
#     messages.append({"role": "assistant", "content": Answer})

#     # Save the updated chat history back to the JSON file
#     with open(r"Data/ChatLog.json", "w") as f:
#         dump(messages, f, indent=4)

#     return Answer  # Return the generated answer (if you need further modifications, let me know)

# Main entry point of the program for interactive querying.
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))