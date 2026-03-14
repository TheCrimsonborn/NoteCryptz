# NoteCryptz

High-security, fully-encrypted notepad application built with Python, PySide6, and the `cryptography` library.

## Features
- Securely encrypts notes using AES-256-GCM authenticated encryption.
- Derives encryption keys using PBKDF2 (SHA-256) with securely generated random salts and IVs.
- Clean and modern Qt-based interface.

## Prerequisites

To run NoteCryptz, you must have the following installed:
1. **Python 3.8+**
2. **pip** (usually included with Python)

## Installation Instructions

1. Open a terminal (PowerShell or Command Prompt).
2. Navigate to the `NoteCryptz` project directory:
   ```cmd
   cd path\to\NoteCryptz
   ```
3. Install the required Python dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

## Running the Application

Once dependencies are installed, you can start the application by running:
```cmd
python main.py
```

## Usage
- Click **File > Save As...** to save a new secure note. You will be prompted to create a password.
- Click **File > Open...** to open an existing `.ncz` file. You will be prompted to enter the password to decrypt it.
- **Security -> Set Password...**: Sets or changes the password kept in memory for the current session.
