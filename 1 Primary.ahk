#Requires AutoHotkey v2.0
#SingleInstance ;forces script to only run one instance
#Include %A_ScriptDir%/2 Sandbox.ahk
#Include %A_ScriptDir%/3 Function Scripts.ahk
#Include %A_ScriptDir%/4 Hotstrings.ahk

KeyHistory()

#HotIf not WinActive("ahk_exe League of Legends.exe") ; Do Not Reload When In Game
^r:: Reload
#HotIf

; Subscripts startup
{
	Run "2 Sandbox.ahk"
	Run "3 Function Scripts.ahk"
	Run "4 Hotstrings.ahk"
}

; SYNTAX GUIDE
{
	/*
	Ctrl = ^, Alt = !, Shift = +, Win = #
	Multiple hotkeys can be stacked vertically to have them perform the same action.
	Each numpad key can be made to launch two different hotkey subroutines depending on the state of NumLock. Alternatively, a numpad key can be made to launch the same subroutine regardless of the state.
	NumLock, CapsLock, and ScrollLock: These keys may be forced to be "AlwaysOn" or "AlwaysOff". For example: SetNumLockState "AlwaysOn".
	*/

}

; AutoHotkey Control Hot Keys
{


	; ^!p:: Pause  ; Press Ctrl+Alt+P to pause. Press it again to resume.

	#HotIf not WinActive("ahk_exe League of Legends.exe") and not WinActive('ahk_exe Code.exe')
	; ^e:: Edit ; Opens Script To Edit


}