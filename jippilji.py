import datetime
import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from openai import OpenAI

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECIPIENTS = os.getenv("RECIPIENTS")

# OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

def get_daily_trivia():
    prompt = (
        "짧고 흥미로운 토막 상식을 만들어 주세요. "
        "인사 등 기타 미사여구는 생략하고 본론만 얘기합니다."
        "길이는 1문단으로 간결하게 해주세요."
    )
    response = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )
    trivia = response.choices[0].message.content.strip()
    return trivia
    # return "테스트이옵니다."


def send_email(subject, body):
    recipients = RECIPIENTS.split(",")

    msg = EmailMessage()
    msg['From'] = f"집필지 (輯弼知) | ⚜ 조선 황실 비밀 보좌관"
    msg['Subject'] = subject
    msg['Bcc'] = ", ".join(recipients)
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


if __name__ == "__main__":
    today = datetime.datetime.now().strftime("%Y년 %m월 %d일")
    trivia = get_daily_trivia()
    subject = f"전하, 오늘의 토막 상식 아뢰옵니다 - {today}"
    body = (
        f"아뢰옵기 황송하오나, 아래는 오늘의 토막 상식이옵니다:\n\n"
        f"{trivia}"
        f"\n\n"
        f"⚜ 조선 황실 비밀 보좌관 | 집필지 (輯弼知)"
    )

    send_email(subject, body)
