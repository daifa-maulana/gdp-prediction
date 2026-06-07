# Contributing Guide

## Branch Strategy

| Branch | Kegunaan |
|---|---|
| `main` | Kode production, hanya PM yang merge |
| `develop` | Branch pengembangan utama |
| `feature/data-analysis` | Data collection, EDA, preprocessing, modeling |
| `feature/ui-ux` | Wireframe, design guide, CSS |
| `feature/frontend` | Implementasi halaman Streamlit |
| `feature/backend` | Logika prediksi, deployment |

## Alur Kerja

1. **Selalu pull dari develop sebelum mulai kerja**
```bash
git checkout develop
git pull origin develop
git checkout feature/branch-kamu
git merge develop
```

2. **Commit dengan pesan yang jelas**
```bash
git commit -m "feat: tambah fungsi plot_gdp_trend di visualization.py"
git commit -m "fix: perbaiki error missing values di preprocessing"
git commit -m "docs: update README cara install"
```

3. **Push dan buat Pull Request ke develop**
```bash
git push origin feature/branch-kamu
# Buka GitHub → New Pull Request → base: develop
```

4. **PM melakukan review sebelum merge ke main**

## Format Commit

```
feat:   fitur baru
fix:    perbaikan bug
docs:   perubahan dokumentasi
style:  formatting, bukan perubahan logika
refactor: refactoring kode
test:   menambah atau mengubah test
```

## Checklist PR

- [ ] Kode berjalan tanpa error
- [ ] Sudah pull dari develop terbaru
- [ ] Nama file sesuai struktur proyek
- [ ] Tidak ada file sensitif (API key, password)
