import gradio as gr
from genbrain_core.engine import process_note

def genbrain_pipeline(text):
    result = process_note(text)

    summary = result["summary"]
    tags = ", ".join(result["tags"])
    questions = "\n".join(result["questions"])
    links = "\n".join([f"→ {link['summary']} (Score: {link['score']})" for link in result["related_notes"]])

    return summary, tags, questions, links

demo = gr.Interface(
    fn=genbrain_pipeline,
    inputs=gr.Textbox(label="Paste your raw note here", lines=10, placeholder="Type or paste your thoughts..."),
    outputs=[
        gr.Textbox(label="📝 Summary"),
        gr.Textbox(label="🔖 Tags"),
        gr.Textbox(label="❓ Follow-Up Questions"),
        gr.Textbox(label="🔗 Related Notes")
    ],
    title="🧠 GenBrain: AI-Powered Notetaking Assistant",
    description="Organize your thoughts with summarization, tagging, question generation and semantic linking"
)

if __name__ == "__main__":
    demo.launch()
