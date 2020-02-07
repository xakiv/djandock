import logging

from django.template.loader import render_to_string
from rest_framework.parsers import BaseParser
from rest_framework.renderers import BaseRenderer
import xmltodict


logger = logging.getLogger(__name__)


class XMLRenderer(BaseRenderer):
    """
    Les retours xml se font pour contextualiser les erreurs de l'api SID
    cf fichiers exemple et schema: error.xml et error.xsd

    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <error xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="error.xsd">
      <classType>ORGANISM</classType>
      <errorCode>004</errorCode>
      <errorLabel>Not Found</errorLabel>
      <errorMessage>Organism u6i not found</errorMessage>
      <methodType>PUT</methodType>
      <resourceId>5</resourceId>
    </error>

    """
    def __init__(self):
        self.media_type = 'application/xml'
        self.format = 'xml'
        self.charset = 'UTF-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        xml_as_string = render_to_string('sid/default_renderer.xml', {'data': data})
        return xml_as_string.replace("\n", "")


class XMLtParser(BaseParser):

    def __init__(self):
        self.media_type = 'application/xml'
        self.charset = 'UTF-8'

    def parse(self, stream, media_type=None, parser_context=None):

        assert xmltodict, 'XMLParser need xmltodict to be installed'

        # parser_context = parser_context or {}
        # encoding = parser_context.get('encoding', self.charset)
        # parser = etree.DefusedXMLParser(encoding=encoding)
        try:
            tree = xmltodict.parse(stream)
        except Exception:
            logger.exception('xmlparser')
        else:
            return tree
