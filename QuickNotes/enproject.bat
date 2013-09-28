@echo off
set CURDIR=%CD%
set PROJNAME=%*
"%CURDIR%\..\AHK\CreateProject.exe" "%PROJNAME%"
@echo on
