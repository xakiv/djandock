"""
POUR dev UNIQUEMENT
"""

from django.contrib import admin

from sid.models import Organisation
from sid.models import OrganisationType
from sid.models import Profile
from sid.models import License

admin.site.register(Profile)
admin.site.register(Organisation)
admin.site.register(OrganisationType)
admin.site.register(License)
