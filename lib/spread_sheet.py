import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
DEFAULT_SHEET_INDEX = 0


class SpreadSheet(object):
    def __init__(self, key_path, spread_sheet_id):
        """SpreadSheet Client Object.
        
        Args:
            key_path (str): The file path to the JSON key file containing credentials for accessing Google Sheets API.
            Spread_sheet_id: The ID of the Google spreadsheet to access.
        """
        self._key_path = key_path
        self._spread_sheet_id = spread_sheet_id

    def _get_client(self):
        """Google spreadsheet Service Object.

        Assuming that it will be used in loop processing,
        create a service instance every time to avoid the access token expiration.

        Returns:
            A Resource object with Google spreadsheet service.
        """
        credentials = Credentials.from_service_account_file(
            self._key_path, scopes=SCOPE
        )
        self.sheet_client = gspread.authorize(credentials).open_by_key(self._spread_sheet_id)
        return gspread.authorize(credentials).open_by_key(self._spread_sheet_id)

    def get_label_value(self, label, index=DEFAULT_SHEET_INDEX):
        """Get Google spreadsheet label value.

        Args:
            label (str): Google spreadsheet label. (ex) "A1"
            index (int): Google spreadsheet tab index. (ex) 0

        Returns:
            Google spreadsheet label value.
        """
        return self._get_client().get_worksheet(index).acell(label).value

    def set_label_value(self, label, value, index=DEFAULT_SHEET_INDEX):
        """Set Google spreadsheet label value.

        Args:
            label (str): Google spreadsheet label. (ex) "A1"
            value: Input value
            index (int): Google spreadsheet tab index. (ex) 0
        """
        self._get_client().get_worksheet(index).update_acell(label, value)

    def col_values(self, col, index=DEFAULT_SHEET_INDEX):
        """Get Google spreadsheet all column values.

        Args:
            col (int): Google spreadsheet column. (ex) 1
            index: Google spreadsheet tab index. (ex) 0

        Returns:
            Google spreadsheet all column values.
        """
        try:
            return self._get_client().get_worksheet(index).col_values(col)
        except Exception as e:
            print(e)
            pass

    def get_all_values(self, index=DEFAULT_SHEET_INDEX):
        """Get Google spreadsheet all sheet values.

        Args:
            index (int): Google spreadsheet tab index. (ex) 0

        Returns:
            Google spreadsheet all sheet values.
        """
        try:
            return self._get_client().get_worksheet(index).get_all_values()
        except Exception as e:
            print(e)
            pass

    def append_row(self, values, index=DEFAULT_SHEET_INDEX):
        """Append Google spreadsheet row at the end.

        Args:
            values (list): Input values list
            index (int): Google spreadsheet tab index. (ex) 0
        """
        try:
            self._get_client().get_worksheet(index).append_row(values)
        except Exception as e:
            print(e)
            pass
