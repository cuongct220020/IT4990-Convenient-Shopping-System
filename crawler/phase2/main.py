from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json
from tqdm import tqdm

from schema.recipe import Recipe

def get_llm():
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model =genai.GenerativeModel("gemini-2.5-flash")
    return model

def make_prompt_template(parser):
    """ 
        prompt template for structured output
    """
    prompt = PromptTemplate(
    template="""
    Bạn là một parser dữ liệu ẩm thực.
    Nhiệm vụ: Trích xuất thông tin từ đoạn text về món ăn,
    và trả về kết quả theo JSON với schema sau:

    {format_instructions}

    Text đầu vào:
    {text}
    """,
        input_variables=['text'],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt

def get_input()-> List[str]:
    example_input = [
        "Món Canh chua cá lóc gồm nguyên liệu: 500g cá lóc, 2 quả cà chua, 1/2 quả thơm, 100g giá đỗ, 1 bó rau ngổ, 1 muỗng canh nước mắm, 1/2 muỗng cà phê muối, và 1 lít nước. "
        "Cách nấu: Làm sạch cá lóc, cắt khúc. Phi thơm hành tím, cho cà chua và thơm vào xào. "
        "Thêm nước, đun sôi rồi cho cá vào. Khi cá chín, thêm giá đỗ và rau ngổ, nêm nếm lại cho vừa miệng.",

        "Món Bò lúc lắc gồm nguyên liệu: 300g thịt bò thăn, 1/2 quả ớt chuông đỏ, 1/2 quả ớt chuông xanh, 1 củ hành tây, 1 muỗng canh dầu hào, 1 muỗng cà phê tiêu, 1/2 muỗng cà phê muối, và 2 muỗng canh dầu ăn. "
        "Cách làm: Cắt thịt bò thành khối vuông, ướp với dầu hào, tiêu, muối trong 15 phút. "
        "Bắc chảo nóng, cho dầu, xào nhanh thịt bò cho săn lại, sau đó cho hành tây và ớt chuông vào đảo đều. "
        "Chiên đến khi rau chín tới, dọn ra đĩa và ăn kèm cơm trắng hoặc bánh mì.",

        "Món Cà ri gà gồm nguyên liệu: 1 con gà ta khoảng 1.2kg, 3 củ khoai tây, 2 củ cà rốt, 400ml nước cốt dừa, 2 muỗng canh bột cà ri, 1 muỗng cà phê đường, 1 muỗng canh nước mắm, và 3 tép tỏi băm. "
        "Cách nấu: Gà chặt miếng vừa ăn, ướp với bột cà ri, muối, tỏi trong 30 phút. "
        "Chiên sơ khoai tây và cà rốt cho hơi vàng. "
        "Phi thơm hành tỏi, cho gà vào xào săn, sau đó thêm nước cốt dừa và 300ml nước. "
        "Nấu nhỏ lửa khoảng 30 phút cho gà mềm, rồi cho khoai và cà rốt vào nấu chín.",

        "Món Bún riêu cua gồm nguyên liệu: 300g cua đồng, 2 quả cà chua, 1 miếng đậu phụ chiên, 100g giò sống, 1 muỗng canh mắm tôm, 1 muỗng cà phê muối, 1/2 muỗng cà phê đường, 500g bún tươi, và 1 bó hành lá. "
        "Cách nấu: Giã cua, lọc lấy nước. Phi hành, xào cà chua, cho nước cua vào đun. "
        "Khi nước sôi, nêm mắm tôm, muối, đường cho vừa miệng. "
        "Thêm đậu phụ chiên, riêu cua và giò sống vào. Dọn ra bát, cho bún và hành lá lên trên.",

        "Món Salad rau củ gồm nguyên liệu: 150g xà lách, 1 quả dưa leo, 1 củ cà rốt, 10 quả cà chua bi, 2 muỗng canh dầu ô liu, 1 muỗng canh giấm táo, 1/2 muỗng cà phê muối, và 1/4 muỗng cà phê tiêu. "
        "Cách làm: Rửa sạch tất cả rau củ, để ráo nước. "
        "Cắt nhỏ xà lách, thái lát dưa leo và cà rốt, bổ đôi cà chua bi. "
        "Cho tất cả vào tô lớn, rưới dầu ô liu và giấm táo, trộn đều, nêm muối tiêu vừa ăn. "
        "Dùng ngay để giữ độ giòn và tươi ngon."
    ]
    return example_input
def main():
    # path define
    out_path = './output/example.json'

    # component define
    parser = PydanticOutputParser(pydantic_object=Recipe)
    input_texts = get_input()
    prompt = make_prompt_template(parser)
    model = get_llm()
    
    # processing
    output = []
    for txt in tqdm(input_texts):
        _input = prompt.format(text=txt)
        response = model.generate_content(_input)

        try:
            recipe = parser.parse(response.text)
            output.append(recipe.model_dump())
        except Exception as e:
            print(f"Parsing error: {e}")
            continue
    
    # export output
    with open(out_path, 'w') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    

        

