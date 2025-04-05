# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'problems', views.ProblemViewSet)

urlpatterns = [
    # Authentication URLs
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Problem URLs
    path('', include(router.urls)),
    path('problem-by-topic/', views.get_problem_by_topic, name='problem-by-topic'),
    
    # Chat URLs
    path('chat/', views.chat_message, name='chat'),
    path('chat/history/', views.chat_history, name='chat-history'),
    
    # Code evaluation URL
    path('evaluate-code/', views.evaluate_code, name='evaluate-code'),
    
    # File upload URL
    path('upload-file/', views.upload_file, name='upload-file'),
    
    # User profile URL
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
]

# codetrek_backend/codetrek_backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)