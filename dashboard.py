import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

st.set_page_config(
    page_title="Brazilian E-Commerce Public Dataset by Olist",
    page_icon="🛍️",
    layout="wide"

)

@st.cache_data
def load_data():
    df = pd.read_csv('all_data.csv')
    df['review_creation_date'] = pd.to_datetime(df['review_creation_date'])
    df['review_answer_timestamp'] = pd.to_datetime(df['review_answer_timestamp'])
    return df

df = load_data()

st.title("🛍️ Brazilian E-Commerce Public Dataset by Olist Analysis Dashboard")

# st.sidebar.header("Filters")
# date_range = st.sidebar.date_input(
#     "Select Date Range",
#     [df['review_creation_date'].min(), df['review_creation_date'].max()]
# )

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Orders", len(df["order_id"].unique()))

with col2:
    avg_rating = round(df["review_score"].mean(), 2)
    st.metric("Average Rating", avg_rating)

with col3:
    total_payment = round(df["payment_value"].sum(), 2)
    st.metric("Total Payment", f"${total_payment:,.2f}")

avg_payment = round(df["payment_value"].mean(), 2)
st.metric("Average Payment", f"${avg_payment:,.2f}")

# Review Score Analysis
st.subheader("Review Score Analysis")
review_counts = df['review_score'].value_counts().sort_index()
count_1_2 = review_counts.loc[1:2].sum()
count_4_5 = review_counts.loc[4:5].sum()

total_count = review_counts.sum()

percentage_1_2 = (count_1_2 / total_count) * 100
percentage_4_5 = (count_4_5 / total_count) * 100

percentages = [percentage_1_2, percentage_4_5]
labels = ['Rating 1-2 Bintang', 'Rating 4-5 Bintang']

fig, ax = plt.subplots(figsize=(10,6))
ax.bar(labels, percentages, color=['orange', 'green'])
ax.set_ylabel('Persentase (%)')
ax.set_title('Persentase Rating 1-2 Bintang vs. Rating 4-5 Bintang')
ax.set_ylim(0, 100)
for i, v in enumerate(percentages):
    ax.text(i, v + 2, f'{v:.2f}%', ha='center', fontweight='bold')
st.pyplot(fig)
plt.close()

# Payment Type Analysis
st.subheader("Payment Type Analysis")
payment_counts = df.groupby('payment_type')['order_id'].nunique().sort_values(ascending=False)

payment_counts = payment_counts.reset_index()
payment_counts.columns = ['Payment Type', 'Unique Order Count']

total_orders = payment_counts['Unique Order Count'].sum()

payment_counts['Percentage'] = (payment_counts['Unique Order Count'] / total_orders) * 100

fig, ax = plt.subplots(figsize=(12,6))
ax.bar(payment_counts['Payment Type'], payment_counts['Unique Order Count'], color=['orange', 'green', 'blue', 'purple',
                                                                                    'red'])
ax.set_title('Jumlah Transaksi Berdasarkan Metode Pembayaran')
ax.set_ylabel("Payment Type")
ax.set_xlabel("Unique Order Count")
plt.xticks(rotation=45)

ax.grid(axis='y')

for i,v in enumerate(payment_counts['Unique Order Count']):
    ax.text(i, v + 0.2, f"{v} ({payment_counts['Percentage'].iloc[i]:.1f}%)", ha='center', fontweight='bold')

plt.tight_layout()
st.pyplot(fig)
plt.close()
