import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Đọc dữ liệu từ tệp 'result.csv'
df = pd.read_csv('result.csv')

# Xác định các cột chỉ số (loại bỏ các cột không phải là chỉ số như tên cầu thủ, đội, v.v.)
columns_to_exclude = ['player', 'age', 'nationality', 'team', 'position']
stat_columns = [col for col in df.columns if col not in columns_to_exclude]

# Giới hạn số lượng chỉ số xuất histogram thành 20
max_histograms = 20
selected_columns = stat_columns[:max_histograms]  # Chọn tối đa 20 chỉ số đầu tiên

# Tạo thư mục 'histograms' nếu chưa tồn tại để lưu các biểu đồ
os.makedirs('histograms', exist_ok=True)

# Vẽ và lưu histogram cho từng chỉ số trong danh sách được chọn
for stat in selected_columns:
    plt.figure(figsize=(8, 6))
    sns.histplot(df[stat].dropna(), kde=True, bins=30)  # Vẽ histogram và đường KDE
    plt.title(f'Histogram of {stat}')
    plt.xlabel(stat)
    plt.ylabel('Frequency')
    
    # Lưu biểu đồ dưới dạng file ảnh PNG
    plt.savefig(f'histograms/{stat}_histogram.png')
    plt.close()  # Đóng biểu đồ sau khi lưu để giải phóng bộ nhớ

print("Histograms have been saved in the 'histograms' folder for the selected 20 attributes.")