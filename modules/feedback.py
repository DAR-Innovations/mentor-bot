from transformers import pipeline
import torch

class FeedbackGenerator:
    def __init__(self):
        device = 0 if torch.cuda.is_available() else -1
        self.generative_pipeline = pipeline("text-generation", model="gpt2", device=device)

    def generate_feedback(self, question, answer, analysis):
        detailed_feedback = self.generative_pipeline(
            f"Question: {question}\nAnswer: {answer}\nAnalysis: {analysis}\nFeedback:",
            max_new_tokens=150,
            num_return_sequences=1,
            truncation=True,
            pad_token_id=50256,
        )[0]["generated_text"]

        return {
            "relevance": f"{analysis['relevance']:.2f}",
            "sentiment": analysis["sentiment"],
            "clarity": analysis["clarity"],
            "score": round((analysis["relevance"] * 6 + analysis["sentiment_score"] * 4), 2),
            "detailed_feedback": detailed_feedback.strip(),
        }

    def generate_overall_feedback(self, responses):
        # Summarize structured responses
        strengths = []
        weaknesses = []
        improvement_suggestions = []

        for r in responses:
            feedback = r["feedback"]
            if "Positive" in feedback["sentiment"]:
                strengths.append(f"Question: {r['question']} - {feedback['detailed_feedback']}")
            else:
                weaknesses.append(f"Question: {r['question']} - {feedback['detailed_feedback']}")
                improvement_suggestions.append(f"Improve response to: {r['question']}")

        summary = f"""
        Strengths:
        {', '.join(strengths) if strengths else 'None'}

        Weaknesses:
        {', '.join(weaknesses) if weaknesses else 'None'}

        Suggestions for Improvement:
        {', '.join(improvement_suggestions) if improvement_suggestions else 'None'}
        """

        return summary.strip()
