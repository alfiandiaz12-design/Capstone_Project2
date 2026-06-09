#%%
import pandas as pd
import numpy as np
import seaborn as sns
%matplotlib inline
import matplotlib.pyplot as plt 
import matplotlib.ticker as ticker
df = pd.read_csv(r'C:\Users\user\Downloads\marketing_campaign.csv', sep='\t')

# %%
df.info()

#%%
#Histogram
df.hist(figsize=(15,10), bins=30, edgecolor='black')
plt.tight_layout()
plt.show()

# %%
df['Income'].isna().sum()

#%%
#Heatmap
df_numerik = df.select_dtypes(include=['number'])
cor_matriks = df_numerik.corr(method='spearman')
plt.figure(figsize=(16,10))
sns.heatmap(cor_matriks, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Heatmap Korelasi Kolom Numerik', fontsize=16)
plt.show()

# %%
print(df['Z_CostContact'].value_counts())
print(df['Z_Revenue'].value_counts())

#%%
#Drop Z_CostContact dan Z_Revenue
df = df.drop(columns=['Z_CostContact', 'Z_Revenue'])

# %%
df['Marital_Status'].value_counts()

# %%
#Hapus klasifikasi Marital_Status
index_buang = df[df['Marital_Status'].isin(['Absurd', 'YOLO', 'Alone'])].index
df = df.drop(index_buang)

#%%
#Merged Together --> Married
marital_map = { 'Together': 'Married'}
df['Marital_Status'] = df['Marital_Status'].replace(marital_map)

#%%
df['Marital_Status'].unique()

#%%
#Mapping Education
edu_map =  {'Basic': 'Bachelor', '2n Cycle': 'Magister', 'Master': 'Magister'}
df['Education'] = df['Education'].replace(edu_map)

#%%
df['Education'].unique()

# %%
#Korelasi Income
p = 'Income'
corr_series = df.select_dtypes(include='number').corr(method='spearman')[[p]].drop(index=p)
plt.figure(figsize=(3,8))
sns.heatmap(corr_series, annot=True, fmt='.2f', cmap='coolwarm', center=0, vmin=-1, vmax=1, linewidths=0.5)
plt.title(f"Korelasi Income")
plt.tight_layout
plt.show()

#%%
#Groupby Mean Marital_Status
df.groupby('Marital_Status')['Income'].mean().round(2).sort_values()

#%%
#Groupby Mean Education
df.groupby('Education')['Income'].mean().round(2).sort_values()

#%%
#Groupby Mean Kidhome
df.groupby('Kidhome')['Income'].mean().round(2).sort_values()

#%%
#Groupby Mean Teenhome
df.groupby('Teenhome')['Income'].mean().round(2).sort_values()

#%%
#Isi Missing Values Income
df['Income'] = df.groupby(['Marital_Status', 'Education', 'Kidhome', 'Teenhome'])['Income'].transform(
    lambda x: x.fillna(x.median())
)

#%%
#Isi 1 Missing Values yang tersisa
df['Income'] = df.groupby(['Education', 'Kidhome'])['Income'].transform(
    lambda x: x.fillna(x.median())
)

'''------------------------------------------------------------------------------------------------'''
'''SEGMENTATION'''

#%%
"""Segmentasi Income"""
p33 = df['Income'].quantile(0.33)
p67 = df['Income'].quantile(0.67)

print(f'Low : < {p33:.1f}')
print(f'Mid: {p33:.1f} - {p67:.1f}')
print(f'High: > {p67:.1f}')

df['Income_Segment'] = pd.cut(
    df['Income'],
    bins=[df['Income'].min(), p33, p67, df['Income'].max()],
    labels=['Low', 'Mid', 'High'],
    include_lowest=True
)

#%%
print(df.groupby('Income_Segment')['Income'].mean())

#%%
print(df['Income_Segment'].value_counts().sort_index())

#%%
'''Segmentasi Kidhome & Teenhome (Mixed Child)'''
Mixed_Child = [
    ((df['Kidhome'] == 0) & (df['Teenhome'] == 0)),
    ((df['Kidhome'] == 1)  & (df['Teenhome'] == 1)),
    ((df['Kidhome'] == 1) & (df['Teenhome'] == 2)),
    ((df['Kidhome'] == 2) & (df['Teenhome'] == 1))
]

kategori = ['No Child', 'Balance Mixed', 'Teen Dominant','Kid Dominant']
df['Child_Segment'] = np.select(Mixed_Child, kategori, default='Other')


#%%
print(df['Child_Segment'].value_counts())


'''------------------------------------------------------------------------------------------------'''
'''INCOME SEGMENTATION CHART'''

#%%
'''100% Bar Chart (Persentase Pembelian Produk Terhadap Segmentasi Income)'''
produk = ['MntWines', 'MntMeatProducts', 'MntGoldProds', 'MntFishProducts', 'MntFruits', 'MntSweetProducts']
df_chart = df.groupby('Income_Segment')[produk].mean()

# Membagi nilai rata-rata setiap produk dengan total rata-rata pembelian di segmen tersebut
df_persen = df_chart.div(df_chart.sum(axis=1), axis=0) * 100
ax = df_persen.plot(kind='bar', stacked=True, figsize=(10, 8), width=0.7)

#Menambahkan label persentase
for container in ax.containers:
    # Hanya menampilkan label jika persentase cukup besar agar teks tidak bertumpuk
    labels = [f'{v.get_height():.2f}%' if v.get_height() > 2 else '' for v in container]
    ax.bar_label(container, labels=labels, label_type='center', color='white', fontsize=9, fontweight='bold')

plt.title('Persentase Pembelian Produk Terhadap Segmentasi Income', fontsize=14, pad=20)
plt.xlabel('Segmentasi Income', fontsize=12)
plt.ylabel('Proporsi Pembelian (%)', fontsize=12)
plt.legend(title='Kategori Produk', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# %%
'''Matrix (Rata-rata Income)'''
p = ['Income']
df[df['Income_Segment'].isin(['Low', 'Mid', 'High'])].groupby('Income_Segment')[p].mean().round(2).sort_values('Income')

#%%
'''Bar Chart (Frekuensi Pembelian per Channel Berdasarkan Segmentasi Income)'''
channels = ['NumWebPurchases','NumCatalogPurchases','NumStorePurchases']
groupby_income = df.groupby('Income_Segment')[channels].sum()

#Membuat Label
ax = groupby_income.plot(kind='barh', figsize=(10,6))
for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.title('Frekuensi Pembelian per Channel Berdasarkan Segmentasi Income')
plt.xlabel('Total Frekuensi Pembelian')
plt.ylabel('Segmentasi Income')
plt.legend(title='Channel')
plt.show()

#%%
'''Bar Chart (Rata-rata Kunjungan Website Perusahaan Berdasarkan Segmen Income)'''
deals = df.groupby('Income_Segment')['NumWebVisitsMonth'].mean()

#Membuat Label
ax = deals.plot(kind='bar', figsize=(10,9))
for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.title('Rata-rata Kunjungan Website Perusahaan Berdasarkan Segmen Income')
plt.xlabel('Income_Segment')
plt.xticks(rotation=0)
plt.ylabel('Total Frekuensi')
plt.legend(title='produk')
plt.show()

'''------------------------------------------------------------------------------------------------'''
'''KIDHOME CHART'''
#%%
'Matrix (Rata-rata Income per Kategori Kidhome)'
data = df.groupby(['Income_Segment', 'Kidhome'])['Income'].mean()
matrix= data.unstack()
print(matrix)

# %%
'''Matrix (Frekuensi Kidhome Berdasarkan Income Segment)'''
data = df.groupby(['Income_Segment', 'Kidhome'])['Kidhome'].count()
matrix = data.unstack()
print(matrix)

#%%
'''100% Bar Chart (Persentase Channel Pembelilan Terhadap Kidhome)'''
produk = ['NumWebPurchases','NumCatalogPurchases','NumStorePurchases']
chart = df.groupby('Kidhome')[produk].sum()

persentase = chart.div(chart.sum(axis=1), axis=0) * 100
ax = persentase.plot(kind= 'bar', stacked=True, figsize=(10,6), width=0.7)
for container in ax.containers:
    labels = [f'{v.get_height():.2f}%' if v.get_height() > 2 else '' for v in container]
    ax.bar_label(container, labels=labels, label_type='center', color='white', fontsize=9, fontweight='bold')

plt.title('Persentase Channel Pembelian Terhadap Kidhome')
plt.xlabel('Kidhome')
plt.ylabel('Channel')
plt.legend(title='Channel', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#%%
'''Bar Chart (Frekuensi Pembelian Produk Berdasarkan Kidhome)'''
produk = ['MntWines', 'MntMeatProducts', 'MntGoldProds', 'MntFishProducts', 'MntFruits', 'MntSweetProducts']
groupby_kidhome = df.groupby('Kidhome')[produk].sum()

#Membuat Label
ax = groupby_kidhome.plot(kind='bar', figsize=(19,9))
for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.title('Frekuensi Pembelian Produk Berdasarkan Kidhome')
plt.xlabel('Kidhome')
plt.xticks(rotation=0)
plt.ylabel('Total Frekuensi')
plt.legend(title='produk')
plt.show()


'''------------------------------------------------------------------------------------------------'''
'''TEENHOME CHART'''
#%%
'Matrix (Rata-rata Income per Kategori Teenhome)'
data = df.groupby(['Income_Segment', 'Teenhome'])['Income'].mean()
matrix= data.unstack()
print(matrix)

# %%
'''Matrix (Frekuensi Teenhome Berdasarkan Income Segment)'''
data = df.groupby(['Income_Segment', 'Teenhome'])['Teenhome'].count()
matrix = data.unstack()
print(matrix)

#%%
'''100% Bar Chart (Persentase Channel Pembelilan Terhadap Teenhome)'''
produk = ['NumWebPurchases','NumCatalogPurchases','NumStorePurchases']
chart = df.groupby('Teenhome')[produk].sum()

persentase = chart.div(chart.sum(axis=1), axis=0) * 100
ax = persentase.plot(kind= 'bar', stacked=True, figsize=(10,6), width=0.7)
for container in ax.containers:
    labels = [f'{v.get_height():.2f}%' if v.get_height() > 2 else '' for v in container]
    ax.bar_label(container, labels=labels, label_type='center', color='white', fontsize=9, fontweight='bold')

plt.title('Persentase Channel Pembelian Terhadap Teenhome')
plt.xlabel('Teenhome')
plt.ylabel('Channel')
plt.legend(title='Channel', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

#%%
'''Bar Chart (Frekuensi Pembelian Produk Berdasarkan Teenhome)'''
produk = ['MntWines', 'MntMeatProducts', 'MntGoldProds', 'MntFishProducts', 'MntFruits', 'MntSweetProducts']
groupby_Teenhome = df.groupby('Teenhome')[produk].sum()

#Membuat Label
ax = groupby_Teenhome.plot(kind='bar', figsize=(19,9))
for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.title('Frekuensi Pembelian Produk Berdasarkan Teenhome')
plt.xlabel('Teenhome')
plt.xticks(rotation=0)
plt.ylabel('Total Frekuensi')
plt.legend(title='produk')
plt.show()


'''------------------------------------------------------------------------------------------------'''
'''MIXED CHILD CHART'''

#%%
'''Matrix (Rata-rata Income Child Mixed) '''
data = df.groupby(['Income_Segment', 'Child_Segment'])['Income'].mean()
matrix = data.unstack()
print(matrix)

# %%
'''Matrix (Frekuensi Mixed Child Berdasarkan Income Segment)'''
data = df.groupby(['Income_Segment', 'Child_Segment'])['Teenhome'].count()
matrix = data.unstack()
print(matrix)

#%%
'''100% Bar Chart (Persentase Channel Pembelilan Terhadap Mixed Child)'''
produk = ['NumWebPurchases','NumCatalogPurchases','NumStorePurchases']
chart = df.groupby('Child_Segment')[produk].sum()

persentase = chart.div(chart.sum(axis=1), axis=0) * 100
ax = persentase.plot(kind= 'bar', stacked=True, figsize=(10,6), width=0.7)
for container in ax.containers:
    labels = [f'{v.get_height():.2f}%' if v.get_height() > 2 else '' for v in container]
    ax.bar_label(container, labels=labels, label_type='center', color='white', fontsize=9, fontweight='bold')

plt.title('Persentase Channel Pembelian Terhadap Mixed Child')
plt.xlabel('Child_Segment')
plt.ylabel('Channel')
plt.legend(title='Channel', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# %%
'''Bar Chart (Frekuensi Pembelian Produk Berdasarkan Mixed Child)'''
produk = ['MntWines', 'MntMeatProducts', 'MntGoldProds', 'MntFishProducts', 'MntFruits', 'MntSweetProducts']
groupby_Child = df.groupby('Child_Segment')[produk].sum()

groupby_Child['Total'] = groupby_Child.sum(axis=1)
groupby_Child = groupby_Child.sort_values('Total', ascending=False)
groupby_Child = groupby_Child.drop(columns=['Total'])

ax = groupby_Child.plot(kind='bar', figsize=(20, 10))
for container in ax.containers:
    ax.bar_label(container, padding=5, rotation=90, fontsize=9)

plt.title('Frekuensi Pembelian Produk Berdasarkan Mixed Child')
plt.xlabel('Mixed Child')
plt.xticks(rotation=0)
plt.ylabel('Total Frekuensi')
plt.legend(title='produk')
plt.tight_layout() 
plt.show()

#%%
df.to_csv('data_bersih_capstone2.csv', index=False)

