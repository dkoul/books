# Streamlit Book Giveaway

## Overview
This is a Streamlit-based web application that allows parents to list book sets (Grades 1-12) for giveaway. Other users can browse the listings and claim available book sets.

## Features
- Parents can list book sets for giveaway by providing their name, phone number, and grade.
- Once listed, a book set cannot be removed but can be claimed by another user.
- Listings show whether book sets are available or claimed, with color-coded backgrounds.
- When a user claims a book set, they receive contact details of the person who listed it.
- The app stores data in a Google Spreadsheet for easy tracking and retrieval.

## Setup Instructions
### Prerequisites
- Python 3.8+
- Streamlit
- Google Cloud Service Account credentials

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/streamlit-book-giveaway.git
   cd streamlit-book-giveaway
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure Streamlit secrets:
   - Create a `.streamlit/secrets.toml` file.
   - Add the following content and update with your Google credentials:
     ```toml
     [gcp_service_account]
     type = "service_account"
     project_id = "your_project_id"
     private_key_id = "your_private_key_id"
     private_key = "your_private_key"
     client_email = "your_service_account_email"
     client_id = "your_client_id"
     auth_uri = "https://accounts.google.com/o/oauth2/auth"
     token_uri = "https://oauth2.googleapis.com/token"
     auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
     client_x509_cert_url = "your_client_x509_cert_url"
     ```
4. Run the app:
   ```sh
   streamlit run books.py
   ```

## Contribution Guide
We welcome contributions to improve the application! Follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```sh
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```sh
   git commit -m "Add new feature"
   ```
4. Push your branch:
   ```sh
   git push origin feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
Made with ❤️ by Aarav and Deepak Koul [The HDFC School, Pune]

