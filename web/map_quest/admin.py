from django.contrib import admin

from map_quest.models import Dataset
from map_quest.models import Edge
from map_quest.models import Node
from map_quest.models import Polygon

admin.site.register(Dataset)
admin.site.register(Edge)
admin.site.register(Node)
admin.site.register(Polygon)
