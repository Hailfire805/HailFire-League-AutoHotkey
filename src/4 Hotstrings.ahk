#Requires AutoHotkey v2.0
#SingleInstance ;forces script to only run one instance

; KeyHistory()
; SYNTAX GUIDE
{
	/*
	Ctrl = ^, Alt = !, Shift = +, Win = #
	Multiple hotkeys can be stacked vertically to have them perform the same action.
	Each numpad key can be made to launch two different hotkey subroutines depending on the state of NumLock. Alternatively, a numpad key can be made to launch the same subroutine regardless of the state.
	NumLock, CapsLock, and ScrollLock: These keys may be forced to be "AlwaysOn" or "AlwaysOff". For example: SetNumLockState "AlwaysOn".
	*/
}
; Hot Functions
{
	#HotIf WinActive('ahk_exe chrome.exe') ; Chrome Hotstrings
	{
		::keyregen:: { ; Riot API Key Regenerator
			Run "https://developer.riotgames.com/" ; Open the riot developer portal in chrome
			WinWait("Riot Developer Portal - Google Chrome", , 5) ; Wait until the window is open
			Sleep(666)
			Send("{Click 1858 160 Left}") ; Click the login button in the top right
			WinWait("Sign in - Google Chrome", , 5) ; Wait until the sign in window is open
			Sleep(666)
			Send("{Click 853 566 Left}") ; Click the google login button
			WinWait("Sign in - Google Accounts - Google Chrome") ; Wait until the next window is open
			Sleep(333)
			Send("{Click 1157 465 Left}") ; Click my primary email account
			WinWait("Riot Developer Portal - Google Chrome") ; Wait until the window returns to the developer portal
			Sleep(333)
			Send("{End}") ; navigate to the bottom of the page
			Sleep(333)
			Send("{Click 719 821 Left}") ; Click I am not a robot
			Sleep(333)
			Send("{Click 786 902 Left}") ; Regenerate the api key
			Sleep(3000) ; wait for page reload
			Send("{Click 1128 920 Left}") ; click to copy key
			Sleep(333)
			Send("^w") ; Close Page
		}
	}
	#HotIf
}

