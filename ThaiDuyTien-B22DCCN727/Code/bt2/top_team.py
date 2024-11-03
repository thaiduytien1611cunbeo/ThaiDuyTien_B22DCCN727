import pandas as pd

# Đọc dữ liệu từ file 'result.csv'
df = pd.read_csv('result.csv')

# Xác định các cột chỉ số (loại bỏ các cột không phải là chỉ số như tên cầu thủ, đội, v.v.)
columns_to_exclude = ['player', 'age', 'nationality', 'team', 'position']
stat_columns = [col for col in df.columns if col not in columns_to_exclude]

# Tính điểm trung bình của mỗi chỉ số cho từng đội
team_stats = df.groupby('team')[stat_columns].mean()

# Tìm đội có điểm số cao nhất ở mỗi chỉ số
best_team_per_stat = team_stats.idxmax()

# Đếm số lần mỗi đội đứng đầu ở các chỉ số để đánh giá phong độ
top_team_counts = best_team_per_stat.value_counts()

# In ra đội có điểm cao nhất ở mỗi chỉ số
print("Đội có điểm cao nhất ở mỗi chỉ số:")
print(best_team_per_stat)

# In ra đội có phong độ tốt nhất (đội đứng đầu nhiều chỉ số nhất)
print("\nĐội có phong độ tốt nhất giải:")
print(top_team_counts.head(1))
