
import openai, requests, os, random
from datetime import datetime

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
GUMROAD_KEY = os.getenv("GUMROAD_API_KEY")

topics = [
    "Personal Growth Mastery",
    "Ultimate Productivity Toolkit",
    "Confidence and Charisma Training",
    "Goal Setting and Achievement Pack",
    "Emotional Intelligence Masterclass",
    "Mindset and Success Habits Bundle",
    "Focus and Deep Work Guide",
    "Morning Routines of Top Achievers",
    "Beat Procrastination Fast",
    "Motivation and Self-Discipline Secrets"
]

def generate_ebook(topic):
    prompt = f"Write a high-quality 10-page guide on '{topic}' with actionable steps and examples. Use Markdown."
    r = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role":"user","content":prompt}],
        max_tokens=3000
    )
    return r.choices[0].message["content"]

def generate_pack(topic):
    ebooks = []
    for i in range(3):  # Create 3 ebooks per pack
        subtopic = topic + f" - Part {i+1}"
        ebooks.append(generate_ebook(subtopic))
    return ebooks

def save_pack(ebooks, topic):
    pack_name = topic.replace(" ","_") + "_" + datetime.now().strftime("%Y%m%d%H%M%S")
    os.makedirs("ebooks", exist_ok=True)
    filepath = f"ebooks/{pack_name}.md"
    with open(filepath, "w", encoding="utf-8") as f:
        for i, content in enumerate(ebooks):
            f.write(f"# Part {i+1}\n\n{content}\n\n")
    return filepath

def upload_to_gumroad(file_path, title, price):
    url = "https://api.gumroad.com/v2/products"
    data = {
        "access_token": GUMROAD_KEY,
        "name": title + " (Premium Pack)",
        "price": price,
        "description": f"A premium self-improvement pack on {title}. Includes multiple guides for fast results. PayPal: fargnom14@gmail.com",
        "custom_permalink": title.lower().replace(" ", "-"),
        "tags": "self improvement, personal growth, productivity, mindset, success",
        "published": True
    }
    files = {"file": open(file_path, "rb")}
    return requests.post(url, data=data, files=files).json()

if __name__ == "__main__":
    for _ in range(3):  # Generate 3 premium packs per run
        topic = random.choice(topics)
        ebooks = generate_pack(topic)
        file_path = save_pack(ebooks, topic)
        gumroad_res = upload_to_gumroad(file_path, topic, random.choice([1900, 2500, 3900]))  # €19-39
        print("Uploaded premium pack:", gumroad_res)
