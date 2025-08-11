# file: main.py
import streamlit as st
import re
import os
import json
from dotenv import load_dotenv
from data_provider import UnitDataProvider
from prompt_generator import PromptGenerator
from llm_service import LLMService

load_dotenv()
st.set_page_config(layout="wide", page_title="Trợ lý Giáo viên AI")

@st.cache_resource
def load_services():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Không tìm thấy GOOGLE_API_KEY. Vui lòng kiểm tra file .env.")
        st.stop()
    data_provider = UnitDataProvider(data_folder='data')
    prompt_generator = PromptGenerator()
    llm_service = LLMService(api_key=api_key)
    return data_provider, prompt_generator, llm_service

try:
    data_provider, prompt_generator, llm_service = load_services()
except Exception as e:
    st.error(f"Lỗi khởi tạo dịch vụ: {e}")
    st.stop()

unit_names_list = [
    "Unit 1: Life Stories We Admire", "Unit 2: A Multicultural World", "Unit 3: Green Living",
    "Unit 4: Urbanisation", "Unit 5: The World of Work", "Unit 6: Artificial Intelligence",
    "Unit 7: The World of Mass Media", "Unit 8: Wildlife Conservation", "Unit 9: Career Paths",
    "Unit 10: Lifelong Learning"
]

st.title("✨ Trợ lý Giáo viên AI - Global Success ✨")
st.markdown("Chỉ cần chọn Unit và Trọng tâm, AI sẽ đề xuất các kế hoạch hoạt động chi tiết và đầy đủ tài liệu cho bạn!")
st.divider()

st.header("Bắt đầu tạo hoạt động")
col1, col2 = st.columns(2)

with col1:
    selected_unit_name = st.selectbox("**1. Chọn Unit:**", unit_names_list)
with col2:
    selected_focus = st.selectbox("**2. Chọn Trọng tâm:**", ["Từ vựng", "Ngữ pháp"])

st.write("")

if st.button("🚀 Sáng tạo Kế hoạch & Tài liệu!", type="primary", use_container_width=True):
    unit_number_match = re.search(r'Unit (\d+)', selected_unit_name)
    if not unit_number_match:
        st.error("Lựa chọn Unit không hợp lệ.")
        st.stop()
    unit_number = int(unit_number_match.group(1))
    
    unit_data = data_provider.get_unit_data(unit_number)
    if unit_data is None:
        st.error(f"Không tìm thấy file dữ liệu cho Unit {unit_number}. Vui lòng tạo file 'unit_{unit_number}_data.csv' trong thư mục 'data'.")
        st.stop()
    
    final_prompt = prompt_generator.create_prompt(
        unit_name=selected_unit_name, unit_data=unit_data, focus_type=selected_focus
    )
    
    with st.spinner("🤖 AI đang tư duy và cấu trúc dữ liệu..."):
        try:
            raw_response = llm_service.generate_lesson_plans(final_prompt)
            json_str = raw_response.strip().replace('```json', '').replace('```', '')
            response_data = json.loads(json_str)
            st.session_state['parsed_plans'] = response_data.get("plans", [])
            st.session_state['raw_response'] = raw_response
            st.balloons()
        except json.JSONDecodeError:
            st.error("Lỗi: AI đã trả về một chuỗi không phải là JSON hợp lệ.")
            st.warning("Hiển thị kết quả thô từ AI:")
            st.code(raw_response, language="text")
            st.session_state['parsed_plans'] = []
        except Exception as e:
            st.error(f"Đã có lỗi xảy ra: {e}")
            st.session_state.clear()

if 'parsed_plans' in st.session_state and st.session_state['parsed_plans']:
    st.header(f"✨ Gợi ý Kế hoạch & Tài liệu Hoàn chỉnh ✨")
    
    parsed_plans = st.session_state['parsed_plans']
    icons = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]

    for i, plan in enumerate(parsed_plans):
        icon = icons[i] if i < len(icons) else "➡️"
        with st.expander(f"**{icon} {plan.get('title', 'Kế hoạch không tên')}**"):
            st.markdown(f"**📝 Mô tả ngắn:** {plan.get('description', 'N/A')}")
            st.markdown(f"**🎯 Mục tiêu:**\n{plan.get('objective', 'N/A')}")
            st.markdown(f"**⏳ Thời gian dự kiến:** {plan.get('time', 'N/A')}")
            st.markdown("---")
            st.subheader("🛠️ Chuẩn bị & Tài liệu")
            col_gv, col_ai = st.columns(2)
            with col_gv:
                st.warning(f"**👩‍🏫 Giáo viên cần:**\n\n{plan.get('teacher_needs', 'N/A')}")
            with col_ai:
                st.info(f"**🤖 Tài liệu AI cung cấp:**")
                st.markdown(plan.get('ai_materials', 'N/A'))
            st.markdown("---")
            st.subheader("👣 Các bước thực hiện")
            st.markdown(plan.get('steps', 'N/A'))
            st.markdown("---")
            st.subheader("⚖️ Phân tích")
            st.markdown(plan.get('analysis', 'N/A'))

st.sidebar.header("Giới thiệu")
st.sidebar.info(
    "Ứng dụng được thiết kế để cung cấp các kế hoạch bài giảng khả thi, đầy đủ tài liệu và dễ sử dụng."
)
st.sidebar.success("Tác giả: Gemini & Bạn")