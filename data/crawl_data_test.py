import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Cấu hình Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = '/opt/google/chrome/google-chrome'  # Đường dẫn đúng đến Google Chrome
# chrome_options.add_argument("--headless")  # Có thể uncomment nếu cần chạy headless
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

# Bước 2: Sau khi năm đã được chọn, chọn tên sàn chứng khoán "LSE (England)"
dropdown_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@type='button' and @class='btn dropdown-toggle bs-placeholder btn-default']"))
)
dropdown_button.click()

# Chọn option "LSE (England)" trong dropdown
option_lse = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[span[text()='LSE (England)']]"))
)
option_lse.click()

# Đợi phần tử "LSE (England)" xuất hiện trong ô đã chọn
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

# Bước 4: Click vào tất cả các nút "Chi tiết" trong bảng và mở các tab mới
# Tìm tất cả các nút "Chi tiết"
detail_buttons = driver.find_elements(By.XPATH, "//td[contains(@class, 'column-link_enreport')]//button[text()='Chi tiết']")

# Lặp qua tất cả các nút và click vào từng nút để mở tab mới
for button in detail_buttons:
    button.click()
    time.sleep(1)  # Đảm bảo có thời gian cho tab mới mở

# Bước 5: Mở các tab mới (từng tab chứa PDF)
# Lưu ý Selenium mở các tab trong trình duyệt, bạn cần chuyển qua lại giữa các tab để xử lý
all_tabs = driver.window_handles

# Tạo thư mục để lưu trữ các file PDF nếu chưa tồn tại
output_dir = "pdf_files"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Chuyển qua từng tab và tải file PDF
for tab in all_tabs:
    driver.switch_to.window(tab)
    time.sleep(2)  # Đảm bảo nội dung PDF đã tải xong

    # Lấy URL của file PDF
    pdf_url = driver.current_url
    print(f"Đang tải PDF từ: {pdf_url}")

    # Tải file PDF và lưu vào thư mục output_dir
    try:
        response = requests.get(pdf_url, stream=True)
        pdf_name = pdf_url.split("/")[-1]  # Lấy tên file từ URL
        pdf_path = os.path.join(output_dir, pdf_name)

        with open(pdf_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Đã tải xuống {pdf_name} vào {pdf_path}")
    except Exception as e:
        print(f"Không thể tải file PDF từ {pdf_url}. Lỗi: {e}")

# Đóng trình duyệt sau khi hoàn thành
driver.quit()
