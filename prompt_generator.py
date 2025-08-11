# file: prompt_generator.py
import pandas as pd
import json

class PromptGenerator:
    """
    Lớp này chịu trách nhiệm tạo ra các prompt chi tiết để gửi đến LLM,
    yêu cầu kết quả trả về dưới định dạng JSON.
    """
    def create_prompt(self, unit_name: str, unit_data: dict, focus_type: str) -> str:
        """
        Xây dựng prompt DUY NHẤT để yêu cầu AI tạo cả kế hoạch và TOÀN BỘ tài liệu
        và trả về dưới dạng một chuỗi JSON hợp lệ.
        """
        unit_theme = unit_data.get('unit_theme', '')
        
        # (Phần tạo knowledge_section giữ nguyên không đổi)
        knowledge_section = ""
        # ... (Bạn có thể giữ nguyên phần code tạo knowledge_section ở đây)

        # Cấu trúc JSON mong muốn
        JSON_TEMPLATE = {
            "plans": [
                {
                    "title": "Tên Hoạt động 1",
                    "description": "Mô tả chi tiết về hoạt động",
                    "objective": "*   Mục tiêu 1\n*   Mục tiêu 2",
                    "time": "XX phút",
                    "teacher_needs": "Những thứ giáo viên cần chuẩn bị",
                    "ai_materials": "TOÀN BỘ NỘI DUNG TÀI LIỆU MÀ AI CUNG CẤP",
                    "steps": "1. (X phút) - Bước 1: ...\n2. (Y phút) - Bước 2: ...",
                    "analysis": "*   Ưu điểm: ...\n*   Nhược điểm: ..."
                }
            ]
        }
        
        json_template_str = json.dumps(JSON_TEMPLATE, indent=4, ensure_ascii=False)

        final_prompt = f"""
Bạn là một AI Cố vấn Soạn Giáo án chuyên nghiệp, hoạt động như một API trả về dữ liệu JSON.

**NGỮ CẢNH:**
- **Sách giáo khoa:** Tiếng Anh 12 - Global Success
- **Bài học (Unit):** {unit_name}
- **Chủ đề chính của Unit:** {unit_theme}
{knowledge_section}

**NHIỆM VỤ:**
Dựa trên ngữ cảnh, hãy đề xuất 4 ý tưởng hoạt động tương tác học tiếng anh giữa học sinh và giáo viên hoặc học sinh với học sinh**thực sự sáng tạo, sâu sắc và hấp dẫn**. Các hoạt động phải **ưu tiên ít chuẩn bị vật chất (low-prep)**.

**YÊU CẦU ĐỊNH DẠNG ĐẦU RA (CỰC KỲ QUAN TRỌNG):**
Bạn phải trả lời bằng một chuỗi JSON hợp lệ và chỉ JSON mà thôi, không có bất kỳ văn bản giải thích nào khác. Chuỗi JSON phải tuân thủ chính xác cấu trúc sau:
```json
{json_template_str}
```
"""
        return final_prompt.strip()