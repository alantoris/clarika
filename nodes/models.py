from django.db import models

class Node(models.Model):
    """
    Class representing a Node of a tree
    """
    value = models.CharField(max_length=30)
    deleted = models.BooleanField(default=False)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'Node: {self.pk} Value: {self.value}'
