
from django.urls import path

from map_quest.views import index
from map_quest.views import dataset_detail
from map_quest.views import dataset_create
from map_quest.views import dataset_delete
from map_quest.views import dataset_update
from map_quest.views import subset_list

app_name = 'map_quest'

urlpatterns = [
    # Si besoin d'urls supplémentaires
    path('accueil/', index, name='index'),
    path('dataset/<int:dataset_id>/', dataset_detail, name='dataset_detail'),
    path('dataset/<int:dataset_id>/delete/', dataset_delete, name='dataset_delete'),
    path('dataset/<int:dataset_id>/update/', dataset_update, name='dataset_update'),
    path('dataset/<int:dataset_id>/subset/', subset_list, name='subset_list'),
    path('dataset/', dataset_create, name='dataset_create'),

]
