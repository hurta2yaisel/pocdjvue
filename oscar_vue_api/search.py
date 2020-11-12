from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import utils, DocType, Text, Date, Integer, Float, Boolean, Object, Nested, Keyword, Long, \
    InnerDoc
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from oscar.core.loading import get_model, get_class

conf = {
    'default': {
        'hosts': [
            {
                'host': 'localhost',
                'port': 9200
            }
        ]
    }
}

connections.configure(**conf)

connections.create_connection(hosts=['elastic:changeme@db.local'], timeout=20)


# connections.create_connection(hosts=[{'host': 'localhost', 'port': 9200}], timeout=20)


class TaxRulesIndex(DocType):
    id = Integer()
    code = Text()
    priority = Integer()
    position = Integer()
    customer_tax_class_ids = Long()
    product_tax_class_ids = Long()
    tax_rate_ids = Long()
    calculate_subtotal = Boolean()
    rates = Object(
        properties={
            'id': Integer(),
            'tax_country_id': Text(),
            'tax_region_id': Integer(),
            'tax_postcode': Text(),
            'rate': Integer(),
            'code': Text(),
        }
    )

    class Index:
        name = 'vue_storefront_catalog'
        doc_type = 'taxrule'

    class Meta:
        doc_type = "taxrule"


def bulk_indexing_taxrules():
    TaxRulesIndex().init()
    es = connections.get_connection()
    all_taxrules = [1]
    return bulk(client=es, actions=(obj_indexing_taxrule() for b in all_taxrules))


def sanitize_dict(dict_):
    print(dict_)
    result = {}
    for k, v in dict_.items():
        for m in utils.META_FIELDS:
            if k.startswith('_') and k.endswith(m):
                result[k] = v
                break
            elif not k.startswith('_'):
                result[k] = v
                break

    return result


def obj_indexing_taxrule():
    obj = TaxRulesIndex(
        meta={
            'id': 2,
        },
        id=2,
        code="Norway",
        priority=0,
        position=0,
        customer_tax_class_ids=[3],
        product_tax_class_ids=[2],
        tax_rate_ids=[4],
        calculate_subtotal=False,
        rates=[{
            'id': 2,
            'tax_country_id': 'NO',
            'tax_region_id': 0,
            'tax_postcode': '*',
            'rate': 25,
            'code': 'VAT25%',
        }]

    )
    obj.save()
    return obj.to_dict(include_meta=True, skip_empty=False)


class CategoriesIndex(DocType):
    id = Integer()
    parent_id = Integer()
    name = Text()
    is_active = Boolean()
    position = Integer()
    level = Integer()
    product_count = Integer()
    include_in_menu = Integer()
    children_data = Nested(include_in_parent=True)
    tsk = Long()
    sgn = Text()

    class Index:
        name = 'vue_storefront_catalog'
        doc_type = 'category'

    class Meta:
        doc_type = "category"


class InnerCategoriesIndex(InnerDoc):
    id = Integer()
    parent_id = Integer()
    name = Text()
    is_active = Boolean()
    position = Integer()
    level = Integer()
    product_count = Integer()
    include_in_menu = Integer()
    children_data = Nested(include_in_parent=True)
    tsk = Long()
    sgn = Text()

    class Index:
        name = 'vue_storefront_catalog'
        doc_type = 'category'

    class Meta:
        doc_type = "category"


def bulk_indexing_categories():
    CategoriesIndex().init()
    es = connections.get_connection()
    Category = get_model('catalogue', 'category')
    return bulk(client=es, actions=(obj_indexing_category(b) for b in Category.get_root_nodes().iterator()))


def category_subs(category, parent):
    depth = category.get_depth()
    sub_categories = []
    obj = InnerCategoriesIndex(
        id=category.id,
        parent_id=parent.id,
        name=category.name,
        is_active=True,
        position=2,
        level=depth + 1,
        product_count=1,
        children_data={},
        tsk=0,
        include_in_menu=0,
        sgn="",
    )
    return obj.to_dict(skip_empty=False)


