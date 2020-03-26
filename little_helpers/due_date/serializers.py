from datetime import date

from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from .models import ToDo


class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = '__all__'

class DoneDateSerializer(serializers.Serializer):
    last_exec_date = serializers.DateField(required=True)

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        instance.last_exec_date = validated_data.get('last_exec_date', instance.last_exec_date)
        instance.save()
        return instance

    def validate_last_exec_date(self, value):
        """Last exec date must be in the past"""
        if value > date.today():
            raise serializers.ValidationError(_("Invalid date: Date in the future."))
        return value
