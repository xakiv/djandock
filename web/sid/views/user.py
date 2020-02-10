import logging

from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

import xmltodict

# Import de test uniquement:
from sid.fake_ckan_module import CkanBaseError
from sid.fake_ckan_module import CkanHandler

# TODO switcher sur modules idgo_admin.models
from sid.models import Organisation, Profile
from sid.xml_io import XMLtParser
from sid.xml_io import XMLRenderer
from sid.exceptions import SidGenericError


logger = logging.getLogger(__name__)


class AbstractUsrViews(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    parser_classes = [
        # Si le contenu est envoyé en raw
        XMLtParser,
        # Si le fichier est envoyé dans le form-data dans la clé 'file'
        MultiPartParser,
    ]
    renderer_classes = [XMLRenderer, ]
    permission_classes = [
        # permissions.IsAuthenticated, # TODO limiter aux connectés
        permissions.AllowAny
    ]
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    http_method_names = ['post', 'put']  # ['post', 'put', 'delete']

    def get_object(self):
        try:
            instance = super().get_object()
        except Exception:
            raise SidGenericError(
                client_error_code='003',
                extra_context={
                    'classType': self.class_type,
                    'methodType': self.request.method,
                    'resourceId': self.kwargs.get('username', 'N/A'),
                },
                status_code=status.HTTP_404_NOT_FOUND
            )
        return instance

    @transaction.atomic
    def parse_and_create(self, data):
        root = data.get(self.profile_element, {})
        sid_id = root.get('id', None)
        if User.objects.filter(username=sid_id).exists():
            raise SidGenericError(
                client_error_code='005',
                extra_context={
                    'classType': self.class_type,
                    'methodType': self.request.method,
                    'resourceId': sid_id,
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data_orga = root[self.orga_dept_element]
        orga = None
        if data_orga.get(self.orga_element):
            orga_sid = data_orga[self.orga_element]['id']
            try:
                orga = Organisation.objects.get(slug=orga_sid)
            except Organisation.DoesNotExist:
                # TODO tester les mécanismes de rejeu de la synchronisation
                raise SidGenericError(
                    client_error_code='004',
                    extra_context={
                        'classType': self.class_orga_type,
                        'methodType': 'POST',  # Méthode en cours ou POST de création d'organisation
                        # 'methodType': self.request.method,  # Méthode en cours ou POST de création d'organisation
                        'resourceId': orga_sid,  # Identifiant de la relation manquante ou de la ressource
                    },
                    status_code=status.HTTP_404_NOT_FOUND
                )

        try:
            data_user = root['user']
            user = User.objects.create(
                username=root['id'],
                email=root['email'],
                first_name=data_user['firstname'][:30],
                last_name=data_user['lastname'][:30],
                is_superuser=root['roles']['role']['name'] == "administrateur",
                is_staff=root['roles']['role']['name'] == "administrateur",
                is_active=data_user['enabled'] == 'true',
            )

            profile = Profile.objects.create(
                user=user,
                organisation=orga,
                is_active=data_user['enabled'] == 'true',
                membership=orga is not None,
            )

        except Exception:
            logger.exception(self.__class__.__name__)
            raise SidGenericError(
                client_error_code='002',
                extra_context={
                    'classType': self.class_type,
                    'methodType': self.request.method,
                    'resourceId': sid_id,
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        try:
            CkanHandler.add_user(user, 'fake', state='active')
        except CkanBaseError:
            logger.exception(CkanBaseError.message)
            raise SidGenericError(
                client_error_code='006',
                extra_context={
                    'classType': self.class_type,
                    'methodType': self.request.method,
                    'resourceId': sid_id,
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return user

    @transaction.atomic
    def parse_and_update(self, user, data):

        root = data.get(self.profile_element, {})
        sid_id = root.get('id', None)
        if sid_id != str(user.username):
            raise SidGenericError(
                client_error_code='002',
                extra_context={
                    'classType': self.class_type,
                    'methodType': self.request.method,
                    'resourceId': user.username,
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if not User.objects.filter(username=sid_id).exists():
            raise SidGenericError(
                client_error_code='003',
                extra_context={
                    'classType': self.class_type,
                    'methodType': self.request.method,
                    'resourceId': user.username,
                },
                status_code=status.HTTP_404_NOT_FOUND
            )

        data_orga = root[self.orga_dept_element]
        orga = None
        if data_orga.get(self.orga_element):
            orga_sid = data_orga[self.orga_element]['id']
            try:
                orga = Organisation.objects.get(slug=orga_sid)
            except Organisation.DoesNotExist:
                # TODO tester les mécanismes de rejeu de la synchronisation
                raise SidGenericError(
                    client_error_code='004',
                    extra_context={
                        'classType': self.class_orga_type,
                        'methodType': 'POST',  # method en cours ou POST de création d'orga
                        # 'methodType': self.request.method,  # method en cours ou POST de création d'orga
                        'resourceId': orga_sid,  # identifiant de la relation manquante ou de la ressource en cours
                    },
                    status_code=status.HTTP_404_NOT_FOUND
                )

        try:
            user.profile.contributions.clear()
            data_user = root['user']
            user.first_name = data_user['firstname'][:30]
            user.last_name = data_user['lastname'][:30]
            # user.username = data_user['username']  # Modifiable
            user.email = root['email']
            user.is_superuser = root['roles']['role']['name'] == "administrateur"
            user.is_staff = root['roles']['role']['name'] == "administrateur"
            user.is_active = data_user['enabled'] == "true"
            user.save()

            user.profile.organisation = orga
            user.profile.is_active = data_user['enabled'] == "true"
            user.profile.membership = orga is not None

        except Exception:
            logger.exception(self.__class__.__name__)
            raise SidGenericError(
                client_error_code='002',
                extra_context={
                    'classType': self.class_type,
                    'methodType': self.request.method,
                    'resourceId': user.username,
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # try:
        #     CkanHandler.update_user(user)
        # except CkanBaseError:
        #     logger.exception(CkanBaseError.message)
        #     raise SidGenericError(
        #         client_error_code='006',
        #         extra_context={
        #             'classType': self.class_type,
        #             'methodType': self.request.method,
        #             'resourceId': user.username,
        #         },
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )

        return user

    def get_data(self, request):
        data = None
        if request.FILES.get('file'):
            _file = request.FILES.get('file')
            data = xmltodict.parse(_file)
        else:
            data = request.data
        return data

    def create(self, request, *args, **kwargs):
        data = self.get_data(request)
        if not data:
            raise SidGenericError(
                client_error_code='001',
                extra_context={
                    'classType': self.class_type,
                    'methodType': self.request.method,
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        instance = self.parse_and_create(data)
        logger.info('User::create() OK: id->{}, username->{}'.format(
            instance.id,
            instance.username,
        ))
        response = HttpResponse(status=201)
        response['Content-Location'] = ''  # Pas de content-Location
        return response

    def update(self, request, *args, **kwargs):

        data = self.get_data(request)
        sid_id = self.kwargs.get(self.lookup_url_kwarg, '')
        if not data:
            raise SidGenericError(
                client_error_code='001',
                extra_context={
                    'classType': self.class_type,
                    'methodType': self.request.method,
                    'resourceId': sid_id,
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )
        else:
            # On permet la creation à partir du PUT
            try:
                # On appel get_object() pour le 404 custom
                instance = self.get_object()
            except SidGenericError:
                instance = self.parse_and_create(data)
                logger.info('create() from PUT OK: id->{}, username->{}'.format(
                    instance.id,
                    instance.username,
                ))
            else:
                instance = self.parse_and_update(instance, data)
                logger.info('update() OK: id->{}, username->{}'.format(
                    instance.id,
                    instance.username,
                ))

            return HttpResponse(status=200)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
            instance.profile.contributions.clear()
            instance.profile.delete()
        except Exception:
            logger.exception(self.__class__.__name__)
            raise SidGenericError(
                client_error_code='006',
                extra_context={
                    'classType': self.class_type,
                    'methodType': self.request.method,
                    'resourceId': instance.username,
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return HttpResponse(status=200)


class AgentViews(AbstractUsrViews):

    class_type = 'AGENT_PROFILE'
    profile_element = 'agentProfile'
    class_orga_type = 'ORGANISM'
    orga_dept_element = 'organismDepartment'
    orga_element = 'organism'


class EmployeeViews(AbstractUsrViews):

    class_type = 'EMPLOYEE_PROFILE'
    profile_element = 'employeeProfile'
    class_orga_type = 'COMPANY'
    orga_dept_element = 'companyDepartment'
    orga_element = 'company'


class TestAuthentViews(APIView):
    queryset = Profile.objects.all()
    parser_classes = [
        # Si le contenu est envoyé en raw
        XMLtParser,
        # Si le fichier est envoyé dans le form-data dans la clé 'file'
        MultiPartParser,
    ]
    # renderer_classes = [XMLRenderer, ]
    permission_classes = [
        # permissions.IsAuthenticated,
        permissions.IsAdminUser,
        # permissions.AllowAny
    ]

    http_method_names = ['get', ]

    def get(self, request, *args, **kargs):
        prf = Profile.objects.get(user=request.user)
        data = {
            'username': prf.user.username,
            'first_name': prf.user.first_name,
            'last_name': prf.user.last_name,
            'is_staff': prf.user.is_staff,
            'organisation': prf.organisation.legal_name if prf.organisation else ''
        }
        return Response(data=data, status=status.HTTP_200_OK)
