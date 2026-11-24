# DUEL — NI23 G3 · akun19 · THE FRONT PAGE

## Konsep
Halaman depan koran lurus (bukan template dekoratif): masthead Playfair
Black raksasa, strip 6 angka, 12 kartu besar berilustrasi gambar-sendiri,
peta dunia titik-titik dengan 12 pin bernomor, timeline UTC 5 slot,
kolom ALSO ON bernomor 13–40, dan kotak DATE CHECK merah berisi 6 buangan
bernama + bertanggal. Total 40 cerita, 8 region, semua dari pool NI23.

Lead (kartu #1): #45 — Tentara AS akan meledakkan bahan peledak tak stabil
di Iowa (BBC). Trio pilihan builder: #43 Demokrat menangi DPR 258–173 dan
#25 India 720/9d di Wellington — dipilih karena keduanya membawa angka
paling keras hari itu dan menyeimbangkan lead Amerika dengan olahraga
Asia Selatan; enam angka strip (258-173 · 720/9d · 7+50 · 14 · $3,538 ·
Rs 28,000 cr) semuanya mengikat kartu.

## Tiga varian yang diadu
- A — putih terang · tinta merah tua · aksen hitam (palet akun19).
  Kontras tertinggi; judul kartu merah tua di atas putih terbaca paling
  jauh pada uji kecil.
- B — krem · tinta merah tua · aksen slate. Hangat, terasa seperti koran
  kertas tua, tetapi kontras judul turun dan strip angka kurang menonjol.
- C — putih · tinta hitam · pita tanggal merah tua. Masthead hitam kurang
  khas dibanding A; pita tanggal memakan ruang vertikal tanpa menambah
  informasi.

## Pemenang: A
Alasan: (1) palet persis yang ditugaskan untuk akun19; (2) pada uji 300px
masthead, tanggal, dan ke-12 judul kartu tetap terbaca, fakta kartu tidak
ada yang tertutup ikon/tag; (3) kontras merah tua–putih–hitam paling
tajam di antara tiga varian untuk papan peringkat yang dilihat sekilas.

## Uji wajib
- Uji 300px: LULUS — render final diperkecil ke 300×300
  (/tmp/ni23g3-akun19-300.png); masthead, tanggal, dan judul 12 kartu
  utama masih terbaca.
- entry.png: 299.037 byte (≤1.048.576), sha256
  57b58cf991b0b238a5b4850b52f4954d3d7158e6bb858bc06ca7e2dbdf851c0b,
  IHDR terverifikasi manual 1024×1024.
- Margin checker --fresh ni23-fresh.txt: 13/13 LOLOS.
- main.py dijalankan dua kali: keluaran byte-identik.

## Kenapa lebih kuat dari G2
Entry G2 akun19 memakai konsep "Api Unggun" — satu adegan dekoratif
tunggal. G3 menggantinya dengan halaman depan koran sungguhan: 40 cerita
terverifikasi tanggal dalam satu halaman, kepadatan data jauh lebih
tinggi, angka-angka kunci tampil besar di strip atas, dan setiap kartu
punya ilustrasi + tag sumber — sesuai temuan audit G3 bahwa bentuk
koran lurus dengan kartu besar yang terbaca di 300px adalah yang dinilai
juri, bukan dekorasi satu adegan.
