# IMPORT LIBRARIES
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# LOAD DATA
pd.set_option('display.max_columns', None)

df = pd.read_csv('dayv1.csv')

# SIDEBAR
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>MARI GO-WES</h2>", unsafe_allow_html=True)
    
    st.image('logo.png', width=250)

    st.markdown("<footer style='text-align: center;'>©LimitMax - Taufiq Q.R.</footer>", unsafe_allow_html=True)

# HEADER
st.markdown("<h1 style='text-align: center;'>DASHBOARD PENYEWAAN SEPEDA TAHUN 2011-2012</h1>", unsafe_allow_html=True)
st.write('')

# DASHBOARD

# jumlahkan register di tahun 2011
cnt_2011 = df[df['yr'] == 2011]['cnt'].sum()
cnt_2012 = df[df['yr'] == 2012]['cnt'].sum()

# hitung persentase
persentase = round((cnt_2012 - cnt_2011) / cnt_2011 * 100 ,2)
# UBAH persentase menjadi string
persentase = str(persentase) + "%"

# hitung total penyewaan sepeda
total = cnt_2011 + cnt_2012

# visualisasi
col1, col2,col3 = st.columns(3)

with col1:
    st.metric(label='Total Penyewaan Sepeda', value=total)

with col2:
    st.metric(label='Jumlah Penyewaan Tahun 2011', value=cnt_2011)

with col3:
    st.metric(label='Jumlah Penyewaan Tahun 2012', value=cnt_2012, delta=persentase
        , delta_color='normal')

# =====================================================================================
# 1. sewa sepedat perbulan dan tahunnya
st.subheader('Jumlah Sewa bulan & Tahun 2011-2012')

# kalkulasi jumlah penyewa pertahunnya
yr = df['cnt'].groupby(df['yr']).sum()

# kalulasi jumlah penyewa perbulan
ren = df.groupby(['yr','mnth'])['cnt'].sum()

# visualisasi jumlah penyewa pertahunnya
color = ['#db5f57','#dbc257']

fig, ax = plt.subplots(nrows=1, ncols=2, 
                       figsize=(25,10))
# lineplot untuk perbulan
ax[0].set_title('Grafik Sewa Sepeda per Bulan', fontsize=25)
sns.lineplot(x=ren.index.get_level_values(1), y=ren.values, hue=ren.index.get_level_values(0), palette=color, marker='o', markersize=10, ax=ax[0])
ax[0].set_xlabel('Bulan', fontsize=15)
ax[0].set_ylabel('Jumlah Sewa', fontsize=15)
ax[0].set_xticks(np.arange(1,13))
ax[0].set_xticklabels(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
ax[0].set_yticks([0,25000, 50000, 75000,100000,125000,150000,175000,200000,225000])
ax[0].set_yticklabels(['0','25 Ribu', '50 Ribu', '75 Ribu', '100 Ribu', '125 Ribu', '150 Ribu', '175 Ribu', '200 Ribu', '225 Ribu'])
# tambahkan annotate
for i in range(0,2):
    for j in range(0,12):
        ax[0].annotate(format(ren.values[i*12+j], '.0f'),
                    (ren.index.get_level_values(1)[i*12+j], ren.values[i*12+j]),
                    ha = 'center',
                    va = 'center',
                    xytext = (0, 10),
                    textcoords = 'offset points')
ax[0].spines['top'].set_visible(False)

# barplot untuk pertahun
color2 = ['#ff9e81','#ff0000']
ax[1].set_title('Jumlah Sewa Sepeda per Tahun', fontsize=25)
sns.barplot(x=yr.index, y=yr.values, palette=color2, ax=ax[1])
ax[1].set_xlabel('Tahun', fontsize=15)
ax[1].set_ylabel('Jumlah Sewa', fontsize=15)
ax[1].set_yticks([0,250000, 500000,750000,1000000,1250000,1500000,1750000,2000000,2250000])
ax[1].set_yticklabels(['0', '250 Ribu','500 Ribu', '750 Ribu', '1 Juta', '1.25 Juta', '1.5 Juta', '1.75 Juta', '2 Juta', '2.25 Juta'])
# TAMPILKAN ANNOTATE
for p in ax[1].patches:
    ax[1].annotate(format(p.get_height(), '.0f'),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center',
                xytext = (0, 10),
                textcoords = 'offset points')
ax[1].spines['top'].set_visible(False)
ax[1].spines['right'].set_visible(False)

# tiglayout
plt.tight_layout()
st.pyplot(fig)

# =====================================================================================

# 2. Musim yang paling diminati
df['season'] = df['season'].replace([1,2,3,4],['Spring','Summer','Fall','Winter'])

st.subheader('Musim yang Paling Diminati')

# hitung
season = df['cnt'].groupby(df['season']).sum().sort_values(ascending=False)

# visualisasi
color3 = ['#dd2000','#ffe3d5','#ffe3d5','#ffe3d5']

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=season.index, y=season.values, palette=color3, ax=ax)
ax.set_title('Musim Bersepeda ', fontsize=15)
ax.set_xlabel('Musim', fontsize=15)
ax.set_ylabel('Jumlah Sewa', fontsize=15)
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.0f'),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center',
                xytext = (0, 10),
                textcoords = 'offset points')
