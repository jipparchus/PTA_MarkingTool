@echo off
REM %1: anaconda env name
REM %2: .ipynb file name
REM %3: full path to the directory containing the .ipynb file 

cd %3
call conda activate %1

echo Converting %2 to LaTeX...
jupyter nbconvert --execute --to latex --allow-errors "%2"
echo Converting %2 to PDF...
xelatex -interaction=nonstopmode "%~n2.tex"

REM Remove unnecessary files and directory
del /q "%~n2.aux"
del /q "%~n2.log"
del /q "%~n2.out"
del /q "%~n2.tex"
rmdir /s /q "%~n2_files"

call conda deactivate