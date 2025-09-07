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

sender_name = "오늘의 토막상식"  # "Today's Daily Trivia"
sender_email = f"{sender_name} <bots@yunuchoi.me>"

subject_options = [
    "하루 한 입 지식, 받으셨나요? 🔍",  # "A bite of knowledge a day, did you get it? 🔍"
    "오잉? 이런 사실 알고 계셨나요? 📬",  # "Oh? Did you know this fact? 📬"
    "오늘의 지식 간식 드셔보세요 🍿🧠",  # "Try today's knowledge snack 🍿🧠"
    "사알짝 똑똑해지는 오늘의 한 줄 ✨",  # "A line to make you a bit smarter today ✨"
    "오늘의 호기심 한 방울 도착! 💌",  # "A drop of curiosity for today has arrived! 💌"
    "헉! 이런 것도 있었어? 🧠",  # "Wow! This existed too? 🧠"
    "당신의 두뇌에 오늘도 한 입 💡",  # "A bite for your brain today as well 💡"
    "딱! 하고 떨어지는 지식 한 조각 📸",  # "A perfect piece of knowledge 📸"
    "상큼한 오늘의 상식 🍋",  # "Refreshing today's trivia 🍋"
    "당신의 인박스에 작은 놀라움 ✉️",  # "A small surprise in your inbox ✉️"
]

topics_by_day = {
    0: [
        "과학",  # "Science"
        "물리학",  # "Physics"
        "화학",  # "Chemistry"
        "생물학",  # "Biology"
        "지구과학",  # "Earth Science"
        "뇌과학",  # "Neuroscience"
        "유전학",  # "Genetics"
        "진화",  # "Evolution"
        "에너지",  # "Energy"
        "나노기술",  # "Nanotechnology"
        "의학",  # "Medicine"
        "신경과학",  # "Neuroscience"
        "광학",  # "Optics"
        "양자역학",  # "Quantum Mechanics"
        "생명공학",  # "Biotechnology"
    ],
    1: [
        "역사",  # "History"
        "고대문명",  # "Ancient Civilization"
        "근대사",  # "Modern History"
        "세계사",  # "World History"
        "한국사",  # "Korean History"
        "중세유럽",  # "Medieval Europe"
        "산업혁명",  # "Industrial Revolution"
        "전쟁사",  # "History of War"
        "왕조",  # "Dynasty"
        "유물",  # "Artifact"
        "고고학",  # "Archaeology"
        "혁명",  # "Revolution"
        "탐험",  # "Exploration"
        "역사적 인물",  # "Historical Figure"
        "문화유산",  # "Cultural Heritage"
    ],
    2: [
        "예술",  # "Art"
        "미술",  # "Fine Art"
        "음악",  # "Music"
        "문학",  # "Literature"
        "영화",  # "Film"
        "사진",  # "Photography"
        "조각",  # "Sculpture"
        "건축",  # "Architecture"
        "디자인",  # "Design"
        "연극",  # "Theater"
        "무용",  # "Dance"
        "만화",  # "Comics"
        "예술사",  # "Art History"
        "현대미술",  # "Modern Art"
        "예술가",  # "Artist"
    ],
    3: [
        "기술",  # "Technology"
        "컴퓨터",  # "Computer"
        "인공지능",  # "Artificial Intelligence"
        "로봇",  # "Robot"
        "인터넷",  # "Internet"
        "모바일",  # "Mobile"
        "가상현실",  # "Virtual Reality"
        "블록체인",  # "Blockchain"
        "자동차",  # "Automobile"
        "항공우주",  # "Aerospace"
        "전자공학",  # "Electronic Engineering"
        "프로그래밍",  # "Programming"
        "보안",  # "Security"
        "게임",  # "Game"
        "스타트업",  # "Startup"
    ],
    4: [
        "문화",  # "Culture"
        "언어",  # "Language"
        "풍습",  # "Custom"
        "음식",  # "Food"
        "축제",  # "Festival"
        "패션",  # "Fashion"
        "종교",  # "Religion"
        "철학",  # "Philosophy"
        "여행",  # "Travel"
        "전통",  # "Tradition"
        "의례",  # "Ritual"
        "세계관",  # "Worldview"
        "유행",  # "Trend"
        "사회",  # "Society"
        "예절",  # "Etiquette"
    ],
    5: [
        "자연",  # "Nature"
        "동물",  # "Animal"
        "식물",  # "Plant"
        "기후",  # "Climate"
        "지리",  # "Geography"
        "생태계",  # "Ecosystem"
        "바다",  # "Sea"
        "산",  # "Mountain"
        "강",  # "River"
        "사막",  # "Desert"
        "지진",  # "Earthquake"
        "화산",  # "Volcano"
        "날씨",  # "Weather"
        "환경",  # "Environment"
        "자연재해",  # "Natural Disaster"
    ],
    6: [
        "우주",  # "Space"
        "천문학",  # "Astronomy"
        "행성",  # "Planet"
        "별",  # "Star"
        "블랙홀",  # "Black Hole"
        "우주탐사",  # "Space Exploration"
        "외계생명",  # "Extraterrestrial Life"
        "은하",  # "Galaxy"
        "우주선",  # "Spaceship"
        "우주정거장",  # "Space Station"
        "달",  # "Moon"
        "태양",  # "Sun"
        "우주과학",  # "Space Science"
        "우주비행사",  # "Astronaut"
        "우주망원경",  # "Space Telescope"
    ],
}


