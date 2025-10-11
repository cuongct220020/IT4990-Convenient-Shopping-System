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
    Bạn là một trình phân tích văn bản công thức nấu ăn.
    Nhiệm vụ: Trích xuất thông tin từ đoạn text về món ăn,
    và trả về kết quả theo JSON với schema sau:

    {format_instructions}

    Text đầu vào:
    {text}
    Chỉ trả về dữ liệu JSON hợp lệ, không kèm lời giải thích.
    """,
        input_variables=['text'],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt

def get_input(path) -> List[str]:
    with open(path, 'r', encoding='utf-8') as f:
        text = json.load(f)
    return text  

def main():
    # path define
    input_path = './input/exam_input.json'
    out_path = './output/example.json'

    # component define
    parser = PydanticOutputParser(pydantic_object=Recipe)
    input_texts = get_input(input_path)
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
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
if __name__=='__main__':
    main()

        

