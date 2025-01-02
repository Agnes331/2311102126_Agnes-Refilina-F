import time
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import List, Dict
import heapq

class Turnamen:
    def _init_(self, nama: str, tanggal: datetime, poin: int, level: str):
        self.nama = nama
        self.tanggal = tanggal
        self.poin = poin
        self.level = level

    def dalam_52_minggu(self, tanggal_sekarang: datetime) -> bool:
        selisih = tanggal_sekarang - self.tanggal
        return selisih.days <= 365

class Pemain:
    def _init_(self, nama: str, negara: str):
        self.nama = nama
        self.negara = negara
        self.daftar_turnamen: List[Turnamen] = []

    def tambah_turnamen(self, turnamen: Turnamen):
        self.daftar_turnamen.append(turnamen)

    def hitung_poin_peringkat(self, tanggal_sekarang: datetime) -> int:
        turnamen_valid = [
            t for t in self.daftar_turnamen
            if t.dalam_52_minggu(tanggal_sekarang)
        ]

        if len(turnamen_valid) <= 10:
            return sum(t.poin for t in turnamen_valid)
        else:
            poin_top_10 = heapq.nlargest(10, [t.poin for t in turnamen_valid])
            return sum(poin_top_10)

    def hitung_poin_rekursif(self, turnamen_index=0):
        if turnamen_index >= len(self.daftar_turnamen):
            return 0
        else:
            return (
                self.daftar_turnamen[turnamen_index].poin
                + self.hitung_poin_rekursif(turnamen_index + 1)
            )

    def hitung_poin_iteratif(self):
        return sum(t.poin for t in self.daftar_turnamen)

class SistemPemeringkatanBWF:
    def _init_(self):
        self.pemain: Dict[str, Pemain] = {}
        self.tanggal_sekarang = datetime.now()

    def tambah_pemain(self, nama: str, negara: str):
        if nama not in self.pemain:
            self.pemain[nama] = Pemain(nama, negara)
            return True
        return False

    def catat_hasil_turnamen(self, nama_pemain: str, nama_turnamen: str, 
                             tanggal: datetime, poin: int, level: str):
        if nama_pemain in self.pemain:
            turnamen = Turnamen(nama_turnamen, tanggal, poin, level)
            self.pemain[nama_pemain].tambah_turnamen(turnamen)
            return True
        return False

    def dapatkan_peringkat(self) -> List[Dict]:
        peringkat = []
        for pemain in self.pemain.values():
            total_poin = pemain.hitung_poin_peringkat(self.tanggal_sekarang)
            peringkat.append({
                'nama': pemain.nama,
                'negara': pemain.negara,
                'poin': total_poin,
                'jumlah_turnamen': len([t for t in pemain.daftar_turnamen 
                                          if t.dalam_52_minggu(self.tanggal_sekarang)])
            })

        peringkat.sort(key=lambda x: x['poin'], reverse=True)

        for i, pemain in enumerate(peringkat, 1):
            pemain['peringkat'] = i

        return peringkat

def ukur_waktu_iteratif(pemain: Pemain):
    start_time = time.time()
    pemain.hitung_poin_iteratif()
    return time.time() - start_time

def ukur_waktu_rekursif(pemain: Pemain):
    start_time = time.time()
    pemain.hitung_poin_rekursif()
    return time.time() - start_time

