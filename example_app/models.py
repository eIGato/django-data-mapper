from django.db import models


class Channel(models.Model):
    link = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    language = models.CharField(max_length=255, blank=True, null=True)
    copyright = models.CharField(max_length=255, blank=True, null=True)
    managing_editor = models.CharField(max_length=255, blank=True, null=True)
    web_master = models.CharField(max_length=255, blank=True, null=True)
    generator = models.CharField(max_length=255, blank=True, null=True)
    docs = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=255, blank=True, null=True)

    pub_date = models.CharField(max_length=255, blank=True, null=True)
    last_build_date = models.CharField(max_length=255, blank=True, null=True)
    ttl = models.CharField(max_length=255, blank=True, null=True)

    # cloud = models.ForeignKey('Cloud', null=True)
    # text_input = models.ForeignKey('TextInput', null=True)
    # categories = models.ManyToManyField('Category')
    # skip_hours = models.ManyToManyField('Hour')
    # skip_days = models.ManyToManyField('Day')


class Image(models.Model):
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    width = models.PositiveSmallIntegerField(default=88)
    height = models.PositiveSmallIntegerField(default=31)


class Item(models.Model):
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    comments = models.CharField(max_length=255, blank=True, null=True)
    guid = models.CharField(max_length=255, blank=True, null=True)
    pubDate = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    # categories = models.ManyToManyField('Category')
    # enclosures = models.ManyToManyField('Enclosure')
