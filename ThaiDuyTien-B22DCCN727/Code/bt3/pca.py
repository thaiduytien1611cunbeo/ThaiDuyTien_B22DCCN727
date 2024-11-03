import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# Đọc dữ liệu
data = pd.read_csv("results2.csv")

# Lựa chọn các chỉ số để phân tích
attributes = data[['age', 'nationality', 'team', 'position']]

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
scaled_data = scaler.fit_transform(attributes)

# Sử dụng thuật toán K-means để phân cụm (giả sử số cụm là 4)
kmeans = KMeans(n_clusters=4, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# Áp dụng PCA để giảm số chiều xuống 2
pca = PCA(n_components=2)
pca_data = pca.fit_transform(scaled_data)

# Tạo DataFrame cho dữ liệu PCA và cụm
pca_df = pd.DataFrame(data=pca_data, columns=['PC1', 'PC2'])
pca_df['Cluster'] = clusters

# Vẽ phân cụm các cầu thủ trên mặt phẳng 2D
plt.figure(figsize=(10, 8))
for cluster in pca_df['Cluster'].unique():
    subset = pca_df[pca_df['Cluster'] == cluster]
    plt.scatter(subset['PC1'], subset['PC2'], label=f'Cluster {cluster}', s=50)

plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.title('PCA - K-means Clustering of Players')
plt.legend()
plt.grid(True)
plt.show()
