import time
from typing import Any, List, Mapping, Optional, Literal, Union, TypedDict

class GLM:
    """GLM (智谱AI) using ZhipuAI Python SDK
    https://github.com/zai-org/z-ai-sdk-python
    """

    Message_Type = TypedDict('Message', { 'role': Literal['user', 'assistant', 'system'], 'content': str })

    def __init__(self,
        api_key: str,
        model: str = "glm-4",
        max_tokens: int = 1024,
        temperature: Optional[float] = 0.7,
        top_p: Optional[float] = 0.9,
        timeout: int = 3600,
        ):

        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.timeout = timeout
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from zai import ZhipuAiClient
                self._client = ZhipuAiClient(api_key=self.api_key)
            except ImportError:
                raise ImportError("zhipuai package not found. Please install it with: pip install zhipuai")
        return self._client

    def set_params(self,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        ):

        if max_tokens is not None: self.max_tokens = max_tokens
        if temperature is not None: self.temperature = temperature
        if top_p is not None: self.top_p = top_p

    def ensure_array(self,
            input_msg: List[Message_Type] | Message_Type
        ) -> List[Message_Type]:
        if isinstance(input_msg, (list, tuple)):
            return input_msg
        else:
            return [input_msg]

    def chat(self,
            messages: Message_Type,
            max_retries: int = 10,
            seed: int = None
    ):
        messages = self.ensure_array(messages)
        client = self._get_client()

        params = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }

        if seed is not None:
            params["seed"] = seed

        retries = 0
        while retries < max_retries:
            try:
                response = client.chat.completions.create(**params)

                if response.choices and len(response.choices) > 0:
                    message = response.choices[0].message
                    content = message.content
                    reasoning_content = getattr(message, 'reasoning_content', None)

                    # GLM models often return actual content in reasoning_content field
                    actual_content = reasoning_content if reasoning_content and reasoning_content.strip() else content

                    if actual_content and actual_content.strip():
                        return actual_content
                    else:
                        print(f"GLM response content is empty or whitespace only, retry attempt {retries + 1}.")
                        print(f"Raw response: {response}")
                else:
                    print(f"GLM response without choices, retry attempt {retries + 1}.")
                    print(f"Raw response: {response}")

            except Exception as e:
                error_msg = str(e)
                print(f"GLM API error: '{error_msg}', retry attempt {retries + 1}.")

                if "1301" in error_msg:
                    raise Exception("Invalid API key (Authorization failed)")
                elif "1302" in error_msg:
                    print("API request rate limit exceeded")
                    print("Waiting 10 seconds")
                    time.sleep(10)
                elif "1303" in error_msg:
                    raise Exception("Insufficient account balance")
                elif "1310" in error_msg:
                    print("Request timeout")
                elif "1311" in error_msg:
                    print("Model service unavailable")
                elif "1312" in error_msg:
                    raise Exception("Model does not exist")
                elif "1313" in error_msg:
                    print("Invalid request parameters")
                    print("Waiting 10 seconds")
                    time.sleep(10)
                elif "1314" in error_msg:
                    print("Content in request violates content security policy")
                elif "rate limit" in error_msg.lower():
                    print("Rate limited, waiting 10 seconds")
                    time.sleep(10)

            retries += 1

        raise Exception(f"GLM API request failed after {max_retries} retries")