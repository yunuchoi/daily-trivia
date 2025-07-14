import datetime
import os
import random
import smtplib
from dotenv import load_dotenv
from email.message import EmailMessage
from openai import OpenAI

load_dotenv()

SMTP_SERVER = "mail.privateemail.com"
SMTP_PORT = 587

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENTS = os.getenv("RECIPIENTS")

client = OpenAI(api_key=OPENAI_API_KEY)

sender_name = "오늘의 토막상식"
sender_email = f"{sender_name} <bots@yunuchoi.me>"

subject_options = [
    "하루 한 입 지식, 받으셨나요? 🔍",
    "오잉? 이런 사실 알고 계셨나요? 📬",
    "오늘의 지식 간식 드셔보세요 🍿🧠",
    "사알짝 똑똑해지는 오늘의 한 줄 ✨",
    "오늘의 호기심 한 방울 도착! 💌",
    "헉! 이런 것도 있었어? 🧠",
    "당신의 두뇌에 오늘도 한 입 💡",
    "딱! 하고 떨어지는 지식 한 조각 📸",
    "상큼한 오늘의 상식 🍋",
    "당신의 인박스에 작은 놀라움 ✉️",
]

topics_by_day = {
    0: ["과학", "물리학", "화학", "생물학", "지구과학"],
    1: ["역사", "고대문명", "근대사", "세계사", "한국사"],
    2: ["예술", "미술", "음악", "문학", "영화"],
    3: ["기술", "컴퓨터", "인공지능", "로봇", "인터넷"],
    4: ["문화", "언어", "풍습", "음식", "축제"],
    5: ["자연", "동물", "식물", "기후", "지리"],
    6: ["우주", "천문학", "행성", "별", "블랙홀"],
}


def get_daily_trivia():
    today_weekday = datetime.datetime.now().weekday()
    topic_list = topics_by_day.get(today_weekday, ["일반"])
    topic = random.choice(topic_list)
    print(f"Selected topic for today: {topic}")
    prompt = (
        f"'{topic}'를 주제로 짧고 흥미로운 토막 상식을 만들어 주세요."
        "소개 → 지식 → 연장의 흐름을 따르되, 전체는 3~4문장 정도의 간결한 한 문단으로 구성해 주세요. "
        "소개는 흥미를 끄는 간단한 질문이나 상황 제시로 시작해 주세요. "
        "이후 본론인 지식 정보를 간결하고 명확하게 전달해 주세요. "
        "마지막은 그 지식에 대한 흥미로운 연장 설명이나, 연결 가능한 관련 정보로 마무리해 주세요. "
        "딸기, 바나나, 베리류에 관한 내용은 제외해 주세요. "
        "인사말이나 여는 말 등은 생략하고, 본문만 작성해 주세요."
    )

    response = client.chat.completions.create(
        model="o4-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    trivia = response.choices[0].message.content.strip()
    return trivia


def send_email(body):
    recipients = RECIPIENTS.split(",")
    selected_subject_base = random.choice(subject_options)

    today = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    selected_subject = f"{selected_subject_base} - {today} 오늘의 토막상식"

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = "지식 구독자 <hello@yunuchoi.me>"
    msg["Subject"] = selected_subject
    msg["Bcc"] = ", ".join(recipients)
    msg.set_content(body)

    print(f"Sending email to Bcc recipients:\n{recipients}\n")
    print(f"Email Subject: {selected_subject}\n")
    print(f"Email Body:\n{body}\n")

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


if __name__ == "__main__":
    trivia = get_daily_trivia()
    body = (
        "오늘의 뇌를 자극하는 한 입 정보입니다 🧠✨\n\n"
        f"{trivia}\n\n"
        "— 오늘의 토막상식팀 드림"
    )

    send_email(body)
