from rest_framework import serializers

class GoogleCallbackSerializer(serializers.Serializer):
    code = serializers.CharField(help_text="Authorization code from Google", required=True)

class GoogleCallbackResponseSerializer(serializers.Serializer):
    token = serializers.CharField(help_text="Authentication token")
    user = serializers.DictField(child=serializers.CharField(), help_text="User details")
