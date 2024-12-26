import heapq
import math

class Tempat:
    def __init__(self, nama, rating, latitude, longitude):
        self.nama = nama
        self.rating = rating
        self.latitude = latitude
        self.longitude = longitude

    def jarak_dari(self, user_lat, user_lon):
        # Rumus Haversine untuk menghitung jarak antara dua koordinat (dalam km)
        radius = 6371  # Jari-jari Bumi dalam km
        lat1, lon1, lat2, lon2 = map(math.radians, [user_lat, user_lon, self.latitude, self.longitude])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return radius * c

    def __lt__(self, other):
        # Membandingkan tempat berdasarkan rating, jika sama dibedakan dengan jarak
        return self.rating > other.rating

def cari_tempat_terbaik_iteratif(user_lat, user_lon, tempat, top_n=5):
    # Menggunakan heapq untuk mengimplementasikan pendekatan iteratif
    heap = []

    for t in tempat:
        jarak = t.jarak_dari(user_lat, user_lon)
        heapq.heappush(heap, (-t.rating, jarak, t))

    tempat_terbaik = []
    for _ in range(min(top_n, len(heap))):
        _, _, t = heapq.heappop(heap)
        tempat_terbaik.append(t)

    return tempat_terbaik

def cari_tempat_terbaik_rekursif(user_lat, user_lon, tempat, index=0, heap=None, top_n=5):
    if heap is None:
        heap = []

    if index >= len(tempat):
        tempat_terbaik = []
        for _ in range(min(top_n, len(heap))):
            _, _, t = heapq.heappop(heap)
            tempat_terbaik.append(t)
        return tempat_terbaik

    t = tempat[index]
    jarak = t.jarak_dari(user_lat, user_lon)
    heapq.heappush(heap, (-t.rating, jarak, t))

    # Rekursi untuk tempat berikutnya
    return cari_tempat_terbaik_rekursif(user_lat, user_lon, tempat, index + 1, heap, top_n)

def utama(method="iteratif"):
    # Lokasi pengguna
    user_lat = -6.200000
    user_lon = 106.816666

    # Daftar tempat makan (nama, rating, latitude, longitude)
    tempat = [
        Tempat("Restoran A", 4.5, -6.201, 106.816),
        Tempat("Restoran B", 4.7, -6.202, 106.817),
        Tempat("Restoran C", 4.6, -6.203, 106.818),
        Tempat("Restoran D", 4.2, -6.204, 106.819),
        Tempat("Restoran E", 4.8, -6.205, 106.820),
    ]

    if method == "iteratif":
        tempat_terbaik = cari_tempat_terbaik_iteratif(user_lat, user_lon, tempat)
    elif method == "rekursif":
        tempat_terbaik = cari_tempat_terbaik_rekursif(user_lat, user_lon, tempat)
    else:
        print("Metode tidak valid. Pilih 'iteratif' atau 'rekursif'.")
        return

    print(f"Tempat terbaik yang direkomendasikan ({method} approach):")
    for t in tempat_terbaik:
        jarak = t.jarak_dari(user_lat, user_lon)
        print(f"{t.nama} (Rating: {t.rating}, Jarak: {jarak:.2f} km)")

if __name__ == "__main__":
    utama(method="iteratif")  # Ubah menjadi "rekursif" untuk menggunakan pendekatan rekursif
