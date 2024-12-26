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

def input_tanggal():
    while True:
        try:
            print("\nMasukkan tanggal turnamen:")
            tahun = int(input("Tahun (YYYY): "))
            bulan = int(input("Bulan (1-12): "))
            hari = int(input("Hari (1-31): "))
            return datetime(tahun, bulan, hari)
        except ValueError:
            print("Format tanggal tidak valid. Silakan coba lagi.")

def tampilkan_menu():
    print("\n=== SISTEM PERINGKAT BWF ===")
    print("1. Tambah Pemain Baru")
    print("2. Catat Hasil Turnamen")
    print("3. Lihat Peringkat")
    print("4. Keluar")
    return input("Pilih menu (1-4): ")

def main():
    bwf = SistemPemeringkatanBWF()
    
    while True:
        pilihan = tampilkan_menu()
        
        if pilihan == "1":
            print("\n=== TAMBAH PEMAIN BARU ===")
            nama = input("Masukkan nama pemain: ")
            negara = input("Masukkan kode negara (contoh: INA, MAS, CHN): ")
            
            if bwf.tambah_pemain(nama, negara):
                print(f"Pemain {nama} berhasil ditambahkan!")
            else:
                print("Pemain sudah terdaftar!")

        elif pilihan == "2":
            print("\n=== CATAT HASIL TURNAMEN ===")
            nama_pemain = input("Masukkan nama pemain: ")
            
            if nama_pemain in bwf.pemain:
                nama_turnamen = input("Nama turnamen: ")
                tanggal = input_tanggal()
                
                print("\nLevel Turnamen:")
                print("1. Super 1000 (12000 poin)")
                print("2. Super 750 (9000 poin)")
                print("3. Super 500 (7000 poin)")
                print("4. Super 300 (5000 poin)")
                level_pilihan = input("Pilih level turnamen (1-4): ")
                
                level_poin = {
                    "1": ("Super 1000", 12000),
                    "2": ("Super 750", 9000),
                    "3": ("Super 500", 7000),
                    "4": ("Super 300", 5000)
                }
                
                if level_pilihan in level_poin:
                    level, poin = level_poin[level_pilihan]
                    bwf.catat_hasil_turnamen(nama_pemain, nama_turnamen, tanggal, poin, level)
                    print("Hasil turnamen berhasil dicatat!")
                else:
                    print("Level turnamen tidak valid!")
            else:
                print("Pemain tidak ditemukan!")

        elif pilihan == "3":
            print("\n=== PERINGKAT DUNIA BWF ===")
            peringkat = bwf.dapatkan_peringkat()
            
            if peringkat:
                print("\nPERINGKAT DUNIA BWF")
                print("-" * 50)
                for pemain in peringkat:
                    print(f"Peringkat {pemain['peringkat']}: {pemain['nama']} ({pemain['negara']})")
                    print(f"Total Poin: {pemain['poin']}")
                    print(f"Jumlah turnamen dalam 52 minggu terakhir: {pemain['jumlah_turnamen']}")
                    print("-" * 50)
            else:
                print("Belum ada data peringkat.")

        elif pilihan == "4":
            print("\nTerima kasih telah menggunakan sistem peringkat BWF!")
            break
            
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if _name_ == "_main_":
    main()
