import json

from django.db.models import F
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import FeatureGeoJSONSerializer
from api.serializers import FeatureSerializer
from api.serializers import ProjectSerializer
from geocontrib.models import Authorization
from geocontrib.models import Feature
from geocontrib.models import Project

User = get_user_model()


class ExportFeatureList(APIView):

    http_method_names = ['get', ]

    def get(self, request, slug, feature_type_slug):
        """
            Vue de téléchargement des signalements lié à un projet.
        """
        features = Feature.objects.filter(
            status="published", project__slug=slug, feature_type__slug=feature_type_slug)
        serializer = FeatureGeoJSONSerializer(features, many=True, context={'request': request})
        response = HttpResponse(json.dumps(serializer.data), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=export_projet.json'
        return response


class AvailablesFeatureLinkList(APIView):

    http_method_names = ['get', ]

    def get(self, request, slug, feature_type_slug):
        """
            Vue retournant un abstract des signalements d'un type donnée,
            permettant de rechercher les signalements liés
        """
        features = Feature.objects.filter(
            status="published", project__slug=slug, feature_type__slug=feature_type_slug)
        serializer = FeatureSerializer(features, many=True, context={'request': request})
        return Response(serializer.data)


class ProjectView(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    http_method_names = ['get', 'delete']

    lookup_field = 'slug'


class ProjectAuthorization(APIView):
    queryset = Project.objects.all()
    lookup_field = 'slug'
    http_method_names = ['get', ]

    def get(request, slug):

        members = Authorization.objects.filter(project__slug=slug).annotate(
            user_pk=F('user__pk'),
            email=F('user__email'),
            username=F('user__username'),
            first_name=F('user__first_name'),
            last_name=F('user__last_name'),
        ).values(
            'user_pk', 'email', 'username', 'first_name', 'last_name',
        )

        others = User.objects.filter(
            is_active=True
        ).exclude(
            pk__in=[mem.get('user_pk') for mem in members]
        ).values(
            'pk', 'email', 'username', 'first_name', 'last_name'
        )
        data = {
            'members': list(members),
            'others': list(others),
        }
        return Response(data=data, status=200)
