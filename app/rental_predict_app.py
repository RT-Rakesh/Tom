import pandas as pd
import streamlit as st
import re
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
import folium as fl
from folium import Element
from streamlit_folium import folium_static
import time
import ml_predict as ml
import sklearn


def get_lan_long_from_postal_code(postal_code):
  """
  This function takes a postal code as input and returns the latitude and longitude of the corresponding location in Canada using the Nominatim geocoder.
  """
  geolocator = Nominatim(user_agent="GetLoc")
  location = geolocator.geocode(postal_code, country_codes="CA")
  if location:
    return location.latitude, location.longitude
  else:
    return None, None

def is_valid_postal_code(postal_code):
    pattern = re.compile(r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$")
    return bool(pattern.match(postal_code))
            

def select_on_map(lat, lon):
    # Initialize Streamlit app
    st.title("Select Location on the Map")
    def get_pos(lat, lng):
        return lat, lng
    #def update_check(lat, lng):

    default_location = [lat, lon]
    m = fl.Map(location=default_location, zoom_start=50)
    m.add_child(fl.LatLngPopup())
    map = st_folium(m, height=500, width=700)
    data = None
    acceptance=True
    if map.get("last_clicked"):
        # st.write('lasst clicked')
        data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])
        _lat, _lng = data[0], data[1]
        # acceptance = st.button(f'Use Lat:{_lat}and log:{_lng}')
    time.sleep(2)
    if data and  acceptance is not None:
        return _lat,_lng #if acceptance==True else select_on_map(_lat, _lng)

def main():

    bedrooms=st.sidebar.slider("No.of Bed Rooms", min_value=1.0, max_value=6.0, value=1.0, step=1.0)
    bathrooms=st.sidebar.slider("No.of Bathrooms", min_value=1.0,max_value=5.0,value=1.0,step=1.0)
    dens=st.sidebar.slider("No.of Den",min_value=0.0,max_value=3.0,value=0.0,step=1.0)

    postal_code = st.sidebar.text_input("Enter your postal code:")
    btn_submit=None
    if postal_code:
        if is_valid_postal_code(postal_code):
            st.sidebar.success("The postal code is valid!",icon="✅")
            lat, lon = get_lan_long_from_postal_code(postal_code)
            if lat is not None and lon is not None:
                # st.success(f"Latitude: {lat}, Longitude: {lon}")
                lat,lon=select_on_map(lat,lon)
            else:
                st.sidebar.error("Could not find the location's longitue and latitude. Please selct the location on the map beside to get the longitue and latitude.")
                lat,lon=select_on_map(43.642567,-79.387054)
            st.subheader('The lat and log are {lat} & {lon}'.format(lat=lat,lon=lon), divider='rainbow')
            btn_submit=st.button("Find the good rental range for this property.")

        else:
            st.sidebar.error("Invalid postal code. Please enter a valid postal code (e.g., H3H 1J7).")
    if btn_submit:
        prop=ml.property_prediction()
        prop.set_bedrooms(bedrooms)
        prop.set_bathrooms(bathrooms)
        prop.set_den(dens)
        prop.set_postalcode(postal_code)
        prop.set_latitude(lat)
        prop.set_longitude(lon)
        prop.find_neighborhood()
        prop.build_df()
        st.write(prop._df)
        prop.encode_neighborhood()
        prop.scale_features()
        prop.find_rental_price()
        st.success(prop._rental_price)

if __name__=="__main__":
    main()