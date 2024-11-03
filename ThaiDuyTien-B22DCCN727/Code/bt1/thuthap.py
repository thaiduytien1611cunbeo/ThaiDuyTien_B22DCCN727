from bs4 import BeautifulSoup as bs  # Import BeautifulSoup để phân tích cú pháp HTML
from bs4 import Comment  # Import Comment để xử lý các bình luận HTML
import requests  # Import requests để thực hiện các yêu cầu HTTP
import pandas as pd  # Import pandas để xử lý dữ liệu trong DataFrames

# Hàm thu thập dữ liệu từ một URL cho trước
def crawler(url, id_div, cnt):
    # In ra URL và ID của div được nhắm đến
    print(url, id_div)
    # Thực hiện yêu cầu HTTP GET tới URL cho trước
    r1 = requests.get(url)
    # Phân tích nội dung của phản hồi bằng BeautifulSoup
    soup1 = bs(r1.content, 'html.parser')
    # Tìm thẻ div với ID được chỉ định
    table1 = soup1.find('div', {'id': id_div})
    # Tìm tất cả các bình luận trong div (dữ liệu có thể nằm trong các bình luận HTML)
    comment1 = table1.find_all(string=lambda text: isinstance(text, Comment))
    # Phân tích bình luận đầu tiên tìm thấy dưới dạng HTML để trích xuất các hàng của bảng
    data1 = bs(comment1[0], 'html.parser').find_all('tr')  # Chuyển chuỗi về dạng thẻ HTML

    # Tạo một từ điển rỗng để lưu trữ dữ liệu
    ans1 = dict()
    # Khởi tạo các khóa của từ điển dựa trên hàng tiêu đề của bảng
    for i, g in enumerate(data1[1].find_all('th')):
        if i != 0:  # Bỏ qua cột đầu tiên
            ans1[g.get('data-stat')] = []
    
    # Trích xuất dữ liệu cầu thủ từ các hàng của bảng
    for i in range(2, len(data1)):  # Bắt đầu từ hàng thứ ba (chỉ mục 2)
        tmp1 = data1[i].find_all('td')  # Lấy tất cả các ô dữ liệu của hàng
        for j, x in enumerate(tmp1):
            if x.get('data-stat') in ans1.keys():
                if x.get('data-stat') == 'nationality':  # Xử lý đặc biệt cho cột quốc tịch
                    s = x.getText().split(" ")  # Lấy quốc tịch mà không lấy biểu tượng cờ
                    ans1[x.get('data-stat')].append(s[0])
                else:
                    ans1[x.get('data-stat')].append(x.getText())  # Thêm nội dung vào danh sách
    
    # Chuyển dữ liệu thu thập được vào DataFrame
    df1 = pd.DataFrame(ans1)
    # Bỏ các cột nhất định đối với thủ môn nếu cnt bằng 2
    if cnt == 2:
        df1.drop(['gk_games', 'gk_games_starts', 'gk_minutes', 'minutes_90s'], axis=1, inplace=True)
    # Lưu DataFrame vào tệp CSV
    df1.to_csv(f'table{cnt}.csv')

