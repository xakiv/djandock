from django.urls import path
from rest_framework import routers

from sid.views.user import AgentViews
from sid.views.user import EmployeeViews


# TODO a supprimer en fin de dev du middleware
from sid.views.user import TestAuthentViews

from sid.views.organisation import CompanyViews
from sid.views.organisation import OrganismViews


app_name = 'sid'

router = routers.DefaultRouter()

router.register('agent', AgentViews, basename='agent')
router.register('employee', EmployeeViews, basename='employee')
router.register('organism', OrganismViews, basename='organism')
router.register('company', CompanyViews, basename='company')

urlpatterns = [
    # Si besoin d'urls supplémentaires
    path('mon-compte/', TestAuthentViews.as_view())
]

urlpatterns += router.urls
