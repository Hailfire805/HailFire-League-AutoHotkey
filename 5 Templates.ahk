#Requires AutoHotkey v2.0
Exit()

; Click Sequence Function
ClickSequenceTemplate() {
	SetMouseDelay(333)
	Target := ""
	WinActivate(Target) ;
	WinWaitActive(Target) ;
	CoordMode("Mouse", "Window") ;
	Send("{Click {location one} Left}") ;
	Send("{Click {location two} Left}") ;
	Send("{Click {location three} Left}") ;
	Send("{Click {location four} Left}") ;
}

; Message box with custom names
CustomMsgBox() {

	ChangePromptButtonNames()
	{
		if !WinExist("Prompt Title")
			return  ; Keep waiting.

		SetTimer , 0
		WinActivate

		ControlSetText "&Clicks", "Button1"
		ControlSetText "&Inputs", "Button2"
	}

	SetTimer ChangePromptButtonNames, 50

	Result := MsgBox("Message Prompt?", "Prompt Title", 4)

	if Result = "Yes" {

	}
	else {

	}
}

; Hot If Context Block
{
	#HotIf WinActive()
	{

	}
	#HotIf
}