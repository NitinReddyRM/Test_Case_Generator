import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from .Preprocessing import Precessing




class Generate:
    def __init__(self):
        load_dotenv()

        os.environ['groq_api_key']=os.getenv('groq_api_key')
        self.llm_Client = ChatGroq(
            model_name='qwen/qwen3-32b',  # Use a valid model name from Groq
            temperature=0.7
        )

    def generate_test_cases(self, input_requirement: str):
        prompt = [
            {"role": "system", "content": "You are a helpful assistant. Generate test cases in JSON format based on the user's input requirement. dont include any explanantion"},
            {"role": "user", "content": input_requirement}
        ]
        
        response = self.llm_Client.invoke(prompt)
        
        return Precessing.extract_json_structure(response.content)
