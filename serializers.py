# api/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Problem, UserProfile, ChatMessage, CodeSubmission, UploadedFile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        # Check if passwords match
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'email', 'bio', 'preferred_language', 'preferred_topics')

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('id', 'message_type', 'content', 'timestamp')
        read_only_fields = ('id', 'timestamp')

class ChatHistorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ('id', 'username', 'message_type', 'content', 'timestamp')

class CodeSubmissionSerializer(serializers.ModelSerializer):
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    
    class Meta:
        model = CodeSubmission
        fields = ('id', 'problem', 'problem_title', 'code', 'language', 'feedback', 'is_correct', 'submitted_at')
        read_only_fields = ('id', 'feedback', 'is_correct', 'submitted_at')

class UploadedFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = UploadedFile
        fields = ('id', 'file', 'file_name', 'file_type', 'uploaded_at', 'file_url')
        read_only_fields = ('id', 'uploaded_at', 'file_url')
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url') and request:
            return request.build_absolute_uri(obj.file.url)
        return None