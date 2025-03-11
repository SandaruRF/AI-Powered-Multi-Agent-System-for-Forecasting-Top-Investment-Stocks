import os
from typing import Literal

import google.generativeai as genai
from anthropic import Anthropic

class SupervisorAgent:
    def __init__(self, api_type: Literal["gemini", "claude"] = "gemini"):
        """
        Initialize the supervisor agent with the specified API type.

        Args:
            api_type (str): The API to use. Options: "gemini" (default) or "claude".
        """
        self.api_type = api_type

        if self.api_type == "gemini":
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model = genai.GenerativeModel("gemini-2.0-flash")
        elif self.api_type == "claude":
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3.7-sonnet"
        else:
            raise ValueError("Invalid API type. Choose 'gemini' or 'claude'.")
        
    def decide_next_step(self, context: str) -> str:
        """
        Decides the next team or agent to invoke based on the current context.

        Args:
            context (str): The current context of the workflow.

        Returns:
            str: The next step to take (e.g., "fetch_stock_data").
        """
        if self.api_type == "gemini":
            response = self.model.generate_content(
                f"You are a supervisor for a multi-agent stock prediction system. Decide the next team or agent to invoke based on the current context: {context}"
            )
            return response.text
        elif self.api_type == "claude":
            response = self.client.messages.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a supervisor for a multi-agent stock prediction system. Decide the next team or agent to invoke based on the current context."},
                    {"role": "user", "content": context},
                ],
                max_tokens=100,
            )
            return response.content[0].text
        
    def is_work_complete(self, context: str) -> bool:
        """
        Determines if the workflow is complete based on the current context.

        Args:
            context (str): The current context of the workflow.

        Returns:
            bool: True if the workflow is complete, False otherwise.
        """
        if self.api_type == "gemini":
            response = self.model.generate_content(
                f"You are a supervisor for a multi-agent stock prediction system. Determine if the workflow is complete based on the current context: {context}. Respond with 'yes' or 'no'."
            )
            return response.text.lower() == "yes"
        elif self.api_type == "claude":
            response = self.client.messages.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a supervisor for a multi-agent stock prediction system. Determine if the workflow is complete based on the current context. Respond with 'yes' or 'no'."},
                    {"role": "user", "content": context},
                ],
                max_tokens=10,
            )
            return response.content[0].text.lower() == "yes"