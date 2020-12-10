def get_bedrooms(params):
    bedrooms = -1
    if params['bedrooms'] != '-':
        bedrooms = params['bedrooms']

    return bedrooms


def get_beds(params):
    beds = -1
    if params['beds'] != '-':
        beds = params['beds']

    return beds


def get_accommodates(params):
    accommodates = -1
    if params['accommodates'] != '-':
        accommodates = params['accommodates']

    return accommodates


def get_bathrooms(params):
    bathrooms = -1
    if params['bathrooms'] != '-':
        bathrooms = params['bathrooms']

    return bathrooms


def get_amounts(params):
    if params['values_amount'] == 'wszystkie':
        return 10000000
    else:
        return params['values_amount']


def get_max_price(price):
    max_price = 100
    if price:
        max_price = price

    return max_price
