@echo off
chcp 65001 >nul
title Editar no CapCut (clique unico)
setlocal

REM pasta onde este .bat (e o automate_capcut.py) estao
set "AQUI=%~dp0"
REM pasta do VectCutAPI (venv + servidor)
set "VECT=C:\Users\moret\VectCutAPI"

echo ============================================
echo    EDICAO AUTOMATICA -^> CAPCUT
echo ============================================
echo.

cd /d "%VECT%" || (echo ERRO: nao achei %VECT% & pause & exit /b)

REM ativa a venv
call "%VECT%\venv-capcut\Scripts\activate.bat"

REM acha o automate_capcut.py (do lado do .bat ou dentro do VectCutAPI)
set "SCRIPT=%AQUI%automate_capcut.py"
if not exist "%SCRIPT%" set "SCRIPT=%VECT%\automate_capcut.py"
if not exist "%SCRIPT%" (echo ERRO: nao achei automate_capcut.py & pause & exit /b)

echo [1/4] Instalando dependencias (so na 1a vez)...
pip install -q requests gdown faster-whisper pydub

echo [2/4] Subindo o servidor da API (porta 9001)...
start "VectCut Server" cmd /k "call "%VECT%\venv-capcut\Scripts\activate.bat" && python "%VECT%\capcut_server.py""

echo [3/4] Aguardando o servidor...
timeout /t 8 /nobreak >nul

echo [4/4] Editando (cortes, transicao, efeito, trilha, legenda)...
echo.
python "%SCRIPT%"

echo.
echo ============================================
echo    TERMINOU. Abra o CapCut: o projeto ja
echo    aparece na lista, editado.
echo ============================================
pause
