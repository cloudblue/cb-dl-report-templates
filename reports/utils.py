# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, CloudBlue
# All rights reserved.
#

from datetime import datetime, timezone, date
import calendar
import json
import os

class DatalakeReportsException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

def get_param_value_by_name(params: list, value: str) -> str:
    try:
        if params[0]['name'] == value:
            return params[0]['value']
        if len(params) == 1:
            return '-'
        return get_param_value_by_name(list(params[1:]), value)
    except Exception:
        return '-'


def get_param_value(params: list, value: str) -> str:
    try:
        if params[0]['id'] == value:
            return params[0]['value']
        if len(params) == 1:
            return '-'
        return get_param_value(list(params[1:]), value)
    except Exception:
        return '-'

def get_parameter_value(params: list, value: str) -> str:
    try:
        if params[0]['parameter']['id'] == value:
            return params[0]['value']
        if len(params) == 1:
            return '-'
        return get_parameter_value(list(params[1:]), value)
    except Exception:
        return '-'


def get_basic_value(base, value):
    try:
        if base and value in base:
            return base[value]
        return '-'
    except Exception:
        return '-'


def get_value(base, prop, value):
    try:
        if prop in base:
            return get_basic_value(base[prop], value)
        return '-'
    except Exception:
        return '-'

def convert_to_datetime(param_value):
    if param_value == "" or param_value == "-" or param_value is None:
        return "-"

    return datetime.strptime(
        param_value.replace("T", " ").replace("+00:00", ""),
        "%Y-%m-%d %H:%M:%S",
    )


def today() -> datetime:
    return datetime.datetime.today()


def today_str() -> str:
    return datetime.today().strftime('%Y-%m-%d %H:%M:%S')


def get_discount_level(discount_group: str) -> str:
    """
    Transform the discount_group to a proper level of discount

    :type discount_group: str
    :param discount_group:
    :return: str with level of discount
    """
    if len(discount_group) > 2 and discount_group[2] == 'A' and discount_group[0] == '1':
        discount = 'Level ' + discount_group[0:2]
    elif len(discount_group) > 2 and discount_group[2] == 'A':
        discount = 'Level ' + discount_group[1]
    elif len(discount_group) > 2 and discount_group[2] == '0':
        discount = 'TLP Level ' + discount_group[1]
    else:
        discount = 'Empty'

    return discount


def get_all_products(parameters):
    if parameters.get('connexion_type') and parameters['connexion_type']['all'] is True:
        raise DatalakeReportsException("Please, select [preview and/or test] or [production]")
    all_products = [product for x in select_config(parameters) for product in x["products"]]
    return all_products

def select_config(parameters):
    if parameters.get('connexion_type') and parameters['connexion_type']['all'] is True:
        raise DatalakeReportsException("Please, select [preview and/or test] or [production]")
    json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'conf.json')
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
    if (parameters.get('connexion_type').get("choices")[0]) in ["preview", "test"]:
        res = [x.get("data") for x in data.get("conf") if x.get("id") == "PRODUCT_FIELDS_DEV"][0]
    if (parameters.get('connexion_type').get("choices")[0]) in ["production"]:
        res = [x.get("data") for x in data.get("conf") if x.get("id") == "PRODUCT_FIELDS_PRO"][0]
    return res

def get_product_field_name(config, product_code, field_name):
    for x in config:
        if product_code in x["products"]:
            return x["fields"][field_name]
    return ''
