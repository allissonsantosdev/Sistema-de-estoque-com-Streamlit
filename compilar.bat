@echo off
title Compilando Sistema de Gestao de Manutencao
echo ========================================================
echo  Compilando Sistema de Gestao de Manutencao
echo ========================================================
echo.

echo 1. Fechando processos antigos caso estejam abertos...
taskkill /f /im GestaoManutencao.exe >nul 2>&1

if exist "dist\GestaoManutencao" (
    echo 2. Limpando versao anterior...
    rmdir /s /q "dist\GestaoManutencao" >nul 2>&1
    ping 127.0.0.1 -n 2 >nul
)

echo 3. Iniciando PyInstaller...
if exist "GestaoManutencao.spec" (
    .\.venv\Scripts\pyinstaller.exe --noconfirm GestaoManutencao.spec
) else (
    .\.venv\Scripts\pyinstaller.exe --noconfirm --onedir --noconsole ^
      --name "GestaoManutencao" ^
      --copy-metadata streamlit ^
      --collect-all streamlit ^
      --collect-all altair ^
      --collect-all pandas ^
      --add-data "icones;icones" ^
      --add-data "app.py;." ^
      --add-data "database.py;." ^
      run.py
)

echo.
echo 4. Sincronizando banco de dados e arquivos auxiliares...
if exist "estoque_setor.db" (
    if not exist "dist\GestaoManutencao\estoque_setor.db" (
        copy "estoque_setor.db" "dist\GestaoManutencao\estoque_setor.db"
    )
)

if exist "fechar_sistema.bat" (
    copy "fechar_sistema.bat" "dist\GestaoManutencao\fechar_sistema.bat" >nul 2>&1
)

echo.
echo ========================================================
echo  Compilacao concluida com sucesso!
echo  Executavel gerado em: dist\GestaoManutencao\GestaoManutencao.exe
echo ========================================================
pause
