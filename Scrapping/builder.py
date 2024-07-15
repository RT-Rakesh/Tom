# builder.py

import requests
from bs4 import BeautifulSoup
import csv
import time
from src.output import Property  # Import the Property class from output.py


# Function to extract details from a single listing page
def extract_listing_details(listing_url, selectors):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(listing_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed for {listing_url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Create an instance of Property to store details
    property_details = Property()

    # Extract specific details using CSS selectors
    try:
        property_details.Title = soup.select_one(selectors['title']).text.strip() if selectors.get('title') else "N/A"
        property_details.NumberOfRooms = soup.select_one(selectors['rooms']).text.strip() if selectors.get(
            'rooms') else "N/A"
        property_details.NumberOfBedrooms = soup.select_one(selectors['bedrooms']).text.strip() if selectors.get(
            'bedrooms') else "N/A"
        property_details.NumberOfBathrooms = soup.select_one(selectors['bathrooms']).text.strip() if selectors.get(
            'bathrooms') else "N/A"

        # Check for different area types
        area_types = ['Net area', 'Gross area', 'Lot area']
        area_found = False
        for area_type in area_types:
            area_value = soup.select_one(f'div:contains("{area_type}") + div')
            if area_value:
                property_details.AreaType = area_type
                property_details.AreaValue = area_value.text.strip()
                area_found = True
                break

        if not area_found:
            property_details.AreaType = "N/A"
            property_details.AreaValue = "N/A"

        # Find other details if available
        property_details.Occupancy = soup.select_one(selectors['occupancy']).text.strip() if selectors.get(
            'occupancy') else "N/A"
        property_details.AdditionalFeatures = soup.select_one(selectors['features']).text.strip() if selectors.get(
            'features') else "N/A"
        property_details.YearBuilt = soup.select_one(selectors['year_built']).text.strip() if selectors.get(
            'year_built') else "N/A"
        property_details.ParkingTotal = soup.select_one(selectors['parking']).text.strip() if selectors.get(
            'parking') else "N/A"
    except AttributeError as e:
        print(f"Error extracting details: {e}")
        return None

    # Print the extracted details for debugging
    print(f"Details extracted from {listing_url}: {property_details}")
    return property_details


# Function to scrape rental listings from a given URL with configurable parameters
def scrape_listings(url, max_records, selectors):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    base_url = url.split('/en/')[0] if '/en/' in url else url.split('/fr/')[0]
    all_properties = []
    page = 1

    while len(all_properties) < max_records:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            break

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all rental listings (adjust the selector if needed)
        listings = soup.find_all('div', class_='property-thumbnail-item')

        if not listings:
            print("No listings found.")
            break

        for listing in listings:
            title_tag = listing.find('meta', itemprop='name')
            title = title_tag['content'].strip() if title_tag else "N/A"

            price_tag = listing.find('div', class_='price')
            price = price_tag.text.strip() if price_tag else "N/A"

            location_address_tag = listing.find('span', class_='address')
            location_address = location_address_tag.text.strip() if location_address_tag else "N/A"

            listing_url = base_url + listing.find('a', class_='property-thumbnail-summary-link')['href']

            # Extract details from the listing page
            property_details = extract_listing_details(listing_url, selectors)

            if property_details:
                property_details.Title = title
                property_details.Price = price
                property_details.Location = location_address
                all_properties.append(property_details)

            if len(all_properties) >= max_records:
                break

            time.sleep(1)  # Add a delay to avoid hitting the server too frequently

        # Move to the next page if not enough properties scraped yet
        page += 1
        url = f'{base_url}/en/properties~for-rent?view=Thumbnail&uc=3&page={page}'

    return all_properties[:max_records]  # Return up to max_records properties


# Function to save properties to a CSV file
def save_to_csv(properties, filename):
    keys = vars(properties[0]).keys()  # Get attribute names of the first property
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        for prop in properties:
            dict_writer.writerow(vars(prop))
