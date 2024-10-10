import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

with st.sidebar:
   
    st.image("https://avatars.githubusercontent.com/u/17227515?v=4", use_column_width=True)
    

    st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Ariq Luthfi Rifqi</h2>", unsafe_allow_html=True)
    
  
    st.markdown("""
    <p style='text-align: center; color: #808080;'>
    Data Scientist | Machine Learning Enthusiast <br>
    Passionate about uncovering insights from data to drive business growth.
    </p>
    """, unsafe_allow_html=True)
    
  
    st.markdown("<hr style='border:1px solid #4CAF50;'>", unsafe_allow_html=True)


    st.markdown("""
    <p style='text-align: center;'>
    <a href='https://github.com/ariqluth' style='text-decoration:none; color: #4CAF50;'>GitHub</a> | 
    </p>
    """, unsafe_allow_html=True)

st.title("Database yang digunakan : E-commerce-public-dataset")
code = '''Deskripsi file dataset yang digunakan dalam analisis ini adalah sebagai berikut,

*`orders_dataset :`*

File ini berisi informasi tentang pesanan, seperti ID pesanan, status pesanan, waktu pembelian, dan waktu pengiriman pesanan.

`*order_items_dataset :*`

File ini berisi informasi terperinci tentang setiap item yang dibeli dalam pesanan

*`order_payments_dataset`* :

File ini berisi informasi terperinci tentang jenis pembayaran yang digunakan dari setiap item yang dibeli dalam pesanan

*`order_reviews_dataset :`*

File ini berisi informasi terperinci tentang review dari setiap item yang dibeli dalam pesanan

*`products_dataset`* :

File ini berisi informasi tentang produk, termasuk ID produk dan nama produk.

*`product_category_dataset`* :

File ini berisi informasi tentang kategori produk, termasuk ID produk dan kategori produk.

*`sellers_dataset`* :

File ini berisi informasi tentang penjual, seperti ID penjual, nama penjual, dan lokasi penjual (kota dan negara bagian).

`*`customers_dataset`*` :

File ini berisi informasi tentang pelanggan, seperti ID pelanggan, nama pelanggan, dan lokasi pelanggan (kota dan negara bagian).

geolocation_dataset :

File ini menyediakan informasi geografis tentang kota dan negara bagian di Brazil. Ini membantu dalam analisis berdasarkan lokasi geografis.'''

with st.expander("dataset penjelasan"):
    st.code(code, language="python")
st.divider()



st.title(" Analisis Tren Penjualan Bulanan")

df_real_tengkulak = pd.read_csv('../df_real_tengkulak.csv')

df_real_tengkulak['order_purchase_timestamp'] = pd.to_datetime(df_real_tengkulak['order_purchase_timestamp'])

df_real_tengkulak['order_year_month'] = df_real_tengkulak['order_purchase_timestamp'].dt.to_period('M')

df_real_tengkulak['order_month_name'] = df_real_tengkulak['order_purchase_timestamp'].dt.strftime('%B')

df_2017 = df_real_tengkulak[df_real_tengkulak['order_purchase_timestamp'].dt.year == 2017]

monthly_sales_2017 = df_2017.groupby('order_year_month')['price'].sum()

df_2018 = df_real_tengkulak[df_real_tengkulak['order_purchase_timestamp'].dt.year == 2018]

monthly_sales_2018 = df_2018.groupby('order_year_month')['price'].sum()

col1, col2 = st.columns(2)

with col1:
    plt.figure(figsize=(12, 6))
    monthly_sales_2017.plot(kind='line', marker='o')
    plt.title('Tren Penjualan Bulanan (2017)')
    plt.xlabel('Bulan')
    plt.ylabel('Pendapatan Total')
    plt.grid(True)
    st.pyplot(plt)

with col2:
    plt.figure(figsize=(12, 6))
    monthly_sales_2018.plot(kind='line', marker='o')
    plt.title('Tren Penjualan Bulanan (2018)')
    plt.xlabel('Bulan')
    plt.ylabel('Pendapatan Total')
    plt.grid(True)
    st.pyplot(plt)

code = '''# Menambahkan kolom tahun dan bulan
df_real_tengkulak['order_year_month'] = df_real_tengkulak['order_purchase_timestamp'].dt.to_period('M')

# Menambahkan kolom nama bulan
df_real_tengkulak['order_month_name'] = df_real_tengkulak['order_purchase_timestamp'].dt.strftime('%B')'''

with st.expander("Deskripsi dibawah"):
    st.write(
        """penjulanan bulanan pada tahun 2017 dan 2018 dari hasil data
        """
    )
    st.code(code,  language="python")

st.divider()

region_sales = df_real_tengkulak.groupby('customer_city')['price'].sum()

top_5_regions = region_sales.nlargest(5)
bottom_5_regions = region_sales.nsmallest(5)

st.title("Dimana geolocation tempat yang 5 tertinggi dan terendah Pendapatan uang ?")
colsales1, colsales2 = st.columns(2)

