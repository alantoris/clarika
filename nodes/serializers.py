from rest_framework import serializers
from .models import Node

class NodeSerializer(serializers.ModelSerializer):
    """
    Serializers of Node class
    """
    parent = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all())

    class Meta:
        model = Node
        fields = ('value', 'parent')
