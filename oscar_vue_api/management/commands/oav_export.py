from django.core.management.base import BaseCommand, CommandError
from oscar_vue_api import search


class Command(BaseCommand):
    help = "Export products to ElasticSearch"

    def handle(self, *args, **kwargs):
        self.stdout.write("Indexing...")
        self.stdout.write("")
        bulk_products = search.bulk_indexing_products()
        self.stdout.write("Products: {0}".format(bulk_products[0]))
        bulk_categories = search.bulk_indexing_categories()
        self.stdout.write("Categories: {0}".format(bulk_categories[0]))
        bulk_taxrules = search.bulk_indexing_taxrules()
        self.stdout.write("Tax Rules: {0}".format(bulk_taxrules[0]))
        self.stdout.write("")
        self.stdout.write("Just finished indexing!")
