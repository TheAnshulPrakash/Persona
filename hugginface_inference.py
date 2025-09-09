from huggingface_hub import InferenceClient
import flet as ft
client = InferenceClient(
    "openai/gpt-oss-20b",
    token="<hf_YourToken>"
)


class GPTInterviewHuggingFace:
    def __init__(self, user_info, job_role, interview_type, no_of_questions, interview_req, file_name ):
        self.filename=file_name
        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are a professional job interviewer speaking with the candidate. "
                    "Your main goal is to evaluate the candidate’s suitability for the role while making the conversation feel natural, "
                    "engaging, and respectful — just like a real human interviewer. "
                    f"You should ask up to {no_of_questions} thoughtful questions based on the candidate’s background. "
                    f"The candidate’s skills are: {user_info}. "
                    f"The job role is {job_role}, with key requirements: {interview_req}. "
                    f"Conduct the interview in a {interview_type} style. "
                    "If the candidate asks you something, you may respond conversationally (brief, natural replies) "
                    "before continuing the interview flow. "
                    "Avoid robotic phrasing — keep your wording warm, human-like, and adaptive."
                ),
            },
            {
                "role": "system",
                "content": (
                    "Your reply must ALWAYS be in a single JSON object (no Markdown, no text outside JSON). "
                    "Never repeat the same object twice. Never output arrays unless explicitly asked. "
                    "Use exactly this schema:\n\n"
                    "{\n"
                    '  "question_number": <integer>,\n'
                    '  "type": "<General | Programming | Behavioral | Technical | DSA>",\n'
                    '  "text": "<the next interview question or conversational reply, phrased naturally>",\n'
                    '  "evaluation": {\n'
                    '    "english_proficiency": <0-10 or null>,\n'
                    '    "confidence": <0-10 or null>,\n'
                    '    "content_quality": <0-10 or null>,\n'
                    '    "notes": "<short natural note about the candidate’s last answer, or empty if no answer yet>"\n'
                    "  },\n"
                    '  "end": <true | false>\n'
                    "}\n\n"
                    "Evaluation rules:\n"
                    "- If this is the very first question (no answer yet), leave all evaluation fields null.\n"
                    "- Otherwise, score english_proficiency (clarity & grammar), confidence (assurance & fluency), and content_quality (depth & relevance) on 1–10.\n"
                    "- notes should be short and natural, like an interviewer jotting impressions (not robotic)."
                ),
            },
            {
                "role": "system",
                "content": (
                    "Question rules:\n"
                    "- Always choose exactly one type.\n"
                    "- 'General' for introductions, background, and motivation.\n"
                    "- 'Behavioral' for teamwork, conflict resolution, and soft skills.\n"
                    "- 'Technical' for system design, architecture, applied technology.\n"
                    "- 'Programming' for language-specific or conceptual discussions (without requiring code).\n"
                    "- 'DSA' only when asking the candidate to explain/write an algorithm or implementation.\n"
                    "You may also give short conversational replies to candidate’s questions or comments — keep them warm and professional, "
                    "then smoothly continue with the interview."
                ),
            },
            {
                "role": "system",
                "content": (
                    "Start with: question_number=1, type='General', asking the candidate to introduce themselves in a friendly, natural way."
                ),
            },
        ]

        

    def chat_with_model(self, user_input: str, container: ft.Container, text: ft.Text, mic: ft.Container, current_theme, current_text_theme):
        global messages
        
        
        messages.append({"role": "user", "content": user_input})

        
        stream = client.chat.completions.create(
            model="openai/gpt-oss-20b",  
            messages=messages,
            stream=True,
        )

        collected_response = ""

        for chunk in stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            if delta and delta.content:
                print(delta.content, end="", flush=True)
                collected_response += delta.content

        print("\n--- done ---")

        messages.append({"role": "assistant", "content": collected_response})
        
