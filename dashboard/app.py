import streamlit as st
import pandas as pd

st.title('Znajdź mieszkanie dla siebie!')
st.subheader('System rekomendacji mieszkań')


@st.cache
def load_data():
    df = pd.read_csv(
        'https://ids-storage-football-prediction.s3-eu-west-1.amazonaws.com/data_mmwd/listings_scalled.csv',
        index_col=['Unnamed: 0'])
    df = df[df['price'] > 0]
    df = df[df['bedrooms'] > 0]
    df = df[df['bathrooms'] > 0]
    return df


df = load_data()

st.sidebar.subheader('Opcje wyszukiwania')
# Sidebar Options:
params = {
    'bedrooms': st.sidebar.selectbox('Liczba sypialni', ('-', 1, 2, 3, 4, 5, 6)),
    'beds': st.sidebar.selectbox('Liczba łóżek', ('-', 1, 2, 3, 4, 5, 6, 7)),
    'bathrooms': st.sidebar.selectbox('Liczba łazienek', ('-', 1, 2, 3, 4)),
    'accommodates': st.sidebar.selectbox('Liczba osób', ('-', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)),
    'values_amount': st.sidebar.selectbox('Liczba wyszukań', ('wszystkie', 5, 10, 15, 20, 30)),
}

test_size = st.sidebar.slider('Maksymalna cena', 0, 2000, 100, step=5)


def map_df(frame: pd.DataFrame) -> pd.DataFrame:
    BEDROOMS = -1
    BEDS = -1
    ACCOMMODATES = -1
    BATHROOMS = -1
    MAX_PRICE = 100

    if params['bedrooms'] != '-':
        BEDROOMS = params['bedrooms']
    if params['beds'] != '-':
        BEDS = params['beds']
    if params['bathrooms'] != '-':
        BATHROOMS = params['bathrooms']
    if params['accommodates'] != '-':
        ACCOMMODATES = params['accommodates']
    if params['values_amount'] == 'wszystkie':
        VALUES = 10000000
    else:
        VALUES = params['values_amount']

    filters = {
        'bedrooms': BEDROOMS,
        'beds': BEDS,
        'accommodates': ACCOMMODATES,
        'bathrooms': BATHROOMS
    }

    sub_filters = {
        'bedrooms': BEDROOMS + 1,
        'beds': BEDS + 1,
        'accommodates': ACCOMMODATES + 1,
        'bathrooms': BATHROOMS + 1
    }

    sub_sub_filters = {
        'bedrooms': BEDROOMS - 1,
        'beds': BEDS - 1,
        'accommodates': ACCOMMODATES - 1,
        'bathrooms': BATHROOMS - 1
    }

    features_to_filter = []
    features_no_filter = []

    if BEDROOMS != -1:
        features_to_filter.append('bedrooms')
    else:
        features_no_filter.append('bedrooms')

    if BEDS != -1:
        features_to_filter.append('beds')
    else:
        features_no_filter.append('beds')

    if ACCOMMODATES != -1:
        features_to_filter.append('accommodates')
    else:
        features_no_filter.append('accommodates')

    if BATHROOMS != -1:
        features_to_filter.append('bathrooms')
    else:
        features_no_filter.append('bathrooms')

    for feature in features_to_filter:
        if feature == 'bathrooms' or feature == 'beds':
            frame = frame[
                (frame[feature] == filters[feature]) | (frame[feature] == sub_filters[feature]) | (
                        frame[feature] == sub_sub_filters[feature])]
        else:
            frame = frame[
                (frame[feature] == filters[feature]) | (frame[feature] == sub_filters[feature])]

    frame = frame[frame['price'] <= MAX_PRICE]

    frame['classified'] = 3 * frame['scaled_polarity'] + 2 * frame['scaled_distance'] + 1 * frame['scaled_number_of_reviews']

    frame = frame.sort_values(by=['classified'], ascending=False)
    st.write(f'Dopasowano **{frame.shape[0]}** mieszkań.')
    frame = frame.head(VALUES)

    return frame


def run_data():
    data = map_df(df)
    st.map(data)
    return data


btn = st.sidebar.button("Szukaj")
if btn:
    data = run_data()
    # data
    st.dataframe(data=data, height=600)
else:
    pass
