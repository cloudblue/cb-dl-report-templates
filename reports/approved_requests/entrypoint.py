# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, CloudBlue
# All rights reserved.
#

from reports import utils
from connect.client import R
import requests
import json

HEADERS = [
    'Request ID', 'Connect Subscription ID', 'End Customer Subscription ID', 'Action', 'Vendor Order #',
    'Vendor Transfer #', 'Vendor Subscription #', 'Vendor Customer ID', 'Pricing SKU Level (Volume Discount level)',
    'Product Description', 'Part Number', 'Product Period', 'Cumulative Seat', 'Order Delta', 'Reseller ID',
    'Reseller External ID', 'Reseller ID #', 'Reseller Name', 'End Customer Name', 'End Customer External ID', 'Provider ID',
    'Provider Name', 'Marketplace', 'HUB ID', 'HUB Name', 'Product ID', 'Product Name', 'Subscription Status',
    'Effective Date', 'Creation Date', 'Connect Order Type', 'Customer Tenant Value', 'Currency',
    'Connection Type', 'Exported At'
]


def generate(client, parameters, progress_callback, renderer_type='xlsx', extra_context_callback=None):
    all_products = utils.get_all_products(parameters)
    requests = request_approved_requests(client, parameters, all_products)
    progress = 0
    total = requests.count()
    config = utils.select_config(parameters)

    if renderer_type == 'csv':
        yield HEADERS

    for request in requests:
        parameters_list = request['asset']['params']
        for item in request['asset']['items']:
            product = utils.get_value(request['asset'], 'product', 'id')
            yield _process_line(request, config, product, parameters_list, item)
        progress += 1
        progress_callback(progress, total)


def _get_delta_str(item):
    try:
        return str(int(item.get('quantity')) - int(item.get('old_quantity')))
    except Exception:
        return ''


def request_approved_requests(client, parameters, all_products):
    query = R()
    query &= R().status.eq('approved')
    query &= R().created.ge(parameters['date']['after'])
    query &= R().created.le(parameters['date']['before'])

    if parameters.get('connexion_type') and parameters['connexion_type']['all'] is False:
        query &= R().asset.connection.type.oneof(parameters['connexion_type']['choices'])
    if parameters.get('product') and parameters['product']['all'] is False:
        query &= R().asset.product.id.oneof(parameters['product']['choices'])
    if parameters.get('rr_type') and parameters['rr_type']['all'] is False:
        query &= R().type.oneof(parameters['rr_type']['choices'])
    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().marketplace.id.oneof(parameters['mkp']['choices'])

    query &= R().asset.product.id.oneof(all_products)
    return client.requests.filter(query).order_by("created")


def _process_line(request, config, product, parameters_list, item):

    return (
        utils.get_basic_value(request, 'id'),  # Request ID
        utils.get_value(request, 'asset', 'id'),  # Connect Subscription ID
        utils.get_value(request, 'asset', 'external_id'),  # End Customer Subscription ID
        utils.get_param_value(parameters_list, utils.get_product_field_name(config, product, 'action')),  # Action
        utils.get_param_value(parameters_list, utils.get_product_field_name(config, product, 'order')), # Vendor Order #
        utils.get_param_value(parameters_list, utils.get_product_field_name(config, product, 'transfer')), # Vendor Transfer #
        utils.get_param_value(parameters_list, utils.get_product_field_name(config, product, 'vip')), # Vendor Subscription
        utils.get_param_value(parameters_list, utils.get_product_field_name(config, product, 'customer_id')), # Vendor Customer ID
        utils.get_param_value(parameters_list, utils.get_product_field_name(config, product, 'discount_group')), # Pricing SKU Level (Volume Discount level)
        utils.get_basic_value(item, 'display_name'),  # Product Description
        utils.get_basic_value(item, 'mpn'),  # Part Number
        utils.get_basic_value(item, 'period'),  # Product Period
        utils.get_basic_value(item, 'quantity'),  # Cumulative Seat
        _get_delta_str(item),  # Order Delta
        utils.get_value(request['asset']['tiers'], 'tier1', 'id'),  # Reseller ID (RESELLER EXTERNAL)
        utils.get_value(request['asset']['tiers'], 'tier1', 'external_uid'),  # Reseller External ID
        utils.get_value(request['asset']['tiers'], 'tier1', 'external_id'),  # Reseller ID #
        utils.get_value(request['asset']['tiers'], 'tier1', 'name'),  # Reseller Name
        utils.get_value(request['asset']['tiers'], 'customer', 'name'),  # End Customer Name
        utils.get_value(request['asset']['tiers'], 'customer', 'external_id'),  # End Customer External ID
        utils.get_value(request['asset']['connection'], 'provider', 'id'),  # Provider ID
        utils.get_value(request['asset']['connection'], 'provider', 'name'),  # Provider Name
        utils.get_value(request, 'marketplace', 'name'),  # Marketplace
        utils.get_value(request['asset']['connection'], 'hub', 'id'),  # HUB ID
        utils.get_value(request['asset']['connection'], 'hub', 'name'),  # HUB Name
        utils.get_value(request['asset'], 'product', 'id'),  # Product ID
        utils.get_value(request['asset'], 'product', 'name'),  # Product Name
        utils.get_value(request, 'asset', 'status'),  # Subscription Status
        utils.convert_to_datetime(utils.get_basic_value(request, 'effective_date')),  # Effective  Date
        utils.convert_to_datetime(utils.get_basic_value(request, 'created')),  # Creation  Date
        utils.get_basic_value(request, 'type'),  # Connect Order Type
        utils.get_param_value(parameters_list, utils.get_product_field_name(config, product, 'mail')), # Customer Tenant Value
        '',  # Currency (EMPTY)
        utils.get_basic_value(request['asset']['connection'], 'type'),  # Connection Type,
        utils.today_str(),  # Exported At
    )
