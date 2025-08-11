# file: llm_service.py
import google.generativeai as genai

class LLMService:
    """
    Lớp này đóng gói tất cả các tương tác với Google Gemini API.
    """
    def __init__(self, api_key: str, model_name='gemini-1.5-flash'): # <-- THAY ĐỔI DUY NHẤT Ở ĐÂY
    
        if not api_key:
            raise ValueError("API key không được cung cấp.")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_lesson_plans(self, prompt: str) -> str:
        """
        Gửi một prompt đến Gemini API và nhận lại kết quả dưới dạng văn bản.
        """
        try:
            # Các thiết lập an toàn để tránh chặn nội dung hợp lệ
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]

            # Thêm yêu cầu trả về JSON cho các model mới
            generation_config = genai.types.GenerationConfig(
                response_mime_type="application/json"
            )

            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            return response.text
        except Exception as e:
            # Bắt các lỗi có thể xảy ra trong quá trình gọi API
            error_message = f"Lỗi khi gọi Gemini API: {e}"
            print(error_message)
            return error_message