class Property:
    def __init__(self):
        self.Title = ""
        self.Price = ""
        self.Location = ""
        self.NumberOfRooms = ""
        self.NumberOfBedrooms = ""
        self.NumberOfBathrooms = ""
        self.AreaType = ""
        self.AreaValue = ""
        self.Occupancy = ""
        self.AdditionalFeatures = ""
        self.YearBuilt = ""
        self.ParkingTotal = ""

    def __str__(self):
        return (f'Title: {self.Title}\n'
                f'Price: {self.Price}\n'
                f'Location: {self.Location}\n'
                f'Number of Rooms: {self.NumberOfRooms}\n'
                f'Number of Bedrooms: {self.NumberOfBedrooms}\n'
                f'Number of Bathrooms: {self.NumberOfBathrooms}\n'
                f'Area Type: {self.AreaType}\n'
                f'Area Value: {self.AreaValue}\n'
                f'Occupancy: {self.Occupancy}\n'
                f'Additional Features: {self.AdditionalFeatures}\n'
                f'Year Built: {self.YearBuilt}\n'
                f'Parking Total: {self.ParkingTotal}\n')
