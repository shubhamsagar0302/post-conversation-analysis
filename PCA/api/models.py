from django.db import models

class Conversation(models.Model):
    """
    Represents a single chat conversation. [cite: 33]
    """
    title = models.CharField(max_length=255, blank=True, null=True) # [cite: 34]
    created_at = models.DateTimeField(auto_now_add=True) # [cite: 35]

    def __str__(self):
        return f"Conversation {self.id} on {self.created_at.strftime('%Y-%m-%d')}"

class Message(models.Model):
    """
    Represents a single message within a conversation. [cite: 36]
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages" # [cite: 37]
    )
    sender = models.CharField(max_length=20)  # "user" or "ai" [cite: 38]
    text = models.TextField() # [cite: 38]
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.text[:50]}..."

class ConversationAnalysis(models.Model):
    """
    Stores the analysis results for a single conversation. [cite: 39]
    Based on the parameters in the PDF. [cite: 24, 25]
    """
    conversation = models.OneToOneField(
        Conversation,
        on_delete=models.CASCADE,
        related_name="analysis" # [cite: 40, 41]
    )
    # Quality Parameters [cite: 24]
    clarity_score = models.FloatField(null=True, blank=True)
    relevance_score = models.FloatField(null=True, blank=True)
    accuracy_score = models.FloatField(null=True, blank=True)
    completeness_score = models.FloatField(null=True, blank=True)
    
    # Interaction Parameters [cite: 25]
    sentiment = models.CharField(max_length=20, null=True, blank=True) # positive, neutral, negative
    empathy_score = models.FloatField(null=True, blank=True)
    response_time_avg = models.FloatField(null=True, blank=True) # Mocked data
    
    # Resolution Parameters [cite: 25]
    resolution = models.BooleanField(null=True, blank=True) # Was the issue resolved?
    escalation_need = models.BooleanField(null=True, blank=True) # Should this be escalated?
    
    # AI Ops [cite: 25]
    fallback_frequency = models.IntegerField(default=0) # Count of "I don't know"
    
    # Overall [cite: 25]
    overall_score = models.FloatField(null=True, blank=True) # Computed score
    
    created_at = models.DateTimeField(auto_now_add=True) # [cite: 46]

    def __str__(self):
        return f"Analysis for Conversation {self.conversation.id}"