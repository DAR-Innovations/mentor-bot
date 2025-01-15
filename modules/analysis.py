from transformers import pipeline

class ResponseAnalyzer:
    def __init__(self):
        self.qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad", truncation=True)
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    def analyze(self, question, answer):
        relevance = self.qa_pipeline(question=question, context=answer, truncation=True)["score"]
        sentiment = self.sentiment_pipeline(answer)[0]
        clarity = "Clear" if len(answer.split()) > 5 else "Too short"
        score = (relevance * 0.6) + (sentiment["score"] * 0.4)
        return {
            "relevance": relevance,
            "sentiment": sentiment["label"],
            "sentiment_score": sentiment["score"],
            "clarity": clarity,
            "score": score,
        }