def get_daily_trivia():
    today_weekday = datetime.datetime.now().weekday()
    topic_list = topics_by_day.get(today_weekday, ["일반"])  # "General"
    topic = random.choice(topic_list)
    print(f"Selected topic for today: {topic}")
    prompt = (
        f"'{topic}'를 주제로 짧고 흥미로운 토막 상식을 만들어 주세요."  # "Please create a short and interesting trivia based on the topic '{topic}'."
        "소개 → 지식 → 연장의 흐름을 따르되, 전체는 3~4문장 정도의 간결한 한 문단으로 구성해 주세요. "  # "Follow the flow of introduction → knowledge → extension, and make it a concise paragraph of about 3-4 sentences."
        "소개는 흥미를 끄는 간단한 질문이나 상황 제시로 시작해 주세요. "  # "Start the introduction with an engaging question or scenario."
        "이후 본론인 지식 정보를 간결하고 명확하게 전달해 주세요. "  # "Then, deliver the main knowledge information concisely and clearly."
        "마지막은 그 지식에 대한 흥미로운 연장 설명이나, 연결 가능한 관련 정보로 마무리해 주세요. "  # "Finally, end with an interesting extension or related information about the knowledge."
        "인사말이나 여는 말 등은 생략하고, 본문만 작성해 주세요."  # "Omit greetings or opening remarks, and write only the main text."
        "모든 문장은 존댓말로 작성하되 어투를 딱딱하지 않게 자연스럽고 친근하게 해 주세요. "  # "Write all sentences in polite form, but keep the tone natural and friendly, not stiff."
    )

    response = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
    )
    trivia = response.choices[0].message.content.strip()
    return trivia


def send_email(body):
    recipients = RECIPIENTS.split(",")
    selected_subject_base = random.choice(subject_options)

    today = datetime.datetime.now().strftime(
        "%Y년 %m월 %d일"
    )  # "%Y year %m month %d day"
    selected_subject = f"{selected_subject_base} - {today} 오늘의 토막상식"  # "... - ... Today's Trivia"

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = (
        "지식 구독자 <hello@yunuchoi.me>"  # "Knowledge Subscriber <hello@yunuchoi.me>"
    )
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
        "오늘의 뇌를 자극하는 한 입 정보입니다 🧠✨\n\n"  # "Here's a bite of information to stimulate your brain today 🧠✨"
        f"{trivia}\n\n"
        "— 오늘의 토막상식팀 드림"  # "— From the Today's Daily Trivia Team"
    )

    send_email(body)
