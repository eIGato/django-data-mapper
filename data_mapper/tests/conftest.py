from os import path

import pytest


@pytest.fixture
def rss_file():
    current_dir = path.dirname(path.abspath(__file__))
    return open(path.join(current_dir, 'rss-feed-example.xml'))


@pytest.fixture
def rss_str():
    return '''<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
            <channel>
                <title>Channel title</title>
                <description>Channel description</description>
                <link>http://example.com/</link>
                <item>
                    <title><![CDATA[Item title]]></title>
                    <link>http://example.com/item/</link>
                </item>
            </channel>
        </rss>
    '''
