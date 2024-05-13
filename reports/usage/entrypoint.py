# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, CloudBlue
# All rights reserved.
#

from reports import utils
from connect.client import R
import requests

HEADERS = [
    "Record ID", "Subscription ID", "Subscription External ID",
    "Subscription Recon ID", "Status", "Item ID",
    "Item Name", "Item MPN", "Quantity", "MSRP",
    "Cost", "Price", "Product ID", "Currency", "Schema",
    "Start Date", "End Date", "to_exchange_rate_by_config",
    "to_exchange_rate", "from_exchange_rate_by_config",
    "from_exchange_rate", "entitlement_id",
    "plan_subscription_id", "invoice_number", "publisher_name",
    "aobo", "Exported At"
]


def generate(client, parameters, progress_callback, renderer_type='xlsx', extra_context_callback=None):
    progress = 0
    all_products = utils.get_all_products(parameters)
    usage_files = _get_usage_files(parameters, client, all_products)
    total = usage_files.count()
    config = utils.select_config(parameters)

    if renderer_type == 'csv':
        yield HEADERS

    for file in usage_files:
        records = _get_usage_records(client, utils.get_basic_value(file, 'id'))
        tier_level = _get_tier_level(utils.get_basic_value(file, "schema"))
        for record in records:
            yield _process_line(record, tier_level, config)

        progress += 1
        progress_callback(progress, total)


def _get_usage_files(parameters, client, all_products):
    query = R()
    query &= R().created.ge(parameters['date']['after'])
    query &= R().created.le(parameters['date']['before'])
    if parameters.get('mkp') and parameters['mkp']['all'] is False:
        query &= R().marketplace.id.oneof(parameters['mkp']['choices'])

    query &= R().product.id.oneof(all_products)

    return client.ns("usage").files.filter(query)


def _get_usage_file(client, file_id):
    return client.ns("usage").files[file_id].get()


def _get_tier_level(schema):
    res = 0
    if schema == "pr":
        res = 0
    elif schema == "cr":
        res = 2
    elif schema == "tr":
        res = x.get("tier")
    return res


def _get_usage_records(client, file_id):
    query = R()
    query &= R().usagefile.id.eq(file_id)

    return client.ns("usage").records.filter(query)


def _process_line(record, tier_level, config):
    product = record.get("product_id")
    amount_tier_0 = utils.get_basic_value(record, "amount") if tier_level == 0 else "-"
    amount_tier_1 = utils.get_basic_value(record, "amount") if tier_level == 1 else "-"
    amount_tier_2 = utils.get_basic_value(record, "amount") if tier_level == 2 else "-"

    return (
        utils.get_basic_value(record, "id"),
        utils.get_basic_value(record.get('asset'), "id"),
        utils.get_basic_value(record.get('asset'), "external_id"),
        utils.get_basic_value(record.get('asset'), "recon_id"),
        utils.get_basic_value(record, "status"),
        utils.get_basic_value(record.get('item'), "id"),
        utils.get_basic_value(record.get('item'), "name"),
        utils.get_basic_value(record.get('item'), "mpn"),
        utils.get_basic_value(record, "status"),
        utils.get_basic_value(record, "usage"),
        amount_tier_0,
        amount_tier_1,
        amount_tier_2,
        utils.get_basic_value(record.get('usagefile'), "currency"),
        utils.get_basic_value(record.get('usagefile'), "schema"),
        utils.get_basic_value(record, "start_date"),
        utils.get_basic_value(record, "end_date"),
        utils.get_param_value_by_name(
            record.get('params'),
            utils.get_product_field_name(config, product, 'to_exchange_rate_by_config')),
        utils.get_param_value_by_name(
            record.get('params'),
            utils.get_product_field_name(config, product, 'to_exchange_rate')),
        utils.get_param_value_by_name(
            record.get('params'),
            utils.get_product_field_name(config, product, 'from_exchange_rate_by_config')),
        utils.get_param_value_by_name(
            record.get('params'),
            utils.get_product_field_name(config, product, 'from_exchange_rate')),
        utils.get_param_value_by_name(
            record.get('params'),
            utils.get_product_field_name(config, product, 'entitlement_id')),
        utils.get_param_value_by_name(
            record.get('params'),
            utils.get_product_field_name(config, product, 'plan_subscription_id')),
        utils.get_param_value_by_name(
            record.get('params'),
            utils.get_product_field_name(config, product, 'invoice_number')),
        utils.get_param_value_by_name(
            record.get('params'),
            utils.get_product_field_name(config, product, 'publisher_name')),
        utils.get_param_value_by_name(
            record.get('params'),
            utils.get_product_field_name(config, product, 'aobo')),
        utils.today_str()
    )
