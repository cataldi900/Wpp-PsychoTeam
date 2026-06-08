@echo off
chcp 65001 >nul
title Automacao CapCut - Esforco x Resultado
cd /d C:\Users\moret\VectCutAPI

echo ============================================
echo   AUTOMACAO CAPCUT (clique unico)
echo ============================================
echo.

REM 1) ativa a venv
call venv-capcut\Scripts\activate.bat

REM 2) instala dependencias (so demora na 1a vez)
echo [1/4] Verificando dependencias...
pip install -q requests gdown faster-whisper pydub

REM 3) sobe o servidor da API em outra janela
echo [2/4] Iniciando servidor da API (porta 9001)...
start "VectCut Server" cmd /k "call venv-capcut\Scripts\activate.bat && python capcut_server.py"

echo [3/4] Aguardando o servidor subir...
timeout /t 8 /nobreak >nul

REM 4) roda a automacao (corta silencios, transicoes, efeitos, trilha, legenda, move pro CapCut)
echo [4/4] Editando o video...
echo.
python automate_capcut.py

echo.
echo ============================================
echo   TERMINOU. Abra o CapCut: o projeto deve
echo   aparecer na lista, ja editado.
echo ============================================
pause
