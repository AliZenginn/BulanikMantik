import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import messagebox

# 1. Bulanık değişkenler

# Girdiler
stres = ctrl.Antecedent(np.arange(0, 11, 1), 'stres')
uyku = ctrl.Antecedent(np.arange(0, 11, 1), 'uyku')
aktivite = ctrl.Antecedent(np.arange(0, 121, 1), 'aktivite')  # dakika
nabiz = ctrl.Antecedent(np.arange(40, 121, 1), 'nabiz')       # bpm
enerji = ctrl.Antecedent(np.arange(0, 11, 1), 'enerji')

# Çıktılar
sure = ctrl.Consequent(np.arange(0, 61, 1), 'sure')           # dakika
yontem = ctrl.Consequent(np.arange(0, 3, 1), 'yontem')

# 2. Üyelik fonksiyonları

# stres
stres['cok_az_stresli'] = fuzz.trimf(stres.universe, [0, 0, 2])
stres['az_stresli'] = fuzz.trimf(stres.universe, [1, 2, 4])
stres['orta_stresli'] = fuzz.trimf(stres.universe, [3, 5, 7])
stres['yuksek_stresli'] = fuzz.trimf(stres.universe, [6, 8, 9])
stres['cok_yuksek_stresli'] = fuzz.trimf(stres.universe, [8, 10, 10])

# uyku
uyku['kotu_uyku'] = fuzz.trimf(uyku.universe, [0, 0, 3])
uyku['orta_uyku'] = fuzz.trimf(uyku.universe, [2, 5, 7])
uyku['iyi_uyku'] = fuzz.trimf(uyku.universe, [6, 10, 10])

# aktivite
aktivite['dusuk_aktivite'] = fuzz.trimf(aktivite.universe, [0, 0, 40])
aktivite['orta_aktivite'] = fuzz.trimf(aktivite.universe, [30, 60, 90])
aktivite['yuksek_aktivite'] = fuzz.trimf(aktivite.universe, [80, 120, 120])

# nabiz
nabiz['dusuk_nabiz'] = fuzz.trimf(nabiz.universe, [40, 40, 60])
nabiz['normal_nabiz'] = fuzz.trimf(nabiz.universe, [55, 75, 95])
nabiz['yuksek_nabiz'] = fuzz.trimf(nabiz.universe, [90, 120, 120])

# enerji
enerji['cok_az_enerji'] = fuzz.trimf(enerji.universe, [0, 0, 2])
enerji['az_enerji'] = fuzz.trimf(enerji.universe, [1, 3, 5])
enerji['orta_enerji'] = fuzz.trimf(enerji.universe, [4, 6, 8])
enerji['yuksek_enerji'] = fuzz.trimf(enerji.universe, [7, 9, 10])
enerji['cok_yuksek_enerji'] = fuzz.trimf(enerji.universe, [9, 10, 10])

# sure (çıktı)
sure['cok_kisa'] = fuzz.trimf(sure.universe, [0, 0, 10])
sure['kisa'] = fuzz.trimf(sure.universe, [5, 15, 25])
sure['orta'] = fuzz.trimf(sure.universe, [20, 30, 40])
sure['uzun'] = fuzz.trimf(sure.universe, [35, 45, 55])
sure['cok_uzun'] = fuzz.trimf(sure.universe, [50, 60, 60])

# yontem (0=Nefes Egzersizi, 1=Meditasyon, 2=Hafif Egzersiz)
yontem['nefes_egzersizi'] = fuzz.trimf(yontem.universe, [0, 0, 1])
yontem['meditasyon'] = fuzz.trimf(yontem.universe, [0, 1, 2])
yontem['hafif_egzersiz'] = fuzz.trimf(yontem.universe, [1, 2, 2])

# 3. Kurallar (40 adet)

rule1 = ctrl.Rule(stres['cok_yuksek_stresli'] & uyku['kotu_uyku'], (yontem['meditasyon'], sure['cok_uzun']))
rule2 = ctrl.Rule(stres['cok_yuksek_stresli'] & uyku['orta_uyku'], (yontem['meditasyon'], sure['uzun']))
rule3 = ctrl.Rule(stres['cok_yuksek_stresli'] & uyku['iyi_uyku'], (yontem['meditasyon'], sure['orta']))

