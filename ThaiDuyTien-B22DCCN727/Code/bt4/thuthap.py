import requests
from bs4 import BeautifulSoup
import csv

# URL của trang cần thu thập dữ liệu (thay đổi URL nếu cần)
url = "https://www.footballtransfers.com"

# Gửi yêu cầu GET đến trang
response = requests.get(url)

# Kiểm tra mã trạng thái của phản hồi
if response.status_code == 200:
    # Phân tích cú pháp HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Tìm tất cả các giá chuyển nhượng
    transfer_values = soup.find_all('span', class_='player-tag')  # Lấy tất cả các span có class 'player-tag'
    
    # Mở tệp CSV để ghi dữ liệu
    with open('transfer_values.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Cầu thủ', 'Giá chuyển nhượng'])  # Ghi tiêu đề cột

        # Lặp qua từng giá chuyển nhượng và ghi vào tệp CSV
        for idx, value in enumerate(transfer_values, start=1):
            transfer_value = value.text.strip()  # Lấy giá chuyển nhượng
            writer.writerow([f'Cầu thủ {idx}', transfer_value])  # Ghi dữ liệu vào tệp CSV

    print("Đã ghi giá chuyển nhượng vào tệp 'transfer_values.csv'.")

else:
    print(f"Không thể truy cập trang web. Mã trạng thái: {response.status_code}")
