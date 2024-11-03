import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu từ file CSV
data = pd.read_csv('result.csv')

# Lọc ra các cột chỉ chứa dữ liệu số
attributes = data.select_dtypes(include=[float, int])

# Điền các giá trị NaN bằng giá trị trung bình của mỗi cột
attributes = attributes.fillna(attributes.mean())

# Chuẩn hóa dữ liệu để đảm bảo các chỉ số có cùng thang đo
scaler = StandardScaler()
scaled_data = scaler.fit_transform(attributes)

# Sử dụng phương pháp "elbow" để xác định số cụm tối ưu
inertia = []
K = range(1, 11)  # Thử từ 1 đến 10 cụm
for k in K:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    inertia.append(kmeans.inertia_)

# Vẽ biểu đồ Elbow để xác định số cụm tối ưu
plt.figure(figsize=(8, 5))
plt.plot(K, inertia, 'bx-')
plt.xlabel('Số cụm (k)')
plt.ylabel('Inertia')
plt.title('Phương pháp Elbow để xác định số cụm tối ưu')
plt.show()

# Sau khi xác định k (giả sử k = 4 từ biểu đồ elbow)
k = 4
kmeans = KMeans(n_clusters=k, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# Thêm nhãn cụm vào DataFrame gốc
data['Cluster'] = clusters

# Tính trung bình mỗi chỉ số cho từng cụm để hiểu đặc điểm của các nhóm
cluster_means = data.groupby('Cluster').mean()

# Hiển thị đặc điểm trung bình của từng cụm
print("Trung bình các chỉ số của từng cụm:")
print(cluster_means)

# Trực quan hóa các cụm bằng biểu đồ phân tán với 2 chỉ số đầu tiên (hoặc chọn các chỉ số khác)
plt.figure(figsize=(10, 6))
sns.scatterplot(x=scaled_data[:, 0], y=scaled_data[:, 1], hue=clusters, palette='viridis', s=100)
plt.xlabel('Chỉ số 1 (chuẩn hóa)')
plt.ylabel('Chỉ số 2 (chuẩn hóa)')
plt.title('Phân cụm các cầu thủ bằng K-means')
plt.legend(title='Cụm')
plt.show()

# Lưu kết quả phân cụm vào file CSV
data.to_csv('clustered_players.csv', index=False)
