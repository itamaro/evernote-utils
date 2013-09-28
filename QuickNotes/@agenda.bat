@echo off
set CURDIR=%CD%
set NOTETITLE=%*
python "%CURDIR%\..\PyEvernote\ImportEvernoteTemplate.py" --open-note --notebook "2-Actions" action --context @Agenda --action-title "%NOTETITLE%"
@echo on
