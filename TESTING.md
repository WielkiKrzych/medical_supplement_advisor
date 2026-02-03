# Medical Supplement Advisor .app - Test Instructions

## Current Status: ✅ READY TO TEST

The macOS .app bundle has been successfully created and is ready for testing.

## How to Test

### Method 1: Double-Click from Finder (RECOMMENDED)

1. Open Finder
2. Navigate to: `/Users/wielkikrzych/medical-supplement-advisor/`
3. Double-click on `AutomatorApp.app`
4. **Expected Result**: GUI window should appear

**What you should see:**
- Window title: "Medical Supplement Advisor"
- Button: "Wybierz plik z wynikami badań" (Select blood test file)
- Status label: "Gotowy do analizy" (Ready for analysis)

### Method 2: Using Terminal

```bash
cd /Users/wielkikrzych/medical-supplement-advisor
open AutomatorApp.app
```

## Troubleshooting

### If GUI doesn't appear:

1. **Check Console.app for errors:**
   ```bash
   open /Applications/Utilities/Console.app
   ```
   Filter for "Python" or "Medical Supplement Advisor"

2. **Verify PyQt5 is installed:**
   ```bash
   pip3 install PyQt5
   ```

3. **Test the launcher manually:**
   ```bash
   cd /Users/wielkikrzych/medical-supplement-advisor
   ./AutomatorApp.app/Contents/MacOS/launcher
   ```
   (Press Ctrl+C to exit if it hangs)

### If GUI appears but doesn't respond:

- This might be a display connection issue when run from terminal
- **Solution**: Always launch from Finder (double-click) for proper GUI support

## Testing with Sample Files

Once GUI is open:

### Test 1: JSON Format (Legacy)
1. Click "Wybierz plik z wynikami badań"
2. Navigate to: `examples/sample_blood_tests.json`
3. Click "Open"
4. Expected: PDF generated in `output/` directory

### Test 2: DOCX Format (New Auto-Parsing)
1. Click "Wybierz plik z wynikami badań"
2. Navigate to: `examples/sample_blood_tests.docx`
3. Click "Open"
4. Expected: PDF generated in `output/` directory

### Test 3: PDF Format (New Auto-Parsing)
1. If you have a PDF blood test, try selecting it
2. Expected: Auto-detection and parsing

## Verifying the Output

After selecting a file:

```bash
ls -lh output/
```

You should see a PDF file with timestamp in the name.

## If Everything Works

You can move the .app to your Applications folder:

```bash
mv /Users/wielkikrzych/medical-supplement-advisor/AutomatorApp.app /Applications/MedicalSupplementAdvisor.app
```

Then launch from Applications or Spotlight (Cmd+Space, type "Medical Supplement Advisor").

## Technical Details

### .app Structure:
```
AutomatorApp.app/
├── Contents/
│   ├── Info.plist              # App metadata
│   ├── MacOS/
│   │   └── launcher            # Executable script
│   └── Resources/
│       ├── src/                # All source code
│       ├── data/               # Configuration files
│       ├── examples/           # Sample files
│       ├── output/             # Generated PDFs
│       └── config.py           # App config
```

### Launcher Script:
```bash
#!/bin/bash
APP_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RESOURCES_PATH="$APP_PATH/../Resources"
cd "$RESOURCES_PATH" || exit 1
python3 -m src.main  # Runs in GUI mode when no arguments
```

### Why GUI works from Finder but not terminal:

When launched from Finder, macOS:
- Provides a proper display server connection
- Sets up the WindowServer environment
- Enables Qt/PyQt5 to create windows

When launched from terminal:
- No display server connection (in some terminal contexts)
- Qt cannot create GUI windows
- Application may hang waiting for display

**Solution**: Always test the GUI by double-clicking from Finder.

## Dependencies

All required Python packages are installed:
- ✅ PyQt5 (GUI framework)
- ✅ python-docx (DOCX parsing)
- ✅ pdfplumber (PDF parsing)
- ✅ reportlab (PDF generation)

## Support

If you encounter issues:
1. Check Console.app for error messages
2. Verify all dependencies are installed
3. Ensure the .app bundle structure is intact
4. Try launching from a fresh terminal session

## Known Limitations

1. **Terminal Launch**: The GUI may not display properly when launched from certain terminal contexts. Always use Finder for GUI testing.

2. **File Picker**: The file picker dialog is system-provided and should work with all standard file formats.

3. **PDF Generation**: Output PDFs are saved in the `output/` directory within the .app bundle.

## Next Steps After Testing

If the .app works correctly:
1. Move to `/Applications/` folder
2. Test with real blood test files
3. Customize the window title and appearance if needed
4. Add an app icon (currently using default)
5. Consider code signing for distribution (prevents warnings on first launch)

---

**Created**: January 29, 2026
**Status**: ✅ Ready for testing
**Test Command**: `open AutomatorApp.app` (from project directory)