{ ; League "play- " Functions
	EnterQueueSelect() {
		Send("{Click 315 58 Left}") ; Home
		Send("{Click 152 55 Left}") ; Play/Lobby
		Send("{Click 46 134 Left}") ; All Modes

	}

	::playnormal:: {
		primary := ""
		secondary := ""
		getUserInput() {
			FirstRole := InputBox("Primary Position?") ; Primary Position User Wants?
			primary := FirstRole.Value
			SecondRole := InputBox("Secondary Position?") ; Primary Position User Wants?
			secondary := SecondRole.Value
		}
		SetRoles(FirstSecond, Role) {
			if FirstSecond = "First" {
				Send("{Click 820 850 Left}") ; Primary Role
				switch Role {
					case "Top":
						Send("{Click 634 777 Left}") ; Top Lane
					case "Jungle":
						Send("{Click 711 787 Left}") ; Jungle
					case "Mid":
						Send("{Click 783 782 Left}") ; Mid Lane
					case "Bot":
						Send("{Click 848 785 Left}") ; Bot Lane
					case "Support":
						Send("{Click 913 785 Left}") ; Support
				}
			}
			else if FirstSecond = "Second" {
				Send("{Click 870 850 Left}") ; Secondary Role
				switch Role {
					case "Top":
						Send("{Click 684 777 Left}") ; Top Lane
					case "Jungle":
						Send("{Click 761 787 Left}") ; Jungle
					case "Mid":
						Send("{Click 823 782 Left}") ; Mid Lane
					case "Bot":
						Send("{Click 898 785 Left}") ; Bot Lane
					case "Support":
						Send("{Click 963 785 Left}") ; Support
				}
			}

		}
		Config() {
			SetDefaultMouseSpeed(0)
			SetMouseDelay(333)
			Target := "ahk_exe LeagueClientUx.exe"
			WinActivate(Target) ;
			WinWaitActive(Target) ;
			CoordMode("Mouse", "Window") ;
		}
		Navigate() {
			EnterQueueSelect()
			SetDefaultMouseSpeed(1)
			Send("{Click 172 302 Left}") ; Summoner's Rift
			Send("{Click 175 302 Left}") ; Summoner's Rift
			Send("{Click 117, 678 Left}") ; Normal Draft
			Send("{Click 686 854 Left}") ; Confirm

		}

		getUserInput()
		Config() ;
		Navigate()
		Sleep(1000)
		SetRoles("First", primary)
		SetRoles("Second", secondary)
		Send("{Click 664 826 Left}") ; Find Match
	}

	::playranked:: {
		primary := ""
		secondary := ""
		getUserInput() {
			FirstRole := InputBox("Primary Position?") ;
			primary := FirstRole.Value
			SecondRole := InputBox("Secondary Position?")
			secondary := SecondRole.Value
		}
		SetRoles(FirstSecond, Role) {
			if FirstSecond = "First"
				Send("{Click 818 853 Left}") ; Primary Role
			else if FirstSecond = "Second"
				Send("{Click 866 847 Left}") ; Secondary Role
			switch Role {
				case "Top":
					Send("{Click 634 777 Left}") ; Top Lane
				case "Jungle":
					Send("{Click 711 787 Left}") ; Jungle
				case "Mid":
					Send("{Click 783 782 Left}") ; Mid Lane
				case "Bot":
					Send("{Click 848 785 Left}") ; Bot Lane
				case "Support":
					Send("{Click 913 785 Left}") ; Support
			}
		}
		Config() {
			SetDefaultMouseSpeed(0)
			SetMouseDelay(333)
			Target := "ahk_exe LeagueClientUx.exe"
			WinActivate(Target) ;
			WinWaitActive(Target) ;
			CoordMode("Mouse", "Window") ;
		}
		Navigate() {
			EnterQueueSelect()
			SetDefaultMouseSpeed(1)

			Send("{Click 172 302 Left}") ; Summoner's Rift
			Send("{Click 175 302 Left}") ; Summoner's Rift
			Send("{Click 124 715 Left}") ; Ranked Solo/Duo
			Send("{Click 686 854 Left}") ; Confirm

		}

		Config()
		Navigate()
		Sleep(1000)
		getUserInput()
		SetRoles("First", primary)
		SetRoles("Second", secondary)
		Send("{Click 664 826 Left}") ; Find Match
	}

	::playaram:: {
		Config() {
			SetDefaultMouseSpeed(0)
			SetMouseDelay(333)
			Target := "ahk_exe LeagueClientUx.exe"
			WinActivate(Target) ;
			WinWaitActive(Target) ;
			CoordMode("Mouse", "Window") ;
		}
		Navigate() {
			EnterQueueSelect()
			SetDefaultMouseSpeed(1)
			Send("{Click 473 334 Left}") ; Aram
			Sleep(100)
			Send("{Click 476 334 Left}") ; Aram
			Send("{Click 686 854 Left}") ; Confirm
		}

		Config()
		Navigate()
		Sleep(1000)
		Send("{Click 664 826 Left}") ; Find Match
	}

	::playtft:: {
		Config() {
			SetDefaultMouseSpeed(0)
			SetMouseDelay(333)
			Target := "ahk_exe LeagueClientUx.exe"
			WinActivate(Target) ;
			WinWaitActive(Target) ;
			CoordMode("Mouse", "Window") ;
		}
		Navigate() {
			EnterQueueSelect()
			SetDefaultMouseSpeed(1)
			Send("{Click 797 290 Left}") ; TFT
			Sleep(100)
			Send("{Click 800 290 Left}") ; TFT
			Send("{Click 718 718 Left}") ; Ranked TFT
			Send("{Click 686 854 Left}") ; Confirm
		}

		Config()
		Navigate()
		Sleep(1000)
		Send("{Click 664 826 Left}") ; Find Match
	}

	::playarena:: {
		Config() {
			SetDefaultMouseSpeed(0)
			SetMouseDelay(333)
			Target := "ahk_exe LeagueClientUx.exe"
			WinActivate(Target) ;
			WinWaitActive(Target) ;
			CoordMode("Mouse", "Window") ;
		}
		Navigate() {
			EnterQueueSelect()
			SetDefaultMouseSpeed(1)
			Send("{Click 1109 304 Left}") ; Arena
			Sleep(100)
			Send("{Click 1111 304 Left}") ; Arena

			Send("{Click 686 854 Left}") ; Confirm
		}

		Config()
		Navigate()
		Sleep(1000)
		Send("{Click 664 826 Left}") ; Find Match
	}
}