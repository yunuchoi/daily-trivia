import datetime
import os
import random
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from openai import OpenAI

load_dotenv()

SMTP_SERVER = "mail.privateemail.com"
SMTP_PORT = 587

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENTS = os.getenv("RECIPIENTS")

# OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

sender_name = "오늘의 토막상식"
sender_subject_pairs = [
    (f"{sender_name} <bots@yunuchoi.me>", "하루 한 입 지식, 받으셨나요? 🔍"),
    (f"{sender_name} <bots@yunuchoi.me>", "오잉? 이런 사실 알고 계셨나요? 📬"),
    (f"{sender_name} <bots@yunuchoi.me>", "오늘의 지식 간식 드셔보세요 🍿🧠"),
    (f"{sender_name} <bots@yunuchoi.me>", "사알짝 똑똑해지는 오늘의 한 줄 ✨"),
    (f"{sender_name} <bots@yunuchoi.me>", "오늘의 호기심 한 방울 도착! 💌"),
    (f"{sender_name} <bots@yunuchoi.me>", "헉! 이런 것도 있었어? 🧠"),
    (f"{sender_name} <bots@yunuchoi.me>", "당신의 두뇌에 오늘도 한 입 💡"),
    (f"{sender_name} <bots@yunuchoi.me>", "딱! 하고 떨어지는 지식 한 조각 📸"),
    (f"{sender_name} <bots@yunuchoi.me>", "상큼한 오늘의 상식 🍋"),
    (f"{sender_name} <bots@yunuchoi.me>", "당신의 인박스에 작은 놀라움 ✉️")
]

def get_daily_trivia():
    prompt = (
        "짧고 흥미로운 토막 상식을 만들어 주세요. 주제는 자유입니다. "
        "소개 → 지식 → 연장의 흐름을 따르되, 전체는 3~4문장 정도의 간결한 한 문단으로 구성해 주세요. "
        "소개는 흥미를 끄는 간단한 질문이나 상황 제시로 시작해 주세요. "
        "이후 본론인 지식 정보를 간결하고 명확하게 전달해 주세요. "
        "마지막은 그 지식에 대한 흥미로운 연장 설명이나, 연결 가능한 관련 정보로 마무리해 주세요. "
        "인사말이나 여는 말 등은 생략하고, 본문만 작성해 주세요."
    )

    response = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    trivia = response.choices[0].message.content.strip()
    return trivia


def send_email(body):
    recipients = RECIPIENTS.split(",")
    selected_sender, selected_subject_base = random.choice(sender_subject_pairs)

    today = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    selected_subject = f"{selected_subject_base} - {today} 오늘의 토막상식"

    msg = EmailMessage()
    msg['From'] = selected_sender
    msg['To'] = "지식 구독자 <hello@yunuchoi.me>"
    msg['Subject'] = selected_subject
    msg['Bcc'] = ", ".join(recipients)
    msg.set_content(body)

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
