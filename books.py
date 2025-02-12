import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Authentication Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your_google_credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("BookGiveaway").sheet1

def add_giveaway(name, number, grade):
    sheet.append_row([name, number, grade, "Unclaimed"])

def get_listings():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def claim_book(index):
    sheet.update_cell(index + 2, 4, "Claimed")

# Streamlit UI
st.title("Used Bookset Giveaway Platform")

menu = st.sidebar.radio("Menu", ["Register Giveaway", "View Listings"])

if menu == "Register Giveaway":
    st.header("List Your Books for Giveaway")
    name = st.text_input("Your Name")
    number = st.text_input("Your Phone Number")
    grade = st.selectbox("Book Grade", list(range(1, 13)))
    if st.button("Submit Giveaway"):
        if name and number:
            add_giveaway(name, number, grade)
            st.success("Your book set has been listed for giveaway!")
        else:
            st.error("Please fill all fields.")

elif menu == "View Listings":
    st.header("Available Book Sets")
    listings = get_listings()
    grade_filter = st.selectbox("Filter by Grade", ["All"] + list(range(1, 13)))
    
    if grade_filter != "All":
        listings = listings[listings['Grade'] == grade_filter]
    
    for index, row in listings.iterrows():
        bg_color = "#ffcccc" if row['Status'] == "Claimed" else "#ccffcc"
        st.markdown(f'<div style="background-color: {bg_color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">' +
                    f'**Grade {row["Grade"]} bookset listed by {row["Name"]} - Status: {row["Status"]}**' +
                    '</div>', unsafe_allow_html=True)
        
        if row['Status'] == "Unclaimed" and st.button(f"Claim Bookset {index}"):
            claim_book(index)
            whatsapp_link = f"https://wa.me/{row['Phone']}"
            st.success(f"Congratulations! You have claimed the bookset. Contact {row['Name']} on [WhatsApp]({whatsapp_link})")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Made with ❤️ by Aarav and Deepak Koul [The HDFC School, Pune]</p>", unsafe_allow_html=True)