with colsales1:
    st.subheader("5 Wilayah Teratas dengan Pendapatan Tertinggi")
    st.write(top_5_regions)

with colsales2:
    st.subheader("5 Wilayah Terendah dengan Pendapatan Terendah")
    st.write(bottom_5_regions)

df_revenue = df_real_tengkulak.groupby('seller_state')['payment_value'].sum().reset_index()

top_5_high = df_revenue.nlargest(5, 'payment_value') 
top_5_low = df_revenue.nsmallest(5, 'payment_value') 

required_states = pd.concat([top_5_high, top_5_low])['seller_state'].unique()

geolocation_cols = ['geolocation_state', 'geolocation_city', 'geolocation_lat', 'geolocation_lng']
chunk_size = 1000 

df_geolocation_filtered = pd.DataFrame(columns=geolocation_cols)

for chunk in pd.read_csv('../dataset/geolocation_dataset.csv', usecols=geolocation_cols, chunksize=chunk_size):
    filtered_chunk = chunk[chunk['geolocation_state'].isin(required_states)]
    df_geolocation_filtered = pd.concat([df_geolocation_filtered, filtered_chunk], ignore_index=True)
    
    if df_geolocation_filtered['geolocation_state'].nunique() >= len(required_states):
        break


brazil = mpimg.imread('../brazil-map.jpeg')

lng_min, lng_max = -73.98283055, -33.75116944  
lat_min, lat_max = -33.8, 5.4

df_top5_high_geo = pd.merge(top_5_high, df_geolocation_filtered, left_on='seller_state', right_on='geolocation_state', how='left')
df_top5_low_geo = pd.merge(top_5_low, df_geolocation_filtered, left_on='seller_state', right_on='geolocation_state', how='left')


df_top5_high_geo_filtered = df_top5_high_geo[
    (df_top5_high_geo['geolocation_lng'] >= lng_min) & (df_top5_high_geo['geolocation_lng'] <= lng_max) &
    (df_top5_high_geo['geolocation_lat'] >= lat_min) & (df_top5_high_geo['geolocation_lat'] <= lat_max)
]

df_top5_low_geo_filtered = df_top5_low_geo[
    (df_top5_low_geo['geolocation_lng'] >= lng_min) & (df_top5_low_geo['geolocation_lng'] <= lng_max) &
    (df_top5_low_geo['geolocation_lat'] >= lat_min) & (df_top5_low_geo['geolocation_lat'] <= lat_max)
]

col1, col2 = st.columns(2)

with col1:
    fig_high, ax_high = plt.subplots(figsize=(10, 10))
    ax_high.imshow(brazil, extent=[lng_min, lng_max, lat_min, lat_max]) 
    ax_high.scatter(df_top5_high_geo_filtered['geolocation_lng'], df_top5_high_geo_filtered['geolocation_lat'],
                    c='green', alpha=0.6, s=50, label='Pendapatan Tinggi')
    ax_high.set_title('Wilayah dengan Pendapatan Tertinggi')
    ax_high.axis('off') 
    ax_high.legend()

    st.pyplot(fig_high)

with col2:
    fig_low, ax_low = plt.subplots(figsize=(10, 10))
    ax_low.imshow(brazil, extent=[lng_min, lng_max, lat_min, lat_max]) 
 
    ax_low.scatter(df_top5_low_geo_filtered['geolocation_lng'], df_top5_low_geo_filtered['geolocation_lat'],
                   c='red', alpha=0.6, s=50, label='Pendapatan Rendah')
    ax_low.set_title('Wilayah dengan Pendapatan Terendah')
    ax_low.axis('off') 
    ax_low.legend()

    st.pyplot(fig_low)

st.divider()
st.title("jenis pembayaran yang sering digunakan pelanggan ?")

df_payment_type = df_real_tengkulak.groupby(by="payment_type").agg({
    "customer_id": "count",
}).reset_index()


fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_payment_type['payment_type'],
    y=df_payment_type['customer_id'],
    text=df_payment_type['customer_id'],  
    textposition='outside',  
    textfont=dict(
        color='black',  
    ),
    marker=dict(
        color='rgb(173, 216, 230)', 
    ),
))


fig.update_layout(
    title='Customer pembayaran type pada 2017 - 2018',
    xaxis=dict(title='Payment Type', tickangle=45),
    yaxis=dict(title='Total Customers'),
    showlegend=False,
    width=700,
    height=500,
)


st.plotly_chart(fig, use_container_width=True)

with st.expander("Deskripsi dibawah"):
   st.write("Jenis pembayaran yang paling banyak digunakan pelanggan adalah credit card dan juga boleto dengan jumlah transaksi sebanyak 8896 dan 2136 transaksi pada masing - masing jenis pembayaran tersbut.")
st.divider()

st.title("Kapan waktu yang paling banyak pelanggan yang melakukan transaksi ?")

