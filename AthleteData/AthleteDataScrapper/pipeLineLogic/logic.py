from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from AthleteData.AthleteDataScrapper.athleteDb.db import PostgresConnector


def scrap_data(clg_url, email_directory, college_name):
    """Developed a web scrapping logic that first scarps all the roster urls
    and the data of all the athletes from all the rosters"""
    pg_conn = PostgresConnector(host='Your AWS host link', port='Your Port Number', user='Your Own Username', password='Your Own Password')
    pg_conn.connect()
    # Creating table for the college
    pg_conn.create_table(college_name)
    driver = webdriver.Chrome()
    driver.get(clg_url)
    driver.implicitly_wait(5)
    # Made a list of all the roster urls
    new_page_data = [link.get_attribute('href') for link in
                     driver.find_elements(By.XPATH, '//a[contains(@href,"roster")]')]
    # Visiting each roster url and getting the data of all the athletes.
    for ele in new_page_data:
        driver.get(ele)
        driver.implicitly_wait(5)
        sport_name = driver.find_element(By.XPATH, '//a[contains(@href,"/index.aspx?path=")]').text
        # Making a list of all the players in the roster and getting their HTML codes
        player_divs = [each_player.get_attribute("innerHTML") for each_player in
                       driver.find_elements(By.XPATH, '//ul[contains(@class,"sidearm-roster-players")]/li')]
        for i in range(0, len(player_divs)):
            roster_players = []
            driver.execute_script("document.body.innerHTML = arguments[0]", player_divs[i])
            # Getting all the necessary data by locating the elements where the required data is present
            try:
                full_name = driver.find_element(By.XPATH, '//h3/a').text
                name = full_name.split(" ")
                first_name = name[0]
                last_name = name[1]
            except:
                print("Player's name not found for element {{i}} on page {{link}}".format(i=str(i), link=ele))
                continue
            try:
                position = driver.find_element(By.XPATH, '//span[@class="text-bold"]').text
            except:
                position = None
            try:
                academic_year = driver.find_element(By.XPATH,
                                                    '//span[@class="sidearm-roster-player-academic-year"]').text
            except:
                academic_year = None
            try:
                hometown = driver.find_element(By.XPATH,
                                               '//div[@class="sidearm-roster-player-other flex-item-1 columns hide-on-medium-down"]//span[@class="sidearm-roster-player-hometown"]').text
            except:
                hometown = None
            try:
                previous_school = driver.find_element(By.XPATH,
                                                      '//div[@class="sidearm-roster-player-other flex-item-1 columns hide-on-medium-down"]//span[@class="sidearm-roster-player-previous-school"]').text
            except:
                previous_school = None
            try:
                height = driver.find_element(By.XPATH, '//span[@class="sidearm-roster-player-height"]').text
            except:
                height = None
            try:
                weight = driver.find_element(By.XPATH, '//span[@class="sidearm-roster-player-weight"]').text
            except:
                weight = None
            try:
                jersey_number = driver.find_element(By.XPATH,
                                                    '//span[@class="sidearm-roster-player-jersey-number"]').text
            except:
                jersey_number = None

            # Getting the email_id from university's directory
            student_email = email_fetcher(full_name, email_directory)
            # Making a directory with all the information to be inserted into the database.
            roster_players.append({
                "school": college_name,
                "firstName": first_name,
                "lastName": last_name,
                "sportName": sport_name,
                "jerseyNumber": jersey_number,
                "position": position,
                "weight": weight,
                "height": height,
                "academicYear": academic_year,
                "hometown": hometown,
                "previousSchool": previous_school,
                "email": student_email
            })
            insert_resp = pg_conn.insert_data(roster_players, college_name)
            if insert_resp:
                continue
            else:
                print("Data not entered for {f_name}".format(f_name=full_name))
    pg_conn.disconnect()
    return True


def email_fetcher(full_name, email_url):
    driver_new = webdriver.Chrome()
    driver_new.get(email_url)
    search_field = driver_new.find_element(By.XPATH, '//input[@class="search-form__input"]')
    search_field.send_keys(full_name)
    search_button = driver_new.find_element(By.XPATH, '//button[contains(@class,"search-form__button")]')
    search_button.send_keys(Keys.ENTER)
    driver_new.implicitly_wait(5)
    try:
        # Locating the email id
        email_id = driver_new.find_element(By.XPATH, '//div[@class="contact__info-item"]').text
    except:
        email_id = None
        print("Email ID not found for {p_name}".format(p_name=full_name))
    return email_id