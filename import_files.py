import requests
import json
import smtplib
from enviro_variables import TO_EMAIL, FROM_EMAIL, FROM_PASS, CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN


# def generate_new_token():
#     url = "https://cloud.lightspeedapp.com/oauth/access_token.php"
#     refresh_payload = {
#         'refresh_token': REFRESH_TOKEN,
#         'client_secret': CLIENT_SECRET,
#         'client_id': CLIENT_ID,
#         'grant_type': 'refresh_token'}
#     r = requests.get(url, data=refresh_payload).json()
#     access_token = r["access_token"]
#     return {"authorization": f"Bearer {access_token}"}


def success_email(payload):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        # TODO look into how long everything takes, this process is slowing things down quite a bit
        smtp.login(FROM_EMAIL, FROM_PASS)

        order_number = payload['order']['number']
        creation = payload['order']['createdAt']

        subject = f'{order_number} Successfully Uploaded'
        body = f'{order_number} was uploaded at {creation}'
        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(TO_EMAIL, FROM_EMAIL, msg)


def sale_line_items(payload):
    empty_dict = {"SaleLine": []}

    for key in payload['order']['products']['resource']['embedded']:
        quantity = key['quantityOrdered']
        price = key['basePriceExcl']
        sku = key['variant']['resource']['sku']

        empty_dict['SaleLine'].append(
            {"itemCode": sku,
             "quantityOrdered": quantity,
             "unitPrice": price,
             "taxCategoryID": "1",
             # todo figure our tax category id for line items in sale
             "tax": "true",
             "tax1Rate": "0.05",
             "tax2Rate": "0.09975",
             })

    return empty_dict


def format_json(payload, url):
    condition_1 = payload['order']['addressShippingRegion']
    condition_2 = payload['order']['status']
    condition_3 = payload['order']['email']
    condition_4 = payload['order']['shipmentBasePriceExcl']

    quebec_sale = [condition_1 == 'Quebec', condition_2 == 'processing_awaiting_shipment']
    amazon_order_conditions = ['amazon' in condition_3]
    shipping_paid_condition = [condition_4 != 0.00]

    headers = {"authorization": "Bearer 1345891846"}

    if all(quebec_sale):
        if all(amazon_order_conditions):
            amazon_dict = {
                "employeeID": 1,
                "registerID": 1,
                "shopID": 1,
                "enablePromotions": "true",
                "isTaxInclusive": "false",
                "customerID": payload['order']['customer']['resource']['id'],
                "completed": "true",
                "referenceNumber": payload['order']['number'],
                "SaleLines": sale_line_items(payload),
                "taxCategoryID": "14",
                # todo figure out tax category for entire sale
            }

            amazon_shipping_dict = {
                "employeeID": 1,
                "registerID": 1,
                "shopID": 1,
                "enablePromotions": "true",
                "customerID": payload['order']['customer']['resource']['id'],
                "completed": "true",
                "referenceNumber": payload['order']['number'],
                "SaleLines": {"SaleLine": [{
                    "itemID": 210000028217,
                    "unitQuantity": 1,
                    "unitPrice": payload['order']['shipmentBasePriceExcl'],
                    "tax": "true",
                    "tax1Rate": "0.05",
                    "tax2Rate": "0.09975",
                }]},
                "taxCategoryID": "2"}

            requests.post(url, data=json.dumps(amazon_dict),  headers=headers)
            requests.post(url, data=json.dumps(amazon_shipping_dict), headers=headers)

            return 'success', 200

        elif all(shipping_paid_condition):
            order_with_shipping_dict = {
                "employeeID": 1,
                "registerID": 1,
                "shopID": 1,
                "enablePromotions": "true",
                "customerID": payload['order']['customer']['resource']['id'],
                "completed": "true",
                "referenceNumber": payload['order']['number'],
                "SaleLines": {"SaleLine": [{
                    "itemID": 210000028217,
                    "unitQuantity": 1,
                    "unitPrice": payload['order']['shipmentBasePriceExcl'],
                    "tax": "true",
                    "tax1Rate": "0.05",
                    "tax2Rate": "0.09975",
                }]},
                "taxCategoryID": "2"}

            shipping_dict = {
                "employeeID": 1,
                "registerID": 1,
                "shopID": 1,
                "enablePromotions": "true",
                "customerID": payload['order']['customer']['resource']['id'],
                "completed": "true",
                "referenceNumber": payload['order']['number'],
                "SaleLines": sale_line_items(payload),
                "taxCategoryID": "14",
                # todo figure out tax category for entire sale
            }

            requests.post(url, data=json.dumps(order_with_shipping_dict), headers=headers)
            requests.post(url, data=json.dumps(shipping_dict), headers=headers)

            return 'success', 200

        else:
            order_no_shipping_dict = {
                "employeeID": 1,
                "registerID": 1,
                "shopID": 1,
                "enablePromotions": "true",
                "customerID": payload['order']['customer']['resource']['id'],
                "completed": "true",
                "referenceNumber": payload['order']['number'],
                "SaleLines": sale_line_items(payload),
                "taxCategoryID": "14",
                # todo figure out tax category for entire sale
            }

            requests.post(url, data=json.dumps(order_no_shipping_dict), headers=headers)

            return 'success', 200
