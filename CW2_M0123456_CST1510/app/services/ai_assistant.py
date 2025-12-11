# app/services/ai_assistant.py
import google.generativeai as genai
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class DomainAssistantConfig:
    system_prompts: Dict[str, str]
    default_model: str = "gemini-2.5-flash"


class DomainAssistant:
    def __init__(self, api_key: str, config: DomainAssistantConfig) -> None:
        genai.configure(api_key=api_key)
        self.config = config

    def _build_gemini_messages(self, messages: List[Dict]) -> List[Dict]:
        gemini_messages = []
        for m in messages:
            role = "user" if m["role"] == "user" else "model"
            gemini_messages.append(
                {"role": role, "parts": [{"text": m["content"]}]}
            )
        return gemini_messages

    def stream_reply(
        self,
        domain: str,
        history: List[Dict],
        model_name: str,
        temperature: float,
    ):
        system_prompt = self.config.system_prompts[domain]

        model = genai.GenerativeModel(
            model_name,
            system_instruction=system_prompt,
            generation_config={"temperature": temperature},
        )

        gemini_messages = self._build_gemini_messages(history)
        return model.generate_content(gemini_messages, stream=True)
