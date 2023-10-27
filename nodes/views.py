from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Node
from .serializers import CreateNodeSerializer, UpdateNodeSerializer

class NodeViewSet(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                viewsets.GenericViewSet):
    """
    Viewset for handling the Node operations
    """
    queryset = Node.objects.filter(deleted=False)
    serializer_class = CreateNodeSerializer

    def get_serializer_class(self):
        if self.action in ["create"]:
            return self.serializer_class
        elif self.action in ["partial_update", "update", "restore"]:
            return UpdateNodeSerializer
    
    def get_queryset(self):
        if self.action in ["restore"]:
            return Node.objects.all()
        else:
            return super().get_queryset()

    @action(detail=True, methods=['post'])
    def restore(self, request, pk):
        """Restore deleted node."""
        serializer = self.get_serializer_class()(
            data=request.data,
            context={"instance_id": pk}
        )
        if serializer.is_valid(raise_exception=True):
            node = Node.objects.get(pk=pk)
            node.deleted = False
            node.save()
        data = self.get_serializer_class()(node).data
        return Response(data, status=status.HTTP_200_OK)
