import pandas as pd

# Đọc dữ liệu từ file 'result.csv'
df = pd.read_csv('result.csv')

# Xác định các chỉ số cần tính (bỏ qua các cột như tên cầu thủ, đội, quốc tịch, v.v.)
columns_to_exclude = ['player', 'age', 'nationality', 'team', 'position']
stat_columns = [col for col in df.columns if col not in columns_to_exclude]

# Tạo danh sách lưu trữ kết quả
results = []

# Tính trung vị, trung bình và độ lệch chuẩn cho toàn giải
overall_stats = ['all']
for stat in stat_columns:
    median_val = df[stat].median()
    mean_val = df[stat].mean()
    std_val = df[stat].std()
    overall_stats.extend([median_val, mean_val, std_val])

# Thêm kết quả cho toàn giải vào danh sách kết quả
results.append(overall_stats)

# Tính trung vị, trung bình và độ lệch chuẩn cho từng đội
for team in df['team'].unique():
    team_stats = [team]
    team_data = df[df['team'] == team]
    
    for stat in stat_columns:
        median_val = team_data[stat].median()
        mean_val = team_data[stat].mean()
        std_val = team_data[stat].std()
        team_stats.extend([median_val, mean_val, std_val])
    
    # Thêm kết quả của từng đội vào danh sách kết quả
    results.append(team_stats)

# Tạo các tên cột cho DataFrame kết quả
columns = ['team']
for stat in stat_columns:
    columns.extend([f"Median of {stat}", f"Mean of {stat}", f"Std of {stat}"])

# Chuyển danh sách kết quả thành DataFrame và lưu vào file CSV
results_df = pd.DataFrame(results, columns=columns)
results_df.to_csv('results2.csv', index=False)

print("Kết quả đã được lưu vào 'results2.csv'.")