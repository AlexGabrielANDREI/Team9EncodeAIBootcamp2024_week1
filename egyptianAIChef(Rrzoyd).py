from openai import OpenAI

client = OpenAI(api_key="xxxxxxxxxxxxxxxxxxxxxxxxx")

# System message with Egyptian Grandma Chef Personality
messages = [
    {
        "role": "system",
        "content": (
            "You are an experienced Egyptian grandma, a warm and skilled home-cook. "
            "You have a vast knowledge of Egyptian recipes, techniques, and flavors, "
            "and you're especially familiar with traditional dishes. You love to share the secrets "
            "behind making these meals perfect and enjoy helping others with your cooking wisdom. "
            "You respond to three types of requests:\n\n"
            "1. **Ingredient-based dish suggestions**: Suggest dishes only by name, without full recipes.\n"
            "2. **Recipe requests for specific dishes**: Provide a detailed recipe with preparation steps.\n"
            "3. **Recipe critiques and improvement suggestions**: Offer constructive critique and suggestions.\n\n"
            "If the request does not match these scenarios, politely explain that you can only respond "
            "to one of the valid requests listed above."
        ),
    }
]

# Initial User Prompt
dish = input("Type your request (dish name, ingredients, or a recipe critique):\n")
messages.append({"role": "user", "content": dish})

# Process User Input based on Scenarios
if "ingredients" in dish.lower():  # Ingredient-based suggestions
    messages.append({"role": "system", "content": "Suggest dishes only by name based on the ingredients provided."})
elif "recipe for" in dish.lower():  # Specific dish request
    messages.append({"role": "system", "content": f"Provide a detailed recipe for {dish}."})
elif "critique" in dish.lower():  # Recipe critique
    messages.append({"role": "system", "content": "Offer a constructive critique with suggestions to improve the recipe."})
else:
    print("Please ask for a dish suggestion by ingredients, a specific recipe, or a recipe critique.")

model = "gpt-4o-mini"

# Streaming Response
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

# Continuous Interaction with AI Chef
while True:
    print("\n")
    user_input = input()
    messages.append({"role": "user", "content": user_input})

    # Logic to determine type of response based on input
    if "ingredients" in user_input.lower():
        messages.append({"role": "system", "content": "Suggest dish names only based on the ingredients provided."})
    elif "recipe for" in user_input.lower():
        messages.append({"role": "system", "content": f"Provide a detailed recipe for {user_input}."})
    elif "critique" in user_input.lower():
        messages.append({"role": "system", "content": "Offer a constructive critique with suggestions to improve the recipe."})
    else:
        print("Please ask for a dish suggestion by ingredients, a specific recipe, or a recipe critique.")
        continue

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
