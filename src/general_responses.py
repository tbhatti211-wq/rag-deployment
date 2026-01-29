# general_responses.py
"""
General knowledge and conversational response handler.
This file contains predefined responses for non-technical questions.
"""

def get_general_response(question: str) -> str:
    """
    Return appropriate response for general/conversational questions.
    """
    question_lower = question.lower().strip()

    # Conversational responses
    if 'how are you' in question_lower or 'how do you do' in question_lower:
        return "I'm doing well, thank you! I'm here to help with questions about machine learning, web development, data science, and cloud computing. What would you like to know about these topics?"

    elif any(greeting in question_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
        return "Hello! I'm your technical assistant specializing in machine learning, web development, data science, and cloud computing. How can I help you today?"

    elif any(thanks in question_lower for thanks in ['thank you', 'thanks', 'thank you very much']):
        return "You're welcome! Feel free to ask me more questions about technology topics."

    elif any(bye in question_lower for bye in ['goodbye', 'bye', 'see you', 'farewell']):
        return "Goodbye! Have a great day!"

    # General knowledge questions - redirect to technical topics
    elif any(word in question_lower for word in ['what', 'where', 'when', 'why', 'how', 'who']) and not any(tech in question_lower for tech in ['machine learning', 'web development', 'data science', 'cloud computing', 'programming', 'software', 'code', 'algorithm', 'database', 'api']):
        return "I'm sorry, but I specialize in technical topics like machine learning, web development, data science, and cloud computing. I don't have information about general knowledge questions. Would you like to ask me something about these technical areas instead?"

    # Default fallback
    else:
        return "I'm a technical assistant focused on machine learning, web development, data science, and cloud computing. I don't have information about that topic. What technical question can I help you with?"