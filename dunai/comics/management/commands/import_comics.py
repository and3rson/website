#!/usr/bin/env python2
from django.core.files import File

from django.core.management import BaseCommand
from dunai.comics.models import Comic

import unicodecsv
from collections import namedtuple
from xml.etree import ElementTree as ET


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('data/comics.csv', 'rbU') as f:
            r = unicodecsv.reader(f, encoding='utf-8', delimiter='\t')
            line = r.next()

            row_type = namedtuple('row_type', line)

            items = []

            while line:
                try:
                    line = r.next()
                except StopIteration:
                    break
                row = row_type(*line)
                print row.id, row.title, row.content_html
                src = u'<?xml version="1.0" encoding="utf-8"?>\n' + row.content.replace('\\n', '\n')
                try:
                    tree = ET.fromstring(src.encode('utf-8'))
                except:
                    print src
                    raise

                try:
                    desc = tree.find('desc').text
                except AttributeError:
                    desc = tree.find('descr').text
                items.append(dict(title=row.title, comment=desc, src=tree.find('img').text, added_on=row.created_on, slug=row.slug))

        for item in items:
            comic = Comic.objects.create(
                title=item['title'],
                slug=item['slug'],
                image=File(open('data/' + item['src'], 'rb')),
                comment=item['comment'],
                added_on=item['added_on']
            )
