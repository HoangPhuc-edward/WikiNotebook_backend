import os
import requests
from openai import OpenAI
from sambanova import SambaNova
from together import Together

class LLMManager:
    def __init__(self, provider, base_url, api_key, model_name):
        self.provider = provider
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name

    def test_connection(self):
        try:
            if self.provider == "OpenAI":
                client = OpenAI(base_url=self.base_url, api_key=self.api_key)
                res = client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": "Hi"}],
                    max_tokens=10
                )
                return True, f"OpenAI OK: {res.choices[0].message.content}"
            
            elif self.provider == "Ollama":
                url = f"{self.base_url}/api/generate"
                payload = {
                    "model": self.model_name,
                    "prompt": "Hi",
                    "stream": False
                }
                res = requests.post(url, json=payload)
                if res.status_code == 200:
                    return True, f"Ollama OK: {res.json().get('response', '')}"
                return False, f"Ollama Error: {res.text}"
            elif self.provider == "SambaNova":
                client = SambaNova(api_key=self.api_key, base_url=self.base_url)
                response = client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": "Hi"}],
                    temperature=0.1,
                    top_p=0.9
                )
                return True, f"SambaNova OK: {response.choices[0].message.content}"
                
            elif self.provider == "Together":
                client = Together(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": "Hi"}],
                    temperature=0.1,
                    top_p=0.9
                )
                return True, f"Together OK: {response.choices[0].message.content}"
            
            return False, "Provider không hợp lệ"
        except Exception as e:
            return False, str(e)

    def send_prompt(self, prompt: str, options: dict = None) -> str:
        # is_ok, msg = self.test_connection()
        # if not is_ok:
        #     print(f"[ERROR] Kết nối thất bại: {msg}")
        #     return f"Lỗi kết nối: {msg}"

        if options is None: options = {}
        
        print(f"--- Đang dùng: {self.provider} ({self.model_name}) ---")
        
        if self.provider == "OpenAI":
            return self._call_openai_compatible(prompt, options)
        elif self.provider == "Ollama":
            return self._call_ollama_raw(prompt, options)
        elif self.provider == "SambaNova":
            return self._call_sambanova(prompt, options)
        elif self.provider == "Together":
            return self._call_together(prompt, options)
        else:
            return "Provider chưa được hỗ trợ."

    def _call_openai_compatible(self, prompt: str, options: dict) -> str:
        try:
            client = OpenAI(base_url=self.base_url, api_key=self.api_key)
            
            system_msg = options.get("system_message", "Bạn là trợ lý AI hữu ích, trả lời bằng Tiếng Việt.")
            temp = options.get("temperature", 0.2)
            max_tok = options.get("max_tokens", 15000)
            top_p = options.get("top_p", 0.9)

            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                temperature=temp,
                max_tokens=max_tok,
                top_p=top_p,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Lỗi API OpenAI: {str(e)}"

    def _call_ollama_raw(self, prompt: str, options: dict) -> str:
        try:
            url = f"{self.base_url}/api/generate"
            
            ollama_options = {
                "temperature": options.get("temperature", 0.2),
                "top_p": options.get("top_p", 0.9),
                "num_predict": options.get("max_tokens", 4000) # Ollama dùng num_predict thay cho max_tokens
            }

            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": ollama_options
            }
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                return res.json().get("response", "")
            return f"Lỗi Ollama: {res.text}"
        except Exception as e:
            return f"Lỗi kết nối Ollama: {e}"


    def _call_sambanova(self, prompt: str, options: dict) -> str:
        try:
            client = SambaNova(api_key=self.api_key, base_url=self.base_url)
            system_msg = options.get("system_message", "Bạn là trợ lý AI hữu ích, trả lời bằng Tiếng Việt.")
            temp = options.get("temperature", 0.1)

            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                temperature=temp,
                top_p=0.9
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Lỗi API SambaNova: {str(e)}"
        
    def _call_together(self, prompt: str, options: dict) -> str:
        try:
            client = Together(api_key=self.api_key)
            system_msg = options.get("system_message", "Bạn là trợ lý AI hữu ích, trả lời bằng Tiếng Việt.")
            temp = options.get("temperature", 0.1)

            response = client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                temperature=temp,
                top_p=0.9
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Lỗi API Together: {str(e)}"

if __name__ == "__main__":
    config = {}
    try:
        with open("LLM.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    config[key.strip()] = value.strip()
        
        print("Đã đọc cấu hình!", config)
        
        manager = LLMManager(
            provider=config.get("Provider"),
            base_url=config.get("Base URL"),
            api_key=config.get("API KEY"),
            model_name=config.get("Model Name")
        )

        print("\n--- TEST SEND PROMPT ---")
        response = manager.send_prompt(
            "Chào bạn, 1 + 1 bằng mấy?", 
            options={"temperature": 0.5, "system_message": "Bạn là giáo viên toán."}
        )
        print("Kết quả:", response)

    except FileNotFoundError:
        print("Không tìm thấy file LLM.txt")
    except Exception as e:
        print(f"Lỗi khởi chạy: {e}")