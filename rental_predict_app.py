
import streamlit as st
import app.ml_predict as ml
from app.app_builder import app_builder


def main():

    ren_app=app_builder()
    ren_app._get_bedrooms()
    ren_app._get_bathrooms()
    ren_app._get_den()
    ren_app._get_postal_code()
    ren_app._get_lat_lon()


    if ren_app._btn_submit:
        prop=ml.property_builder()
        prop.set_bedrooms(ren_app._bedrooms)
        prop.set_bathrooms(ren_app._bathrooms)
        prop.set_den(ren_app._den)
        prop.set_postalcode(ren_app._postal_code)
        prop.set_latitude(ren_app._latitude)
        prop.set_longitude(ren_app._longitude)
        prop.find_neighborhood()
        prop.build_df()
        st.write(prop._df)
        prop.encode_neighborhood()
        prop.scale_features()
        prop.find_rental_price()
        prop.build()
        st.success(f"{CAD int(prop._rental_price[0])} per month would be a good rental price.")


if __name__=="__main__":
    main()