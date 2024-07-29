import re
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
import folium as fl
# from folium import Element
import time
import pandas as pd
import streamlit as st
from Logger.Logger import App_Logger
from Logger.log_adapters import FileLogAdapter
from Logger.log_observers import ErrorLogObserver,InfoLogObserver
from app.obj_model import App

def is_valid_postal_code(postal_code):
    pattern = re.compile(r"^[A-Za-z]\d[A-Za-z] \d[A-Za-z]\d$")
    return bool(pattern.match(postal_code))

def get_lan_long_from_postal_code(postal_code):
  """
  This function takes a postal code as input and returns the latitude and longitude of the corresponding location in Canada using the Nominatim geocoder.
  """
  geolocator = Nominatim(user_agent="GetLoc")
  location = geolocator.geocode(postal_code, country_codes="CA")
  if location:
    logger.log_message(level="INFO", message=f"The lat and lon have been successfully retrived.\n")
    return location.latitude, location.longitude
  else:
    return None, None

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



info_file_adapter=FileLogAdapter(filename="app_log.txt")
error_file_adapter=FileLogAdapter(filename="error.txt")

logger = App_Logger()
logger.add_observer(ErrorLogObserver(adapter=error_file_adapter))
logger.add_observer(InfoLogObserver(adapter=info_file_adapter))



class app_builder:
    def __init__(self):
        self._bedrooms = 0
        self._bathrooms = 0
        self._den = 0
        self._latitude = None
        self._longitude = None
        self._postal_code = ""
        self._neighborhood = ""
        self._df = None
        self._rental_price = None
        self._btn_submit=None
    def _get_bedrooms(self):
        try:
            self._bedrooms = st.sidebar.slider("No.of Bed Rooms", min_value=1.0, max_value=6.0, value=1.0, step=1.0)
            logger.log_message(level="INFO",message=f"The request for bedroom has been made and the user has given {self._bedrooms} as the input.")
        except Exception as e:
            logger.log_message(level="ERROR",message=f"There is an error {e} in the getting bedrooms\n")
        return self
    def _get_bathrooms(self):
        try:
            self._bathrooms = st.sidebar.slider("No.of Bathrooms", min_value=1.0,max_value=5.0,value=1.0,step=1.0)
            logger.log_message(level="INFO",
                               message=f"The request for bathrooms has been made and the user has given {self._bathrooms} as the input.")
        except Exception as e:
            logger.log_message(level="ERROR", message=f"There is an error {e} in the getting bathrooms\n")
        return self
    def _get_den(self):
        try:
            self._den = st.sidebar.slider("No.of Den",min_value=0.0,max_value=3.0,value=0.0,step=1.0)
            logger.log_message(level="INFO",
                               message=f"The request for dens has been made and the user has given {self._den} as the input.")
        except Exception as e:
            logger.log_message(level="ERROR", message=f"There is an error {e} in the getting dens.\n")
        return self

    def _get_postal_code(self):
        try:
            self._postal_code = st.sidebar.text_input("Enter your postal code:")
            logger.log_message(level="INFO",
                               message=f"The request for postal code has been made and the user has given {self._postal_code} as the input.")
            if self._postal_code:
                if  is_valid_postal_code(self._postal_code):
                    st.sidebar.success("The postal code is valid!", icon="✅")
                    logger.log_message(level="INFO", message=f"The postal code received is validated and accepted")
                else:
                    st.sidebar.error("Invalid postal code. Please enter a valid postal code (e.g., H3H 1J7).")
                    logger.log_message(level="ERROR",
                                       message=f"The postal code received is not validated and has to be corrected.")
        except Exception as e:
            logger.log_message(level="ERROR", message=f"There is an error '{e}' in the getting postal code.\n")
        return self


    def _get_lat_lon(self):
        try:
            if self._postal_code:
                lat, lon = get_lan_long_from_postal_code(self._postal_code)
                if lat is not None and lon is not None:
                    # st.success(f"Latitude: {lat}, Longitude: {lon}")
                    lat, lon = select_on_map(lat, lon)
                else:
                    st.sidebar.error(
                        "Could not find the location's longitude and latitude. Please select the location on the map beside to get the longitude and latitude.")
                    lat, lon = select_on_map(43.642567, -79.387054)
                st.write('The selected lat and log are {lat} & {lon}'.format(lat=lat, lon=lon), divider='rainbow')
                self._latitude=lat
                self._longitude=lon
                logger.log_message(level="INFO", message=f"The lat and lon has been set and validated.")
                self._btn_submit = st.button("Find the good rental range for this property.")
        except Exception as e:
            logger.log_message(level="ERROR", message=f"There is an error '{e}' in the getting lat and lon.\n")
        return self

    def _build(self):
        return App(self._bedrooms,
                    self._bathrooms,
                    self._den,
                    self._latitude,
                    self._longitude,
                    self._postal_code,
                    self._btn_submit,
                    )






