from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager

from models.GameJamModel import GameJamModel
from scraper.When import When
from datetime import datetime, timedelta

class GameJamsScraper:
    GAME_JAMS_URL: str = 'https://itch.io/jams/upcoming/sort-date'
    
    def __init__(self, headless: bool = True):
        """Initialize the firefox driver in headless mode by default.

        Args:
            headless (bool, optional): Enable or disable headless mode (to see browser). Defaults to True.
        """

        # Init driver options
        firefox_options = Options()
        if headless:
            firefox_options.add_argument("--headless")

        # Init driver & get the default james url
        self._driver = Firefox(
            service=Service(GeckoDriverManager().install()),
            options=firefox_options
        ) 
        self._driver.get(GameJamsScraper.GAME_JAMS_URL)
    
    def scrap_jams(self, count: int = 50, when: When = When.UPCOMING) -> list[GameJamModel]:
        """Scraps the given number of jams with the given time filter (upcoming, in progress or ended).

        Args:
            count (int, optional): The number of jams to scrap. Defaults to 50.
            when (When, optional): The time filter to apply. Defaults to When.UPCOMING.

        Returns:
            list[GameJamModel]: The scrapped game jams.
        """
        
        jams: list[GameJamModel] = []
        
        # Apply filters
        self._filter_when(when)
        
        jams_per_page: int = self._get_nb_jams_per_page()
        nb_jams_to_scrap: int = count
        
        last_page: int = self._get_last_page()
        for i in range(last_page):
            # Compute number of jams to scrap
            if count > jams_per_page:
                nb_jams_to_scrap = jams_per_page
            
            jams += self._scrap_page_jams(nb_jams_to_scrap, when)
            
            count -= nb_jams_to_scrap
            nb_jams_to_scrap = count
            if count == 0:
                break
            
            if i < last_page - 1:
                self._next_jam_page()
        
        if when != When.UPCOMING:
            self._set_jams_dates_in_page(jams)
        
        return jams
    
    def _filter_when(self, when: When) -> None:
        if when.value in self._driver.current_url:
            return
        
        container: WebElement = self._driver.find_element(By.CLASS_NAME, 'browse_filter_group_widget').find_element(By.TAG_NAME, 'ul')
        if when == When.UPCOMING:
            container.find_element(By.XPATH, 'li[1]//a').click()
        elif when == When.IN_PROGRESS:
            container.find_element(By.XPATH, 'li[4]//a').click()
        else:
            container.find_element(By.XPATH, 'li[5]//a').click()
    
    def _get_nb_jams_per_page(self) -> int:
        return len(self._driver.find_elements(By.CLASS_NAME, 'padded_content'))
    
    def _get_last_page(self) -> int:
        pager_label: str = self._driver.find_element(By.CLASS_NAME, 'pager_label').text
        return int(pager_label.split(' ')[3])
    
    def _next_jam_page(self) -> None:
        self._driver.find_element(By.CLASS_NAME, 'next_page').click()
    
    def _scrap_page_jams(self, count: int, when: When) -> list[GameJamModel]:
        jams: list[GameJamModel] = []
        counter = 0

        self._driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        jam_containers = self._driver.find_elements(By.CLASS_NAME, 'padded_content')
        for jam_container in jam_containers:
            # If number of jams wanted reached, stops here and returns
            if counter == count:
                break
            
            # Prevent just started jams to be returned if only upcomming wanted
            if when == When.UPCOMING and 'Submission' in jam_container.text:
                continue
            
            jams.append(self._get_jam(jam_container, when))
            counter += 1
        
        return jams
    
    def _get_jam(self, jam_container: WebElement, when: When) -> GameJamModel:
        jam_start_date: datetime = None
        jam_end_date: datetime = None
        if when == When.UPCOMING:
            jam_start_date = self._get_jam_start_date(jam_container)
            jam_end_date = self._get_jam_end_date(jam_container, jam_start_date)
        
        return GameJamModel(
            name=self._get_jam_name(jam_container),
            url=self._get_jam_url(jam_container),
            bg_image_url=self._get_jam_bg_image_url(jam_container),
            start_date=jam_start_date,
            end_date=jam_end_date,
            joined=self._get_jam_joined(jam_container),
            ranked=self._is_jam_ranked(jam_container),
            featured=self._is_jam_featured(jam_container)
        )
    
    def _get_jam_name(self, jam_container: WebElement) -> str:
        return jam_container.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').text

    def _get_jam_url(self, jam_container: WebElement) -> str:
        return jam_container.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute('href')

    def _get_jam_bg_image_url(self, jam_container: WebElement) -> str | None:
        bg_image_url: str
        try:
            bg_image_url = jam_container.find_element(By.CLASS_NAME, 'jam_cover').get_attribute('data-background_image')
        except NoSuchElementException:
            return None
        return bg_image_url
    
    def _get_jam_start_date(self, jam_container: WebElement) -> datetime:
        date_str: str = jam_container.find_element(By.CLASS_NAME, 'date_countdown').get_attribute('title')
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    
    def _get_jam_end_date(self, jam_container: WebElement, start_date: datetime) -> datetime:
        duration_str: str = jam_container.find_element(By.CLASS_NAME, 'date_duration').text
        duration: int = int(duration_str.split(' ')[0])
        return start_date + timedelta(days=duration)
    
    def _set_jams_dates_in_page(self, jams: list[GameJamModel]) -> None:
        for jam in jams:
            self._driver.get(jam.url)
            start_date, end_date = self._get_jam_dates_in_page()
            jam.start_date = start_date
            jam.end_date = end_date
    
    def _get_jam_dates_in_page(self) -> tuple[datetime, datetime]:
        html_dates: list[WebElement] = self._driver.find_elements(By.CLASS_NAME, 'date_format')
        return [
            datetime.strptime(html_dates[0].get_attribute('title').split(' UTC')[0], '%Y-%m-%d %H:%M:%S'),
            datetime.strptime(html_dates[1].get_attribute('title').split(' UTC')[0], '%Y-%m-%d %H:%M:%S')
        ]

    def _get_jam_joined(self, jam_container: WebElement) -> int:
        joined: int = 0
        try:
            joined_str = jam_container.find_element(By.CLASS_NAME, 'number').text
            joined = int(joined_str.replace(',', ''))
        except NoSuchElementException:
            return 0
        return joined
    
    def _is_jam_ranked(self, jam_container: WebElement) -> bool:
        try:
            jam_container.find_element(By.CLASS_NAME, 'jam_ranked')
        except NoSuchElementException:
            return False
        return True
    
    def _is_jam_featured(self, jam_container: WebElement) -> bool:
        try:
            jam_container.parent.find_element(By.CLASS_NAME, 'featured_flag') != None
        except NoSuchElementException:
            return False
        return True
    
    def __del__(self):  
        self._driver.quit()