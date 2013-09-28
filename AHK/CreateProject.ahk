#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

CreateEvernoteProject(project_name)
{
	if StrLen(project_name) = 0
	{
		; No project name as argument - so ask user
		InputBox,project_name,Create Project,Enter new project name (will be the name of the notebook, and prefixed with "$" for a new tag)
		if ((ErrorLevel) || (StrLen(project_name) = 0))
		{
			; Abort
			Return
		}
	}
	; Verify that we're an in main Evernote window
	IfWinExist,ahk_class ENMainFrame
	{
		WinActivate
	}
	Else
	{
		MsgBox,Evernote main window must open.
		Return
	}
	; Open the create notebook dialog (ctrl+shift+n)
	SendInput,^N
	; Wait for the notebook dialog to open
	WinWaitActive,ahk_class #32770,,5
	if ErrorLevel
	{
		MsgBox,Notebook dialog did not open within 5 second.
		Return
	}
	; Create the notebook
	SendInput,%project_name%
	SendInput,{Enter}
	Sleep,100
	Run,python "..\PyEvernote\ImportEvernoteTemplate.py" --notebook "%project_name%" project
}

arg = %1%
CreateEvernoteProject(arg)
