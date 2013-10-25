@echo off
set CURDIR=%CD%
set NOTETITLE=%*
python "%CURDIR%\..\PyEvernote\ImportEvernoteTemplate.py" --open-note --notebook "2-Actions" action --context @Out --action-title "%NOTETITLE%"
@echo on
