import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selNdriv import calc_wrkHrs, openEsign, gotoTimeSheetEsign, entryTimeSheetEsign
def main():
    out_string4 = ""
    st.set_page_config(page_title="This is timesheet application")
    st.title("Timesheet application")
    r1col1, r1col2, r1col3 = st.columns(3)
    r2col1, r2col2 = st.columns([0.8, 0.2])
    r3col1, r3col2, r3col3, r3col4 = st.columns(4)

    with r1col1:
        l_name = st.text_input("Last Name", placeholder='Doe')
    with r1col2:
        f_name = st.text_input("First Name", placeholder='John')
    with r1col3:
        posn = st.text_input("Position", placeholder='1064')
    with r2col1:
        supEmail = st.text_input("Supervisor Email", placeholder='<EMAIL>@ccsf.edu')
    with r3col1:
        arrival = st.text_input("Arrived", placeholder='8:00')
    with r3col2:
        lunch_out = st.text_input("Out for Lunch", placeholder='12:00')
    with r3col3:
        lunch_in = st.text_input("In for Lunch", placeholder='13:00')
    with r3col4:
        depart = st.text_input("Leaving", placeholder='16:30')

    if st.button("Process"):
        workHrs, rwwHrs = calc_wrkHrs(arrival, lunch_out, lunch_in, depart)
        out_string = f"{posn} submission for {l_name}, {f_name}. <br> Send to {supEmail}."
        out_string2 = f"Arrive: {arrival} Lunch Out: {lunch_out}<br> Lunch In: {lunch_in} Depart: {depart}"
        out_string3 = f"Total Hours: {workHrs} Rww: {rwwHrs} "
        if rwwHrs < 0:
            out_string4 = "Hours worked exceeds 8 hrs please revise and submit."
        else:
            out_string4 = "Thank you for your submission"

            #if st.button("Submit"):
            l_url = 'https://citycollegesf.na1.echosign.com/'
            gChromeOptions = webdriver.ChromeOptions()
            gChromeOptions.add_argument("window-size=1920x1480")
            gChromeOptions.add_argument("disable-dev-shm-usage")

            chrome_options = Options()
            chrome_options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(options=gChromeOptions, service=Service(ChromeDriverManager().install()))
            openEsign(driver, l_url)
            gotoTimeSheetEsign(driver, supEmail)
            entryTimeSheetEsign(driver, f_name, l_name, posn, arrival, lunch_out, lunch_in, depart)

            driver.save_screenshot("my_screenshot.png")

        st.write(out_string4)
        st.write(out_string, unsafe_allow_html=True)
        st.write(out_string2, unsafe_allow_html=True)
        st.write(out_string3)

if __name__ == '__main__':
    main()