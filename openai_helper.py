import os
import openai

class OpenAIHelper:
    """OpenAI Helper class."""

    def __init__(self):
        """
        Initialize the OpenAIHelper.
        """
        self.api_key = os.environ['OPENAI_API_KEY']
        self.model = os.environ['MODEL']

        # Initialize the OpenAI client
        self.client = openai.Client(api_key=self.api_key)

    def analyze_code(self, prompt, max_length):
        """
        Analyze the code changes using OpenAI.
        """
        # Generate a response based on the prompt
        response = self.client.create_completion(
            model=self.model,
            prompt=prompt,
            max_tokens=max_length,
            temperature=0.5,
            top_p=0.9
        )

        # Return the response
        return response.choices[0].text
