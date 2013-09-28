#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

WinActivate,ahk_class ENMainFrame
WinWaitActive,ahk_class ENMainFrame,,5
if ErrorLevel
{
	MsgBox,Evernote did not launch within 5 seconds! Aborting script.
	ExitApp
}
Sleep,750
SendInput,!n
SendInput,o
