# Django data mapper

Package to get data from given source and put it into existing Django models.
Example app contains RSS related models. If you feed RSS XML file to this
program then it would put found elements into corresponding models.
Program automatically discovers all models in target project and chooses
most appropriate of them.

## Dev and test

Optionally create and activate virtual environment:
```bash
virtualenv -p python3 .venv
source .venv/bin/activate
```

Install dependencies and test tools:
```bash
pip install -r requirements.txt
```

Create local settings for example project:
```bash
cp example_project/settings/local.py.example example_project/settings/local.py
vim example_project/settings/local.py
```

Now you may run tests and see test coverage:
```bash
pytest
```

## Installation

Install this package into your `site-packages`:
```bash
pip install -e .
```

After installation you may remove (or move) `data_mapper` directory.
Example project will work and have access to management commands:
```bash
rm -rf data_mapper
./manage.py import_xml --help
```

To use data mappers in your Django project you should just add `'data_mapper'`
into settings, `INSTALLED_APPS` section.

## Usage

From command line:
```bash
./manage.py import_xml path/to/rss-feed.xml
```

From python code:
```python
from data_mapper import XmlMapper

xml_mapper = XmlMapper(open('path/to/rss-feed.xml'))
xml_mapper.import_data()
```
