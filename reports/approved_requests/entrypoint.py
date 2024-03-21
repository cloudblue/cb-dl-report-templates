# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, CloudBlue
# All rights reserved.
#

from reports import utils
from connect.client import R
import requests
import json
from reports.utils import PRODUCT_FIELDS

ALL_PRODUCTS = [product for x in PRODUCT_FIELDS for product in x["products"]]

def generate(client, parameters, progress_callback, renderer_type='xlsx', extra_context_callback=None):
    requests = request_approved_requests(client, parameters)

    progress = 0
    total = requests.count()
    for request in requests:
        parameters_list = request['asset']['params']

        for item in request['asset']['items']:
            product = utils.get_value(request['asset'], 'product', 'id')
            yield (
                utils.get_basic_value(request, 'id'),  # Request ID
                utils.get_value(request, 'asset', 'id'),  # Connect Subscription ID
                utils.get_value(request, 'asset', 'external_id'),  # End Customer Subscription ID
                utils.get_param_value(parameters_list, 'action_type'), # Action
                utils.get_param_value(parameters_list, get_product_field_name(product, 'order')), # Vendor Order #
                utils.get_param_value(parameters_list, get_product_field_name(product, 'transfer')), # Vendor Transfer #
                utils.get_param_value(parameters_list, get_product_field_name(product, 'vip')), # Vendor Subscription
                utils.get_param_value(parameters_list, get_product_field_name(product, 'customer_id')), # Vendor Customer ID
                utils.get_param_value(parameters_list, get_product_field_name(product, 'discount_group')), # Pricing SKU Level (Volume Discount level)
                utils.get_basic_value(item, 'display_name'),  # Product Description
                utils.get_basic_value(item, 'mpn'),  # Part Number
                utils.get_basic_value(item, 'period'),  # Product Period
                utils.get_basic_value(item, 'quantity'),  # Cumulative Seat
                _get_delta_str(item),  # Order Delta
                utils.get_value(request['asset']['tiers'], 'tier1', 'id'),  # Reseller ID (RESELLER EXTERNAL)
                utils.get_value(request['asset']['tiers'], 'tier1', 'id'), # Reseller External ID
                utils.get_value(request['asset']['tiers'], 'tier1', 'name'),  # Reseller Name
                utils.get_value(request['asset']['tiers'], 'customer', 'name'),  # End Customer Name
                utils.get_value(request['asset']['tiers'], 'customer', 'external_id'),  # End Customer External ID
                utils.get_value(request['asset']['connection'], 'provider', 'id'),  # Provider ID
                utils.get_value(request['asset']['connection'], 'provider', 'name'),  # Provider Name
                utils.get_value(request, 'marketplace', 'name'),  # Marketplace
                utils.get_value(request['asset']['connection'], 'hub', 'id'), # HUB ID
                utils.get_value(request['asset']['connection'], 'hub', 'name'), # HUB Name
                utils.get_value(request['asset'], 'product', 'id'),  # Product ID
                utils.get_value(request['asset'], 'product', 'name'),  # Product Name
                utils.get_value(request, 'asset', 'status'),  # Subscription Status
                utils.convert_to_datetime(utils.get_basic_value(request, 'effective_date')),  # Effective  Date
                utils.convert_to_datetime(utils.get_basic_value(request, 'created')),  # Creation  Date
                '',  # Connect Order Type: purchase, cancel... # TODO: is the same as action_type?
                utils.get_param_value(parameters_list, get_product_field_name(product, 'mail')), # Customer Tenant Value
                '', # Currency (EMPTY)
                utils.get_basic_value(request['asset']['connection'], 'type'),  # Connection Type,
                utils.today_str(),  # Exported At
            )
        progress += 1
        progress_callback(progress, total)


def _get_delta_str(item):
    try:
        return str(int(item.get('quantity')) - int(item.get('old_quantity')))
    except Exception:
        return ''

def request_approved_requests(client, parameters):
    query = R()
    query &= R().status.eq('approved')
    query &= R().created.ge(parameters['date']['after'])
    query &= R().created.le(parameters['date']['before'])

    if parameters.get('connexion_type') and parameters['connexion_type']['all'] is False:
        query &= R().asset.connection.type.oneof(parameters['connexion_type']['choices'])
    if parameters.get('product') and parameters['product']['all'] is False:
        query &= R().asset.product.id.oneof(parameters['product']['choices'])
    if parameters.get('product') and parameters['product']['all'] is True:
        query &= R().asset.product.id.oneof(ALL_PRODUCTS)
    if parameters.get('rr_type') and parameters['rr_type']['all'] is False:
        query &= R().type.oneof(parameters['rr_type']['choices'])
    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().marketplace.id.oneof(parameters['mkp']['choices'])
    return client.requests.filter(query).order_by("created")

def get_product_field_name(product_code, field_name):
    for x in PRODUCT_FIELDS:
        if product_code in x["products"]:
            return x["fields"][field_name]
    return ''
