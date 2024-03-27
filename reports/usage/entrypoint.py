# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, CloudBlue
# All rights reserved.
#

from reports import utils
from connect.client import R
import requests
import json
import pandas as pd
import io
import zipfile
from io import BytesIO
from openpyxl import load_workbook

def generate(client, parameters, progress_callback, renderer_type='xlsx', extra_context_callback=None):
    progress = 0
    # TODO: HARDCODED
    parameters = {'date': {'after': '2020-12-31T23:00:00+00:00', 'before': '2023-12-31T23:00:00+00:00'},
                  'mkp': {'all': True, 'choices': []},
                  'connexion_type': {'all': False, 'choices': ['preview']}}
    all_products = utils.get_all_products(parameters)
    print("all_products")
    print(all_products)
    usage_files = _get_usage_files(parameters, client,  all_products)
    print(usage_files)
    total = usage_files.count()
    print("total")
    print(total)
    for file in usage_files:
        print(f"------{utils.get_basic_value(file, 'id')}")
        usage_file = _get_usage_file(client, utils.get_basic_value(file, 'id'))
        excel_data = _read_excel_file(usage_file.get("processed_file_uri"))
        print(excel_data)
        for x in excel_data:
            yield(
            x.get("record_id"),# Record ID UR-2023-08-8243-8211-5060-5873
            x.get(""),  # Subscription ID AS-4994-0353-9179
            x.get("asset_external_id"),# Subscription External ID    1090540
            x.get("asset_recon_id"),# Subscription Recon ID    ed76e650-600b-4bb4-d7ff-358f996b40c4:7d395730-0bce-4061-94e8-b68b323612cc
            x.get("status"),# Status    closed
            x.get("item_id"),# Item ID    PRD-561-716-033-0051
            x.get("item_name"),# Item Name    Advanced Threat Protection
            x.get("item_mpn"),# Item MPN    Advanced_Threat_Protection
            x.get("quantity"),# Quantity    1
            x.get(""),# MSRP    27.41155727
            x.get(""),# Cost    0
            x.get(""),# Price    0
            x.get("product_id"),# Product ID    PRD-561-716-033
            utils.get_basic_value(file, "currency"),# Currency    EUR
            x.get(""),# Schema    pr
            x.get("start_time_utc"),# Start Date    2023-07-01 0:00:00
            x.get("end_time_utc"),# End Date    2023-07-31 23:59:59
            x.get(""),# to_exchange_rate_by_config    0
            x.get(""),# to_exchange_rate    -
            x.get(""),# from_exchange_rate_by_config    0
            x.get(""),# from_exchange_rate    -
            x.get("v.entitlement_id"),# entitlement_id    7d395730-0bce-4061-94e8-b68b323612cc
            x.get("v.plan_subscription_id"),# plan_subscription_id    ed76e650-600b-4bb4-d7ff-358f996b40c4
            x.get("v.invoice_number"),# invoice_number    G026626974
            x.get("v.publisher_name"),# publisher_name    Microsoft
            x.get("v.aobo"),# aobo    1
            utils.today_str(),# Exported At    2024-01-23 12:22:13,
            )
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


def _read_excel_file(url):
    response = requests.get(url)
    if response.status_code != 200:
        return print({"error": "Failed to download the file"})
    try:
        with io.BytesIO(response.content) as f:
            df = pd.read_excel(f, 'records', engine='openpyxl')
    except Exception as e:
        return {"error": f"Failed to read the Excel file: {str(e)}"}

    return df.to_dict(orient='records')