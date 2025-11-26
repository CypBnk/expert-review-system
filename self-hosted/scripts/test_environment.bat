@echo off
REM Quick Test Script - Verifies setup without installing anything

echo ========================================
echo Expert Review Analysis System V2
echo Environment Test
echo ========================================
echo.

echo [TEST 1] Checking Python...
python --version 2>nul
if %errorlevel% neq 0 (
    echo [FAIL] Python not found
    echo Install from https://www.python.org/
    set TEST_FAILED=1
) else (
    echo [PASS] Python is installed
)

echo.
echo [TEST 2] Checking pip...
pip --version 2>nul
if %errorlevel% neq 0 (
    echo [FAIL] pip not found
    set TEST_FAILED=1
) else (
    echo [PASS] pip is installed
)

echo.
echo [TEST 3] Checking required files...
if not exist "frontend\index.html" (
    echo [FAIL] frontend\index.html not found
    set TEST_FAILED=1
) else (
    echo [PASS] frontend\index.html exists
)

if not exist "backend\api_server.py" (
    echo [FAIL] backend\api_server.py not found
    set TEST_FAILED=1
) else (
    echo [PASS] backend\api_server.py exists
)

if not exist "backend\expert_review_system.py" (
    echo [FAIL] backend\expert_review_system.py not found
    set TEST_FAILED=1
) else (
    echo [PASS] backend\expert_review_system.py exists
)

if not exist "frontend\config.js" (
    echo [FAIL] frontend\config.js not found
    set TEST_FAILED=1
) else (
    echo [PASS] frontend\config.js exists
)

echo.
echo [TEST 4] Checking setup scripts...
if not exist "setup.bat" (
    echo [FAIL] setup.bat not found
    set TEST_FAILED=1
) else (
    echo [PASS] setup.bat exists
)

if not exist "start_all.bat" (
    echo [FAIL] start_all.bat not found
    set TEST_FAILED=1
) else (
    echo [PASS] start_all.bat exists
)

echo.
echo ========================================
echo Test Results
echo ========================================
if defined TEST_FAILED (
    echo [RESULT] Some tests failed
    echo Please fix the issues above
) else (
    echo [RESULT] All tests passed!
    echo.
    echo You're ready to setup the environment
    echo Next step: Run setup.bat
)
echo ========================================
echo.

pause
