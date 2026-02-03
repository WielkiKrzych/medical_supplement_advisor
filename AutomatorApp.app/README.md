# Medical Supplement Advisor - macOS .app

## Jak używać aplikacji?

### Otwieranie aplikacji
1. **Przenieś .app do folderu Applications** (opcjonalnie, ale zalecane):
   ```bash
   mv AutomatorApp.app /Applications/MedicalSupplementAdvisor.app
   ```

2. **Uruchom aplikację**:
   - Kliknij dwukrotnie na `AutomatorApp.app`
   - Lub użyj terminala: `open AutomatorApp.app`

### Co się stanie?
- Aplikacja otworzy **okno graficzne (GUI)**
- Możesz wybrać plik z wynikami badań:
  - **JSON** (stary format)
  - **PDF** z tabelami wyników badań
  - **DOCX** z tabelami wyników badań

### Jak używać GUI?
1. Kliknij "Wybierz plik z wynikami badań"
2. Wybierz plik JSON, PDF lub DOCX
3. Aplikacja automatycznie:
   - Parsuje dane pacjenta
   - Parsuje wyniki badań krwi
   - Generuje rekomendacje suplementów
   - Zapisuje PDF w folderze `output/`

## Testowanie aplikacji

### Test CLI (wiersz poleceń)
```bash
# Z folderu projektu
cd /Users/wielkikrzych/medical-supplement-advisor

# Uruchom z przykładowym plikiem JSON
python3 -m src.main --json examples/sample_blood_tests.json

# Uruchom z plikiem DOCX
python3 -m src.main --document examples/sample_blood_tests.docx
```

### Test .app (GUI)
```bash
# Otwórz aplikację
open AutomatorApp.app
```

## Struktura .app bundle

```
AutomatorApp.app/
├── Contents/
│   ├── Info.plist           # Metadane aplikacji
│   ├── MacOS/
│   │   └── launcher         # Skrypt uruchamiający (executable)
│   └── Resources/
│       ├── src/             # Kod źródłowy
│       ├── data/            # Dane (reguły, suplementy)
│       ├── examples/        # Przykładowe pliki
│       ├── output/          # Wygenerowane PDF
│       └── config.py        # Konfiguracja
```

## Rozwiązywanie problemów

### Aplikacja nie otwiera się?
**Sprawdź uprawnienia:**
```bash
chmod +x AutomatorApp.app/Contents/MacOS/launcher
```

**Sprawdź logi:**
```bash
# Uruchom z terminala, aby zobaczyć błędy
./AutomatorApp.app/Contents/MacOS/launcher
```

### Błąd "ModuleNotFoundError"
Upewnij się, że masz zainstalowane wszystkie wymagane pakiety:
```bash
pip3 install -r requirements.txt
```

### GUI się nie otwiera?
Upewnij się, że masz zainstalowane PyQt5:
```bash
pip3 install PyQt5
```

## Wymagania systemowe

- macOS 10.13 lub nowszy
- Python 3.8+
- Zainstalowane pakiety Python:
  - PyQt5 (GUI)
  - python-docx (parsowanie DOCX)
  - pdfplumber (parsowanie PDF)
  - reportlab (generowanie PDF)

## Uwagi

- Aplikacja korzysta z **python3** (systemowy Python)
- Wszystkie dane są przechowywane wewnątrz .app bundle
- Wygenerowane PDF są zapisywane w `Resources/output/`
- Aplikacja działa w trybie GUI, gdy nie podano argumentów CLI
