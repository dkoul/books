import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def connect_to_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    return client.open("Carpool")

def get_data(sheet):
    records = sheet.get_all_records()
    return pd.DataFrame(records)

def add_car(sheet, event_name, event_date, seats, owner, phone, make, start_from, time):
    time_str = time.strftime("%H:%M")  # Convert time object to string
    sheet.append_row([event_name, event_date, seats, owner, phone, make, start_from, time_str, seats])


def book_seat(listings_sheet, bookings_sheet, owner, name, phone):
    data = get_data(listings_sheet)  # Fetch car listings data
    matching_cars = data[data['Owner Name'] == owner]
    
    if matching_cars.empty:
        st.error("No car found for this owner.")
        return

    row_index = matching_cars.index[0] + 2  # Adjust for 1-based index in Google Sheets
    available_seats = int(listings_sheet.cell(row_index, 9).value)  # Column 9 = "Seats Left"

    if available_seats > 0:
        listings_sheet.update_cell(row_index, 9, available_seats - 1)  # Update seat count
        bookings_sheet.append_row([owner, name, phone])  # Log the booking
        st.success("Seat booked successfully!")
    else:
        st.error("No seats available!")


def main():
    st.title("Carpool Manager")
    sheet = connect_to_gsheet()
    events_sheet = sheet.worksheet("Events")
    listings_sheet = sheet.worksheet("Listings")
    bookings_sheet = sheet.worksheet("Bookings")

    # Load event data
    event_data = get_data(events_sheet)
    event_names = event_data['Event Name'].tolist()
    
    selected_event = st.sidebar.selectbox("Select Event", event_names)
    event_details = event_data[event_data['Event Name'] == selected_event].iloc[0]
    event_date = event_details['Event Date']
    
    tab1, tab2 = st.tabs(["Add Car", "View & Book"]) 

    with tab1:
        st.header("Add a Car to the Pool")
        st.write(f"Event: {selected_event} | Date: {event_date}")
        seats = st.number_input("Available Seats", min_value=1, step=1)
        owner = st.text_input("Owner Name")
        phone = st.text_input("Owner Phone Number")
        make = st.text_input("Car Make")
        start_from = st.text_input("Starting Location")
        time = st.time_input("Start Time")
        if st.button("Add Car"):
            add_car(listings_sheet, selected_event, event_date, seats, owner, phone, make, start_from, time)
            st.success("Car added successfully!")

    with tab2:
        st.header("Available Cars")
        data = get_data(listings_sheet)
        event_cars = data[data['Event Name'] == selected_event]
        st.dataframe(event_cars[['Owner Name', 'Car Make', 'Starting Location', 'Start Time', 'Seats Left']])

        selected_car = st.selectbox("Choose whose car to book a seat", event_cars['Owner Name'].unique())
        name = st.text_input("Your Name")
        phone = st.text_input("Your Phone Number")
        if st.button("Book Seat"):
            book_seat(listings_sheet, bookings_sheet, selected_car, name, phone)

if __name__ == "__main__":
    main()
