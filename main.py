from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI()
conversation = ["안녕 내이름은 link 야"]
exit_commands = {"q", "quit", "ㅕquit", "exit"}

while True:
    user_message = input("대화를 입력하세요: ").strip()

    if user_message.lower() in exit_commands:
        print("대화를 종료합니다.")
        break

    if not user_message:
        continue

    conversation.append(f"사용자: {user_message}")

    response = client.responses.create(
        model="gpt-4o-mini",
        input="\n".join(conversation),
    )
    answer = response.output_text
    conversation.append(f"어시스턴트: {answer}")
    print(answer)
