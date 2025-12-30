@echo off
echo ================================================
echo   Configuration de la base de donnees
echo ================================================
echo.

echo [1/4] Creation des migrations...
python manage.py makemigrations
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Echec de la creation des migrations
    pause
    exit /b 1
)
echo.

echo [2/4] Application des migrations...
python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Echec de l'application des migrations
    pause
    exit /b 1
)
echo.

echo [3/4] Verification de la configuration...
python manage.py check
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Probleme de configuration detecte
    pause
    exit /b 1
)
echo.

echo ================================================
echo   Configuration terminee avec succes !
echo ================================================
echo.
echo Vous pouvez maintenant :
echo   1. Creer un superutilisateur : python manage.py createsuperuser
echo   2. Lancer le serveur : python manage.py runserver
echo.
pause
