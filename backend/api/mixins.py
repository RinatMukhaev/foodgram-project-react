from rest_framework import mixins, viewsets


class GetCreateDeleteViewSet(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    pass
