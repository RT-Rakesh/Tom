from builder import scrape_listings
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

    batch_size = 10  # Number of records to fetch in each batch
    output_file = 'centris_rental_properties.csv'

    # Scrape rental listings from Centris.ca
    rental_properties = scrape_listings(centris_rentals_url, centris_selectors, batch_size, output_file)

    if rental_properties:
        print(f"Scraped and saved rental properties to {output_file}.")
    else:
        print("No properties found.")

if __name__ == "__main__":
    main()
