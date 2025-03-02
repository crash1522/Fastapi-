from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


class LLMAgent:
    def __init__(self, api_key, provider="openai", model_name=None, system_prompt=None, format_prompt=None, rules_prompt=None):
        """
        Initializes the MultiLLMProcessor with the given API key and provider.

        Args:
            api_key (str): Your API key for the respective provider.
            provider (str, optional): The provider to use ("openai" or "anthropic"). Defaults to "openai".
            model_name (str, optional): The model name to use. Defaults depend on the provider.
        """
        self.api_key = api_key
        self.provider = provider.lower()
        if self.provider == "openai":
            self.model_name = model_name or "o3-mini-2025-01-31"
            self.processor = ChatOpenAI(api_key=self.api_key, model_name=self.model_name)
        elif self.provider == "anthropic":
            self.model_name = model_name or "claude-3-5-sonnet-20241022" #claude-3-5-haiku-20241022
            self.processor = ChatAnthropic(api_key=self.api_key, model_name=self.model_name)
        else:
            raise ValueError("Unsupported provider. Choose 'openai' or 'anthropic'.")
        
        self.output_parser = StrOutputParser()
        self.system_prompt = system_prompt
        self.format_prompt = format_prompt
        self.rules_prompt = rules_prompt
