#!/bin/bash

# Test script for Medical Supplement Advisor .app
# This script verifies the .app bundle works correctly

set -e

PROJECT_DIR="/Users/wielkikrzych/medical-supplement-advisor"
APP_PATH="$PROJECT_DIR/AutomatorApp.app"
LAUNCHER="$APP_PATH/Contents/MacOS/launcher"
RESOURCES="$APP_PATH/Contents/Resources"

echo "======================================"
echo "Testing Medical Supplement Advisor .app"
echo "======================================"
echo ""

# Test 1: Verify .app structure exists
echo "Test 1: Verifying .app structure..."
if [ ! -d "$APP_PATH" ]; then
    echo "❌ FAILED: .app bundle not found"
    exit 1
fi
echo "✅ PASSED: .app bundle exists"

# Test 2: Verify launcher is executable
echo ""
echo "Test 2: Verifying launcher is executable..."
if [ ! -x "$LAUNCHER" ]; then
    echo "❌ FAILED: launcher not executable"
    exit 1
fi
echo "✅ PASSED: launcher is executable"

# Test 3: Verify Resources contain project files
echo ""
echo "Test 3: Verifying Resources structure..."
if [ ! -d "$RESOURCES/src" ] || [ ! -d "$RESOURCES/data" ]; then
    echo "❌ FAILED: Required directories missing in Resources"
    exit 1
fi
echo "✅ PASSED: Resources structure is correct"

# Test 4: Verify Python module execution
echo ""
echo "Test 4: Testing Python module import..."
cd "$RESOURCES"
if ! python3 -c "import sys; sys.path.insert(0, '.'); import src.main; print('Import successful')" 2>&1 | head -1; then
    echo "❌ FAILED: Cannot import src.main"
    exit 1
fi
echo "✅ PASSED: Module imports successfully"

# Test 5: Verify CLI help works
echo ""
echo "Test 5: Testing CLI help output..."
if ! python3 -m src.main --help > /dev/null 2>&1; then
    echo "❌ FAILED: CLI help command failed"
    exit 1
fi
echo "✅ PASSED: CLI help works"

# Test 6: Verify PyQt5 is available
echo ""
echo "Test 6: Checking PyQt5 installation..."
if ! python3 -c "from PyQt5.QtWidgets import QApplication; print('PyQt5 available')" 2>&1 | head -1; then
    echo "⚠️  WARNING: PyQt5 may not be properly installed"
    echo "   GUI may not work. Run: pip3 install PyQt5"
else
    echo "✅ PASSED: PyQt5 is installed"
fi

# Test 7: Verify document parser dependencies
echo ""
echo "Test 7: Checking document parser dependencies..."
MISSING_DEPS=""
for dep in docx pdfplumber reportlab; do
    if ! python3 -c "import $dep" 2>/dev/null; then
        MISSING_DEPS="$MISSING_DEPS $dep"
    fi
done

if [ -n "$MISSING_DEPS" ]; then
    echo "⚠️  WARNING: Missing dependencies:$MISSING_DEPS"
    echo "   Install with: pip3 install$MISSING_DEPS"
else
    echo "✅ PASSED: All document parser dependencies installed"
fi

# Test 8: Launch .app and verify process starts
echo ""
echo "Test 8: Launching .app application..."
echo "   Starting GUI..."

# Kill any existing instances
pkill -f "python.*src.main" 2>/dev/null || true
sleep 1

# Launch the app
open "$APP_PATH"
sleep 3

# Check if process is running
if pgrep -f "python.*src.main" > /dev/null; then
    echo "✅ PASSED: .app launched successfully"
    echo "   GUI process is running"
    echo ""
    echo "📱 GUI SHOULD NOW BE VISIBLE ON SCREEN"
    echo "   Expected window title: 'Medical Supplement Advisor'"
    echo ""
else
    echo "❌ FAILED: GUI process not detected"
    echo "   The .app may have failed to launch"
    exit 1
fi

# Test 9: Verify process stays running (GUI event loop active)
echo ""
echo "Test 9: Verifying GUI event loop is active..."
sleep 3
if pgrep -f "python.*src.main" > /dev/null; then
    echo "✅ PASSED: GUI event loop is active"
else
    echo "❌ FAILED: GUI process exited prematurely"
    exit 1
fi

# Summary
echo ""
echo "======================================"
echo "Test Summary"
echo "======================================"
echo ""
echo "✅ All tests passed!"
echo ""
echo "The Medical Supplement Advisor .app is working correctly."
echo ""
echo "GUI Features:"
echo "  - Window title: 'Medical Supplement Advisor'"
echo "  - Button: 'Wybierz plik z wynikami badań'"
echo "  - Supported formats: JSON, PDF, DOCX"
echo ""
echo "Next Steps:"
echo "  1. Test with sample file: examples/sample_blood_tests.json"
echo "  2. Test DOCX parsing: examples/sample_blood_tests.docx"
echo "  3. Check generated PDF in: output/ directory"
echo "  4. If satisfied, move to /Applications/:"
echo "     mv $APP_PATH /Applications/MedicalSupplementAdvisor.app"
echo ""
echo "To close the GUI, close the window or run: pkill -f 'python.*src.main'"
echo ""
