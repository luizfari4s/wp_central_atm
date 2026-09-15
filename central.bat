@echo off
chcp 65001 >nul

set LOGIN=%USERNAME%

set PYTHON=C:\Program Files\Python314\python.exe

set PROJETO=C:\Users\%LOGIN%\OneDrive - Numerator International\Área de Trabalho\Workspace\PROD\wp_central_atm


REM ========================================
REM ENTRA NA PASTA DO PROJETO
REM ========================================

cd /d "%PROJETO%"


REM ========================================
REM VERIFICA SE O PYTHON EXISTE
REM ========================================

IF NOT EXIST "%PYTHON%" (
    echo.
    echo [ERRO] Python nao foi encontrado.
    echo Caminho esperado:
    echo %PYTHON%
    echo.
    pause
    exit /b 1
)


REM ========================================
REM INSTALA AS DEPENDENCIAS
REM ========================================

echo.
echo ========================================
echo   VERIFICANDO DEPENDENCIAS
echo ========================================
echo.

"%PYTHON%" -m pip install -r requirements.txt


REM ========================================
REM INICIA A APLICACAO
REM ========================================

echo.
echo ========================================
echo   INICIANDO CENTRAL DE AUTOMACOES
echo ========================================
echo.

"%PYTHON%" -m streamlit run app.py

pause