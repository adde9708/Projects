import contextlib
import os
import pickle
import re
from dataclasses import dataclass
from typing import ClassVar
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from gspread import auth


@dataclass
class Constants:
    EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    INVALID_EMAIL_REGEX = r"sentry|wixpress|ingest|report|error|test|example"

    PHONE_REGEX = r"(\+?\d[\d\s().-]{7,}\d)"
    HEADERS: ClassVar[dict[str, str]] = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
    }

    SCOPES: tuple = (
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    )
    TOKEN_PATH: str = "token.pickle"
    CREDENTIALS_PATH: str = "creds.json"
    SPREADSHEET_NAME: str = "Test"
    SHEET_HEADERS = (
        "Company Name",
        "Website",
        "Contact Email",
        "Phone Number",
        "Contact Page URL",
        "Contact Type",
        "Notes",
        "Source",
    )


def authenticate_google_sheets():
    """Authenticate with Google Sheets API using OAuth 2.0 and return a gspread client."""
    creds = None

    if os.path.exists(Constants.TOKEN_PATH):
        with open(Constants.TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                Constants.CREDENTIALS_PATH, Constants.SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(Constants.TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    return auth.authorize(creds)


def normalize_url(url):

    if not isinstance(url, str):
        return ""

    parsed = urlparse(url.strip().lower())

    domain = parsed.netloc.replace("www.", "")

    return domain.rstrip("/")


def get_page(url):
    with contextlib.suppress(requests.RequestException):
        r = requests.get(url, headers=Constants.HEADERS, timeout=10)
        if r.status_code == 200:
            return r.text

    return ""


def extract_emails(text):

    found_emails = re.findall(Constants.EMAIL_REGEX, text)
    valid_emails = []

    for email in found_emails:

        email_lower = email.lower()

        if re.search(Constants.INVALID_EMAIL_REGEX, email_lower):
            continue

        valid_emails.append(email)

    return list(set(valid_emails))


def extract_phones(text):
    return list(set(re.findall(Constants.PHONE_REGEX, text)))


def find_contact_page(soup, base_url):
    for link in soup.find_all("a", href=True):
        href = link["href"].lower()
        if "contact" in href or "about" in href:
            return urljoin(base_url, link["href"])
    return ""


def scrape_company(name, website):
    print(f"Scraping {name}")
    html = get_page(website)

    if not html:
        return {
            "Company Name": name,
            "Website": website,
            "Contact Email": "",
            "Phone Number": "",
            "Contact Page URL": "",
            "Contact Type": "None",
            "Notes": "Website unreachable",
            "Source": "Website",
        }

    soup = BeautifulSoup(html, "html.parser")

    emails = extract_emails(html)
    phones = extract_phones(html)
    contact_page = find_contact_page(soup, website)

    # Try contact page if no email found
    if not emails and contact_page:
        contact_html = get_page(contact_page)
        emails = extract_emails(contact_html)
        phones = list(set(phones + extract_phones(contact_html)))

    contact_type = "Email" if emails else ("Form" if contact_page else "None")

    return {
        "Company Name": name,
        "Website": website,
        "Contact Email": emails[0] if emails else "",
        "Phone Number": phones[0] if phones else "",
        "Contact Page URL": contact_page,
        "Contact Type": contact_type,
        "Notes": "",
        "Source": "Website",
    }


def main():
    companies = pd.read_csv("companies.csv")
    companies["Normalized"] = companies["Website"].apply(normalize_url)
    companies = companies.drop_duplicates(subset="Normalized")
    companies = companies.drop(columns=["Normalized"])
    client = authenticate_google_sheets()
    worksheet = client.open(Constants.SPREADSHEET_NAME).sheet1
    existing_rows = worksheet.get_all_values()
    existing_websites = {
        normalize_url(row[1]) for row in existing_rows[1:] if len(row) > 1
    }

    if not existing_rows or existing_rows[0] != Constants.SHEET_HEADERS:
        worksheet.clear()
        worksheet.append_row(Constants.SHEET_HEADERS)
        existing_rows = []

    for _, row in companies.iterrows():
        website = normalize_url(row["Website"])

        if website in existing_websites:
            continue

        data = scrape_company(row["Company Name"], row["Website"])

        worksheet.append_row(
            [
                data["Company Name"],
                data["Website"],
                data["Contact Email"],
                data["Phone Number"],
                data["Contact Page URL"],
                data["Contact Type"],
                data["Notes"],
                data["Source"],
            ]
        )

        existing_websites.add(website)

    print("Done. Data pushed to Google Sheets.")


if __name__ == "__main__":
    main()
