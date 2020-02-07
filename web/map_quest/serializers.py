import logging

from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from map_quest.models import Cluster

logger = logging.getLogger(__name__)


class GeoJSONSerializer(GeoFeatureModelSerializer):

    feature_type = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Cluster
        geo_field = 'geom'
        fields = (
            'feature_id',
            'title',
            'description',
            'status',
            'created_on',
            'updated_on',
            'archived_on',
            'deletion_on',
            'feature_type',
        )
