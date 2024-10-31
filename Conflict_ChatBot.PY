import os
import openai
from chatbot import get_chatbot_response, recognize_speech, speak # type: ignore
import speech_recognition as sr
import random

openai.api_key = "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"
openai.api_key = os.getenv("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")


def get_chatbot_response(prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Using GPT-3.5
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Sorry, I didn't catch that. Could you please repeat?"

def detect_conflict(query):
    # List of keywords related to common service conflicts
    conflict_keywords = [
        "late", "overcharge", "wrong", "bad service", "dirty", "poor quality",
        "did not show up", "canceled", "bad experience", "unhappy", "problem"
    ]
    return any(keyword in query.lower() for keyword in conflict_keywords)

def handle_conflict(query):
    speak("I'm really sorry you're having this issue. Could you provide more details about the problem?")
    detailed_complaint = recognize_speech()

    if detailed_complaint:
        speak("Thank you for the details. Let me check with the service provider.")
        response = simulate_provider_response(detailed_complaint)

        if response:
            speak(f"The service provider has responded: {response}")
        else:
            speak("I couldn't get a response from the service provider. Let me escalate this matter.")

def simulate_provider_response(detailed_complaint):
    simulated_responses = [
        "We apologize for the inconvenience. A representative will contact you shortly.",
        "Your complaint has been noted, and we are working to resolve the issue.",
        "Thank you for bringing this to our attention. A refund has been initiated."
    ]
    return random.choice(simulated_responses)

def predefined_answers(query):
    qa_pairs = {
        "what is your refund": "Our refund policy allows you to request a refund within 30 days of service completion.",
        "where are you located": "We are located at institute technology university of morattuwa.",
        "what service do you offer": "We offer a range of services including home cleaning, plumbing, and electrical repairs.",
        "how can I contact customer support": "You can contact customer support at muhammed naveeth@gmail.com or call us at 0759560114.",
        "what are your hours of operation": "Our hours of operation are Monday to Friday, 9 AM to 5 PM.",
        "Can I book online": "Yes, you can easily book a service online through our website or mobile app.",
        "Do you offer emergency services?": "Yes, we offer emergency services 24/7 for immediate assistance.",
        "How is my booking confirmed?": "You'll receive a confirmation email with all details after booking.",
        "How do you ensure service quality?": "We work with experienced professionals and encourage customer ratings.",
        "What payment methods do you accept?": "We accept credit/debit cards, mobile wallets, and cash on delivery.",
        "Do you offer recurring services?": "Yes, we offer weekly or monthly cleaning and maintenance packages.",
        "Is there a warranty for services?": "Yes, we offer a warranty period for most services to address any issues."
    }
    
    query = query.lower()
    for question, answer in qa_pairs.items():
        if all(word in query for word in question.split()):
            return answer
    return None

def naveeth_chatbot():
    speak("Hello Tapon Guys. How can I assist you today?")
    
    while True:
        try:
            query = recognize_speech()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you please repeat?")
            continue
        except sr.RequestError:
            speak("There was an issue with the speech recognition service.")
            continue

        if query:
            # Check for predefined questions first
            answer = predefined_answers(query)
            if answer:
                print(f"TapOn: {answer}")
                speak(answer)
                continue

            # Detect if there is a conflict
            if detect_conflict(query):
                speak("I'm sorry to hear you're having an issue. Let me help you resolve it.")
                handle_conflict(query)
                continue

            # Exit condition
            if "exit" in query.lower() or "stop" in query.lower():
                speak("Goodbye! Have a nice day.")
                break

            # Get a chatbot response for other queries
            chatbot_response = get_chatbot_response(query)
            print(f"TapOn: {chatbot_response}")
            speak(chatbot_response)

if __name__ == "__main__":
    naveeth_chatbot()
