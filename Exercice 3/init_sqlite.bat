@echo off
cd /d "%~dp0"
echo =======================================================
echo          SYSTEME D'AUDIT - SUPERSMARTMARKET
echo =======================================================

:: 1. Generation de la base si besoin
echo [1/1] Verification et Generation de la base de donnees...
python init_sqlite_demo.py

echo.
echo =======================================================
echo         SUCCESS : Base de donnees prete !
echo =======================================================
echo  - Fichier : ..\supersmartmarket.db
echo  - Action : Ouvrez ce fichier dans "DB Browser for SQLite"
echo  - Demo : Executez "demo_presentation_sqlite.sql"
echo =======================================================
pause
