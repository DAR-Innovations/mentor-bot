import random
from datetime import datetime
from modules.text_to_speech import TextToSpeech
from modules.speech_to_text import SpeechToText
from modules.analysis import ResponseAnalyzer
from modules.feedback import FeedbackGenerator
from modules.utils import load_questions, save_responses

def main():
    # Load questions from JSON and randomize
    questions = load_questions("data/questions.json")
    random.shuffle(questions)

    # Initialize modules
    tts = TextToSpeech()
    stt = SpeechToText()
    analyzer = ResponseAnalyzer()
    feedback_generator = FeedbackGenerator()

    print("Welcome to the AI Job Interview Simulator!")
    session_responses = []

    for i, question in enumerate(questions, 1):
        timestamp = datetime.now().isoformat()
        print(f"\n[{timestamp}] Question {i}: {question}")
        tts.speak_text(question)

        # Listen and transcribe answer with retries
        retries = 3
        answer = None
        while retries > 0 and not answer:
            print("Listening for your answer...")
            answer, transcript = stt.record_and_transcribe()
            if answer:
                break
            print("I couldn't understand your answer. Please try again.")
            retries -= 1

        if not answer:
            print("\nNo answer detected. Moving to the next question.")
            session_responses.append({
                "timestamp": timestamp,
                "question": question,
                "answer": "",
                "feedback": "No answer provided."
            })
            continue

        print(f"\nYour Answer: {transcript}")

        # Analyze response
        analysis = analyzer.analyze(question, answer)
        feedback = feedback_generator.generate_feedback(question, answer, analysis)

        # Save session data
        session_responses.append({
            "timestamp": timestamp,
            "question": question,
            "answer": answer,
            "feedback": feedback
        })

        # Display feedback
        print("\nFeedback:")
        print(f"- Relevance: {feedback['relevance']}")
        print(f"- Sentiment: {feedback['sentiment']}")
        print(f"- Clarity: {feedback['clarity']}")
        print(f"- Score: {feedback['score']} / 10")
        print("-" * 50)

    # Generate and display overall feedback
    overall_feedback = feedback_generator.generate_overall_feedback(session_responses)
    print("\n=== Overall Interview Feedback ===")
    print(overall_feedback)

    # Save responses to file
    save_responses("data/responses.json", session_responses)
    print("\nYour responses and overall feedback have been saved. Thank you!")

if __name__ == "__main__":
    main()
