from dtp import app, db
from dtp.models import Faculty, University
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

with open('values.txt', 'r') as file:
    values = file.readlines()
with app.app_context():
    for university in values:
        university = university.strip()
        driver.get("https://yokatlas.yok.gov.tr/lisans-anasayfa.php")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'flip1'))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="flip1"]/div/div[2]/div/form/div/div/div/button'))).click()
        print(f"İşlem yapılıyor: {university}")

        select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "univ")))

        select = Select(select_element)
        try:
            select.select_by_value(str(university)) 
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="bs-collapse"]/div/div/h4/a/small/font')))
            faculty_names = driver.find_elements(By.XPATH, '//*[@id="bs-collapse"]/div/div/h4/a/small/font')
            faculty_names2 = driver.find_elements(By.XPATH, '//*[@id="bs-collapse2"]/div/div/h4/a/small/font')
            faculty_names.extend(faculty_names2)
            print(f'{university} Fakülteleri:')
            uni_name = driver.find_element(By.XPATH, "//div[@class='page-header']/h3").text.split("ÜNİVERSİTESİ")[0] + "ÜNİVERSİTESİ"
            uni = University.query.filter_by(name=uni_name).first()
            for faculty_name in faculty_names:
                faculty_name_to_db = faculty_name.text.replace('(', '').replace(')', '')
                print(faculty_name_to_db)
                faculty = Faculty.query.filter_by(name=faculty_name_to_db, university_id=uni.id).first()
                if faculty:
                    continue
                faculty_to_db = Faculty(name=faculty_name_to_db, university_id=uni.id)
                db.session.add(faculty_to_db)
                db.session.commit()
            print('-' * 50)
        except Exception as e:
            print(f'{university} üniversitesi için fakülte bilgileri alınamadı. Hata: {e}')
    db.session.close()
driver.quit()

