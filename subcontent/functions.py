
from openai import OpenAI
from config import openai_api_key


def btd_bot(question, message_history=[], model="gpt-3.5-turbo-1106", liquor1="", liquor2="", liquor3=""):
    client = OpenAI(api_key=openai_api_key)
    system_instruction = f"""사용자가 가진 술: {liquor1}, 사용자가 좋아하는 술: {liquor2}, 사용자가 싫어하는 술: {liquor3}
    이 데이터를 기반으로 사용자의 질문에 대답해줘."""
    if len(message_history) == 0:
        # 최초 질문

        message_history.append(
            {
                "role": "system", "content": system_instruction
            }
        )

    # 사용자 질문 추가
    message_history.append({
        "role": "user",
        "content": question,
    }
    )

    # GPT에 질문을 전달하여 답변을 생성
    completion = client.chat.completions.create(
        model=model,
        messages=message_history,
    )
    # 사용자 질문에 대한 답변을 추가
    message_history.append(
        {"role": "assistant", "content": completion.choices[0].message.content}
    )

    return message_history
