# -*- coding: utf-8 -*-
#
# Copyright (c) 2024, CloudBlue
# All rights reserved.
#

from datetime import datetime, timezone, date
import calendar

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


def get_basic_value(base, value):
    try:
        if base and value in base:
            return base[value]
        return '-'
    except Exception:
        return '-'


def get_value(base, prop, value):
    if prop in base:
        return get_basic_value(base[prop], value)
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

PRODUCT_FIELDS = [
   {
      "id": "Adobe",
      "products":[
          "PRD-207-752-513", "PRD-466-278-670", "PRD-308-433-016", "PRD-265-651-368"
      ],
      "fields":{
         "vip":"adobe_vip_number",
         "order":"adobe_order_id",
         "transfer":"transfer_id",
         "action":"action_type",
         "mail":"adobe_user_email",
         "customer_id":"adobe_customer_id",
         "discount_group":"discount_group"
      }
   },
   {
      "id": "Microsoft NCE",
      "products":[
         "PRD-450-658-035", "PRD-007-563-386", "PRD-136-332-888", "PRD-672-364-473"
      ],
      "fields":{
         "vip":"microsoft_subscription_id",
         "order":"microsoft_order_id",
         "transfer":"",
         "action":"",
         "mail":"microsoft_domain",
         "customer_id":"customer_id",
         "discount_group":""
      }
   },
   {
      "id": "Azure NCE",
      "products":[
         "PRD-421-575-828"
      ],
      "fields":{
         "vip":"subscription_id",
         "order":"csp_order_id",
         "transfer":"nce_migration_id",
         "action":"migration_type",
         "mail":"microsoft_domain",
         "customer_id":"ms_customer_id",
         "discount_group":"cart_id"
      }
   },
   {
      "id": "Azure RI",
      "products":[
         "PRD-815-848-109"
      ],
      "fields":{
         "vip":"asset_recon_id",
         "order":"",
         "transfer":"",
         "action":"",
         "mail":"microsoft_domain",
         "customer_id":"customer_id",
         "discount_group":""
      }
   }
]