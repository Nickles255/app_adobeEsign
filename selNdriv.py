from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import time
import datetime as dt

def calc_wrkHrs(arrive, lunch_out, lunch_in, leave):
    """calculate work and reduced work week hrs based on
       8 hour work day
       all input formats are %H:%M
    :param arrive: time arrived at work
    :param lunch_out: time out for lunch
    :param lunch_in: time in from lunch
    :param leave: time leave from work
    :return: wrk_hrs: decimal hours of worked hours
    :return: rww_hrs: decimal hours of reduced work week
    """

    l_hrFormat = "%H:%M"
    t_arr =  dt.datetime.strptime(arrive, l_hrFormat)
    t_olun = dt.datetime.strptime(lunch_out, l_hrFormat)
    t_ilun = dt.datetime.strptime(lunch_in, l_hrFormat)
    t_leav = dt.datetime.strptime(leave, l_hrFormat)
    l_totHrs = ((t_olun - t_arr) + (t_leav - t_ilun))

    wrk_hrs = l_totHrs.seconds//3600 + l_totHrs.seconds//60%60/60
    rww_hrs = 8.0 - wrk_hrs

    return wrk_hrs, rww_hrs
def openEsign(in_driver, in_url='https://citycollegesf.na1.echosign.com/'):
    """open adobe esign site login through MFA
    :param in_driver: streamlit webdriver
    :param in_url: adobe esign URL
    """
    in_driver.get(in_url)
    l_pause = True
    while l_pause == True:
        try:
            l_class = "spectrum-Button--secondary"
            btnLibraryStart = in_driver.find_element(By.CLASS_NAME, l_class)
            ActionChains(in_driver).double_click(btnLibraryStart).perform()
            l_pause = False
        except:
            l_pause = True
            time.sleep(2)  ##in seconds


def gotoTimeSheetEsign(in_driver, in_supervisorEmail):
    """follow esign links to get to timesheet workflow
    :param in_driver: streamlit webdriver
    :param in_supervisorEmail: supervisor email to submit time sheet
    """
    # initialize time sheet workflow
    l_pause = True
    while l_pause == True:
        try:
            l_class = "libraryWorkflows"
            workFlowLink = in_driver.find_element(By.CLASS_NAME, l_class)
            ActionChains(in_driver).click(workFlowLink).perform()

            l_class = 'single-select-row'
            workFlowMenu = in_driver.find_elements(By.CLASS_NAME, l_class)
            timeSheetLink = workFlowMenu[5]
            ActionChains(in_driver).double_click(timeSheetLink).perform()
            l_pause = False
        except:
            l_pause = True
            time.sleep(1)  ##in seconds

    time.sleep(2)
    l_class = "recipient-email-input"
    tbRecpEmail = in_driver.find_elements(By.CLASS_NAME, l_class)
    tbRecpEmail[1].send_keys(in_supervisorEmail)

    l_class = "send-btn"
    btnSubmit = in_driver.find_element(By.CLASS_NAME, l_class)
    ActionChains(in_driver).double_click(btnSubmit).perform()

def entryTimeSheetEsign(in_driver, in_fname, in_lname, in_posnClass, in_arrive, in_outLunch, in_inLunch, in_leave, in_submit='N'):
    """fill out time sheet as specified by ITS
    :param in_driver: streamlit webdriver
    :param in_fname: first name on time sheet
    :param in_lname: last name on time sheet
    :param in_posnClass: position (i.e. 1063, 1544)
    :param in_arrive: time arrived at work
    :param in_outLunch: time out for lunch
    :param in_inLunch: time in from lunch
    :param in_leave: time leave from work
    :param in_submit: defaults to 'N' but flip to 'Y' to auto submit
    """
    l_workHrs, l_rwwHrs = calc_wrkHrs(in_arrive, in_outLunch,
                                      in_inLunch, in_leave)

    # adjust to beginning saturday of 2 weeks
    # day of week is 0-monday to 6-sunday
    l_day = dt.date.today()
    l_diff = 4 - l_day.weekday()  # 4 is friday
    l_startDate = l_day + dt.timedelta(days=(l_diff - 13))
    l_startDate = l_startDate.strftime("%m/%d/%Y")

    l_pause = True
    while l_pause == True:
        try:
            l_class = "text_field_input"
            tbInputs = in_driver.find_elements(By.CLASS_NAME, l_class)

            tbLname = tbInputs[0]  ##last name
            tbLname.send_keys(in_lname)

            l_pause = False
        except:
            l_pause = True
            time.sleep(1)  ##in seconds

    tbFname = tbInputs[1]  ##first name
    tbFname.send_keys(in_fname)

    tbClass = tbInputs[2]  ##class number
    tbClass.send_keys(in_posnClass)

    # %% populate form times
    tbClass = tbInputs[3]  # initial date
    keys = tbClass.send_keys(l_startDate)

    # Each row is 8
    l_entryPoints = list(range(20, 53, 8)) + list(range(76, 109, 8))
    for i in l_entryPoints:
        tbArrive = tbInputs[i]
        tbLunchOut = tbInputs[i + 1]
        tbLunchIn = tbInputs[i + 2]
        tbDepart = tbInputs[i + 3]
        tbTotalHr = tbInputs[i + 4]
        tbRWW = tbInputs[i + 5]

        tbArrive.send_keys(in_arrive)
        tbLunchOut.send_keys(in_outLunch)
        tbLunchIn.send_keys(in_inLunch)
        tbDepart.send_keys(in_leave)
        tbTotalHr.send_keys(l_workHrs)
        tbRWW.send_keys(l_rwwHrs)

    l_class = 'faux_field'
    signField = in_driver.find_element(By.CLASS_NAME, l_class)
    ActionChains(in_driver).click(signField).perform()
    # wait for form to appear
    l_pause = True
    while l_pause == True:
        try:
            l_class = 'apply'
            btnApply = in_driver.find_element(By.CLASS_NAME, l_class)
            ActionChains(in_driver).click(btnApply).perform()
            l_pause = False
        except:
            l_pause = True
            time.sleep(2)  ##in seconds

    l_pause = True
    while l_pause == True:
        try:
            l_class = 'click-to-esign'
            btnEsign = in_driver.find_element(By.CLASS_NAME, l_class)
            if in_submit == 'Y':
                ActionChains(in_driver).double_click(btnEsign).perform()
            l_pause = False
        except:
            l_pause = True
            time.sleep(2)  ##in seconds
