


import google.generativeai as genai

def setup_gemini(api_key):
    # Configure the API key
    genai.configure(api_key=api_key)

    available_models = genai.list_models()
    
    selected_model = None
    for model in available_models:
        if 'generateContent' in model.supported_generation_methods:
            # Check for models like gemini-1.5-flash or other available models
            if 'gemini-1.5-flash' in model.name:
                print(f"✅ Using model: {model.name}")
                selected_model = model.name
                break
            else:
                print(f"⚠️ Model {model.name} doesn't support the required features.")
    
  
    if not selected_model:
        raise ValueError("❌ No valid model found that supports content generation.")

   
    model = genai.GenerativeModel(model_name=selected_model)
    chat = model.start_chat()
    return chat

def get_gemini_response(chat, prompt):
    try:
        
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        # Handle any errors that occur during message sending
        return f"❌ Error during chat response: {e}"
