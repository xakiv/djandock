import logging
from pprint import pformat

from django.contrib.auth import get_user_model
from django.test import tag
from django.urls import reverse
from rest_framework.test import APITransactionTestCase

from sid.models import Organisation


User = get_user_model()
logger = logging.getLogger(__name__)


class BaseTestCase(APITransactionTestCase):
    create_xml_path = ''
    pust_xml_path = ''
    update_xml_path = ''

    create_url_path = ''
    update_url_path = ''

    queryset = None

    defaults = {}
    defaults_pust = {}

    def test_create(self):
        with open(self.create_xml_path) as fp:
            resp = self.client.post(
                reverse(self.create_url_path),
                data=fp.read(),
                content_type='application/xml',
            )
            self.assertEqual(resp.status_code, 201)

            self.assertEqual(self.queryset.filter(**self.defaults).count(), 1)

    def test_create_update(self):

        with open(self.create_xml_path) as fp:
            d = {'file': fp}

            r = self.client.post(
                reverse(self.create_url_path),
                data=d,
            )

            self.assertEqual(r.status_code, 201)
            self.assertEqual(self.queryset.all().count(), 1)
        logger.debug(__name__)
        logger.info(
            pformat(self.queryset.get(**self.defaults).__dict__)
        )

        with open(self.update_xml_path) as fp2:
            d = {'file': fp2}

            r = self.client.put(
                reverse(self.update_url_path, kwargs=self.defaults),
                data=fp2.read(),
                content_type='application/xml',
            )

            logger.info(
                pformat(self.queryset.get(**self.defaults).__dict__)
            )
            self.assertEqual(r.status_code, 200)
            self.assertEqual(self.queryset.all().count(), 1)

    def test_pust(self):
        """
        On test la création d'orga & company & employee & agent à travers un PUT
        """

        with open(self.pust_xml_path) as fp2:
            r = self.client.put(
                reverse(
                    self.update_url_path,
                    kwargs=self.defaults_pust
                ),
                data=fp2.read(),
                content_type='application/xml',
            )
            logger.info(
                pformat(self.queryset.get(**self.defaults_pust).__dict__)
            )
            self.assertEqual(r.status_code, 200)
            self.assertEqual(self.queryset.all().count(), 1)


class UserBaseTestCase(BaseTestCase):

    fixtures = [
        'data/initial/license.json',
        'data/initial/organisation_type.json',
        'data/initial/organisation.json',
    ]

    create_user_with_missing_orga_xml_path = ''
    create_missing_orga_xml_path = ''
    create_orga_url_path = ''

    def test_create_missing_orga(self):

        with open(self.create_user_with_missing_orga_xml_path) as fp:
            d = {'file': fp}

            r = self.client.post(
                reverse(self.create_url_path),
                data=d,
            )

            self.assertEqual(r.status_code, 404)
            self.assertEqual(self.queryset.all().count(), 0)

        with open(self.create_missing_orga_xml_path) as fp:
            d = {'file': fp}

            r = self.client.post(
                reverse(self.create_orga_url_path),
                data=d,
            )

            self.assertEqual(r.status_code, 201)

        with open(self.create_user_with_missing_orga_xml_path) as fp:
            d = {'file': fp}

            r = self.client.post(
                reverse(self.create_url_path),
                data=d,
            )

            self.assertEqual(r.status_code, 201)
            self.assertEqual(self.queryset.all().count(), 1)


# @tag('selected')
class TestOrganism(BaseTestCase):

    create_xml_path = 'data/test/organism.xml'
    pust_xml_path = 'data/test/organism_pust.xml'
    update_xml_path = 'data/test/organism_update1.xml'

    create_url_path = 'sid:organism-list'
    update_url_path = 'sid:organism-detail'

    queryset = Organisation.objects.all()

    unique_field_name = 'slug'
    unique_field_value = None
    defaults = {'slug': '294680'}
    defaults_pust = {'slug': '123456789'}


# @tag('selected')
class TestCompany(BaseTestCase):

    create_xml_path = 'data/test/company.xml'
    pust_xml_path = 'data/test/company_pust.xml'
    update_xml_path = 'data/test/company_update1.xml'

    create_url_path = 'sid:company-list'
    update_url_path = 'sid:company-detail'

    queryset = Organisation.objects.all()

    unique_field_name = 'slug'
    unique_field_value = None
    defaults = {'slug': '294679'}
    defaults_pust = {'slug': '123456789'}


# @tag('selected')
class TestAgent(UserBaseTestCase):

    create_xml_path = 'data/test/agent.xml'
    update_xml_path = 'data/test/agent_update1.xml'
    pust_xml_path = 'data/test/agent_pust.xml'
    create_url_path = 'sid:agent-list'
    update_url_path = 'sid:agent-detail'
    queryset = User.objects.all()
    defaults = {'username': '307164'}
    defaults_pust = {'username': '123456789'}

    create_user_with_missing_orga_xml_path = 'data/test/agent_with_missing_orga.xml'
    create_missing_orga_xml_path = 'data/test/organism_create_missing.xml'
    create_orga_url_path = 'sid:organism-list'


@tag('selected')
class TestEmployee(UserBaseTestCase):
    create_xml_path = 'data/test/employee.xml'
    pust_xml_path = 'data/test/employee_pust.xml'
    update_xml_path = 'data/test/employee_update1.xml'
    create_url_path = 'sid:employee-list'
    update_url_path = 'sid:employee-detail'

    queryset = User.objects.all()
    defaults = {'username': '307163'}
    defaults_pust = {'username': '123456789'}

    create_user_with_missing_orga_xml_path = 'data/test/employee_with_missing_orga.xml'
    create_missing_orga_xml_path = 'data/test/company_create_missing.xml'
    create_orga_url_path = 'sid:company-list'