rule4 = ctrl.Rule(stres['yuksek_stresli'] & uyku['kotu_uyku'], (yontem['meditasyon'], sure['uzun']))
rule5 = ctrl.Rule(stres['yuksek_stresli'] & uyku['orta_uyku'], (yontem['nefes_egzersizi'], sure['orta']))
rule6 = ctrl.Rule(stres['yuksek_stresli'] & uyku['iyi_uyku'], (yontem['nefes_egzersizi'], sure['kisa']))

rule7 = ctrl.Rule(stres['orta_stresli'] & uyku['kotu_uyku'], (yontem['meditasyon'], sure['orta']))
rule8 = ctrl.Rule(stres['orta_stresli'] & uyku['orta_uyku'], (yontem['nefes_egzersizi'], sure['orta']))
rule9 = ctrl.Rule(stres['orta_stresli'] & uyku['iyi_uyku'], (yontem['hafif_egzersiz'], sure['orta']))

rule10 = ctrl.Rule(stres['az_stresli'] & uyku['kotu_uyku'], (yontem['nefes_egzersizi'], sure['kisa']))
rule11 = ctrl.Rule(stres['az_stresli'] & uyku['orta_uyku'], (yontem['hafif_egzersiz'], sure['kisa']))
rule12 = ctrl.Rule(stres['az_stresli'] & uyku['iyi_uyku'], (yontem['hafif_egzersiz'], sure['kisa']))

rule13 = ctrl.Rule(stres['cok_az_stresli'] & uyku['kotu_uyku'], (yontem['nefes_egzersizi'], sure['cok_kisa']))
rule14 = ctrl.Rule(stres['cok_az_stresli'] & uyku['orta_uyku'], (yontem['nefes_egzersizi'], sure['cok_kisa']))
rule15 = ctrl.Rule(stres['cok_az_stresli'] & uyku['iyi_uyku'], (yontem['hafif_egzersiz'], sure['cok_kisa']))

rule16 = ctrl.Rule(aktivite['dusuk_aktivite'] & enerji['cok_az_enerji'], (yontem['nefes_egzersizi'], sure['uzun']))
rule17 = ctrl.Rule(aktivite['dusuk_aktivite'] & enerji['az_enerji'], (yontem['meditasyon'], sure['uzun']))
rule18 = ctrl.Rule(aktivite['dusuk_aktivite'] & enerji['orta_enerji'], (yontem['meditasyon'], sure['orta']))
rule19 = ctrl.Rule(aktivite['dusuk_aktivite'] & enerji['yuksek_enerji'], (yontem['nefes_egzersizi'], sure['orta']))
rule20 = ctrl.Rule(aktivite['dusuk_aktivite'] & enerji['cok_yuksek_enerji'], (yontem['hafif_egzersiz'], sure['kisa']))

rule21 = ctrl.Rule(aktivite['orta_aktivite'] & enerji['cok_az_enerji'], (yontem['meditasyon'], sure['uzun']))
rule22 = ctrl.Rule(aktivite['orta_aktivite'] & enerji['az_enerji'], (yontem['meditasyon'], sure['orta']))
rule23 = ctrl.Rule(aktivite['orta_aktivite'] & enerji['orta_enerji'], (yontem['nefes_egzersizi'], sure['orta']))
rule24 = ctrl.Rule(aktivite['orta_aktivite'] & enerji['yuksek_enerji'], (yontem['hafif_egzersiz'], sure['kisa']))
rule25 = ctrl.Rule(aktivite['orta_aktivite'] & enerji['cok_yuksek_enerji'], (yontem['hafif_egzersiz'], sure['cok_kisa']))

