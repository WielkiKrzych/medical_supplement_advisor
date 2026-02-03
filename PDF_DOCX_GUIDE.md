# 📚 Jak używać Medical Supplement Advisor z PDF/DOCX

## ✨ NOWA FUNKCJONALNOŚĆ: Automatyczne czytanie PDF i DOCX!

System teraz **automatycznie czyta** pliki PDF i DOCX z wynikami badań krwi! ✅

---

## 🚀 SZYBKI START (2 minuty)

### Opcja 1: GUI (Najprostszy) ⭐

```bash
cd medical-supplement-advisor
python src/main.py
```

1. **Kliknij "Przeglądaj..."**
2. **Wybierz plik** (PDF, DOCX lub JSON)
3. **Kliknij "Generuj raport PDF"**
4. **Gotowe!** Raport w folderze `output/`

### Opcja 2: CLI (Dla zaawansowanych)

```bash
# JSON
python src/main.py --json moje_badania.json

# PDF/DOCX (Nowość!)
python src/main.py --document moje_badania.pdf
python src/main.py --document moje_badania.docx
```

---

## 📋 OBSŁUGIWANE FORMATY PLIKÓW

| Format | Status | Opis |
|--------|--------|------|
| **JSON** | ✅ Pełna obsługa | Format strukturyzowany |
| **DOCX** | ✅ Automatyczny parsing | Word (preferowany) |
| **PDF** | ✅ Automatyczny parsing | Acrobat (dobry jakości) |

---

## 🎯 JAK DZIAŁA PARSOWANIE PDF/DOCX

### Krok 1: Wybierz plik z wynikami badań

```
Przykładowy plik: wyniki_badan_laboratoryjnych.pdf
```

### Krok 2: System automatycznie wyekstrahuje dane

**System szuka:**
- ✅ Dane pacjenta (imię, nazwisko, wiek, schorzenia)
- ✅ Wyniki badań (nazwa, wartość, jednostka)

**Obsługiwane struktury:**
```
Tabela 1: Dane pacjenta
├─ Imię: Jan
├─ Nazwisko: Kowalski
├─ Wiek: 45
└─ Schorzenia: osteoporoza

Tabela 2: Wyniki badań
├─ Witamina D (25-OH) | 22 ng/mL
├─ Witamina B12 | 150 pg/mL
├─ Żelazo | 45 ug/dL
└─ ...
```

### Krok 3: System analizuje wyniki

```
Witamina D: 22 ng/mL
    └─ Porównanie z normą (30-100 ng/mL)
    └─ Status: LOW (niski)
    └─ Rekomendacja: Witamina D3 2000 IU
```

### Krok 4: Generuje PDF z rekomendacjami

```
output/Jan_Kowalski_supplements.pdf
```

---

## 📁 STRUKTURA DOCX (Przykład)

Jeśli tworzysz własny DOCX, użyj tego formatu:

### Tabela 1: Dane pacjenta

| Imię | Nazwisko | Wiek | Schorzenia |
|------|----------|------|------------|
| Jan | Kowalski | 45 | osteoporoza |

### Tabela 2: Wyniki badań

| Badanie | Wartość | Jednostka |
|---------|---------|-----------|
| Witamina D (25-OH) | 22 | ng/mL |
| Witamina B12 | 150 | pg/mL |
| Żelazo | 45 | ug/dL |

---

## ⚙️ WYMAGANIA DLA PLIKÓW PDF/DOCX

### ✅ DOBRZE:
- Tabelaryczne formaty
- Czytelne nagłówki
- Jednolita struktura
- Standardowe jednostki

### ❌ UNIKAJ:
- Skanowane obrazy (nie będzie działało!)
- Chaos w formacie
- Brak nagłówków
- Niestandardowe jednostki

---

## 🔧 PRZYKŁADY UŻYCIA

### Przykład 1: Wyniki z laboratorium (PDF)

```bash
# Pobierz PDF z laboratorium
# Uruchom GUI
python src/main.py

# Wybierz PDF
# Wynik: Raport z rekomendacjami
```

### Przykład 2: Dokument lekarza (DOCX)

```bash
# Lekarz daje Ci DOCX
python src/main.py

# Wybierz DOCX
# Wynik: Personalizowane suplementy
```

### Przykład 3: Własne pomiary (JSON)

```json
{
  "patient": {
    "name": "Anna",
    "surname": "Nowak",
    "age": 35,
    "conditions": []
  },
  "blood_tests": [
    {"name": "Witamina D (25-OH)", "value": 18, "unit": "ng/mL"}
  ]
}
```

---

## 🐛 ROZWIĄZYWANIE PROBLEMÓW

### Problem: "Nie udało się sparsować dokumentu"

**Rozwiązanie:**
1. Sprawdź czy plik nie jest skanem (obrazem)
2. Upewnij się że ma czytelną strukturę tabelaryczną
3. Spróbuj przekonwertować PDF na DOCX
4. Użyj JSON jeśli parsowanie zawiedzie

### Problem: "Brak danych pacjenta"

**Rozwiązanie:**
- Upewnij się że dokument ma tabelę z danymi pacjenta
- Sprawdź format pliku

### Problem: "Nie znaleziono badań krwi"

**Rozwiązanie:**
- Sprawdź czy dokument ma tabelę z wynikami badań
- Upewnij się że nagłówki są czytelne

---

## 💡 WSKAZÓWKI

**Dla najlepszych wyników:**

1. **Używaj DOCX zamiast PDF** (lepsza jakość danych)
2. **Upewnij się że dokument jest tabelaryczny**
3. **Używaj standardowych nazw badań** (np. "Witamina D (25-OH)")
4. **Sprawdź przykładowe pliki** w folderze `examples/`

---

## 📞 POMOC

Potrzebujesz pomocy ze swoim konkretnym plikiem?

**Opcje:**
1. Sprawdź `examples/sample_blood_tests.docx` - przykładowy format
2. Przeczytaj pełny README.md
3. Utwórz issue na GitHub ze swoim plikiem (usuń dane osobiste!)

---

## ✅ PODSUMOWANIE

**Teraz możesz:**
- ✅ Wrzucić PDF z wynikami badań
- ✅ Wrzucić DOCX od lekarza
- ✅ Otrzymać automatyczne rekomendacje suplementów
- ✅ Zdobyć profesjonalny raport PDF

**Koniec z ręcznym przepisywaniem do JSON!** 🎉

---

*Dokumentacja powstała dla Medical Supplement Advisor v1.0*
