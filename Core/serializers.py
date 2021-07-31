from rest_framework import serializers
from .models import Book


class LanguageSerializer(serializers.StringRelatedField):
    def to_internal_value(self, data):
        return data


class BookSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(many=False)

    class Meta:
        model = Book
        fields = '__all__'
