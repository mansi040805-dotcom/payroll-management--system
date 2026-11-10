"""
file_manager.py - JSON File Manager for Data Persistence

This module handles all file read/write operations using JSON format.
It keeps file operations separate from business logic and GUI code.

Classes:
    FileManager - Reads, writes, and manages JSON data files

OOP Concepts Demonstrated:
    - Encapsulation      : File operations encapsulated in one class
    - Exception Handling  : Handles file I/O errors gracefully
    - File Handling       : Reading and writing JSON files
"""

import json
import os


# ============================================================
# Custom Exception
# ============================================================

class FileError(Exception):
    """Raised when a file operation fails."""
    pass


# ============================================================
# FileManager Class
# ============================================================

class FileManager:
    """
    Manages reading and writing data to JSON files.

    All data persistence goes through this class. It creates the
    necessary directories and files automatically if they don't exist.

    This class is the ONLY place in the project that directly
    interacts with the file system. Other classes use FileManager
    to save and load their data.

    Demonstrates: Encapsulation, File Handling, Exception Handling
    """

    # --- File name constants (used throughout the project) ---
    EMPLOYEES_FILE = "employees.json"
    ATTENDANCE_FILE = "attendance.json"
    LEAVES_FILE = "leaves.json"
    PAYROLL_FILE = "payroll.json"
    PAYMENTS_FILE = "payments.json"
    COMPENSATION_FILE = "compensation.json"

    # --- Directory names ---
    DATA_DIR = "data"
    PAYSLIPS_DIR = "payslips"

    def __init__(self, base_path=""):
        """
        Initialize FileManager and create directories if needed.

        Args:
            base_path: Optional base directory path. If empty,
                       uses the current working directory.
        """
        if base_path:
            self._data_path = os.path.join(base_path, self.DATA_DIR)
            self._payslips_path = os.path.join(base_path, self.PAYSLIPS_DIR)
        else:
            self._data_path = self.DATA_DIR
            self._payslips_path = self.PAYSLIPS_DIR

        # Create directories if they don't exist
        self._ensure_directories()

    def _ensure_directories(self):
        """Create the data/ and payslips/ directories if they don't exist."""
        try:
            os.makedirs(self._data_path, exist_ok=True)
            os.makedirs(self._payslips_path, exist_ok=True)
        except OSError as error:
            raise FileError(f"Could not create directories: {error}")

    def _get_file_path(self, filename):
        """Get the full path for a data file."""
        return os.path.join(self._data_path, filename)

    # ---- Core Read/Write Operations ----

    def read_data(self, filename):
        """
        Read all records from a JSON file.

        Returns an empty list if the file doesn't exist or is empty.
        This ensures the application works even on first run.

        Args:
            filename: Name of the JSON file (e.g., "employees.json")

        Returns:
            list: List of record dictionaries.

        Raises:
            FileError: If there is an I/O error (not file-not-found).
        """
        file_path = self._get_file_path(filename)

        try:
            # Return empty list if file doesn't exist yet
            if not os.path.exists(file_path):
                return []

            with open(file_path, "r") as file:
                data = json.load(file)
                # Make sure we always return a list
                if isinstance(data, list):
                    return data
                else:
                    return []

        except json.JSONDecodeError:
            # File exists but has invalid/corrupt JSON - return empty
            return []
        except IOError as error:
            raise FileError(f"Error reading {filename}: {error}")

    def write_data(self, filename, data):
        """
        Write data to a JSON file (overwrites entire file).

        Args:
            filename: Name of the JSON file.
            data: List of record dictionaries to write.

        Raises:
            FileError: If there is an I/O error.
        """
        file_path = self._get_file_path(filename)

        try:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
        except IOError as error:
            raise FileError(f"Error writing to {filename}: {error}")

    # ---- Record Operations ----

    def add_record(self, filename, record):
        """
        Add a single record to a JSON file.

        Reads existing data, appends the new record, and writes back.

        Args:
            filename: JSON file name.
            record: Dictionary to add.
        """
        data = self.read_data(filename)
        data.append(record)
        self.write_data(filename, data)

    def update_record(self, filename, key_field, key_value, updated_record):
        """
        Update a record in a JSON file.

        Finds the record where key_field matches key_value and replaces it.

        Args:
            filename: JSON file name.
            key_field: Field name to search by (e.g., "employee_id").
            key_value: Value to match (e.g., "EMP001").
            updated_record: New dictionary to replace the old one.

        Returns:
            bool: True if record was found and updated, False otherwise.
        """
        data = self.read_data(filename)

        for i in range(len(data)):
            if data[i].get(key_field) == key_value:
                data[i] = updated_record
                self.write_data(filename, data)
                return True

        return False

    def delete_record(self, filename, key_field, key_value):
        """
        Delete a record from a JSON file.

        Removes the record where key_field matches key_value.

        Args:
            filename: JSON file name.
            key_field: Field name to search by.
            key_value: Value to match.

        Returns:
            bool: True if record was found and deleted, False otherwise.
        """
        data = self.read_data(filename)
        original_count = len(data)

        # Keep all records EXCEPT the one matching the key
        filtered_data = []
        for record in data:
            if record.get(key_field) != key_value:
                filtered_data.append(record)

        if len(filtered_data) < original_count:
            self.write_data(filename, filtered_data)
            return True

        return False

    def find_record(self, filename, key_field, key_value):
        """
        Find a single record by key.

        Returns:
            dict or None: The matching record, or None if not found.
        """
        data = self.read_data(filename)

        for record in data:
            if record.get(key_field) == key_value:
                return record

        return None

    def find_records(self, filename, key_field, key_value):
        """
        Find all records matching a key-value pair.

        Returns:
            list: List of matching record dictionaries.
        """
        data = self.read_data(filename)

        matching = []
        for record in data:
            if record.get(key_field) == key_value:
                matching.append(record)

        return matching

    # ---- Payslip File Operations ----

    def save_payslip(self, filename, content):
        """
        Save a payslip as a text file in the payslips/ directory.

        Args:
            filename: Name of the payslip file (e.g., "payslip_EMP001_10_2026.txt")
            content: Text content of the payslip.

        Returns:
            str: Full path of the saved file.
        """
        file_path = os.path.join(self._payslips_path, filename)

        try:
            with open(file_path, "w") as file:
                file.write(content)
            return file_path
        except IOError as error:
            raise FileError(f"Error saving payslip: {error}")

    def get_payslips_path(self):
        """Get the payslips directory path."""
        return self._payslips_path
