@echo off
set CURDIR=%CD%
set NOTETITLE=%*
python "%CURDIR%\..\PyEvernote\ImportEvernoteTemplate.py" --notebook "2-Actions" action --context @Home --action-title "%NOTETITLE%"
@echo on
