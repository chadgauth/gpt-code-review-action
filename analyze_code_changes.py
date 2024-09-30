import sys
import os
import re
from typing import Dict
from openai_helper import OpenAIHelper

class CodeAnalyzer:
    """Code Analyzer class."""

    def __init__(self, excluded_files: str, prompt_template: str, commit_title: str, commit_body: str, max_code_length: int):
        """
        Initialize the CodeAnalyzer.

        Args:
        - excluded_files (str): A comma-separated list of file patterns to exclude.
        - prompt_template (str): The prompt template to use for the analysis.
        - commit_title (str): The commit title.
        - commit_body (str): The commit body.
        - max_code_length (int): The maximum number of characters to submit to OpenAI.
        """
        self.excluded_files = re.split(r'\s*,\s*', excluded_files)
        self.prompt_template = prompt_template
        self.commit_title = commit_title
        self.commit_body = commit_body
        self.max_code_length = max_code_length

    def analyze(self):
        """
        Analyze the code changes and generate feedback.
        """
        openai_helper = OpenAIHelper()
        diff_output = sys.stdin.read()

        # Parse the diff output to extract the file names and changes
        file_names_and_changes = self._parse_diff_output(diff_output)

        for file_name, file_changes in file_names_and_changes.items():
            # Check if the file should be excluded
            if self._should_exclude_file(file_name):
                continue

            # Generate the prompt for the file
            prompt = self._generate_prompt(file_name, file_changes)

            # Analyze the code changes using OpenAI
            analysis = openai_helper.analyze_code(prompt, self.max_code_length)

            # Print the analysis
            print(analysis)

    def _parse_diff_output(self, diff_output):
        """
        Parse the diff output to extract the file names and changes.
        """
        # Split the diff output into lines
        lines = diff_output.splitlines()

        # Initialize a dictionary to store the file names and changes
        file_names_and_changes = {}

        # Initialize the current file name
        current_file_name = None

        # Iterate over the lines
        for line in lines:
            # Check if the line starts with '---' or '+++', which indicates a new file
            if line.startswith('---') or line.startswith('+++'):
                # Extract the file name from the line
                file_name = line.split()[1]

                # Add the file name to the dictionary
                file_names_and_changes[file_name] = ''

                # Update the current file name
                current_file_name = file_name

            # Check if the line starts with '+', which indicates a change
            elif line.startswith('+'):
                # Append the line to the current file's changes
                file_names_and_changes[current_file_name] += line[1:] + '\n'

        return file_names_and_changes

    def _should_exclude_file(self, file_name):
        """
        Check if the file should be excluded based on the excluded files list.
        """
        for excluded_file in self.excluded_files:
            if re.match(excluded_file, file_name):
                return True

        return False

    def _generate_prompt(self, file_name, file_changes):
        """
        Generate the prompt for the file.
        """
        # Replace placeholders in the prompt template
        prompt = self.prompt_template.replace('{{ file_name }}', file_name)

        # Add the file changes to the prompt
        prompt += '\n\nFile changes:\n' + file_changes

        return prompt

if __name__ == '__main__':
    # Read environment variables
    openai_api_key = os.environ['OPENAI_API_KEY']
    model = os.environ['MODEL']
    prompt_template = os.environ['PROMPT_TEMPLATE']
    max_length = int(os.environ['MAX_LENGTH'])
    commit_title = os.environ['COMMIT_TITLE']
    commit_body = os.environ['COMMIT_BODY']
    excluded_files = os.environ['EXCLUDED_FILES']

    # Create a CodeAnalyzer instance
    analyzer = CodeAnalyzer(excluded_files, prompt_template, commit_title, commit_body, max_length)

    # Analyze the code changes
    analyzer.analyze()
