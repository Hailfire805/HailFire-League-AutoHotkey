#Requires AutoHotkey v2.0
#SingleInstance ;forces script to only run one instance

KeyHistory()


/* SYNTAX GUIDE
Ctrl = ^, Alt = !, Shift = +, Win = #
Multiple hotkeys can be stacked vertically to have them perform the same action.
Each numpad key can be made to launch two different hotkey subroutines depending on the state of NumLock. Alternatively, a numpad key can be made to launch the same subroutine regardless of the state.
NumLock, CapsLock, and ScrollLock: These keys may be forced to be "AlwaysOn" or "AlwaysOff". For example: SetNumLockState "AlwaysOn".
*/

# Context-Specific Functions

{
	#HotIf WinActive("ahk_exe chrome.exe") or WinActive("ahk_exe spotify.exe") and not WinActive("ahk_exe League of Legends.exe") ; Chrome & Spotify Functions. Do Not use when in game

	!n:: { ; Next Page Tool, Replace CheckWindowX, CheckWindowY for Different Websites
		CoordMode("Mouse", "Window")
		Send("{End}") ; Navigate to the bottom of the page
		Sleep(1000)
		MouseClick("Left", 1130, 658, 1) ; Input Click On Next Page Button
	}

	!XButton1:: { ; Audio Sampler and Stopper
		MouseStartX := 0
		MouseStartY := 0
		PlayAudioSample(location, time, MouseStartX, MouseStartY) {
			Send("{Click {location} Left}") ; Spotify mid song location
			MouseMove(MouseStartX, MouseStartY) ; Move back to starting position
			Sleep(time) ; Wait 7 Seconds
		}
		CaptureMouseStartPosition() {
			SetDefaultMouseSpeed 0 ; Set mouse to instant movement
			CoordMode("Mouse", "Window") ; Switch to window based coordinates for usage on either monitor
			MouseGetPos &MouseStartX, &MouseStartY ; Capture starting position
			MouseClick("Left") ; Left click from starting position
			Sleep(300) ; Delay 0.3 seconds
		}

		CaptureMouseStartPosition()
		if WinActive("ahk_exe Spotify.exe") ; If active window is spotify
			PlayAudioSample("960 1021", 7000, MouseStartX, MouseStartY)
		else ; If Window is not spotify
			PlayAudioSample("1070 1001", 3000, MouseStartX, MouseStartY)

		MouseClick("Left", MouseStartX, MouseStartY, 1) ; Click starting location to pause audio
	}

	#HotIf WinActive("ahk_exe Discord.exe") ; Discord Functions

	Numpad0:: { ; Discord Mass Share Macro
		RepeatCount := InputBox("Times to repeat?") ; Prompts UserId for number of times to repeat
		if RepeatCount.Result = "Cancel"
			return
		else {
			CurrentCounter := Integer(RepeatCount.Value)
			Recipients := CurrentCounter
			WinActivate("ahk_exe Discord.exe")
			Sleep(1000)
			Send "{Up}" ; Edits text of last message sent
			Sleep(1000)
			Send "^a" ; Selects all text
			Sleep(1000)
			Send "^c" ; Copies text
			Sleep(1000)

			while (CurrentCounter > 0) { ; Loops based on userId input for repeats
				loop Recipients {
					Send "!{Down}"
					Sleep(100)
				} ; Moves to next recipent or channel in list
				Sleep(1000)
				Send("^a") ; Selects all existing text
				Sleep(1000)
				Send "^v" ; Pastes in copied text
				Sleep(1000)
				Send "{Enter}" ; Sends message
				Sleep(1000)

				CurrentCounter := CurrentCounter - 1 ; Decrements repeat CurrentCounter
			}
		}
	}


	#HotIf WinActive("ahk_exe LeagueClientUx.exe") ; League Client Functions
	{
		!m:: { ; League DoesUserIdIncludeTag History
			CoordMode("mouse", "Window")
			Send("{Click 1389 43 Left}") ; Go To Profile
			sleep(1000)
			Send("{Click 414 122 Left}") ; Go To DoesUserIdIncludeTag History
		}

		!c:: { ; League Arena Challenges
			CoordMode("mouse", "Window")
			Send("{Click 1389 43 Left}") ; Go To Profile
			sleep(500)
			Send("{Click 248 122 Left}") ; Go To Challenges
			sleep(3000)
			Send("{Click 88 736 Left}") ; Go To Legacy
			sleep(500)
			Send("{Click 819 398 Left}") ; Focus Main Window
			sleep(500)
			Send("{PgDn}") ; Navigate Down Page To Arena Challenges
			sleep(500)
			Send("{PgDn}")
			sleep(500)
			Send("{Click 446 479 Left}") ; Open "Adapt To All Situations"
		}

	}
}

