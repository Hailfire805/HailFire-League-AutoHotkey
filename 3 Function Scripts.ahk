#Requires AutoHotkey v2.0
#SingleInstance ;forces script to only run one instance

KeyHistory()

/* SYNTAX GUIDE
Ctrl = ^, Alt = !, Shift = +, Win = #
Multiple hotkeys can be stacked vertically to have them perform the same action.
Each numpad key can be made to launch two different hotkey subroutines depending on the state of NumLock. Alternatively, a numpad key can be made to launch the same subroutine regardless of the state.
NumLock, CapsLock, and ScrollLock: These keys may be forced to be "AlwaysOn" or "AlwaysOff". For example: SetNumLockState "AlwaysOn".
*/


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

	!l:: { ; Fetch Champion Matchup Data By Lane
		UrlRunner(Champion, Lane, matchups, patch) { ; Using Matchup Data Load Urls
			counter := 1 ; Set counter for iterating through
			loop matchups.Length { ; For each matchup in matchup group
				if (matchups[counter] != Champion) { ; If Matchup is Not The Same as User Champion
					switch patch { ; Ask User For Data Timeframe
						case 7: ; 7 Days
							Url := "https://lolalytics.com/lol/" Champion "/vs/" matchups[counter] "/build/?lane=" Lane "&vslane=" Lane "&patch=7"
						case 14: ; 14 Days
							Url := "https://lolalytics.com/lol/" Champion "/vs/" matchups[counter] "/build/?lane=" Lane "&vslane=" Lane "&patch=14"
						case 30: ; 30 Days
							Url := "https://lolalytics.com/lol/" Champion "/vs/" matchups[counter] "/build/?lane=" Lane "&vslane=" Lane "&patch=30"
						default: ; This Patch
							Url := "https://lolalytics.com/lol/" Champion "/vs/" matchups[counter] "/build/?lane=" Lane "&vslane=" Lane ""
					}

					Run(Url) ; Run URL
				}
				counter++ ; Increment Counter
			}
		}
		LoadMatchups(Champion, Lane, Section, patch?) { ; Open 10 Matchups based on champion given and lane
			switch Lane { ; Set Data Endpoint to Desired Lane
				case "top": ; Filter to desired sub sections
					switch Section {
						case 1: ; Top 10
							data := TopLane1
						case 2: ; 11-20
							data := TopLane2
						case 3: ; 21-30
							data := TopLane3
						case 4: ; 31-40
							data := TopLane4
						case 5: ; 41-50
							data := TopLane5
						case 6: ; 51-60
							data := TopLane6
						case 7: ; 61-70
							data := TopLane7
						default: ; All Combined
							data := TopLane1
							data.push(TopLane2*)
							data.push(TopLane3*)
							data.push(TopLane4*)
							data.push(TopLane5*)
							data.push(TopLane6*)
							data.push(TopLane7*)
					}
				case "jungle": ; Filter to desired sub sections
					switch Section {
						case 1: ; 10 Most common Matchups
							data := Jungle1
						case 2:
							data := Jungle2
						case 3:
							data := Jungle3
						case 4:
							data := Jungle4
						case 5:
							data := Jungle5
						default:
							data := Jungle1
							data.push(Jungle2*)
							data.push(Jungle3*)
							data.push(Jungle4*)
							data.push(Jungle5*)
					}
				case "middle": ; Filter to desired sub sections
					switch Section {
						case 1: ; 10 Most common Matchups
							data := MiddleLane1
						case 2:
							data := MiddleLane2
						case 3:
							data := MiddleLane3
						case 4:
							data := MiddleLane4
						case 5:
							data := MiddleLane5
						case 6:
							data := MiddleLane6
						default:
							data := MiddleLane1
							data.push(MiddleLane2*)
							data.push(MiddleLane3*)
							data.push(MiddleLane4*)
							data.push(MiddleLane5*)
							data.push(MiddleLane6*)

					}
				case "bottom": ; Filter to desired sub sections
					switch Section {
						case 1: ; 10 Most common Matchups
							data := BottomLane1
						case 2:
							data := BottomLane2
						case 3:
							data := BottomLane3
						case 4:
							data := BottomLane4
						default:
							data := BottomLane1
							data.push(BottomLane2*)
							data.push(BottomLane3*)
							data.push(BottomLane4*)
					}
				case "support": ; Filter to desired sub sections
					switch Section {
						case 1:
							data := SupportLane1
						case 2:
							data := SupportLane2
						case 3:
							data := SupportLane3
						case 4:
							data := SupportLane4
						case 5:
							data := SupportLane5
						default:
							data := SupportLane1
							data.push(SupportLane2*)
							data.push(SupportLane3*)
							data.push(SupportLane4*)
							data.push(SupportLane5*)
					}
			}
			UrlRunner(Champion, Lane, data, patch?) ; Using Matchup Selection
		}

		{ ; Top Lane Champions
			TopLane1 := [
				"aatrox", "darius", "garen", "sett", "jax", "camille", "renekton", "volibear", "mordekaiser", "drmundo"]
			TopLane2 := [
				"malphite", "nasus", "fiora", "ksante", "yone", "riven", "gragas", "irelia", "rumble", "gnar"]
			TopLane3 := [
				"jayce", "kayle", "yorick", "tryndamere", "twistedfate", "shen", "illaoi", "gangplank", "gwen", "pantheon"]
			TopLane4 := [
				"skarner", "teemo", "vladimir", "vayne", "sion", "kennen", "urgot", "quinn", "tahmkench", "akali"]
			TopLane5 := [
				"kled", "warwick", "zac", "chogath", "trundle", "olaf", "singed", "yasuo", "heimerdinger", "wukong"]
			TopLane6 := [
				"cassiopeia", "smolder", "sylas", "udyr", "varus", "shyvana", "rengar", "naafiri", "rammus", "sejuani"]
			TopLane7 := [
				"akshan", "maokai", "leesin", "briar", "viego", "zed", "karma", "tristana", "lucian", "swain"]
		}
		{ ; Jungle Champions
			Jungle1 := [
				"hecarim", "brand", "masteryi", "jarvaniv", "zyra", "ekko", "vi", "zac", "kindred"]
			Jungle2 := [
				"xinzhao", "sejuani", "karthus", "amumu", "taliyah", "udyr", "fiddlesticks", "belveth", "shyvana"]
			Jungle3 := [
				"volibear", "briar", "gragas", "warwick", "rengar", "evelynn", "nunu", "elise", "sylas", "talon"]
			Jungle4 := [
				"reksai", "rammus", "ivern", "jax", "skarner", "poppy", "rumble", "wukong", "morgana", "maokai"]
			Jungle5 := [
				"zed", "gwen", "pantheon", "naafiri", "mordekaiser", "teemo", "trundle", "olaf", "qiyana", "yorick", "twitch", "drmundo"]
		}
		{ ; MiddleLaneChampions
			MiddleLane1 := [
				"lux", "syndra", "akali", "vex", "orianna", "xerath", "viktor", "lissandra", "galio", "malzahar"]
			MiddleLane2 := [
				"twistedfate", "aurelionsol", "irelia", "fizz", "naafiri", "veigar", "talon", "vladimir", "brand", "akshan"]
			MiddleLane3 := [
				"taliyah", "diana", "azir", "zoe", "ekko", "cassiopeia", "anivia", "kassadin", "qiyana", "malphite"]
			MiddleLane4 := [
				"lucian", "velkoz", "ryze", "annie", "ziggs", "ezreal", "jayce", "pantheon", "quinn", "neeko"]
			MiddleLane5 := [
				"swain", "gragas", "garen", "kayle", "smolder", "rumble", "nasus", "kennen", "tryndamere", "karma"]
			MiddleLane6 := [
				"renekton", "heimerdinger", "seraphine", "chogath", "varus", "zac", "sion", "nunu", "viego", "sett"]
		}
		{ ;BottomLaneChampions
			BottomLane1 := [
				"jinx", "karthus", "kaisa", "twitch", "draven", "ezreal", "brand", "zeri", "cassiopeia", "jhin"]
			BottomLane2 := [
				"tristana", "nilah", "yasuo", "seraphine", "kogmaw", "ashe", "aurelionsol", "swain", "lux", "lucian"]
			BottomLane3 := [
				"xayah", "vayne", "missfortune", "hwei", "caitlyn", "veigar", "heimerdinger", "tahmkench", "velkoz", "samira"]
			BottomLane4 := [
				"ziggs", "sivir", "kalista", "varus", "smolder", "akshan", "senna", "aphelios", "corki", "chogath"]
		}
		{ ;SupportLaneChampions
			SupportLane1 := [
				"alistar", "yuumi", "braum", "rell", "janna", "rakan", "senna", "seraphine", "soraka", "zyra"]
			SupportLane2 := [
				"xerath" "morgana" "bard" "sona" "brand" "poppy" "zilean" "velkoz" "maokai" "ashe"]
			SupportLane3 := [
				"hwei", "pantheon", "neeko", "renataglasc", "swain", "shaco", "taric", "tahmkench", "camille", "leblanc"]
			SupportLane4 := [
				"zac", "amumu", "galio", "sylas", "shen", "fiddlesticks", "zoe", "skarner", "heimerdinger", "rumble"]
			SupportLane5 := [
				"teemo", "annie", "missfortune", "twitch", "veigar", "malphite", "gragas", "anivia", "twistedfate", "sett"]
		}

		Main() { ; Main Function
			Champion := StrLower(InputBox("Champion?", "Champion Selection", "w250 h150").Value) ; Ask user for champion
			Lane := StrLower(InputBox("
			(
				Lane? enter as shown:
				top, jungle, middle, bottom, support
				)", "Lane Selection", "w250 h150").Value) ; Ask user for Lane
			switch Lane { ; Ask user for section of that lane
				Case "top":
					Section := Inputbox("
					(
					Answer with Section Number: Example, 1 = Section 1
					Section To Show? (Groups Of 10 In Order Of Most To Least Common)
					Section 1: Aatrox, Darius, Garen, Sett, Jax, Camille, Renekton, Volibear, Mordekaiser, Dr Mundo
					Section 2: Malphite, Nasus, Fiora, Ksante, Yone, Riven, Gragas, Irelia, Rumble, Gnar
					Section 3: Jayce, Kayle, Yorick, Tryndamere, Twisted Fate, Shen, Illaoi, Gangplank, Gwen, Pantheon
					Section 4: Skarner, Teemo, Vladimir, Vayne, Sion, Kennen, Urgot, Quinn, Tahm Kench, Akali
					Section 5: Kled, Warwick, Zac, Cho'gath, Trundle, Olaf, Singed, Yasuo, Heimerdinger, Wukong
					Section 6: Cassiopeia, Smolder, Sylas, Udyr, Varus, Shyvana, Rengar, Naafiri, Rammus, Sejuani
					Section 7: Akshan, Maokai, Lee Sin, Briar, Viego, Zed, Karma, Tristana, Lucian, Swain
					Leave Blank To Open All (Warning Long Load Time)

					)", "Section Select", "w680 h300").Value
				Case "jungle":
					Section := Inputbox("
					(
					Answer with Section Number: Example, 1 = Section 1
					Section To Show? (Groups Of 10 In Order Of Most To Least Common)
					Section 1: Hecarim, Brand, Master Yi, Jarvan Iv, Zyra, Ekko, Vi, Zac, Kindred
					Section 2: Xin Zhao, Sejuani, Karthus, Amumu, Taliyah, Udyr, Fiddlesticks, Bel'veth, Shyvana
					Section 3: Volibear, Briar, Gragas, Warwick, Rengar, Evelynn, Nunu, Elise, Sylas, Talon
					Section 4: Rek'sai, Rammus, Ivern, Jax, Skarner, Poppy, Rumble, Wukong, Morgana, Maokai
					Section 5: Zed, Gwen, Pantheon, Naafiri, Mordekaiser, Teemo, Trundle, Olaf, Qiyana, Yorick, Twitch, Dr Mundo
					Leave Blank To Open All (Warning Long Load Time)
					)", "Section Select", "w680 h300").Value
				Case "middle":
					Section := Inputbox("
					(
					Answer with Section Number: Example, 1 = Section 1
					Section To Show? (Groups Of 10 In Order Of Most To Least Common)
					Section 1: Lux, Syndra, Akali, Vex, Orianna, Xerath, Viktor, Lissandra, Galio, Malzahar
					Section 2: Twisted Fate, Aurelion Sol, Irelia, Fizz, Naafiri, Veigar, Talon, Vladimir, Brand, Akshan
					Section 3: Taliyah, Diana, Azir, Zoe, Ekko, Cassiopeia, Anivia, Kassadin, Qiyana, Malphite
					Section 4: Lucian, Vel'koz, Ryze, Annie, Ziggs, Ezreal, Jayce, Pantheon, Quinn, Neeko
					Section 5: Swain, Gragas, Garen, Kayle, Smolder, Rumble, Nasus, Kennen, Tryndamere, Karma
					Section 6: Renekton, Heimerdinger, Seraphine, Cho'gath, Varus, Zac, Sion, Nunu, Viego, Sett
					Leave Blank To Open All (Warning Long Load Time)
					)", "Section Select", "w680 h300").Value
				Case "bottom":
					Section := Inputbox("
					(
					Answer with Section Number: Example, 1 = Section 1
					Section To Show? (Groups Of 10 In Order Of Most To Least Common)
					Section 1: Jinx, Karthus, Kai'Sa, Twitch, Draven, Ezreal, Brand, Zeri, Cassiopeia, Jhin
					Section 2: Tristana, Nilah, Yasuo, Seraphine, Kog'Maw, Ashe, Aurelion Sol, Swain, Lux, Lucian
					Section 3: Xayah, Vayne, Miss Fortune, Hwei, Caitlyn, Veigar, Heimerdinger, Tahm Kench, Vel'Koz, Samira
					Section 4: Ziggs, Sivir, Kalista, Varus, Smolder, Akshan, Senna, Aphelios, Corki, Cho'Gath
					Leave Blank To Open All (Warning Long Load Time)
					)", "Section Select", "w680 h300").Value
				Case "support":
					Section := Inputbox("
					(
					Answer with Section Number: Example, 1 = Section 1
					Section To Show? (Groups Of 10 In Order Of Most To Least Common)
					Section 1: Alistar, Yuumi, Braum, Rell, Janna, Rakan, Senna, Seraphine, Soraka, Zyra
					Section 2: Xerath, Morgana, Bard, Sona, Brand, Poppy, Zilean, Vel'Koz, Maokai, Ashe
					Section 3: Hwei, Pantheon, Neeko, Renata Glasc, Swain, Shaco, Taric, Tahm Kench, Camille, Leblanc
					Section 4: Zac, Amumu, Galio, Sylas, Shen, Fiddlesticks, Zoe, Skarner, Heimerdinger, Rumble
					Section 5: Teemo, Annie, Miss Fortune, Twitch, Veigar, Malphite, Gragas, Anivia, Twisted Fate, Sett
					Leave Blank To Open All (Warning Long Load Time)
					)", "Section Select", "w680 h300").Value
			}
			Patch := InputBox("
			(
				Data Range?
				Blank = This Patch only
				7 = Last 7 Days
				14 = Last 14 Days
				30 = Last 30 Days
				)", "Data Range", "w250 h200").Value ; Ask User For Patch Range
			WikiWin := "https://leagueoflegends.fandom.com/wiki/" StrTitle(Champion) "/LoL#Details" ; Open Champion Wiki Page
			Run("chrome.exe --new-window " WikiWin) ; Open Url in new window
			sleep(2000)
			LoadMatchups(Champion, Lane, Section, Patch) ; Load User request
			; Function to get the title of the active window
			Sleep(5000)
			Send("^2") ; Move to first matchup tab
			WinMaximize("A") ; Maximize
			Send("^0") ; Reset Zoom
			Send("^-") ; Zoom out to view summoner spells
			Send("^-")
		}
		Main() ; Run Function
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