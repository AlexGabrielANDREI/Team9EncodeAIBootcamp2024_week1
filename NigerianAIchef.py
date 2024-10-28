from openai import OpenAI
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Get the API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# System messages defining Ion's unique personality and response types
messages = [
    {
        "role": "system",
        "content": (
            "You are Ayo, a lively and passionate Nigerian chef who loves to introduce people to the bold, diverse flavors of Nigerian cuisine. "
                   "You share traditional recipes, cultural stories, and cooking tips with warmth and excitement, aiming to bring the vibrant spirit of "
                   "Nigeria into every dish. You have deep knowledge of ingredients like yams, plantains, and a variety of Nigerian spices, and you enjoy "
                   "guiding people to create authentic and flavorful dishes that reflect the rich heritage of Nigeria."
        ),
    },
    {
        "role": "system",
        "content": (
            "Respond to the user depending on their input:\n"
            "a. For ingredient-based dish suggestions: Provide only a list of dish names based on ingredients.\n"
            "b. For specific recipe requests: Give a detailed recipe with preparation steps.\n"
            "c. For critiques and improvement suggestions: Provide a constructive critique with tips for refining the dish."
        ),
    },
    {
        "role": "system",
        "content": (
            "If you do not recognize a dish, respond that you don’t know it and suggest a well-known Nigerian specialty."
        ),
    }
]

# Ask the user for the type of input they want to make
request_type = input("Choose your request type (a: Ingredient-based dish suggestions, b: Specific recipe request, c: Recipe critique): ").strip().lower()

# Handle user input according to their choice
if request_type == 'a':
    ingredients = input("List the ingredients you have (comma-separated):\n")
    messages.append({
        "role": "user",
        "content": f"Suggest dishes based on these ingredients: {ingredients}",
    })
elif request_type == 'b':
    dish = input("Enter the name of the dish you want a recipe for:\n")
    messages.append({
        "role": "user",
        "content": f"Please provide a detailed recipe for {dish}",
    })
elif request_type == 'c':
    critique_dish = input("Enter the name of the dish you want feedback on:\n")
    messages.append({
        "role": "user",
        "content": f"Please provide a critique and suggestions for improving {critique_dish}",
    })
else:
    print("Invalid choice. Please select a, b, or c.")
    exit()

# Run the completion stream based on the user's input
model = "gpt-4o-mini"

stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)

collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

messages.append({"role": "system", "content": "".join(collected_messages)})

# Allow continuous interaction with Ion for follow-up questions or new requests
while True:
    print("\n")
    user_input = input("You can ask a follow-up question or enter a new request:\n")
    messages.append({"role": "user", "content": user_input})
    
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)
    
    messages.append({"role": "system", "content": "".join(collected_messages)})
