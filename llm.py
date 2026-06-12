import requests
import json

def llm_req(mess):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"LLM_TOKEN_HERE",
        "Content-Type": "application/json",
    },
    
    data=json.dumps({
        "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "messages": [
            {
            "role": "user",
            "content": f"""Ты помогаешь разработчику принимать заказы.
            Получаешь сообщение с заказом: {mess}.
            Требуется задать заказчику уточняющий вопрос (1-2 вопроса, больше не надо) по теме программы ответ на который бы по твоему мнению помог разрабочику при разработке
            """
            }
        ],
        "reasoning": {"enabled": True}
    })
    )

    response = response.json()

    final = response['choices'][0]['message']['content']

    print(final)
    
    return final


