import pandas as pd

# Đọc dữ liệu từ tệp `result.csv`
df = pd.read_csv('result.csv')

# Loại bỏ các cột không phải là chỉ số (như tên cầu thủ, tuổi)
columns_to_exclude = ['player', 'age', 'nationality', 'team', 'position']
stat_columns = [col for col in df.columns if col not in columns_to_exclude]

# Tạo từ điển để lưu top 3 cao nhất và thấp nhất cho mỗi chỉ số
top_players = {
    "stat": [],
    "top_3_highest": [],
    "top_3_lowest": []
}

# Duyệt qua từng chỉ số để tìm top 3 cao nhất và thấp nhất
for stat in stat_columns:
    # Loại bỏ các giá trị N/a và chuyển đổi dữ liệu về kiểu số (nếu cần)
    df[stat] = pd.to_numeric(df[stat], errors='coerce')

    # Lấy top 3 cầu thủ có điểm cao nhất
    top_3_high = df[['player', stat]].nlargest(3, stat).reset_index(drop=True)
    top_3_high_list = [f"{row['player']} ({row[stat]})" for _, row in top_3_high.iterrows()]

    # Lấy top 3 cầu thủ có điểm thấp nhất
    top_3_low = df[['player', stat]].nsmallest(3, stat).reset_index(drop=True)
    top_3_low_list = [f"{row['player']} ({row[stat]})" for _, row in top_3_low.iterrows()]

    # Thêm kết quả vào từ điển
    top_players["stat"].append(stat)
    top_players["top_3_highest"].append(", ".join(top_3_high_list))
    top_players["top_3_lowest"].append(", ".join(top_3_low_list))

# Chuyển kết quả vào DataFrame và lưu vào tệp CSV
result_df = pd.DataFrame(top_players)
result_df.to_csv('top_players_stats.csv', index=False)
print("Top 3 cầu thủ có điểm cao nhất và thấp nhất cho mỗi chỉ số đã được lưu vào 'top_players_stats.csv'.")