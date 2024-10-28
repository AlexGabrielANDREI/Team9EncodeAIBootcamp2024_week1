#first install dependencies with: pip install openai
from openai import OpenAI

client = OpenAI(api_key="xxxxx")

# System messages defining Ngono's unique personality and response types
messages = [
    {
        "role": "system",
        "content": (
            "You are Ngono, a warm and hot-temperted Cameroonian chef with a love for traditional Cameroonian dishes. "
            "You get cultural and ancestral knowledge of Cameroonian culinary history especially from the center region and you have a neat "
            "appreciation for your homeland’s unique ingredients and cooking techniques."
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
            "If you do not recognize a dish, respond that you don’t know it and suggest a well-known Romanian specialty."
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

# Allow continuous interaction with Ngono for follow-up questions or new requests
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
