"""Likes view."""

# Django REST Framework
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from apps.publications.models import Publication, Like

# Permissions
from rest_framework.permissions import IsAuthenticated
from apps.publications.permissions import IsComment_LikeOwner

# Serializers
from apps.publications.serializers import LikeModelSerializer

# Utils
from apps.utils.mixins import PublicationDispatchMixin
from apps.utils.views import DynamicFieldView


class LikeViewSet(PublicationDispatchMixin,
                  DynamicFieldView,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Generic view set."""

    serializer_class = LikeModelSerializer

    # Return dynamic fields
    fields_to_return = {
        'list': ('user',)
    }

    def get_queryset(self):
        """Return queryset."""
        return Like.objects.filter(publication=self.publication)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.action == 'destroy':
            permission_classes.append(IsComment_LikeOwner)
        return [p() for p in permission_classes]

    def get_serializer_context(self):
        """Return serializer context."""
        context = super(LikeViewSet, self).get_serializer_context()
        if self.action == 'create':
            context['publication'] = self.publication
        return context

    @action(detail=False, methods=['delete'])
    def dislike(self, request, id):
        """Handle dislike."""
        try:
            instance = Like.objects.get(publication=self.publication, user=request.user)
        except Like.DoesNotExist:
            return Response(
                {'alert': "Yout din't even liked this"},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
