@echo off
chcp 65001 > nul
echo ================================================
echo  COLLECTE MCD MEDIAS BURKINABE
echo ================================================
echo.

cd C:\collecte_mcd

echo [1/8] Test connexion PostgreSQL...
py -3.14 test_connexion.py
if %errorlevel% neq 0 (
    echo.
    echo ERREUR : Connexion BD echouee. Verifiez config.py
    pause > nul
    exit /b 1
)

echo.
echo [2/8] Wayback Machine...
py -3.14 wayback.py

echo.
echo [3/8] Titres des pages Wayback...
py -3.14 wayback_titres.py

echo.
echo [4/8] WHOIS + DNS...
py -3.14 whois_dns.py

echo.
echo [5/8] Google Trends...
py -3.14 google_trends.py

echo.
echo [6/8] YouTube API (chaines + videos)...
py -3.14 youtube_api.py

echo.
echo [7/8] Social Blade (stats journalieres)...
py -3.14 social_blade.py

echo.
echo [8/8] Facebook...
py -3.14 facebook.py

echo.
echo ================================================
echo  COLLECTE TERMINEE
echo ================================================
echo.
pause
