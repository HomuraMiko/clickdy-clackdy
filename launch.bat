@echo off
echo.
echo === Converting samples to 48000Hz 16-bit WAV...
python convert_samples.py --auto
echo.
echo === Select version:
echo [1] Standard
echo [2] Low Latency (try this if sounds feel delayed)
echo.
set /p choice="Choice [1]: "
if "%choice%"=="2" (
    echo Starting Low Latency engine...
    python sfx_lowlatency.py
) else (
    echo Starting Standard engine...
    python sfx.py
)
