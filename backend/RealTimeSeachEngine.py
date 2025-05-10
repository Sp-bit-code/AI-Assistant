from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
import webbrowser
from dotenv import dotenv_values

# Load environment variables from the env file.
env_vars = dotenv_values(".env")

# Retrieve environment variables for the chatbot configuration.
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize the Groq client with the provided API key.
client = Groq(api_key=GroqAPIKey)

# Define the system instructions for the chatbot.
System = """Your system instructions here."""

# Try to load the chat log from a JSON file, or create an empty one if it doesn't exist.
try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)
    messages = []

# Function to perform a Google search and format the results.
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    Answer += "[end]"
    return Answer

# Function to clean up the answer by removing empty lines.
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

# Predefined chatbot conversation system message and an initial user message.
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you?"}
]

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

# List of LinkedIn AI command variants to check against (case-sensitive)
linkedin_ai_variants = [
    "LinkedIn AI", "LinkedIn Ai", "LinkedIn ai", "Linkedin AI", "Linkedin Ai", "Linkedin ai",
    "linkedin AI", "linkedin Ai", "linkedin ai", "linkedIn AI", "linkedIn Ai", "linkedIn ai",
    "LINKEDIN AI", "LINKEDIN Ai", "LINKEDIN ai", "LiNkEdIn AI", "LiNkEdIn Ai", "LiNkEdIn ai",
    "LinkedIn aI", "linkedIN ai"
]

def LinkedInSearch(query):
    # Define titles to remove
    titles_to_remove = ["sir", "ma'am", "maam", "mr", "ms", "mrs", "dr", "professor", "teacher"]

    # Remove titles from the query
    for title in titles_to_remove:
        query = query.replace(title, "").strip()

    # Check if the query starts with any of the LinkedIn AI command variants
    matched_variant = None
    for variant in linkedin_ai_variants:
        if variant in query:
            matched_variant = variant
            break

    if matched_variant:
        # Remove the matched variant from the query to get the search terms
        search_query = query.replace(matched_variant, "").strip()
        linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={'+'.join(search_query.split())}"

        try:
            webbrowser.open(linkedin_url)
            return f"Results opened for LinkedIn search: {search_query}"
        except Exception as e:
            return f"❌ Failed to open LinkedIn search: {e}"

    return "Please say a valid command like 'LinkedIn AI ...'."

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Check for any of the LinkedIn AI variants in the prompt
    if any(variant in prompt for variant in linkedin_ai_variants):
        return LinkedInSearch(prompt)
    # For other queries, proceed with the usual flow
    # Load the chat log from the JSON file.
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})
    
    # Add Google search results to the system chatbot messages.
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})
    
    # Generate a response using the Groq client.
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
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
    # Clean up the response.
    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})
    
    # Save the updated chat log back to the JSON file.
    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)
    
    # Remove the most recent system message from the chatbot conversation.
    SystemChatBot.pop()
    
    return AnswerModifier(Answer)

# Main entry point of the program for interactive querying.
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))


