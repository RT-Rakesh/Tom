class Property:
    def __init__(self, bedrooms, bathrooms,den,latitude,longitude, postalcode, rental_price):
        self._bedrooms = bedrooms
        self._bathrooms = bathrooms
        self._den = den
        self._latitude = latitude
        self._longitude = longitude
        self._postalcode = postalcode
        self._rental_price = rental_price

    def __str__(self):
        return(f"{self._bedrooms} No.of bedrooms\n"
               f"{self._bathrooms} No.of bathrooms\n"
               f"{self._den} No.of den\n"
               f"{self._latitude} No.of latitude\n"
               f"{self._longitude} No.of longitude\n"
               f"{self._postalcode} Postal code of property\n"
               f"{self._rental_price} Rental price of property")
