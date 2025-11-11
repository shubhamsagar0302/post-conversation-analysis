from django.urls import path
from . import views

urlpatterns = [
    # /api/conversations/ 
    path('conversations/', views.ConversationUploadView.as_view(), name='conversation-upload'),
    
    # /api/analyse/<id>/ 
    path('analyse/<int:pk>/', views.TriggerAnalysisView.as_view(), name='trigger-analysis'),
    
    # /api/reports/ 
    path('reports/', views.ReportListView.as_view(), name='report-list'),
]