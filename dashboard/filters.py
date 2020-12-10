def get_filters(bedrooms, beds, accommodates, bathrooms):
    return {
        'bedrooms': bedrooms,
        'beds': beds,
        'accommodates': accommodates,
        'bathrooms': bathrooms
    }


def get_sub_filters(bedrooms, beds, accommodates, bathrooms):
    return {
        'bedrooms': bedrooms + 1,
        'beds': beds + 1,
        'accommodates': accommodates + 1,
        'bathrooms': bathrooms + 1
    }


def get_sub_sub_filters(bedrooms, beds, accommodates, bathrooms):
    return {
        'bedrooms': bedrooms - 1,
        'beds': beds - 1,
        'accommodates': accommodates - 1,
        'bathrooms': bathrooms - 1
    }


def get_filters_arrays(bedrooms, beds, accommodates, bathrooms):
    features_to_filter = []
    features_no_filter = []

    if bedrooms != -1:
        features_to_filter.append('bedrooms')
    else:
        features_no_filter.append('bedrooms')

    if beds != -1:
        features_to_filter.append('beds')
    else:
        features_no_filter.append('beds')

    if accommodates != -1:
        features_to_filter.append('accommodates')
    else:
        features_no_filter.append('accommodates')

    if bathrooms != -1:
        features_to_filter.append('bathrooms')
    else:
        features_no_filter.append('bathrooms')

    return features_to_filter, features_no_filter
