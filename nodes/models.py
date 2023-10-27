from django.db import models


class Node(models.Model):
    """
    Class representing a Node of a tree
    """
    NODE_VALUE_MAX_LENGTH = 30
    value = models.CharField(max_length=NODE_VALUE_MAX_LENGTH)
    deleted = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Node: {self.pk} Value: {self.value}'
    
    def check_tree_level(self):
        """Check level of the tree base on this Node"""
        if self.parent is None:
            return 0
        else:
            return 1 + self.parent.check_tree_level()
    
    def delete_children(self):
        """Loop over children for on cascade deleting"""
        children = Node.objects.filter(parent=self)
        for child in children:
            child.delete()
    
    def delete(self):
        """Mark the record and his children as deleted instead of deleting it""" 
        self.deleted = True
        self.delete_children()
        self.save()