# Hàm làm sạch và kết hợp dữ liệu từ nhiều tệp CSV
def clean_data():
    # Đọc tệp CSV đầu tiên
    result = pd.read_csv('table1.csv')
    # Lặp qua các tệp bảng khác và kết hợp với DataFrame chính
    for x in range(3, 11):
        table = pd.read_csv(f"table{x}.csv")
        # Bỏ các cột trùng lặp từ bảng mới
        for x in table.columns:
            if x in result.columns:
                if x != 'Unnamed: 0':  # Bỏ qua cột chỉ mục
                    table.drop(x, axis=1, inplace=True)
        # Kết hợp các bảng dựa trên chỉ mục
        result = pd.merge(result, table, on=['Unnamed: 0'], how='inner')
    
    # Xác định các cột chung để kết hợp với table2
    merge = []
    table2 = pd.read_csv("table2.csv")
    for x in table2.columns:
        if x in result.columns:
            merge.append(x)
    merge.pop(0)  # Loại bỏ cột chỉ mục khỏi tiêu chí kết hợp
    # Kết hợp với table2, giữ tất cả các hàng từ bảng bên trái
    result = pd.merge(result, table2, on=merge, how='left')
    # Bỏ các cột không cần thiết
    result.drop(['Unnamed: 0_x', 'Unnamed: 0_y', 'minutes_90s', 'birth_year', 'matches'], axis=1, inplace=True)
    # Chuyển đổi phút thành số nguyên, loại bỏ dấu phẩy
    result['minutes'] = result['minutes'].apply(lambda x: int(''.join(x.split(','))))
    # Lọc ra những cầu thủ có thời gian chơi hơn 90 phút
    result = result[result['minutes'] > 90]
    # Sắp xếp theo tên cầu thủ và tuổi giảm dần
    result.sort_values(by=["player", 'age'], ascending=[True, False])
    # Lưu dữ liệu đã làm sạch vào tệp CSV mới
    result.to_csv('result.csv')

# Khối chính để thực thi script
if __name__ == '__main__':
    # URL để lấy dữ liệu ban đầu
    url = 'https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats'
    # Thực hiện yêu cầu HTTP và phân tích phản hồi
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    # Tìm div chứa thống kê và trích xuất dữ liệu bảng
    table = soup.find('div', {'id': 'all_stats_standard'})
    comment = table.find_all(string=lambda text: isinstance(text, Comment))
    data = bs(comment[0], 'html.parser').find_all('tr')  # Chuyển nội dung bình luận về dạng HTML

    # Danh sách các chỉ mục cho các cột cần bỏ qua
    idx = [0, 6, 10, 11, 13, 16, 22, 36]
    # Khởi tạo từ điển để lưu trữ dữ liệu trích xuất
    ans = dict()
    # Xử lý hàng tiêu đề để thiết lập các khóa của từ điển
    for i, g in enumerate(data[1].find_all('th')):
        if i not in idx:
            ans[g.get('data-stat')] = []
    
    # Thu thập dữ liệu cho mỗi cầu thủ từ các hàng của bảng
    for i in range(2, len(data)):
        tmp = data[i].find_all('td')  # Lấy tất cả các ô dữ liệu
        for j, x in enumerate(tmp):
            if x.get('data-stat') in ans.keys():
                if x.get('data-stat') == 'nationality':
                    s = x.getText().split(" ")  # Xử lý cột quốc tịch
                    ans[x.get('data-stat')].append(s[0])
                else:
                    ans[x.get('data-stat')].append(x.getText())  # Thêm dữ liệu văn bản
    
    # Chuyển dữ liệu thu thập được vào DataFrame và điều chỉnh tên cột
    df = pd.DataFrame(ans)
    df.rename(columns={'goals_pens': 'non-Penalty Goals', 'pens_made': 'Penalty Goals'}, inplace=True)
    # Lưu DataFrame vào tệp CSV
    df.to_csv('table1.csv')

    # URLs và các ID div tương ứng để thu thập thêm dữ liệu
    urls = [
        'https://fbref.com/en/comps/9/2023-2024/keepers/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/shooting/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/passing/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/passing_types/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/gca/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/defense/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/possession/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/playingtime/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/misc/2023-2024-Premier-League-Stats'
    ]
    ids = [
        'all_stats_keeper', 'all_stats_shooting', 'all_stats_passing', 'all_stats_passing_types', 
        'all_stats_gca', 'all_stats_defense', 'all_stats_possession', 
        'all_stats_playing_time', 'all_stats_misc'
    ]
    
    # Sử dụng hàm crawler để xử lý mỗi URL và ID div tương ứng
    for _, x in enumerate(zip(urls, ids)):
        crawler(x[0], x[1], _ + 2)
    
    # Làm sạch và kết hợp dữ liệu đã thu thập
    clean_data()
