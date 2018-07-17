from collections import namedtuple
from logging import getLogger
from xml.etree import ElementTree

from django.apps import apps
from django.db import models


logger = getLogger(__name__)
PseudoDictItem = namedtuple('PseudoDictItem', ('key', 'value',))


def _alphize(s):
    return ''.join(filter(lambda c: c.isalpha(), s)).lower()


def find_model(tag):
    logger.debug(f'Finding model for tag "{tag}"')
    tag_alpha = _alphize(tag)
    for app, app_models in apps.all_models.items():
        for name, model in app_models.items():
            name_alpha = _alphize(name)
            if tag_alpha == name_alpha:
                logger.debug(f'Found model "{app}.{name}"')
                return model


def find_field(tag, model):
    logger.debug(f'Finding field for tag "{tag}" in model "{model.__name__}"')
    tag_alpha = _alphize(tag)
    for field in model._meta.fields:
        name_alpha = _alphize(field.name)
        if tag_alpha == name_alpha:
            logger.debug(f'Found field "{field.name}"')
            return field


class BaseMapper():
    def __init__(self, source):
        self.source = source
        self.pseudo_dict = []
        self.extracted_data = []

    def prepare_source(self, source=None):
        raise NotImplementedError()

    def extract(self):
        if not self.extracted_data:
            for item in self.pseudo_dict:
                self.extract_item(item)
        return self.extracted_data

    def extract_item(self, item, parent=None):
        logger.debug(f'Extracting {item}')
        key, value = item
        if isinstance(value, str) and parent is not None:
            field = find_field(key, type(parent))
            if isinstance(field, models.CharField):
                logger.debug(f'Setting {parent}.{key} to {value}')
                setattr(parent, field.name, value)
        elif isinstance(value, list):
            model = find_model(key)
            if model:
                model_instance = model()
                self.extracted_data.append(model_instance)
            else:
                model_instance = None
            for value_item in value:
                self.extract_item(value_item, parent=model_instance)
            if parent is not None:
                foreign_key = find_field(parent.__class__.__name__, model)
                logger.debug(f'Foreign key of type {foreign_key.__class__}')
                if isinstance(foreign_key, models.ForeignKey):
                    logger.debug(f'Setting {model_instance}.{foreign_key.name} to {parent}')
                    setattr(model_instance, foreign_key.name, parent)

    def save(self):
        for obj in self.extracted_data:
            logger.debug(f'Saving {obj}')
            self.fix_instance(obj)
            obj.save()

    @staticmethod
    def fix_instance(obj):
        for field in obj._meta.fields:
            field_value = getattr(obj, field.name)
            if isinstance(field, models.ForeignKey) and field_value is not None:
                setattr(obj, field.name + '_id', field_value.id)
            if field.unique:
                model = type(obj)
                existing_obj = model.objects.filter(**{field.name: field_value}).first()
                if existing_obj is not None:
                    obj.id = existing_obj.id


class XmlMapper(BaseMapper):
    def prepare_source(self, source=None):
        if source is None:
            source = self.source
        else:
            self.source = source
        parser = ElementTree.XMLParser(encoding="utf-8")
        try:
            tree = ElementTree.parse(source, parser=parser)
            root = tree.getroot()
        except IOError:
            root = ElementTree.fromstring(source, parser=parser)
        self.pseudo_dict.append(self.prepare_element(root))

    def prepare_element(self, element):
        pseudo_dict = []
        for child in element:
            pseudo_dict.append(self.prepare_element(child))
        return PseudoDictItem(element.tag, pseudo_dict or element.text)
