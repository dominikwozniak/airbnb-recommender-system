import streamlit as st
import pandas as pd
from filters import get_filters, get_sub_filters, get_sub_sub_filters, get_filters_arrays
from params import get_bedrooms, get_accommodates, get_amounts, get_bathrooms, get_beds, get_max_price
from coefficients import DISTANCE_COEFF, NUMBER_OF_REVIEWS_COEFF, POLARITY_COEFF

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

price = st.sidebar.slider('Maksymalna cena', 0, 2000, 100, step=5)


@st.cache(suppress_st_warning=True)
def map_df(frame: pd.DataFrame) -> pd.DataFrame:
    bedrooms = get_bedrooms(params)
    beds = get_beds(params)
    accommodates = get_accommodates(params)
    bathrooms = get_bathrooms(params)
    max_price = get_max_price(price)
    values = get_amounts(params)

    filters = get_filters(bedrooms, beds, accommodates, bathrooms)
    sub_filters = get_sub_filters(bedrooms, beds, accommodates, bathrooms)
    sub_sub_filters = get_sub_sub_filters(bedrooms, beds, accommodates, bathrooms)

    features_to_filter, features_no_filter = get_filters_arrays(bedrooms, beds, accommodates, bathrooms)

    for feature in features_to_filter:
        if feature == 'bathrooms' or feature == 'beds':
            frame = frame[
                (frame[feature] == filters[feature]) | (frame[feature] == sub_filters[feature]) | (
                        frame[feature] == sub_sub_filters[feature])]
        else:
            frame = frame[
                (frame[feature] == filters[feature]) | (frame[feature] == sub_filters[feature])]

    frame = frame[frame['price'] <= max_price]

    frame['classified'] = POLARITY_COEFF * frame['scaled_polarity'] + DISTANCE_COEFF * frame['scaled_distance'] + NUMBER_OF_REVIEWS_COEFF * frame[
        'scaled_number_of_reviews']

    frame = frame.sort_values(by=['classified'], ascending=False)
    st.write(f'Dopasowano **{frame.shape[0]}** mieszkań.')
    frame = frame.head(values)

    return frame


def run_data():
    data = map_df(df)
    st.map(data)
    return data


show_data = st.sidebar.checkbox('Pokaż szczegóły')
search_btn = st.sidebar.button("Szukaj")

if search_btn:
    data = run_data()
    if show_data:
        st.dataframe(data=data, height=600)
    else:
        st.dataframe(data=data[['id', 'name', 'description', 'price']], height=600)
else:
    pass
