import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

class LLMManager:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found")

        genai.configure(api_key=api_key)
        
        # Robust model selection
        self.model_name = self._select_model()
        self.model = genai.GenerativeModel(self.model_name)
        print(f"Initialized LLM with model: {self.model_name}")

    def _select_model(self):
        """Selects the best available model, with fallbacks."""
        try:
            available_models = [m.name for m in genai.list_models() 
                               if 'generateContent' in m.supported_generation_methods]
            
            # Preference list (stripped of 'models/' prefix for comparison)
            preferences = [
                "models/gemini-1.5-flash",
                "models/gemini-1.5-flash-latest",
                "models/gemini-pro",
                "models/gemini-1.0-pro"
            ]
            
            for pref in preferences:
                if pref in available_models:
                    return pref
            
            # If none of the preferences are found, pick the first available generative model
            if available_models:
                return available_models[0]
                
            return "gemini-1.5-flash" # Default fallback
        except Exception as e:
            print(f"Error listing models: {e}")
            return "gemini-1.5-flash" # Final fallback

    def generate_answer(self, query, context_docs):
        context = "\n\n".join(context_docs)

        prompt = f"""
You are a helpful assistant.
Answer ONLY from the context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""

        try:
            response = self.model.generate_content(prompt)
            if not response or not hasattr(response, "text"):
                return "I don't know."
            return response.text.strip()
        except Exception as e:
            print(f"Error generating content with {self.model_name}: {e}")
            return f"I don't know (Error: {str(e)})"
