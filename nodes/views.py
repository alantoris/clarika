from rest_framework import mixins, viewsets
from .models import Node
from .serializers import CreateNodeSerializer, UpdateNodeSerializer

class NodeViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                viewsets.GenericViewSet):
    """
    Viewset for handling the Node operations
    """
    queryset = Node.objects.all()
    serializer_class = CreateNodeSerializer

    def get_serializer_class(self):
        if self.action in ["create"]:
            return self.serializer_class
        elif self.action in ["partial_update", "update"]:
            return UpdateNodeSerializer
