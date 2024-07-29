# final_project_uml

**###BUILDER.PY** 
Contains the main scraping logic, including functions to load existing URLs, extract property details, fetch pages of listings, scrape listings in batches, and save properties to a CSV file.

**import**
requests: Used for making HTTP requests to web pages.
BeautifulSoup: Used for parsing HTML content.
csv: Used for reading from and writing to CSV files.
time: Used for adding delays to avoid server overload.
ThreadPoolExecutor, as_completed: Used for concurrent execution of web scraping tasks.
Property: Custom class defined in model.py to store property details.

**Function: load_existing_property_urls :** This function reads a CSV file and loads the URLs of properties that have already been scraped. This helps avoid duplicating entries in the CSV file
Purpose: Load URLs of properties already present in the CSV file to avoid duplicates.
Parameters: csv_filename - the name of the CSV file.
Returns: A set of existing URLs.

**Function: extract_listing_details**
Purpose: This function fetches the HTML content of a property listing page and extracts specific details using provided CSS selectors.
Parameters: listing_url - URL of the property listing, selectors - dictionary of CSS selectors for extracting details.
Returns: An instance of Property populated with details or None if extraction fails.

**Function: fetch_page**
Purpose: Fetch a single page of property listings and extract details. This function fetches a page of property listings, extracts basic information from each listing, and uses extract_listing_details to get detailed information.
Parameters: url - URL of the page to fetch, selectors - dictionary of CSS selectors, page - page number, base_url - base URL of the website, csv_filename - name of the CSV file, existing_urls - set of URLs already in the CSV.
Returns: A list of properties extracted from the page.

**Function: scrape_listings**
Purpose: Scrape multiple pages of rental listings and save them in batches to a CSV file.
Parameters: url - base URL for rental listings, selectors - dictionary of CSS selectors, batch_size - number of records to fetch per batch, output_file - name of the CSV file.
Returns: A list of all properties scraped.

**Function: save_to_csv**
Purpose: Save a list of properties to a CSV file.
Parameters: properties - list of properties to save, filename - name of the CSV file.
Returns: None.

**###MAIN.PY** 
This file initializes the scraping process with specific configurations and parameters.

**###MODEL.PY**
Define a class to store property details with attributes and a method to return a string representation of the property.

