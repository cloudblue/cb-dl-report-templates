# Report Approved Requests


This report creates an Excel file with details about all approved requests with subscription scope parameters


## Available parameters

Request can be parametrized by:

* Request creation date range
* Marketplace
* Environment
* Request Type

## Columns
* Request_ID
* Connect_Subscription ID
* End_Customer_Subscription_ID
* Action
* Vendor_Order__
* Vendor_Transfer__
* Vendor_Subscription__
* Vendor_Customer ID__
* Pricing_SKU_Level__Volume_Discount_level_
* Product_Description
* Part_Number
* Product_Period
* Cumulative_Seat
* Order_Delta
* Reseller_ID__RESELLER_EXTERNAL_
* Reseller_External_ID
* Reseller_Name
* End_Customer_Name
* End_Customer_External_ID
* Provider_ID
* Provider_Name
* Marketplace
* HUB_ID
* HUB_Name
* Product_ID
* Product_Name
* _Subscription_Status
* Effective_Date
* Creation_Date
* Connect_Order_Type
* Customer_Tenant_Value
* Currency
* Connection_Type
* Exported_At

Command to create report: ccli report execute approved_requests -d .