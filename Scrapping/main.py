# main.py

from src.builder import scrape_listings, save_to_csv


def main():
    # Example usage for Centris.ca
    centris_url = 'https://www.centris.ca'
    centris_rentals_url = f'{centris_url}/en/properties~for-rent?view=Thumbnail&uc=3'

    # Selectors for Centris.ca (adjust as per the website structure)
    centris_selectors = {
        'title': 'div.piece',
        'rooms': 'div.piece',
        'bedrooms': 'div.cac',
        'bathrooms': 'div.sdb',
        'occupancy': 'div:contains("Occupancy") + div',
        'features': 'div:contains("Additional features") + div',
        'year_built': 'div:contains("Year built") + div',
        'parking': 'div:contains("Parking (total)") + div'
    }

    max_records = 10  # Maximum records to scrape

    # Scrape rental listings from Centris.ca
    rental_properties = scrape_listings(centris_rentals_url, max_records, centris_selectors)

    if rental_properties:
        filename = 'centris_rental_properties.csv'
        save_to_csv(rental_properties, filename)
        print(f"Saved {len(rental_properties)} properties to {filename}.")
    else:
        print("No properties found.")


if __name__ == "__main__":
    main()
