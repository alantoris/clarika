from rest_framework import mixins, viewsets
from .models import Node
from .serializers import NodeSerializer

class NodeViewSet(mixins.CreateModelMixin,
                viewsets.GenericViewSet):
    """
    Viewset for handling the Node operations
    """
    queryset = Node.objects.all()
    serializer_class = NodeSerializer
