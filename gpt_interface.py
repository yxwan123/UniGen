# gpt_interface.py
from openai import OpenAI
import time
from openai import APIError, APIConnectionError, RateLimitError


class GPT4Bot:
    def __init__(self, key_path, model="gpt-4.1"):
        with open(key_path, "r") as f:
            self.key = f.read().strip()
        self.client = OpenAI(api_key=self.key)
        self.model = model

    def ask(self, prompt: str, max_retries=3) -> str:
        base_delay = 5  # Initial delay in seconds

        for i in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=4096,
                    temperature=0,
                )
                return response.choices[0].message.content.strip()

            except (APIError, APIConnectionError, RateLimitError) as e:
                print(f"❌ API call failed. Attempt {i + 1}/{max_retries}.")
                print(f"Error: {type(e).__name__}: {e}")

                if i < max_retries - 1:
                    wait_time = base_delay * (2 ** i)
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("🔴 All retry attempts failed. Please check your network connection or API key.")
                    raise  # Re-raise the last exception