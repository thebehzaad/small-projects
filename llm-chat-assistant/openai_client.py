
#%%

import os
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv

#%%

class CustomOpenAI:

    def __init__(self, api_key: str, config: dict = None):
        if not api_key:
            raise ValueError("API key must be provided.")
        self.api_key = api_key
        self.config = config or {}
        self.client = None
        self.async_client = None

    def get_or_create_client(self) -> OpenAI:
        if not self.client:
            self.client = self._create_client()
        return self.client

    def get_or_create_async_client(self) -> AsyncOpenAI:
        if not self.async_client:
            self.async_client = self._create_async_client()
        return self.async_client

    def _create_client(self) -> OpenAI:
        # Create and return an instance of OpenAI client with additional config
        client = OpenAI(api_key=self.api_key)
        for key, value in self.config.items():
            setattr(client, key, value)
        return client

    def _create_async_client(self) -> AsyncOpenAI:
        # Create and return an instance of AsyncOpenAI client with additional config
        async_client = AsyncOpenAI(api_key=self.api_key)
        for key, value in self.config.items():
            setattr(async_client, key, value)
        return async_client