; General Functions
{
	#HotIf ; Always On Functions

	^l:: { ; Transfer Tab Url to Notepad stage 1
		WinActivate("ahk_exe chrome.exe") ; First in Chrome
		sleep(100)
		CurrentChromeTitle := WinGetTitle("A")
		CoordMode("Mouse", "Window") ; Using location based on the window
		Send("+{Click 1674 28 Left}") ; Shift click to select tabs to transfer
		Sleep(100)
		Send("{F6 2 }") ; Move focus to selected tabs
		Sleep(100)
		Send("{AppsKey}") ; Open Context Menu
		Sleep(100)
		Send("{Down 4}") ; Transfer tabs to new window
		Sleep(100)
		Send("{Right 2}")
		Sleep(100)
		Send("{Enter}")
		Sleep(100)
		Run Format('notepad.exe "{1}\Url Bundle.txt"', A_WorkingDir) ; Create and open a file to store the urls.
		CurrentNotepadTitle := WinGetTitle("A")
		Sleep(100)
		WinActivate(CurrentChromeTitle)
		Sleep(100)
		Send("{Enter}")
		Sleep(100)
		WinActivate(CurrentNotepadTitle)
		Sleep(100)
		Send("^1")
		Sleep(100)
	}

	^+l:: { ; Transfer Tab Urls to Notepad Stage 2
		Loop 10 {
			Sleep(100)
			Send("{F6}")
			Sleep(100)
			Send("^c")
			Sleep(100)
			WinActivate("ahk_class Notepad")
			Sleep(100)
			Send("^v")
			Sleep(100)
			Send("`n")
			WinActivate("ahk_exe chrome.exe")
			Sleep(100)
			Send("^w")
			Sleep(100)
		}
	}

	^o:: { ; Opens the OP.GG of Desired Player and closes Adblock Notification

		CoordMode("Mouse", "Screen")

		UserId := InputBox("UserId?") ; Prompts for OP.GG userId to search
		if UserId.Result = "Cancel" ; Check for cancel command
			return
		else { ; Parse UserIdname and TagLine from Input

			if UserId.Value = "" { ; If no userId is provided, then the default userId is used
				RiotId := "" ; Default UserId RiotId
				TagLine := "" ; Default TagLine
			}
			else { ; If a userId is provided

				DoesUserIdIncludeTag := RegExMatch(UserId.Value, "#") ; Check if provided userId includes a tagline
				if (DoesUserIdIncludeTag = 0) { ; If no TagLine line is provided use default "NA1"
					RiotId := UserId.Value
					TagLine := "NA1"
				}
				else { ; If a TagLine line is provided seperate the RiotId and TagLine line
					SplitCombinedUserId := StrSplit(UserId.Value, "#")
					RiotId := SplitCombinedUserId.Get(1)
					TagLine := SplitCombinedUserId.Get(2)
				}
			}

			target := "https://www.op.gg/summoners/na/" RiotId "-" TagLine ; Set Url to search
		}

		Run target ; Open Url

		WinWait(RiotId "#" TagLine " - Summoner Stats - League of Legends - Google Chrome") ; Wait until URL is opened
		WinGetPos &CheckWindowX, &CheckWindowY, , , RiotId "#" TagLine " - Summoner Stats - League of Legends - Google Chrome" ; Locate URL position

		if (CheckWindowX > -100) { ; If window is on right monitor
			Sleep(5000)
			MouseClick("Left", 1240, 446, 1) ; Close Adblock notification
		}

		if (CheckWindowX < -100) { ; If window is on left monitor
			Sleep(5000)
			MouseClick("Left", -680, 446, 1) ; Close Adblock notification
		}
	}

	!t:: { ; Automatically Start Discord ScreenShare
		CoordMode("Mouse", "Screen")
		WinActivate("ahk_exe Discord.exe") ; Activate Discord
		WinWaitActive("ahk_exe Discord.exe") ; Wait for Discord to be Active
		Sleep(333)
		CoordMode("Mouse", "Window") ; Set Coord Mode to use Window Relative values
		Send("{Click 165 959 Left}") ; Left Click The Share Screen Button in the Lower Left
		Sleep(333)
		Send("{Click 862 407 Left}") ; Left Click The Tab For Screens
		Sleep(333)
		Send("{Click 850 490 Left}") ; Left Click Screen 1
		Sleep(333)
		Send("{Click 1147 826 Left}") ; Left Click Begin Streaming
	}

}

; Shortcut Functions
{
	^u:: {
		Run "https://www.chess.com/play/online/new"
		Sleep(2500)
		Send("{Click 1351 284 Left}")
	}
}