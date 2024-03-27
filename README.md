# Welcome to Data Lake Reports !


Data Lake Reports



## License

**Data Lake Reports** is licensed under the *Apache Software License 2.0* license.

# Report Requests

This report creates an Excel file with details about all approved requests with subscription scope parameters

## Available parameters

Request can be parametrized by:

* Request creation date range
* Product (Of a custom list of products)
* Marketplace
* Environment
* Request Type

## Columns
* Request ID
* Connect Subscription ID
* End Customer Subscription ID
* Action
* Vendor Order #
* Vendor Transfer #
* Vendor Subscription #
* Vendor Customer ID #
* Pricing SKU Level (Volume Discount level)
* Product Description
* Part Number
* Product Period
* Cumulative Seat
* Order Delta
* Reseller ID (RESELLER EXTERNAL)
* Reseller External ID
* Reseller Name
* End Customer Name
* End Customer External ID
* Provider ID
* Provider Name
* Marketplace
* HUB ID
* HUB Name
* Product ID
* Product Name
* #Subscription Status
* Effective  Date
* Creation  Date
* Connect Order Type
* Customer Tenant Value
* Currency
* Connection Type
* Exported At

Command to create report: ccli report execute approved_requests -d .