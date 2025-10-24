from rest_framework import serializers


class EndpointSerializer(serializers.Serializer):
    name = serializers.CharField()
    url = serializers.CharField()
    method = serializers.CharField()
    description = serializers.CharField()


class APISerializer(serializers.Serializer):
    message = serializers.CharField()
    description = serializers.CharField()
    endpoints = serializers.DictField(child=EndpointSerializer(many=True))