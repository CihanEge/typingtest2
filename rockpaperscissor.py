import random
import time

# Seçenekler
secenekler = ["taş", "kağıt", "makas"]

print("Taş Kağıt Makas Oyununa Hoş Geldin!")
print("Seçenekler: taş, kağıt, makas")

# Oyuncudan seçim al
oyuncu_secimi = input("Seçiminizi yazın: ").lower()

# Hatalı giriş kontrolü
if oyuncu_secimi not in secenekler:
    print("Geçersiz seçim yaptınız. Lütfen taş, kağıt veya makas yazın.")
    exit()

# Oyuncu seçim yaptıktan sonra rakip de yapıyor
rakip_secimi = random.choice(secenekler)

# Efekt için bekleme (isteğe bağlı)
print("\nSeçimler yapıldı...")
time.sleep(0.5)

print("\nSEN:   {}".format(oyuncu_secimi))
print("RAKİP: {}".format(rakip_secimi))

# Kazanma kuralları
if oyuncu_secimi == rakip_secimi:
    print("\n🤝 Berabere!")
elif (
    (oyuncu_secimi == "taş" and rakip_secimi == "makas") or
    (oyuncu_secimi == "kağıt" and rakip_secimi == "taş") or
    (oyuncu_secimi == "makas" and rakip_secimi == "kağıt")
):
    print("\n🎉 Tebrikler! Yendin!")
else:
    print("\n😢 Maalesef yenildin.")
