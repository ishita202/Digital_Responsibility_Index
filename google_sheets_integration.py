"""
Google Sheets Integration for Digital Awareness Platform
Connects to Google Sheets to fetch and analyze survey data
"""

import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os
import json

class GoogleSheetsIntegration:
    def __init__(self, credentials_path=None, sheet_url=None):
        """
        Initialize Google Sheets integration
        
        Args:
            credentials_path: Path to Google service account credentials JSON file
            sheet_url: URL of the Google Sheet
        """
        self.sheet_url = sheet_url or 'https://docs.google.com/spreadsheets/d/1ZoZ7ZQXVLnk5JokphSQK0tqIT9IshB2NCg9_UCiAw6s/edit?gid=1620608954#gid=1620608954'
        self.credentials_path = credentials_path
        self.gc = None
        self.spreadsheet = None
        
    def authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            if self.credentials_path and os.path.exists(self.credentials_path):
                # Use service account credentials
                scope = ['https://www.googleapis.com/auth/spreadsheets.readonly',
                        'https://www.googleapis.com/auth/drive.readonly']
                creds = Credentials.from_service_account_file(self.credentials_path, scopes=scope)
                self.gc = gspread.authorize(creds)
                print("Authenticated using service account credentials")
            else:
                # For Colab or local development, use default credentials
                # This requires manual authentication
                print("Note: Service account credentials not found.")
                print("For local use, you may need to set up OAuth2 or use service account.")
                print("For Colab, use: from google.colab import auth; auth.authenticate_user()")
                return False
            return True
        except Exception as e:
            print(f"Authentication error: {e}")
            return False
    
    def connect_to_sheet(self):
        """Connect to the Google Sheet"""
        if not self.gc:
            if not self.authenticate():
                return False
        
        try:
            self.spreadsheet = self.gc.open_by_url(self.sheet_url)
            print(f"Connected to sheet: {self.spreadsheet.title}")
            return True
        except Exception as e:
            print(f"Error connecting to sheet: {e}")
            print("Make sure the sheet is shared with the service account email")
            return False
    
    def get_worksheet_data(self, worksheet_index=0):
        """Get data from a specific worksheet"""
        if not self.spreadsheet:
            if not self.connect_to_sheet():
                return None
        
        try:
            worksheet = self.spreadsheet.get_worksheet(worksheet_index)
            data = worksheet.get_all_values()
            
            if not data:
                return None
            
            # First row as headers
            headers = data[0]
            rows = data[1:]
            
            # Create DataFrame
            df = pd.DataFrame(rows, columns=headers)
            
            print(f"Loaded {len(df)} rows from worksheet: {worksheet.title}")
            return df
        except Exception as e:
            print(f"Error getting worksheet data: {e}")
            return None
    
    def refresh_data(self, save_path='survey_data_backup.csv'):
        """Refresh data from Google Sheets and save locally"""
        df = self.get_worksheet_data()
        
        if df is not None:
            # Save to CSV
            df.to_csv(save_path, index=False)
            print(f"Data saved to {save_path}")
            return df
        else:
            print("Failed to fetch data from Google Sheets")
            return None
    
    def get_latest_responses(self, last_count=None):
        """Get the latest survey responses"""
        df = self.get_worksheet_data()
        
        if df is None:
            return None
        
        # Sort by timestamp if available
        timestamp_cols = [col for col in df.columns if 'timestamp' in col.lower()]
        if timestamp_cols:
            df[timestamp_cols[0]] = pd.to_datetime(df[timestamp_cols[0]], errors='coerce')
            df = df.sort_values(by=timestamp_cols[0], ascending=False)
        
        if last_count:
            df = df.head(last_count)
        
        return df

def setup_google_sheets():
    """
    Setup instructions for Google Sheets integration
    
    To use this integration:
    1. Go to Google Cloud Console (https://console.cloud.google.com/)
    2. Create a new project or select existing one
    3. Enable Google Sheets API and Google Drive API
    4. Create a Service Account
    5. Download the credentials JSON file
    6. Share your Google Sheet with the service account email
    7. Update the credentials_path in the code
    """
    print("""
    Google Sheets Integration Setup:
    
    1. Create a Google Cloud Project
    2. Enable Google Sheets API and Google Drive API
    3. Create a Service Account and download credentials JSON
    4. Share your Google Sheet with the service account email
    5. Update credentials_path in your code
    
    For Colab users, you can use:
    from google.colab import auth
    auth.authenticate_user()
    creds, _ = default()
    gc = gspread.authorize(creds)
    """)

if __name__ == '__main__':
    # Example usage
    print("Google Sheets Integration Test")
    print("=" * 50)
    
    # Initialize (without credentials for now)
    gs = GoogleSheetsIntegration()
    
    # Show setup instructions
    setup_google_sheets()
    
    # Note: Actual connection requires proper authentication
    # Uncomment below after setting up credentials:
    # gs.authenticate()
    # df = gs.refresh_data()
    # print(df.head())

