import requests
from bs4 import BeautifulSoup
from gspread import auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Config:
    """Configuration constants for the script."""

    SCOPES: tuple = (
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    )
    TOKEN_PATH: str = "token.pickle"
    CREDENTIALS_PATH: str = "creds.json"
    SPREADSHEET_NAME: str = "Test"
    TARGET_URL: str = (
        "https://www.motala.se/omsorg-och-hjalp/boenden-sarskilda/gruppboende-vid-funktionsnedsattning/torpavagen-gruppboende/"
    )


def scrape_website(url):
    """Scrape data from the given website and return a list of formatted strings."""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all <a> elements
    elements = soup.find_all("p")
    if not elements:
        print("No <p> elements found on the webpage.")
        return []

    # Extract and clean text
    raw_data = [element.get_text(strip=True) for element in elements]

    # Ensure spaces after specific keywords
    return [
        re.sub(
            r"(Adress:|Telefon:|E-post:)(\S)",
            r"\1 \2",
            text,
        )
        for text in raw_data
    ]


def authenticate_google_sheets():
    """Authenticate with Google Sheets API using OAuth 2.0 and return a gspread client."""
    creds = None

    if os.path.exists(Config.TOKEN_PATH):
        with open(Config.TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                Config.CREDENTIALS_PATH, Config.SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(Config.TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    return auth.authorize(creds)


def write_to_google_sheets(client, data):
    """Write unique data to a single column (Column A) in Google Sheets with added spaces."""
    if not data:
        print("No data to write.")
        return

    spreadsheet = client.open(Config.SPREADSHEET_NAME)
    worksheet = spreadsheet.sheet1  # Access the first sheet

    # Get existing values from column A
    existing_values = set(worksheet.col_values(1))  # Convert to set for faster lookup

    # Sort data before filtering out duplicates
    sorted_data = sorted(data)

    # Filter out duplicates while formatting it
    new_data = [
        [row.replace(".", ". ").replace(",", ", ").strip()]
        for row in sorted_data
        if row not in existing_values
    ]

    if not new_data:
        print("No new data to add. All entries are duplicates.")
        return

    # Append new data in a single operation for efficiency
    worksheet.append_rows(new_data)

    print(f"Added {len(new_data)} new rows to Google Sheets!")


def main():
    """Main function to scrape data and update Google Sheets."""
    print("Scraping data from:", Config.TARGET_URL)
    data = scrape_website(Config.TARGET_URL)

    if not data:
        print("No data scraped. Exiting.")
        return

    print("Authenticating with Google Sheets...")
    client = authenticate_google_sheets()

    print("Writing data to Google Sheets...")
    write_to_google_sheets(client, data)


if __name__ == "__main__":
    main()
