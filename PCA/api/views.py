from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conversation, Message, ConversationAnalysis
from .serializers import ConversationAnalysisSerializer, ConversationUploadSerializer
from .services.analysis_service import perform_analysis

class ConversationUploadView(APIView):
    """
    API endpoint to upload a new chat conversation.
    Expects a JSON list of message objects. [cite: 29]
    e.g., [{"sender": "user", "message": "Hello"}, {"sender": "ai", "message": "Hi"}]
    """
    def post(self, request, *args, **kwargs):
        # Validate the input data structure
        serializer = ConversationUploadSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        chat_data = serializer.validated_data
        
        try:
            # Create the parent Conversation
            conversation = Conversation.objects.create(
                title=f"Chat on {request.data[0].get('message', '... (no message)')[:50]}"
            )
            
            # Create Message objects in bulk
            messages_to_create = [
                Message(
                    conversation=conversation,
                    sender=msg['sender'],
                    text=msg['message']
                ) for msg in chat_data
            ]
            Message.objects.bulk_create(messages_to_create)
            
            return Response(
                {"message": "Conversation uploaded successfully", "conversation_id": conversation.id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TriggerAnalysisView(APIView):
    """
    API endpoint to manually trigger analysis for a specific conversation. 
    """
    def post(self, request, pk, *args, **kwargs):
        try:
            conversation = Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if analysis already exists
        if hasattr(conversation, 'analysis'):
             return Response(
                {"message": "Analysis already exists for this conversation", "analysis_id": conversation.analysis.id},
                status=status.HTTP_200_OK
            )

        # Call the analysis service [cite: 30]
        analysis = perform_analysis(conversation_id=pk)
        
        if analysis:
            return Response(
                {"message": f"Analysis completed for conversation {pk}", "analysis_id": analysis.id},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "Failed to perform analysis"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ReportListView(generics.ListAPIView):
    """
    API endpoint to list all completed conversation analysis reports. 
    """
    queryset = ConversationAnalysis.objects.all().order_by('-created_at')
    serializer_class = ConversationAnalysisSerializer