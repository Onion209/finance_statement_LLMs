from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = '/opt/google/chrome/google-chrome'  # Đường dẫn đúng đến Google Chrome

# chrome_options.add_argument("--headless")   
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = uc.Chrome(options=chrome_options)

# Mở trang web
url = "https://data.kreston.vn/tra-cuu-bao-cao-cong-ty-nuoc-ngoai/"
driver.get(url)
# Bước 1: Mở dropdown và chọn năm 2019
dropdown_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@title='Nothing selected']"))
)
dropdown_button.click()

# Chọn option "2019"
option_2019 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[span[contains(text(),'2019')]]"))
)
option_2019.click()

# Đợi phần tử "2019" xuất hiện trong ô đã chọn
selected_2019 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'2019')]"))
)
time.sleep(5)
# Bước 1: Sau khi năm đã được chọn, chọn tên sàn chứng khoán "LSE (England)"
dropdown_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @class='btn dropdown-toggle bs-placeholder btn-default']"))
)
dropdown_button.click()
# Bước 2: Click vào option "LSE (England)" trong dropdown
option_lse = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[span[text()='LSE (England)']]"))
)
option_lse.click()
# Bước 3: Đợi phần tử "LSE (England)" xuất hiện trong ô đã chọn
selected_lse = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//button[@title='LSE (England)']"))
)


# Bước 3: Click vào nút "Search"
search_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Search filters']"))
)
search_button.click()
# Đợi kết quả tìm kiếm tải
time.sleep(15)

# Tìm bảng trên trang web bằng ID đúng (table_1)
table = driver.find_element(By.ID, 'table_1')

# Lấy tiêu đề cột từ bảng
headers = [header.text.strip() for header in table.find_elements(By.TAG_NAME, 'th')]
print("Headers:", headers)

# Lấy tất cả các hàng trong bảng
rows = table.find_elements(By.TAG_NAME, 'tr')

# Danh sách chứa dữ liệu của bảng
data = []
for row in rows[1:]:  # Bỏ qua dòng tiêu đề (dòng đầu tiên)
    cells = row.find_elements(By.TAG_NAME, 'td')
    if cells:  # Kiểm tra nếu có dữ liệu trong các ô
        row_data = [cell.text.strip() for cell in cells]
        data.append(row_data)

# In kết quả
print("Data:", data)

# Đóng trình duyệt
driver.quit()