def obj_indexing_category(category):
    rootpage = category.get_root()
    depth = category.get_depth()
    children_data = []
    if category.get_children():
        for child in category.get_children():
            obj_child = category_subs(child, category)
            children_data.append(obj_child)

    depth = category.get_depth()
    obj = CategoriesIndex(
        meta={
            'id': category.id,
        },
        id=category.id,
        parent_id=0,
        name=category.name,
        is_active=True,
        position=2,
        level=depth + 1,
        product_count=1,
        children_data=children_data,
        tsk=0,
        include_in_menu=0,
        sgn="",
    )
    obj.save(skip_empty=False)

    # return sanitize_dict(obj.to_dict(include_meta=True, skip_empty=False))
    data = obj.to_dict(include_meta=True, skip_empty=False)
    return data


class ProductsIndex(DocType):
    id = Integer()
    sku = Keyword()
    name = Text()
    attribute_set_id = Integer()
    price = Integer()
    status = Integer()
    visibility = Integer()
    type_id = Text()
    created_at = Date()
    updated_at = Date()
    extension_attributes = Long()
    product_links = Long()
    tier_prices = Long()
    custom_attributes = Long()
    category = Object(
        properties={
            'category_id': Long(),
            'name': Text(),
        }
    )
    description = Text()
    image = Text()
    small_image = Text()
    thumbnail = Text()
    options_container = Text()
    required_options = Integer()
    has_options = Integer()
    url_key = Text()
    tax_class_id = Integer()
    children_data = Nested()

    configurable_options = Object()
    configurable_children = Object()

    category_ids = Long()
    stock = Object(properties={'is_in_stock': Boolean()})

    special_price = Float()
    new = Integer()
    sale = Integer()

    special_from_date = Date()
    special_to_date = Date()
    priceInclTax = Float()
    originalPriceInclTax = Float()
    originalPrice = Float()
    specialPriceInclTax = Float()
    sgn = Text()

    class Index:
        name = 'vue_storefront_catalog'
        doc_type = 'product'

    class Meta:
        doc_type = "product"


def bulk_indexing_products():
    ProductsIndex().init()
    es = connections.get_connection()
    Product = get_model('catalogue', 'product')
    return bulk(client=es, actions=(obj_indexing_product(b) for b in Product.objects.all().iterator()), stats_only=True)


def obj_indexing_product(product):
    Selector = get_class('partner.strategy', 'Selector')
    if product.images.first():
        image = "http://127.0.0.1:8000" + product.images.first().original.url
    else:
        image = "https://dummyimage.com/600x400/000/fff"

    all_categories = []
    category_ids = []
    for category in product.categories.all():
        category_mapping = [{
            'category_id': category.id,
            'name': category.name
        }]
        # category_ids += str(category.id)
        all_categories += category_mapping
        category_ids.append(category.id)
    strategy = Selector().strategy()
    price = strategy.fetch_for_product(product).price
    obj = ProductsIndex(
        meta={
            'id': product.id,
        },
        id=product.id,
        sku=product.upc,
        name=product.title,
        attribute_set_id=None,
        price=price.incl_tax,
        priceInclTax=price.incl_tax,
        status=1,
        visibility=4,
        type_id="simple",
        created_at=product.date_created,
        updated_at=product.date_updated,
        extension_attributes=[],
        product_links=[],
        tier_prices=[],
        custom_attributes=None,
        category=all_categories,
        description=product.description,
        image=image,
        small_image="",
        thumbnail="",
        options_container="container2",
        required_options=0,
        has_options=0,
        url_key=product.slug,
        tax_class_id=2,
        children_data={},
        configurable_options=[],
        configurable_children=[],
        category_ids=category_ids,

        stock={
            'is_in_stock': True,
        },
        sgn="",
    )
    result = obj.save(skip_empty=True)
    return obj.to_dict(include_meta=True, skip_empty=False)


if __name__ == '__main__':
    import django

    django.setup()
    bulk_indexing_products()
