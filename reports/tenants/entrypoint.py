# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, CloudBlue
# All rights reserved.
#

from reports import utils
from connect.client import R
import requests
import json


def generate(client, parameters, progress_callback, renderer_type='xlsx', extra_context_callback=None):
    progress = 0
    all_products = utils.get_all_products(parameters)
    marketplaces = _get_marketplaces(parameters, client)
    total = marketplaces.count()
    for m in marketplaces:
        for hub in m.get("hubs", {}):
            hub_id = utils.get_value(hub, 'hub', 'id')
            hub_connections = _get_hub_connections(client, hub_id, all_products) if hub_id else {}
            hub_info = _get_hub(hub_id, client)
            for conn in hub_connections:
                yield(utils.get_basic_value(m, 'id'), # Marketplace ID
                      utils.get_value(conn, 'product', 'id'), # Partner Id TODO: ¿PARTNER OR PRODUCT_ID?
                      utils.get_basic_value(m, 'name'), # Marketplace Name
                      utils.get_value(conn, 'provider', 'id'), # Provider ID
                      utils.get_value(conn, 'provider', 'name'), # Provider Name
                      utils.get_value(hub, 'hub',  'id'), # Hub ID
                      utils.get_value(hub, 'hub', 'name'), # Hub Name
                      utils.get_value(hub_info, 'instance', 'id'), # Instance GUID
                      utils.get_value(conn, 'vendor', 'id'), # Vendor ID
                      utils.get_value(conn, 'vendor', 'name'), # Vendor Name
                      utils.get_basic_value(hub, 'external_id'), # Reseller Account 1 ID
                      "", # Reseller Account 2 ID
                      "", # (EMPTY) Syndicated Marketplace ID
                      "", # (EMPTY)Syndicated Marketplace Name
                      "", # (EMPTY)Syndicated Provider ID
                      "", # (EMPTY)Syndicated Provider Name
                )
        progress += 1
        progress_callback(progress, total)


def _get_hub_connections(client, hub_id, all_products):
    try:
        query = R()
        query &= R().product.id.oneof(all_products)
        return client.hubs[hub_id].connections.filter(query) or {}
    except Exception as e:
        print("EXCEPTION _get_hub_connections")
        print(str(e))
        return {}

def _get_hub_marketplaces(client, hub_id):
    try:
        return client.hubs[hub_id].marketplaces.all() or {}
    except Exception as e:
        print("EXCEPTION _get_hub_marketplaces")
        print(str(e))
        return {}


def _get_hubs(client):
    return client.hubs.all()

def _get_hub(hub_id, client):
    query = R()
    query &= R().id.eq(hub_id)
    return client.hubs.filter(query)[0]

def request_vendor(client):
    query = R()
    query &= R().status.eq('active')
    query &= R().role.eq('vendor')
    return client.partners.filter(query)


def _get_marketplaces(parameters, client):
    try:
        query = R()
        if parameters.get('mkp') and parameters['mkp']['all'] is False:
            query &= R().id.oneof(parameters['mkp']['choices'])
        return client.marketplaces.filter(query)
    except Exception as e:
        print("EXCEPTION _get_hub_marketplaces")
        print(str(e))
        return {}
