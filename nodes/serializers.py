from rest_framework import serializers
from .models import Node
from .utils import check_deep_children_structure

TREE_LEVEL_ERROR = "The tree has already 10 levels, can't add more nodes under this node"
PARENT_DELETED = "The node can't be updated, his parent {pk} is also deleted"

class CreateNodeSerializer(serializers.ModelSerializer):
    """
    Node class serializers for creations.
    """
    parent = serializers.PrimaryKeyRelatedField(queryset=Node.objects.all())
    children = serializers.JSONField(required=False)

    class Meta:
        model = Node
        fields = ('id', 'value', 'children', 'parent')

    def validate(self, data):
        parent_level = data['parent'].check_tree_level()
        if parent_level >= 10:
            raise serializers.ValidationError(TREE_LEVEL_ERROR)
        if "children" in data:
            max_posible_deep = check_deep_children_structure(data)
            if parent_level + max_posible_deep >= 10:
                raise serializers.ValidationError(TREE_LEVEL_ERROR)
            data.pop("children")
        return data

class UpdateNodeSerializer(serializers.ModelSerializer):
    """
    Node class serializers for updates.
    """
    value = serializers.CharField(max_length=Node.NODE_VALUE_MAX_LENGTH, required=False)

    class Meta:
        model = Node
        fields = ('id', 'value', 'parent')
    
    def validate(self, attrs):
        if "instance_id" in self.context:
            node = Node.objects.get(pk=self.context.get('instance_id'))
            if node.parent is not None and node.parent.deleted:
                raise serializers.ValidationError(PARENT_DELETED.format(pk=node.parent.pk))
        return attrs
