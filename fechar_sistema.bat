@echo off
title Encerrar Sistema de Gestao de Manutencao
echo Encerrando o Sistema de Gestao de Manutencao...
taskkill /f /im GestaoManutencao.exe >nul 2>&1
echo.
echo Concluido! A aplicacao em segundo plano foi finalizada.
ping 127.0.0.1 -n 2 >nul
