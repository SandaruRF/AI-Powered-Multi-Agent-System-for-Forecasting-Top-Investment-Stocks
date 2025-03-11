import os
from typing import Literal
import google.generativeai as genai
from anthropic import Anthropic
from config.settings import GEMINI_API_KEY, ANTHROPIC_API_KEY

class SupervisorAgent:
    def __init__(self, api_type: Literal["gemini", "claude"] = "gemini"):
        """
        Initialize the supervisor agent with the specified API type.

        Args:
            api_type (str): The API to use. Options: "gemini" (default) or "claude".
        """
        self.api_type = api_type

        if self.api_type == "gemini":
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-2.0-flash")
        elif self.api_type == "claude":
            self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
            self.model = "claude-3.7-sonnet"
        else:
            raise ValueError("Invalid API type. Choose 'gemini' or 'claude'.")
        
    def decide_next_step(self, context: dict) -> str:
        """
        Decides the next team or agent to invoke based on the current context.

        Args:
            context (dict): The current context of the workflow.

        Returns:
            str: The next step to take (e.g., "fetch_stock_data").
        """

        available_steps = {
            "start": ["fetch_stock_data", "fetch_fundamentals", "fetch_news_sentiment"],
            "stock_data_fetched": ["fetch_fundamentals", "fetch_news_sentiment"],
            "fundamentals_fetched": ["fetch_news_sentiment", "preprocess_data"],
            "news_sentiment_fetched": ["complete"],
        }

        current_step = context.get("step", "start")
        next_steps = available_steps.get(current_step, [])

        prompt = (
            f"You are a supervisor for a multi-agent stock prediction system. "
            f"Decide the next team or agent to invoke based on the current context: {context}. "
            f"Available next steps: {next_steps}. "
            f"Return only the step name (e.g., 'fetch_stock_data')."
        )

        if self.api_type == "gemini":
            response = self.model.generate_content(prompt)
            return response.text.strip()
        elif self.api_type == "claude":
            response = self.client.messages.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a supervisor for a multi-agent stock prediction system."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=20,
            )
            return response.content[0].text.strip()
        
    def is_work_complete(self, context: dict) -> bool:
        """
        Determines if the workflow is complete based on the current context.

        Args:
            context (dict): The current context of the workflow.

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