import os

files = [
    'app.py',
    'pages/01_Home.py',
    'pages/02_Dataset.py',
    'pages/03_Visualisasi.py',
    'pages/04_Prediksi.py',
    'pages/05_Kesimpulan.py',
    'pages/06_Forecasting.py',
]

old = 'open("assets/style.css")'
new = 'open("assets/style.css", encoding="utf-8")'

for fpath in files:
    if not os.path.exists(fpath):
        print(f'SKIP (tidak ada): {fpath}')
        continue
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {fpath}')
    else:
        print(f'Skip (sudah fix): {fpath}')

print('Selesai!')
