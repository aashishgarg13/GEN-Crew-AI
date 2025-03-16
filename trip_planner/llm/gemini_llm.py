# llm/gemini_llm.py
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
import time
import random
from google.api_core import exceptions
from langchain_core.runnables import RunnablePassthrough

load_dotenv()

class GeminiLLM:
    def __init__(self, model="gemini-1.5-flash"):
        self.model = model
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.llm = ChatGoogleGenerativeAI(model=self.model, convert_system_message_to_human=True)

    def generate_text(self, prompt, max_retries=5, initial_delay=1):
        """
        Generates text using the Gemini API with retry logic.

        Args:
            prompt: The prompt to send to the API.
            max_retries: The maximum number of times to retry the request.
            initial_delay: The initial delay (in seconds) before the first retry.

        Returns:
            The generated text, or None if all retries fail.
        """
        output_parser = StrOutputParser()
        template = PromptTemplate.from_template(prompt)
        chain = {"prompt": RunnablePassthrough()} | template | self.llm | output_parser

        retries = 0
        delay = initial_delay
        while retries < max_retries:
            try:
                return chain.invoke({"prompt": prompt})
            except exceptions.ServiceUnavailable as e:
                print(f"Error: {e}")
                if retries < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay + random.uniform(0,1))  # Add some jitter to avoid thundering herd
                    delay *= 2  # Exponential backoff
                    retries += 1
                else:
                    print("Max retries reached. Request failed.")
                    raise e
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                raise e
        return None