rule26 = ctrl.Rule(aktivite['yuksek_aktivite'] & enerji['cok_az_enerji'], (yontem['meditasyon'], sure['orta']))
rule27 = ctrl.Rule(aktivite['yuksek_aktivite'] & enerji['az_enerji'], (yontem['meditasyon'], sure['kisa']))
rule28 = ctrl.Rule(aktivite['yuksek_aktivite'] & enerji['orta_enerji'], (yontem['hafif_egzersiz'], sure['kisa']))
rule29 = ctrl.Rule(aktivite['yuksek_aktivite'] & enerji['yuksek_enerji'], (yontem['hafif_egzersiz'], sure['cok_kisa']))
rule30 = ctrl.Rule(aktivite['yuksek_aktivite'] & enerji['cok_yuksek_enerji'], (yontem['hafif_egzersiz'], sure['cok_kisa']))

rule31 = ctrl.Rule(nabiz['dusuk_nabiz'] & stres['cok_yuksek_stresli'], (yontem['meditasyon'], sure['uzun']))
rule32 = ctrl.Rule(nabiz['normal_nabiz'] & stres['orta_stresli'], (yontem['nefes_egzersizi'], sure['orta']))
rule33 = ctrl.Rule(nabiz['yuksek_nabiz'] & stres['yuksek_stresli'], (yontem['nefes_egzersizi'], sure['kisa']))

rule34 = ctrl.Rule(nabiz['dusuk_nabiz'] & enerji['cok_az_enerji'], (yontem['meditasyon'], sure['uzun']))
rule35 = ctrl.Rule(nabiz['normal_nabiz'] & enerji['orta_enerji'], (yontem['hafif_egzersiz'], sure['orta']))
rule36 = ctrl.Rule(nabiz['yuksek_nabiz'] & enerji['yuksek_enerji'], (yontem['nefes_egzersizi'], sure['kisa']))

rule37 = ctrl.Rule(stres['cok_yuksek_stresli'] & enerji['cok_az_enerji'], (yontem['meditasyon'], sure['cok_uzun']))
rule38 = ctrl.Rule(stres['orta_stresli'] & enerji['orta_enerji'], (yontem['nefes_egzersizi'], sure['orta']))
rule39 = ctrl.Rule(stres['az_stresli'] & enerji['yuksek_enerji'], (yontem['hafif_egzersiz'], sure['kisa']))
rule40 = ctrl.Rule(stres['cok_az_stresli'] & enerji['cok_yuksek_enerji'], (yontem['hafif_egzersiz'], sure['cok_kisa']))

# Kontrol sistemi ve simülatör
stress_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,
                                  rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17,
                                  rule18, rule19, rule20, rule21, rule22, rule23, rule24, rule25,
                                  rule26, rule27, rule28, rule29, rule30, rule31, rule32, rule33,
                                  rule34, rule35, rule36, rule37, rule38, rule39, rule40])

stress_sim = ctrl.ControlSystemSimulation(stress_ctrl)


import tkinter as tk
from tkinter import messagebox

class StressApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Stres Yönetimi Bulanık Mantık Kontrolcüsü")
        self.geometry("500x400")
        self.resizable(False, False)
        self.configure(bg="#f0f4f8")

        self.entries = {}
        self.create_inputs()
        self.create_calculate_button()
        self.create_result_area()

    def create_inputs(self):
        # Input frame
        frame = tk.Frame(self, bg="#f0f4f8")
        frame.pack(pady=15)

        inputs = [
            ("Stres Seviyesi (0-10):", "stres"),
            ("Uyku Kalitesi (0-10):", "uyku"),
            ("Günlük Fiziksel Aktivite (dk, 0-120):", "aktivite"),
            ("Nabız (bpm, 40-120):", "nabiz"),
            ("Enerji Seviyesi (0-10):", "enerji"),
        ]

        for i, (label_text, key) in enumerate(inputs):
            label = tk.Label(frame, text=label_text, font=("Helvetica", 11), bg="#f0f4f8")
            label.grid(row=i, column=0, sticky="e", padx=5, pady=7)

            entry = tk.Entry(frame, width=7, font=("Helvetica", 11))
            entry.grid(row=i, column=1, padx=5, pady=7)
            self.entries[key] = entry

    def create_calculate_button(self):
        self.calc_button = tk.Button(self, text="Öneri Al", font=("Helvetica", 12, "bold"),
                                     bg="#4a90e2", fg="white", command=self.calculate)
        self.calc_button.pack(pady=10)

    def create_result_area(self):
        self.result_frame = tk.Frame(self, bg="#f0f4f8")
        self.result_frame.pack(pady=20, fill="x", padx=30)

        self.result_label = tk.Label(self.result_frame, text="", font=("Arial", 13, "bold"),
                                     bg="#f0f4f8", justify="center")
        self.result_label.pack()

        # Süre barı için canvas
        self.bar_canvas = tk.Canvas(self.result_frame, width=400, height=25, bg="#ddd", bd=0, highlightthickness=0)
        self.bar_canvas.pack(pady=12)

        # Yöntem etiketi
        self.method_label = tk.Label(self.result_frame, text="", font=("Helvetica", 12), bg="#f0f4f8")
        self.method_label.pack(pady=5)

    def calculate(self):
        try:
            stres_val = float(self.entries['stres'].get())
            uyku_val = float(self.entries['uyku'].get())
            aktivite_val = float(self.entries['aktivite'].get())
            nabiz_val = float(self.entries['nabiz'].get())
            enerji_val = float(self.entries['enerji'].get())

            if not (0 <= stres_val <= 10):
                raise ValueError("Stres seviyesi 0-10 arasında olmalı.")
            if not (0 <= uyku_val <= 10):
                raise ValueError("Uyku kalitesi 0-10 arasında olmalı.")
            if not (0 <= aktivite_val <= 120):
                raise ValueError("Fiziksel aktivite 0-120 dakika arasında olmalı.")
            if not (40 <= nabiz_val <= 120):
                raise ValueError("Nabız 40-120 bpm arasında olmalı.")
            if not (0 <= enerji_val <= 10):
                raise ValueError("Enerji seviyesi 0-10 arasında olmalı.")

            stress_sim.input['stres'] = stres_val
            stress_sim.input['uyku'] = uyku_val
            stress_sim.input['aktivite'] = aktivite_val
            stress_sim.input['nabiz'] = nabiz_val
            stress_sim.input['enerji'] = enerji_val

            stress_sim.compute()

            sure_val = stress_sim.output['sure']
            yontem_val = stress_sim.output['yontem']

            yontem_idx = int(round(yontem_val))
            yontem_adi = {0: "Nefes Egzersizi", 1: "Meditasyon", 2: "Hafif Egzersiz"}.get(yontem_idx, "Bilinmiyor")

            self.show_result(sure_val, yontem_adi, stres_val)

        except ValueError as e:
            messagebox.showerror("Girdi Hatası", str(e))
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

    def show_result(self, sure_val, yontem_adi, stres_val):
        # Sonuç metni
        self.result_label.config(
            text=f"Önerilen Rahatlama Süresi: {sure_val:.1f} dakika\n"
                 f"Önerilen Rahatlama Yöntemi: {yontem_adi}"
        )

        # Süre barını güncelle (maks 30 dk)
        self.bar_canvas.delete("all")
        max_sure = 30
        bar_length = 400
        fill_length = (sure_val / max_sure) * bar_length

        # Renk skalası stres seviyesine göre: düşük stres = yeşil, yüksek stres = kırmızı
        red = int(min(255, (stres_val / 10) * 255))
        green = int(min(255, (1 - stres_val / 10) * 255))
        color = f"#{red:02x}{green:02x}00"

        self.bar_canvas.create_rectangle(0, 0, fill_length, 25, fill=color, width=0)
        self.bar_canvas.create_text(bar_length/2, 12, text=f"{sure_val:.1f} dk", fill="white", font=("Helvetica", 12, "bold"))

        # Yöntem etiketi renkli gösterim
        colors = {
            "Nefes Egzersizi": "#5dade2",
            "Meditasyon": "#58d68d",
            "Hafif Egzersiz": "#f4d03f"
        }
        self.method_label.config(text=f"Önerilen Yöntem: {yontem_adi}", fg=colors.get(yontem_adi, "black"))


if __name__ == "__main__":
    app = StressApp()
    app.mainloop()