def simulasi_perbandingan():
    pemain = Pemain("Contoh", "INA")
    # Tambahkan turnamen
    for i in range(50):
        pemain.tambah_turnamen(Turnamen(f"Turnamen {i+1}", datetime.now() - timedelta(days=i * 10), (i % 10 + 1) * 1000, "Super 500"))

    jumlah_turnamen = range(5, 55, 5)
    waktu_iteratif = []
    waktu_rekursif = []

    print("\nSimulasi Perbandingan Waktu:")
    print(f"{'Jumlah Turnamen':<20}{'Iteratif (detik)':<20}{'Rekursif (detik)'}")

    for n in jumlah_turnamen:
        pemain.daftar_turnamen = pemain.daftar_turnamen[:n]
        waktu_iter = ukur_waktu_iteratif(pemain)
        waktu_rekur = ukur_waktu_rekursif(pemain)

        waktu_iteratif.append(waktu_iter)
        waktu_rekursif.append(waktu_rekur)

        print(f"{n:<20}{waktu_iter:<20.6f}{waktu_rekur:<20.6f}")

    plt.figure(figsize=(10, 6))
    plt.plot(jumlah_turnamen, waktu_iteratif, label="Iteratif", marker="o")
    plt.plot(jumlah_turnamen, waktu_rekursif, label="Rekursif", marker="x")
    plt.title("Perbandingan Running Time: Iteratif vs Rekursif")
    plt.xlabel("Jumlah Turnamen")
    plt.ylabel("Waktu Eksekusi (detik)")
    plt.legend()
    plt.grid()
    plt.show()

def main():
    bwf = SistemPemeringkatanBWF()

    # Tambahkan pemain pertama dan turnamen
    bwf.tambah_pemain("Kevin Sanjaya", "INA")
    bwf.catat_hasil_turnamen("Kevin Sanjaya", "All England", datetime.now() - timedelta(days=30), 12000, "Super 1000")
    bwf.catat_hasil_turnamen("Kevin Sanjaya", "Japan Open", datetime.now() - timedelta(days=90), 9000, "Super 750")
    bwf.catat_hasil_turnamen("Kevin Sanjaya", "Indonesia Open", datetime.now() - timedelta(days=60), 11000, "Super 1000")
    bwf.catat_hasil_turnamen("Kevin Sanjaya", "Denmark Open", datetime.now() - timedelta(days=120), 8500, "Super 750")
    bwf.catat_hasil_turnamen("Kevin Sanjaya", "Thailand Open", datetime.now() - timedelta(days=150), 8000, "Super 500")

    # Tambahkan pemain kedua dan turnamen
    bwf.tambah_pemain("Anthony Sinisuka Ginting", "INA")
    bwf.catat_hasil_turnamen("Anthony Sinisuka Ginting", "All England", datetime.now() - timedelta(days=30), 12000, "Super 1000")
    bwf.catat_hasil_turnamen("Anthony Sinisuka Ginting", "Japan Open", datetime.now() - timedelta(days=90), 9000, "Super 750")
    bwf.catat_hasil_turnamen("Anthony Sinisuka Ginting", "Indonesia Open", datetime.now() - timedelta(days=60), 11000, "Super 1000")
    bwf.catat_hasil_turnamen("Anthony Sinisuka Ginting", "Denmark Open", datetime.now() - timedelta(days=120), 8500, "Super 750")


    # Tambahkan pemain ketiga dan turnamen
    bwf.tambah_pemain("Kento Momota", "JPN")
    bwf.catat_hasil_turnamen("Kento Momota", "All England", datetime.now() - timedelta(days=30), 12000, "Super 1000")
    bwf.catat_hasil_turnamen("Kento Momota", "Japan Open", datetime.now() - timedelta(days=90), 9000, "Super 750")
    bwf.catat_hasil_turnamen("Kento Momota", "Indonesia Open", datetime.now() - timedelta(days=60), 11000, "Super 1000")


    # Tampilkan peringkat
    print("\n=== PERINGKAT DUNIA BWF ===")
    peringkat = bwf.dapatkan_peringkat()
    for pemain in peringkat:
        print(f"Peringkat {pemain['peringkat']}: {pemain['nama']} ({pemain['negara']})")
        print(f"Total Poin: {pemain['poin']}")
        print(f"Jumlah turnamen dalam 52 minggu terakhir: {pemain['jumlah_turnamen']}")
        print("-" * 50)

    # Simulasi perbandingan waktu
    print("\n=== SIMULASI PERBANDINGAN WAKTU ===")
    simulasi_perbandingan()

if _name_ == "_main_":
    main()
