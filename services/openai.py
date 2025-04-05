import openai
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()


client = openai.AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def get_tax_code_response(question: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Вы - помощник по Налоговому кодексу РК. Отвечайте точно и по делу. Вот кодекс https://adilet.zan.kz/rus/docs/K1700000120"},
                {"role": "user", "content": question}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {str(e)}"
