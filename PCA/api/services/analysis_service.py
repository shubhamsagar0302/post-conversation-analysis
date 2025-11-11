import random
from api.models import Conversation, Message, ConversationAnalysis

def perform_analysis(conversation_id: int) -> ConversationAnalysis:
    """
    Performs a (mocked) post-conversation analysis.
    
    In a real application, this function would:
    1. Load messages.
    2. Run NLP models for sentiment, clarity, empathy, etc.
    3. Check for keywords (e.g., "I don't know") for fallback.
    4. Check for resolution keywords (e.g., "thanks, that fixed it").
    5. Calculate a final score.
    
    Here, we just use random data to simulate the process. [cite: 30]
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        print(f"Conversation {conversation_id} not found.")
        return None

    # --- MOCKED ANALYSIS LOGIC ---
    
    messages = conversation.messages.all()
    if not messages:
        return None # Can't analyze an empty conversation

    # [cite: 24] Mocking Quality parameters (scores out of 5)
    clarity = random.uniform(3.0, 5.0)
    relevance = random.uniform(3.0, 5.0)
    accuracy = random.uniform(3.0, 5.0)
    completeness = random.uniform(4.0, 5.0)

    # [cite: 25] Mocking Interaction parameters
    sentiment = random.choice(['positive', 'neutral', 'negative'])
    empathy = random.uniform(1.0, 5.0)
    response_time = random.uniform(5.0, 30.0) # Mocked average response time

    # [cite: 25] Mocking Resolution parameters
    resolution = random.choice([True, False])
    escalation = random.choice([True, False]) if sentiment == 'negative' else False

    # [cite: 25] Mocking AI Ops
    # Count messages from AI containing "don't know"
    fallback_count = 0
    ai_messages = messages.filter(sender='ai')
    for msg in ai_messages:
        if "don't know" in msg.text.lower() or "not sure" in msg.text.lower():
            fallback_count += 1
            
    # [cite: 25] Mocking Overall Score (e.g., average of key parameters)
    key_scores = [clarity, relevance, accuracy, completeness, empathy]
    overall = sum(key_scores) / len(key_scores)

    # --- END MOCKED ANALYSIS ---

    # Create or update the analysis object [cite: 31, 39]
    analysis, created = ConversationAnalysis.objects.update_or_create(
        conversation=conversation,
        defaults={
            'clarity_score': round(clarity, 2),
            'relevance_score': round(relevance, 2),
            'accuracy_score': round(accuracy, 2),
            'completeness_score': round(completeness, 2),
            'sentiment': sentiment,
            'empathy_score': round(empathy, 2),
            'response_time_avg': round(response_time, 2),
            'resolution': resolution,
            'escalation_need': escalation,
            'fallback_frequency': fallback_count,
            'overall_score': round(overall, 2)
        }
    )
    
    print(f"Analysis {'created' if created else 'updated'} for Conversation {conversation.id}")
    return analysis
