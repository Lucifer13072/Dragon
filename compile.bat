@echo off
g++ src/main.cpp src/lexer/Token.cpp src/parser/Parser.cpp src/interpret/Interpretator.cpp -I src -o dragon.exe
if %errorlevel% equ 0 (
    echo Компиляция успешна!
    echo Запуск программы...
    dragon.exe
) else (
    echo Ошибка компиляции!
) 