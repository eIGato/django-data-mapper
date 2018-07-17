from data_mapper import XmlMapper
from example_app.models import Channel
from example_app.models import Item


def test_import_rss_str_expect_1_item_created(db, rss_str):
    xml_mapper = XmlMapper(rss_str)
    xml_mapper.import_data()
    assert Item.objects.count() == 1, f'RSS items imported wrong!'


def test_import_postponed_rss_file_expect_2_items_created(db, rss_file):
    xml_mapper = XmlMapper()
    xml_mapper.import_data(rss_file)
    assert Item.objects.count() == 2, f'RSS items imported wrong!'


def test_import_rss_twice_expect_no_duplicate_channels(db, rss_str):
    xml_mapper = XmlMapper(rss_str)
    xml_mapper.import_data()
    xml_mapper = XmlMapper(rss_str)
    xml_mapper.import_data()
    assert Channel.objects.count() < 2, f'RSS channel duplicates found!'
