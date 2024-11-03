import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import argparse

# Hàm để vẽ biểu đồ radar
def radar_chart(player1, player2, attributes, data):
    # Lấy dữ liệu của hai cầu thủ dựa trên tên
    p1_data = data[data['name'] == player1][attributes].values.flatten()
    p2_data = data[data['name'] == player2][attributes].values.flatten()
    
    if p1_data.size == 0 or p2_data.size == 0:
        print("Lỗi: Không tìm thấy cầu thủ hoặc chỉ số không hợp lệ.")
        return

    # Tạo các góc cho biểu đồ radar
    num_vars = len(attributes)
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]  # Đóng đường tròn

    # Thêm điểm đầu tiên vào cuối để đóng đường tròn
    p1_data = np.append(p1_data, p1_data[0])
    p2_data = np.append(p2_data, p2_data[0])

    # Thiết lập biểu đồ
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    plt.xticks(angles[:-1], attributes, color='grey', size=8)
    ax.plot(angles, p1_data, linewidth=1, linestyle='solid', label=player1)
    ax.fill(angles, p1_data, 'b', alpha=0.1)

    ax.plot(angles, p2_data, linewidth=1, linestyle='solid', label=player2)
    ax.fill(angles, p2_data, 'r', alpha=0.1)

    # Thêm chú thích và hiển thị
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.title(f"So sánh {player1} và {player2}")
    plt.show()

# Đọc dữ liệu và xử lý đầu vào từ dòng lệnh
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vẽ biểu đồ radar so sánh cầu thủ.")
    parser.add_argument("--p1", type=str, required=True, help="Tên cầu thủ thứ nhất")
    parser.add_argument("--p2", type=str, required=True, help="Tên cầu thủ thứ hai")
    parser.add_argument("--Attribute", type=str, required=True, help="Danh sách các chỉ số, cách nhau bởi dấu phẩy")

    args = parser.parse_args()
    
    # Đọc dữ liệu từ file CSV
    data = pd.read_csv("results2.csv")

    # Phân tách danh sách chỉ số từ chuỗi đầu vào
    attributes = args.Attribute.split(",")

    # Gọi hàm vẽ biểu đồ radar
    radar_chart(args.p1, args.p2, attributes, data)
