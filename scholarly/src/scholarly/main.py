import os
from crewai import Crew
import yaml
from PyPDF2 import PdfReader
from gtts import gTTS
from scholarly.crew import Scholarly
from crewai import Agent, Task, Crew 
# Load paper list
papers = [
    {"paper_name": "paper1.pdf", "paper_topic": "Reinforcement Learning"},
    {"paper_name": "paper2.pdf", "paper_topic": "Neurosymbolic AI"}
]

def extract_text_from_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    except Exception as e:
        print(f"❌ Failed to extract PDF text: {e}")
        return ""

def summarize_with_openai(text, topic, section="full paper"):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"Summarize the following {section} about {topic} in 3 paragraphs:\n\n{text[:3000]}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert scientific writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5
    )

    return response.choices[0].message.content
def narrate_text(text, filename="summary.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    print(f"🔊 Saved narration as {filename}")

def load_crew_config(paper):
    # Load agents.yaml
    agents_config_path = os.path.join(os.path.dirname(__file__), "config", "agents.yaml")
    with open(agents_config_path, "r") as f:
        agent_data = yaml.safe_load(f)

    agents = {}
    for key, cfg in agent_data.items():
        agents[key] = Agent(
            role=cfg["role"].format(**paper),
            goal=cfg["goal"].format(**paper),
            backstory=cfg["backstory"].format(**paper),
            verbose=True
        )

    # Load tasks.yaml
    crew_config_path = os.path.join(os.path.dirname(__file__), "config", "tasks.yaml")
    with open(crew_config_path, "r") as f:
        raw_tasks = yaml.safe_load(f)

    tasks = []
    for task_def in raw_tasks.get("tasks", []):
        task = Task(
            description=task_def["description"].format(**paper),
            expected_output=task_def["expected_output"].format(**paper),
            agent=agents[task_def["agent"]],
            async_execution=False,
            depends_on=task_def.get("depends_on", [])
        )
        tasks.append(task)

    return Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True
    )

def scholarly_pipeline(paper):
    print(f"\n📘 Processing: {paper['paper_name']} - Topic: {paper['paper_topic']}")

    pdf_path = os.path.join("papers", paper["paper_name"])
    full_text = extract_text_from_pdf(pdf_path)

    if not full_text:
        return

    # Summarize for MVP
    print("📝 Summarizing content...")
    summary = summarize_with_openai(full_text, topic=paper["paper_topic"])
    print("✅ Summary ready:\n", summary[:300], "...")

    # Narrate
    print("🎤 Narrating summary...")
    narrate_text(summary, filename=f"{paper['paper_name'].replace('.pdf', '')}_narration.mp3")

    # Agent workflow
    print("🧠 Running agent pipeline...")

    inputs = {
        "paper_name": paper["paper_name"],
        "paper_topic": paper["paper_topic"],
        "full_text": full_text,
        "summary": summary
    }

    Scholarly().crew().kickoff(inputs=inputs)

# file: src/scholarly/main.py
def run():
    papers = [
        {"paper_name": "paper1.pdf", "paper_topic": "Reinforcement Learning"},
        {"paper_name": "paper2.pdf", "paper_topic": "Neurosymbolic AI"}
    ]
    for paper in papers:
        scholarly_pipeline(paper)