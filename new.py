import pandas as pd
import random

# Excel dosyasını oku (dosya adını kendine göre değiştir)
df = pd.read_excel("iller.xlsx")

# "iller" sütununu listeye çevir
iller = df["iller"].dropna().tolist()

# Listeyi karışık sıraya sok
random.shuffle(iller)

# Ortadan ikiye böl
orta = len(iller) // 2
grup1 = iller[:orta]
grup2 = iller[orta:]

# Sonuçları DataFrame olarak göster
df_sonuc = pd.DataFrame({
    "Grup 1": pd.Series(grup1),
    "Grup 2": pd.Series(grup2)
})

print(df_sonuc)