ax.set_yticks([0, 250000,500000,750000,1000000,1250000])
ax.set_yticklabels(['0', '250 Ribu', '500 Ribu', '750 Ribu', '1 Juta', '1.25 Juta'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

# =====================================================================================

# 3. Hari orang-orang sering menyewa sepeda
st.subheader('Hari yang Paling Diminati')
df['weekday'] = df['weekday'].replace([0,1,2,3,4,5,6],['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'])

# hitung
day = df['cnt'].groupby(df['weekday']).sum().sort_values(ascending=False)

# color
hari = ['#162a10','#ceffbc','#ceffbc','#ceffbc','#ceffbc','#ceffbc','#ceffbc','#ceffbc']

# visualisasi
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=day.index, y=day.values, palette=hari, ax=ax)
ax.set_title('Hari dengan Jumlah Sewa Sepeda Terbanyak', fontsize=15)
ax.set_xlabel('Hari', fontsize=15)
ax.set_ylabel('Jumlah Sewa', fontsize=15)
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.0f'),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center',
                xytext = (0, 10),
                textcoords = 'offset points')
ax.set_yticks([0, 100000,200000,300000,400000,500000,600000])
ax.set_yticklabels(['0', '100 Ribu', '200 Ribu', '300 Ribu', '400 Ribu', '500 Ribu', '600 Ribu'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

# =====================================================================================


# 4. Kondisi cuaca yang paling diminati orang-orang menggunakan sepeda?
st.subheader('Kondisi Cuaca yang Paling Diminati')
df['weathersit'] = df['weathersit'].replace([1,2,3,4],['Clear','Mist+Cloud','Light Snow','Heavy Rain'])

# hitung
weather = df['cnt'].groupby(df['weathersit']).sum().sort_values(ascending=False)

cuaca = ['#00ffff', '#e7ffff', '#e7ffff', '#e7ffff']
# visualisasi
fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(x=weather.index, y=weather.values, palette=cuaca, ax=ax)
ax.set_title('Kondisi Cuaca yang Paling Diminati', fontsize=15)
ax.set_xlabel('Kondisi Cuaca', fontsize=15)
ax.set_ylabel('Jumlah Sewa', fontsize=15)
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.0f'),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha = 'center',
                va = 'center',
                xytext = (0, 10),
                textcoords = 'offset points')
ax.set_yticks([0, 500000,1000000,1500000,2000000,2500000,3000000])
ax.set_yticklabels(['0', '500 Ribu', '1 Juta', '1.5 Juta', '2 Juta', '2.5 Juta', '3 Juta'])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

# =====================================================================================


# 5. kondisi suhu dan kelembapan apa yang paling banyak menyewa sepeda?
st.subheader('Kondisi Suhu dan Kelembapan yang Paling Diminati')
suhu = df['cnt'].groupby(df['temp']).sum().sort_values(ascending=False)
kelem = df['cnt'].groupby(df['hum']).sum().sort_values(ascending=False)

colorsuhu = ['#71bebd','#e7ffff','#e7ffff','#e7ffff','#e7ffff','#e7ffff']
colorkel = ['#25a2a2','#e7ffff','#e7ffff','#e7ffff','#e7ffff','#e7ffff']
# visualisasi 5 suhu teratas
fig, ax = plt.subplots(nrows=1, ncols=2, 
                       figsize=(25,10))

ax[0].set_title('Jumlah Sewa Sepeda per Suhu', fontsize=25)
# barplot untuk suhu
sns.barplot(x=suhu.index[:5], y=suhu.values[:5], palette=colorsuhu, ax=ax[0],order=suhu.index[:5])

ax[0].set_xlabel('Suhu', fontsize=15)
ax[0].set_ylabel('Jumlah Sewa', fontsize=15)
ax[0].set_yticks([0,5000,10000,15000,20000,25000])
ax[0].set_yticklabels(['0', '5 Ribu', '10 Ribu', '15 Ribu', '20 Ribu', '25 Ribu'])
ax[0].spines['top'].set_visible(False)
ax[0].spines['right'].set_visible(False)

ax[1].set_title('Jumlah Sewa Sepeda per Kelembapan', fontsize=25)
# barplot untuk kelembapan
sns.barplot(x=kelem.index[:5], y=kelem.values[:5], palette=colorkel, ax=ax[1], order=kelem.index[:5])
ax[1].set_xlabel('Kelembapan', fontsize=15)
ax[1].set_ylabel('Jumlah Sewa', fontsize=15)
ax[1].set_yticks([0,5000,10000,15000,20000,25000])
ax[1].set_yticklabels(['0', '5 Ribu', '10 Ribu', '15 Ribu', '20 Ribu', '25 Ribu'])
ax[1].spines['top'].set_visible(False)
ax[1].spines['right'].set_visible(False)

plt.tight_layout()
st.pyplot(fig)