df_product_sales = df_real_tengkulak.groupby(by="order_purchase_time").agg({
    "customer_id": "count"
}).sort_values(by="customer_id", ascending=False).reset_index()


fig = go.Figure(data=[
    go.Bar(x=df_product_sales['order_purchase_time'], y=df_product_sales['customer_id'], marker_color='rgb(173, 216, 230)')
])


fig.update_layout(
    title='Top 10 Best Worst Products 2017 - 2018',
    xaxis=dict(title='Order Purchase Time', tickangle=45),
    yaxis=dict(title='Total Sales'),
    showlegend=False
)


fig.update_traces(texttemplate='%{y}', textposition='outside')


st.plotly_chart(fig, use_container_width=True)

with st.expander("Deskripsi dibawah"):
   st.write("Grafik ini memberikan wawasan yang jelas tentang kapan pelanggan lebih cenderung melakukan pembelian, yang dapat membantu dalam strategi pemasaran dan penjadwalan kampanye promosi. Dengan fokus lebih pada waktu malam dan siang, perusahaan dapat mengoptimalkan upaya penjualannya untuk memaksimalkan pendapatan.")
st.divider()

st.title("Recency, Frequency, Monetary Analysis Customer")


current_date = df_real_tengkulak['order_purchase_timestamp'].max()

rfm = df_real_tengkulak.groupby('customer_id').agg({
    'order_purchase_timestamp': lambda x: (current_date - x.max()).days,  # Recency
    'order_id': 'nunique',  # Frequency
    'payment_value': 'sum'  # Monetary
}).reset_index()

rfm.columns = ['customer_id', 'Recency', 'Frequency', 'Monetary']


quantiles = rfm[['Recency', 'Frequency', 'Monetary']].quantile([0.25, 0.5, 0.75]).to_dict()

def rfm_score(x, metric, q_dict):
    if x <= q_dict[metric][0.25]:
        return 1
    elif x <= q_dict[metric][0.50]:
        return 2
    elif x <= q_dict[metric][0.75]:
        return 3
    else:
        return 4


rfm['R_score'] = rfm['Recency'].apply(rfm_score, args=('Recency', quantiles))
rfm['F_score'] = rfm['Frequency'].apply(rfm_score, args=('Frequency', quantiles))
rfm['M_score'] = rfm['Monetary'].apply(rfm_score, args=('Monetary', quantiles))


rfm['RFM_Segment'] = rfm['R_score'].map(str) + rfm['F_score'].map(str) + rfm['M_score'].map(str)


rfm['R_score'] = rfm['Recency'].rank(ascending=False)
rfm['F_score'] = rfm['Frequency'].rank(ascending=True)
rfm['M_score'] = rfm['Monetary'].rank(ascending=True)

rfm['R_score_norm'] = (rfm['R_score'] / rfm['R_score'].max()) * 100
rfm['F_score_norm'] = (rfm['F_score'] / rfm['F_score'].max()) * 100
rfm['M_score_norm'] = (rfm['F_score'] / rfm['M_score'].max()) * 100

rfm.drop(columns=['R_score', 'F_score', 'M_score'], inplace=True)


rfm['RFM_Score'] = 0.15 * rfm['R_score_norm'] + 0.28 * rfm['F_score_norm'] + 0.57 * rfm['M_score_norm']
rfm['RFM_Score'] *= 0.05
rfm = rfm.round(2)


rfm['Customer_segment'] = pd.cut(
    rfm['RFM_Score'], 
    bins=[0, 1.6, 3, 4, 4.5, 12],  
    labels=[
        'Lost Customers',           
        'Low Value Customers',      
        'Medium Value Customers',   
        'High Value Customers',     
        'Top Customers'             
    ],
    right=False 
)


segment_counts = rfm['Customer_segment'].value_counts().reset_index()
segment_counts.columns = ['Customer_segment', 'Count']


fig = px.bar(
    segment_counts, 
    x='Customer_segment', 
    y='Count', 
    color='Customer_segment',
    title='Customer Segment Distribution',
    labels={'Customer_segment': 'Customer Segment', 'Count': 'Number of Customers'},
    text='Count',  
    height=400
)

fig.update_layout(
    xaxis_tickangle=-45,  
    uniformtext_minsize=8, 
    uniformtext_mode='hide',  
    showlegend=False  
)


st.plotly_chart(fig, use_container_width=True)


with st.expander("Deskripsi dibawah"):
    st.write("Pelanggan dengan status 'Medium Value Customers' merupakan yang terbesar, dengan RFM score sebesar 4, menunjukkan bahwa mereka berada di tengah-tengah skala. Hal ini disebabkan oleh banyaknya pelanggan yang hanya melakukan transaksi sebanyak 4 kali. Di sisi lain, pelanggan yang tergolong 'Low Value Customer' memiliki RFM score di bawah 1.6, yang menunjukkan bahwa mereka hanya melakukan satu transaksi dan tidak pernah kembali untuk bertransaksi lagi selama periode 2017 hingga 2018.")