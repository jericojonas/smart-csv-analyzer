import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Konversi manual string ke float
def convert_to_float_safe(val):
    try:
        val = str(val).strip()
        val = val.replace('.', '').replace(',', '.')
        return float(val)
    except:
        return None

# Deteksi kolom numerik (asli dan yang tersembunyi sebagai teks)
def get_column_types(df):
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    
    for col in df.columns:
        if col not in numeric_cols:
            sample = df[col].dropna().astype(str).str.replace('.', '').str.replace(',', '.', regex=False)
            try:
                parsed = sample.astype(float)
                df[col] = df[col].apply(convert_to_float_safe)
                numeric_cols.append(col)
            except:
                continue
    return numeric_cols

def plot_column(df, col):
    plt.figure(figsize=(8, 4))
    if pd.api.types.is_numeric_dtype(df[col]):
        ax = sns.histplot(df[col].dropna(), kde=True)
        plt.title(f"Distribusi {col}")

        # Tambahkan label jumlah di atas batang histogram
        for patch in ax.patches:
            height = patch.get_height()
            if height > 0:
                ax.annotate(
                    f'{int(height)}',
                    xy=(patch.get_x() + patch.get_width() / 2, height),
                    xytext=(0, 2),  # jarak vertikal
                    textcoords='offset points',
                    ha='center', va='bottom',
                    fontsize=8, color='black'
                )

        # Tambahkan sedikit ruang di atas batang
        max_y = max([p.get_height() for p in ax.patches])
        ax.set_ylim(0, max_y * 1.15)

    else:
        ax = sns.countplot(y=col, data=df)
        plt.title(f"Frekuensi kategori {col}")

        # Tambahkan label jumlah di akhir batang horizontal
        for container in ax.containers:
            for bar in container:
                width = bar.get_width()
                if width > 0:
                    ax.annotate(
                        f'{int(width)}',
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(5, 0),  # jarak horizontal
                        textcoords='offset points',
                        ha='left', va='center',
                        fontsize=8, color='black'
                    )

        # Tambahkan ruang di sisi kanan agar label muat
        max_x = max([bar.get_width() for bar in ax.patches])
        ax.set_xlim(0, max_x * 1.15)

    st.pyplot(plt.gcf())
    plt.clf()

def show_full_summary(df, kolom):
    numeric_cols = get_column_types(df)
    st.write(f"### Ringkasan data kolom **{kolom}**")

    # Pilih kolom lain untuk XLOOKUP
    kolom_lain = [c for c in df.columns if c != kolom]
    default_index = kolom_lain.index("Login ID") if "Login ID" in kolom_lain else 0
    kolom_lookup = st.selectbox(
        "Pilih kolom lain untuk dilihat nilainya (mirip XLOOKUP):",
        kolom_lain,
        index=default_index
    )


    if kolom in numeric_cols:
        total = df[kolom].sum()
        maksimum = df[kolom].max()
        minimum = df[kolom].min()
        rata2 = df[kolom].mean()
        st.write(f"- Total (jumlah): {total}")
        st.write(f"- Nilai tertinggi (max): {maksimum}")
        st.write(f"- Nilai terendah (min): {minimum}")
        st.write(f"- Rata-rata (average): {rata2:.2f}")
        unik = df[kolom].nunique()
        st.write(f"- Jumlah data unik: {unik}")

        freq = df[kolom].value_counts(dropna=False).reset_index()
        freq.columns = [kolom, "Jumlah Muncul"]

        # Gabungkan dengan nilai dari kolom lookup
        contoh_data = df[[kolom, kolom_lookup]].drop_duplicates(subset=kolom).dropna()
        gabung = pd.merge(freq, contoh_data, on=kolom, how='left')
        gabung = gabung[[kolom, "Jumlah Muncul", kolom_lookup]]

        st.dataframe(gabung)
    else:
        st.write(f"⚠️ Kolom **{kolom}** bukan numerik, menampilkan jumlah data unik dan frekuensi kemunculan:")
        unik = df[kolom].nunique()
        st.write(f"- Jumlah data unik: {unik}")

        freq = df[kolom].value_counts(dropna=False).reset_index()
        freq.columns = [kolom, "Jumlah Muncul"]

        contoh_data = df[[kolom, kolom_lookup]].drop_duplicates(subset=kolom).dropna()
        gabung = pd.merge(freq, contoh_data, on=kolom, how='left')
        gabung = gabung[[kolom, "Jumlah Muncul", kolom_lookup]]

        st.dataframe(gabung)

def main():
    st.title("Analisis Data CSV - Fleksibel Format Angka")

    uploaded_file = st.file_uploader("Upload file CSV kamu", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("### Preview Data")
        st.dataframe(df.head())

        numeric_cols = get_column_types(df)
        all_cols = df.columns.tolist()

        st.write(f"Kolom Numerik (setelah deteksi): {numeric_cols}")
        st.write(f"Semua Kolom: {all_cols}")

        st.write("### Visualisasi Kolom")
        selected_col = st.selectbox("Pilih kolom untuk visualisasi", options=all_cols)
        plot_column(df, selected_col)

        st.write("---")
        st.write("### Ringkasan Lengkap Kolom")

        kolom_summary = st.selectbox("Pilih kolom untuk ringkasan lengkap", options=all_cols, key="summary_col")
        if kolom_summary:
            show_full_summary(df, kolom_summary)

if __name__ == "__main__":
    main()