import requests
from bs4 import BeautifulSoup
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.model import Property  # Import the Property class from model.py

# Function to load existing property URLs from the CSV file
def load_existing_property_urls(csv_filename):
    existing_urls = set()
    try:
        with open(csv_filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                if row:
                    existing_urls.add(row[0])
    except FileNotFoundError:
        pass
    return existing_urls

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
        property_details.NumberOfRooms = soup.select_one(selectors['rooms']).text.strip() if selectors.get('rooms') else "N/A"
        property_details.NumberOfBedrooms = soup.select_one(selectors['bedrooms']).text.strip() if selectors.get('bedrooms') else "N/A"
        property_details.NumberOfBathrooms = soup.select_one(selectors['bathrooms']).text.strip() if selectors.get('bathrooms') else "N/A"

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
        property_details.Occupancy = soup.select_one(selectors['occupancy']).text.strip() if selectors.get('occupancy') else "N/A"
        property_details.AdditionalFeatures = soup.select_one(selectors['features']).text.strip() if selectors.get('features') else "N/A"
        property_details.YearBuilt = soup.select_one(selectors['year_built']).text.strip() if selectors.get('year_built') else "N/A"
        property_details.ParkingTotal = soup.select_one(selectors['parking']).text.strip() if selectors.get('parking') else "N/A"
    except AttributeError as e:
        print(f"Error extracting details: {e}")
        return None

    return property_details

# Function to fetch a single page of listings
def fetch_page(url, selectors, page, base_url, csv_filename, existing_urls):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    # Debug: Print the page content to verify it's being fetched correctly
    print(f"Fetched page {page}:")
    print(response.text[:1000])  # Print the first 1000 characters of the page content

    # Find all rental listings (adjust the selector if needed)
    listings = soup.find_all('div', class_='property-thumbnail-item')

    if not listings:
        print(f"No listings found on page {page}.")
        return []

    properties = []
    for listing in listings:
        title_tag = listing.find('meta', itemprop='name')
        title = title_tag['content'].strip() if title_tag else "N/A"

        price_tag = listing.find('div', class_='price')
        price = price_tag.text.strip() if price_tag else "N/A"

        location_address_tag = listing.find('span', class_='address')
        location_address = location_address_tag.text.strip() if location_address_tag else "N/A"

        listing_url = base_url + listing.find('a', class_='property-thumbnail-summary-link')['href']

        # Check if the property already exists in the CSV
        if listing_url in existing_urls:
            continue

        # Extract details from the listing page
        property_details = extract_listing_details(listing_url, selectors)

        if property_details:
            property_details.Title = title
            property_details.Price = price
            property_details.Location = location_address
            properties.append((listing_url, property_details))

    return properties

# Function to scrape rental listings from a given URL with configurable parameters
def scrape_listings(url, selectors, batch_size, output_file):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    base_url = url.split('/en/')[0] if '/en/' in url else url.split('/fr/')[0]
    all_properties = []
    page = 1

    # Load existing property URLs from the CSV file
    existing_urls = load_existing_property_urls(output_file)

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        while True:
            for i in range(10):
                page_url = f'{base_url}/en/properties~for-rent?view=Thumbnail&uc=3&page={page + i}'
                print(f"Fetching page: {page + i}, URL: {page_url}")
                futures.append(executor.submit(fetch_page, page_url, selectors, page + i, base_url, output_file, existing_urls))

            page += 10

            for future in as_completed(futures):
                try:
                    result = future.result()
                    all_properties.extend(result)
                except Exception as e:
                    print(f"Error fetching page: {e}")

            if all_properties:
                save_to_csv(all_properties, output_file)
                all_properties.clear()

            if not futures or (result is not None and len(result) < batch_size):
                break

            futures = []
            time.sleep(1)  # Add a short delay to avoid hitting the server too frequently

    return all_properties

# Function to save properties to a CSV file
def save_to_csv(properties, filename):
    if not properties:
        print("No properties to save.")
        return

    keys = ['Link', 'NumberOfRooms', 'NumberOfBedrooms', 'NumberOfBathrooms', 'AreaType', 'AreaValue', 'Occupancy', 'AdditionalFeatures', 'YearBuilt', 'ParkingTotal', 'Title', 'Price', 'Location']

    with open(filename, 'a', newline='', encoding='utf-8') as output_file:  # 'a' mode to append to the file
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        if output_file.tell() == 0:  # Write header only if the file is empty
            dict_writer.writeheader()
        for listing_url, prop in properties:
            row = vars(prop)
            row['Link'] = listing_url
            dict_writer.writerow(row)
