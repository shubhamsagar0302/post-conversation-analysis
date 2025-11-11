from rest_framework import serializers
from .models import Conversation, Message, ConversationAnalysis

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """
    class Meta:
        model = Message
        fields = ['sender', 'text', 'created_at']

class ConversationAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for the ConversationAnalysis report. 
    """
    # Use 'conversation.id' for a cleaner report
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ConversationAnalysis
        fields = [
            'id', 'conversation', 'clarity_score', 'relevance_score',
            'accuracy_score', 'completeness_score', 'sentiment',
            'empathy_score', 'response_time_avg', 'resolution',
            'escalation_need', 'fallback_frequency', 'overall_score', 'created_at'
        ]

class ConversationUploadSerializer(serializers.Serializer):
    """
    A custom serializer to validate the input JSON structure. [cite: 9-21]
    Each item in the list should be a dict with "sender" and "message".
    """
    sender = serializers.ChoiceField(choices=['user', 'ai'])
    message = serializers.CharField()