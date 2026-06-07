# Design Guide — GDP Prediction App

## Color Palette

| Nama | Hex | Kegunaan |
|---|---|---|
| Primary Blue | `#3B5BA5` | Header, tombol, border utama |
| Dark Navy | `#1A1A2E` | Sidebar background, teks heading |
| Light Blue | `#D6E4F0` | Background info box, row alt tabel |
| Red | `#E74C3C` | Alert, nilai negatif, annotasi krisis |
| Green | `#27AE60` | Nilai positif, sukses |
| Gray | `#666666` | Teks sekunder, caption |

## Typography

- **Font utama:** Streamlit default (sans-serif)
- **Heading h1:** Bold, color `#3B5BA5`
- **Heading h2:** Bold, color `#1A1A2E`
- **Body:** Regular, 16px
- **Caption:** 12px, color `#666666`

## Komponen UI

### Info Box
```html
<div class='info-box'>
  <h4>Judul</h4>
  <p>Konten</p>
</div>
```
Background: `#D6E4F0` | Border-left: 4px solid `#3B5BA5`

### Result Box
```html
<div class='result-box'>
  <h2>Judul</h2>
  <h1>Nilai</h1>
</div>
```
Background: gradient `#3B5BA5` → `#2C4A8A` | Teks: putih

### Tombol Prediksi
- Background: `#3B5BA5`
- Hover: `#2C4A8A`
- Padding: 0.5rem 2rem
- Border-radius: 8px

## Layout Halaman

| Halaman | Layout |
|---|---|
| Home | Full width, 3 kolom info box di atas |
| Dataset | Full width, tabel + statistik |
| Visualisasi | Full width, tab navigasi 4 tab |
| Prediksi | 2 kolom input + full width output |
| Kesimpulan | Full width, tabel + chart |

## Sidebar
- Background: gradient `#1A1A2E` → `#3B5BA5`
- Teks: putih
- Logo/icon: emoji 📊
