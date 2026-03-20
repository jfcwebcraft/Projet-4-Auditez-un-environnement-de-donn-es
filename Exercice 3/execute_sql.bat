@echo off
cd /d "%~dp0"
if "%~1"=="" (
    echo Usage : execute_sql.bat nom_du_fichier.sql
    echo Exemple : execute_sql.bat demo_presentation_sqlite.sql
    pause
    exit /b
)
python terminal_audit.py %1
pause
