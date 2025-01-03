﻿#define characters
define sherlock = Character("Sherlock")
define moriarty = Character("Moriarty")
define narrator = Character(None)

#global variables for player stats
default player_health = 100
default player_max_health = 100
default player_damage_boost = 0
default special_attack_cooldown = 0

#transform to fit the screen size
transform fit_to_screen:
    size (config.screen_width, config.screen_height)

# New positioning transforms
define far_left = Transform(xalign=0.1, yalign=1.0)
define far_right = Transform(xalign=0.9, yalign=1.0)

#define background images
image bg CDO = "CDO.png"
image bg XUMuseum = "XUMuseum.png"
image bg EmptyGlassBox = "EmptyBladeBox.png"
image bg BattleBackground = "BattleBackground.png"
image bg DefaultBackground = "BattleBackground.png"

#sherlock path
image bg PoliceScene = "PoliceScene.png"
image bg MuseumFloor = "MuseumFloor.png"
image bg InterviewStaff = "InterviewStaff.png"
image bg RequestFullFiles = "RequestFullFiles.png"
image bg CrossReference = "CrossReference.png"
image bg LookIntoPolice = "LookIntoPolice.png"
image bg TraceMuseumDesign = "TraceMuseumDesign.png"
image bg IdentifySecurityAccess = "IdentifySecurityAccess.png"
image bg AnalyzeSecurityProtocol = "AnalyzeSecurityProtocol.png"
image bg InsideMuseum = "InsideMuseum.png"
image bg MidInvestigation = "MidInvestigation.png"
image bg ContinueTracking = "ContinueTrackingDagger.png"
image bg InvestigatePolitics = "InvestigatePolitics.png"
image bg InvestigateNetwork = "InvestigateNetwork.png"
image bg TrackBuyer = "TrackBuyer.png"
image bg NegotiateBuyer = "NegotiateBuyer.png"
image bg SherlockConfrontMoriarty = "SherlockConfrontMoriarty.png"
image bg SherlockFocusBlade = "SherlockFocusBlade.png"
image bg PeacefulNegotiation = "PeacefulNegotiation.png"
image bg FocusOnPolitics = "FocusOnPolitics.png"
image bg PoliticalChaosLostBlade = "PoliticalChaosLostBlade.png"
image bg SherlockVictory = "SherlockVictory.png"
image bg MoriartyVictory = "MoriartyVictory.png"
image bg MoriartyLeak = "MoriartyLeak.png"

#moriarty path
image bg GlassBoxwithBlade = "GlassBoxwithBlade.png"
image bg AnnounceArtifact = "AnnounceArtifact.png"
image bg SensitiveInformation = "SensitiveInformation.png"
image bg PoliticalLeaders = "PoliticalLeaders.png"
image bg InternationalInterests = "InternationalInterests.png"
image bg MoriartyRunning = "MoriartyRunning.png"
image bg HidingFestival = "HidingFestival.png"
image bg HidingSafehouse = "HidingSafehouse.png"
image bg HidingLogistics = "HidingLogistics.png"
image bg PrivateCollectors = "PrivateCollectors.png"
image bg Negotiate = "Negotiate.png"
image bg BlackMarket = "BlackMarket.png"
image bg MoriartyMischievous = "MoriartyMischievous.png"
image bg SherlockInvestigate = "SherlockInvestigate.png"
image bg MoriartyDistraction = "MoriartyDistraction.png"
image bg MoriartyMisdirection = "MoriartyMisdirection.png"
image bg MoriartyAngry = "MoriartyAngry.png"
image bg MoriartyAbandon = "MoriartyAbandon.png"
image bg MoriartyWin = "MoriartyWin.png"

#define character images
#main characters
image sherlock_portrait = "SherlockStanding.png"
image moriarty_portrait = "MoriartyStanding.png"
image sherlock_fight = "SherlockFighting.png"
image moriarty_fight = "MoriartyFighting.png"
#random encounter characters
image streetthug_fight = "StreetThug.png"
image pickpocket_fight = "FestivalPickpocket.png"
image rogueofficer_fight = "RogueOfficer.png"
image detectiveinspector_fight = "DetectiveInspector.png"
image bountyhunter_fight = "BountyHunter.png"
image rivalgangleader_fight = "RivalGangLeader.png"
image default_enemy = "RogueOfficer.png"
#npcs
image juniorcurator = "JuniorCurator.png"
image headsecurity = "MuseumSecurity.png"
image maintenanceworker = "MaintenanceWorker.png"


#error handling
init python:
    def custom_exception_handler(e):
        import traceback
        with open("error_log.txt", "a") as f:
            f.write(traceback.format_exc())
        
        #erorr message
        renpy.notify("You have been Sherlocked")

    config.exception_handler = custom_exception_handler

screen sherlock_error:
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        vbox:
            text "You have been Sherlocked" size 40
            textbutton "Continue" action Return() 

screen battle_screen(enemy_name, enemy_health, player_current_health, character_role):
    frame:
        xalign 0.5
        yalign 0.5
        vbox:
            spacing 10
            text "Battle with [enemy_name]" size 24
            
            hbox:
                text "Your Health: [player_current_health]/[player_max_health] |" size 20
                text "Enemy Health: [enemy_health]" size 20
            
            vbox:
                textbutton "Attack" action [SetVariable('battle_action', 'attack'), Return()]
                textbutton "Defend" action [SetVariable('battle_action', 'defend'), Return()]
                if special_attack_cooldown == 0:
                    textbutton "Special Attack" action [SetVariable('battle_action', 'special'), Return()]
                else:
                    textbutton "Special Attack (Cooldown)" action NullAction()

label handle_battle(enemy_name, character_role):
    $ battle_success = True
    
    python:
        try:
            enemy_health = renpy.random.randint(50, 80)
            current_player_health = player_health
            battle_action = None
            defend_active = False
            battle_won = False
        except Exception:
            renpy.notify("Critical battle error: You have been Sherlocked")
            battle_success = False

    scene bg BattleBackground

    python:
        try:
            if character_role == "Sherlock":
                player_fighting_image = "sherlock_fight"
                renpy.show("sherlock_fight", at_list=[Transform(xpos=-300, yalign=1.0)])
            elif character_role == "Moriarty":
                player_fighting_image = "moriarty_fight"
                renpy.show("moriarty_fight", at_list=[Transform(xpos=-300, yalign=1.0)])
        except Exception:
            renpy.notify("Error displaying character: You have been Sherlocked")
            battle_success = False

    python:
        try:
            enemy_sprite = {
                "Street Thug": "streetthug_fight",
                "Festival Pickpocket": "pickpocket_fight",
                "Rogue Officer": "rogueofficer_fight",
                "Detective Inspector": "detectiveinspector_fight",
                "Bounty Hunter": "bountyhunter_fight",
                "Rival Gang Leader": "rivalgangleader_fight"
            }.get(enemy_name, "default_enemy")
            renpy.show(enemy_sprite, at_list=[Transform(xpos=700, yalign=1.0)])
        except Exception:
            renpy.notify("Error displaying enemy: You have been Sherlocked")
            battle_success = False

    while current_player_health > 0 and enemy_health > 0 and battle_success:
        show screen battle_screen(enemy_name, enemy_health, current_player_health, character_role)
        $ battle_action = None
        
        #player turn
        $ result = ui.interact()
        
        if battle_action == "attack":
            $ player_damage = renpy.random.randint(10, 20 + player_damage_boost)
            $ enemy_health -= player_damage
            "[player_damage] damage dealt to [enemy_name]!"
            
            #enemy counter attack
            $ enemy_damage = renpy.random.randint(5, 15)
            $ current_player_health -= enemy_damage
            "[enemy_name] deals [enemy_damage] damage to you!"
            
        elif battle_action == "defend":
            $ defend_active = True
            "You take a defensive stance!"
            
        elif battle_action == "special" and special_attack_cooldown == 0:
            $ player_damage = renpy.random.randint(25, 35 + player_damage_boost)
            $ enemy_health -= player_damage
            $ special_attack_cooldown = 3
            "Special attack deals [player_damage] damage to [enemy_name]!"

    hide screen battle_screen
    
    if current_player_health <= 0:
        "You were defeated!"
        $ battle_success = False
    elif enemy_health <= 0:
        "You defeated [enemy_name]!"
        $ battle_success = True

    return battle_success

#random battle encounters
label random_encounter(character_role):
    $ enemy_types = ["Street Thug", "Festival Pickpocket", "Rogue Officer", 
                    "Detective Inspector", "Bounty Hunter", "Rival Gang Leader"]
    $ enemy_name = renpy.random.choice(enemy_types)
    
    "A [enemy_name] appears!"
    
    call handle_battle(enemy_name, character_role) from _call_handle_battle
    
    if _return:
        "You won the battle!"
    else:
        "The battle was interrupted!"
    
    return True

#start of game
label start:
    $ game_success = True
    
    scene bg CDO at fit_to_screen
    "Welcome to the Shadows of Cagayan de Oro! A high-stakes game of wits awaits between Sherlock Holmes and Professor Moriarty."

    menu:
        "Play as Sherlock Holmes, the consulting detective.":
            $ role = "sherlock"
        "Play as Professor Moriarty, the criminal mastermind.":
            $ role = "moriarty"

    if role == "sherlock":
        play music "audio/Sherlock-Theme.mp3" 
        show sherlock_portrait
        jump sherlock_path
    else:
        play music "audio/Moriarty-Theme.mp3" 
        show moriarty_portrait
        jump moriarty_path

label sherlock_path:
    scene bg XUMuseum with fade
    show sherlock_portrait
    "You are Sherlock Holmes, consulting detective, called to Cagayan de Oro City on a critical mission."
    "The Xavier University Museum has been robbed of a rare ceremonial dagger - the Lumad Heritage Blade."
    scene bg EmptyGlassBox with fade
    show sherlock_portrait
    "This isn't merely a theft, but a potential cultural catastrophe that threatens the indigenous heritage of Mindanao."
    "The Higalaay Festival is days away, and the stolen artifact could be sold to the highest bidder."
    "Your long-time nemesis, Professor Moriarty, is suspected to be behind this elaborate scheme."

    hide moriarty_portrait
    #First Major Investigation Stage: Initial Intelligence Gathering
    menu:
        "Contact local law enforcement for their initial report.":
            $ initial_choice = 1
        "Examine the museum's floor plans and security protocols.":
            $ initial_choice = 2
        "Discreetly interview museum staff about recent suspicious activities.":
            $ initial_choice = 3

    if initial_choice == 1:
        scene bg PoliceScene with fade
        hide sherlock_portrait
        "The local police report is frustratingly vague. Budget cuts have limited their investigative capabilities."
        "However, you notice a subtle pattern in the report - signs of a professionally executed theft."
        menu:
            "Request access to the full investigation files.":
                scene bg RequestFullFiles with fade
                $ police_follow_up = 1
            "Cross-reference the report with your own network of informants.":
                $ police_follow_up = 2
                scene bg CrossReference with fade
            "Look into the backgrounds of the responding officers.":
                $ police_follow_up = 3
                scene bg LookIntoPolice with fade

        if police_follow_up == 1:
            "The full files reveal inconsistencies that suggest an inside connection."
            "A partial fingerprint was found, but mysteriously never followed up on."
        elif police_follow_up == 2:
            "Your informants whisper about unusual movements in the criminal underground."
            "Someone is quietly buying specialized equipment for a high-stakes artifact transfer."
        else:
            "One of the responding officers has an unexplained recent influx of wealth."
            "A potential lead, but not conclusive evidence."

        call random_encounter("Sherlock") from _call_random_encounter
        if _return:
            "You successfully defended yourself during the encounter."
       
    elif initial_choice == 2:
        scene bg MuseumFloor with fade
        hide sherlock_portrait
        "The museum's security system is sophisticated, yet deliberately compromised."
        "Someone with intimate knowledge of security protocols planned this theft."
        menu:
            "Trace the origin of the security system's design.":
                $ security_investigation = 1
                scene bg TraceMuseumDesign with fade
            "Identify who had complete access to the security protocols.":
                $ security_investigation = 2
                scene bg IdentifySecurityAccess with fade
            "Analyze the exact method of bypassing the security.":
                $ security_investigation = 3
                scene bg AnalyzeSecurityProtocol with fade

        if security_investigation == 1:
            "The security system was designed by a former military engineer with a controversial past."
            "Connections to international arms dealers emerge."
        elif security_investigation == 2:
            "Only three people had complete security access."
            "One is a recently transferred curator with an impeccable - perhaps too perfect - background."
        else:
            "The security breach shows signs of a cutting-edge electronic bypass."
            "This requires exceptional technological expertise."


        call random_encounter("Sherlock") from _call_random_encounter_1
        if _return:
            "You successfully defended yourself during the encounter."
            
    elif initial_choice == 3:
        scene bg InterviewStaff with fade
        hide sherlock_portrait
        "Museum staff are nervous, each interview revealing fragments of a complex puzzle."
        "Someone is manipulating the staff, creating an atmosphere of fear and uncertainty."

        menu:
            "The nervous junior curator.":
                $ staff_investigation = 1
                scene bg InsideMuseum
                show juniorcurator
            "The overly calm head of security.":
                $ staff_investigation = 2
                scene bg InsideMuseum
                show headsecurity
            "A maintenance worker who seems out of place.":
                $ staff_investigation = 3
                scene bg InsideMuseum
                show maintenanceworker

        if staff_investigation == 1:
            "The junior curator breaks down, revealing potential blackmail."
            "Someone knows about their significant gambling debts."
        elif staff_investigation == 2:
            "The head of security's background doesn't quite add up."
            "Recent bank transfers suggest a potential payoff."
        else:
            "The maintenance worker has connections to an international smuggling ring."
            "Their movements are suspiciously coordinated."

        call random_encounter("Sherlock") from _call_random_encounter_2
        if _return:
            "You successfully defended yourself during the encounter."
        
    #Mid Investigation: Realizing the Bigger Picture
    scene bg MidInvestigation with fade
    "You are piecing together the puzzle, but there are troubling signs of a much larger conspiracy at play."
    "You start suspecting that Moriarty isn't just after the dagger; he's orchestrating a political crisis in Mindanao."
    
    menu:
        "Focus on tracking the dagger to prevent the auction.":
            $ deeper_choice = 1
            scene bg ContinueTracking with fade
        "Investigate the political unrest and stop the escalation.":
            $ deeper_choice = 2
            scene bg InvestigatePolitics with fade
        "Dig deeper into Moriarty's network and his potential manipulations.":
            $ deeper_choice = 3
            scene bg InvestigateNetwork with fade

    if deeper_choice == 1:
        menu:
            "Track down the buyer, even though the trail is cold.":
                $ path_1 = 1
                scene bg TrackBuyer with fade
                
                call random_encounter("Sherlock") from _call_random_encounter_9
                if _return:
                    "You fend off an attacker while pursuing the buyer."
                
            "Try negotiating with the buyer, but it's too risky.":
                $ path_1 = 2
                scene bg NegotiateBuyer with fade
                
                call random_encounter("Sherlock") from _call_random_encounter_10
                if _return:
                    "You overcome an ambush during negotiations."
                
            "Confront Moriarty directly.":
                $ path_1 = 3
                scene bg SherlockConfrontMoriarty with fade
                
                call random_encounter("Sherlock") from _call_random_encounter_11
                if _return:
                    "You defeat one of Moriarty's henchmen before the confrontation."

    #Decision point: Responding to the realization of Moriarty's deeper motives
        if path_1 == 1:
            "The trail leads nowhere. The blade is gone, and the political unrest in Mindanao spirals out of control."
            jump bad_ending_1_sherlock
        elif path_1 == 2:
            "Your diplomatic approach fails miserably. The buyer demands an astronomical price for the artifact."
            "Moriarty's scheme succeeds, and the region is torn apart by the loss of the blade."
            jump bad_ending_1_sherlock
        else:
            "You confront Moriarty and outwit him, recovering the artifact before it's too late!"
            "The Lumad Heritage Blade is returned to the museum, and Moriarty's plans are foiled. You have won!"
            jump good_ending_sherlock

        
        call random_encounter("Sherlock") from _call_random_encounter_3
        if _return:
            "You successfully defended yourself during the encounter."
        
    elif deeper_choice == 2:
        menu:
            "Focus now on recovering the blade, even though it's too late.":
                $ path_2 = 1
                scene bg SherlockFocusBlade with fade
                
                call random_encounter("Sherlock") from _call_random_encounter_12
                if _return:
                    "You fight off criminals trying to stop your investigation."
                
            "Try to negotiate a peaceful resolution with the buyer.":
                $ path_2 = 2
                scene bg PeacefulNegotiation with fade
                
                call random_encounter("Sherlock") from _call_random_encounter_13
                if _return:
                    "You survive an attempt on your life during negotiations."
                
            "Focus on the escalating unrest and hope the blade is returned.":
                $ path_2 = 3
                scene bg FocusOnPolitics with fade
                
                call random_encounter("Sherlock") from _call_random_encounter_14
                if _return:
                    "You overcome armed thugs stirring up unrest."


        if path_2 == 1:
            "You waste precious time. The auction continues, and the political unrest grows. The blade is lost."
            jump bad_ending_2_sherlock
        elif path_2 == 2:
            "Your attempts to negotiate with the buyer fall apart, and the region descends into chaos."
            jump bad_ending_2_sherlock
        else:
            "You manage to calm the political unrest, allowing time for the blade to be returned safely."
            "You successfully prevent the escalation, ensuring the blade's safe return to the museum. Your victory secures peace!"
            jump good_ending_sherlock
        
        
        call random_encounter("Sherlock") from _call_random_encounter_4
        if _return:
            "You successfully defended yourself during the encounter."
       
    elif deeper_choice == 3:
        menu:
            "Regroup quickly, track down Moriarty's auctioneer contacts, and retrieve the artifact.":
                $ path_3 = 1
                
                call random_encounter("Sherlock") from _call_random_encounter_15
                if _return:
                    "You defeat a group of auction house guards."
                
            "Confront Moriarty, knowing you've fallen into his trap, but now with a plan to turn the tables.":
                $ path_3 = 2
                
                call random_encounter("Sherlock") from _call_random_encounter_16
                if _return:
                    "You fight through Moriarty's security to reach him."
                
            "Use your network of informants to track Moriarty's next move and intercept the blade before it's lost.":
                $ path_3 = 3
                
                call random_encounter("Sherlock") from _call_random_encounter_17
                if _return:
                    "You protect your informant from attackers."

        if path_3 == 1:
            "Your investigation into the auction network leads nowhere. Moriarty's influence runs too deep."
            "The blade disappears into the black market, and your failure haunts you."
            jump bad_ending_3_sherlock
        elif path_3 == 2:
            "Your confrontation with Moriarty reveals you've underestimated his preparation."
            "He escapes with both the blade and crucial political leverage. The region falls into chaos."
            jump bad_ending_3_sherlock
        else:
            "Your network of informants proves invaluable, leading you straight to Moriarty's operation."
            "You not only recover the blade but also expose his entire network. A complete victory!"
            jump good_ending_sherlock
        
        
        call random_encounter("Sherlock") from _call_random_encounter_5
        if _return:
            "You successfully defended yourself during the encounter."
        
#sherlock_path endings
label good_ending_sherlock:
    scene bg SherlockVictory with fade
    "The Lumad Heritage Blade gleams in its rightful place at the Xavier University Museum."
    "Your victory has preserved not just an artifact, but the cultural heritage of Mindanao."
    "The Higalaay Festival can proceed as planned, and Moriarty's attempt to destabilize the region has been thwarted."
    "Another case solved, though you know this won't be the last time you face your nemesis."
    "THE END - Victory for Sherlock Holmes"
    return

label bad_ending_1_sherlock:
    scene bg EmptyGlassBox with fade
    "The empty display case stands as a testament to your failure."
    "The loss of the Lumad Heritage Blade has sparked tensions throughout Mindanao."
    "Moriarty's plan succeeded - the blade is lost, and with it, a piece of cultural heritage that can never be replaced."
    "Sometimes even the great Sherlock Holmes meets defeat..."
    "THE END - The Lost Artifact"
    return

label bad_ending_2_sherlock:
    scene bg PoliticalChaosLostBlade with fade
    "Your focus on the political aspects of the case proved to be your undoing."
    "While you attempted to manage the growing unrest, the blade slipped through your fingers."
    "Now both the artifact is lost and the region faces unprecedented turmoil."
    "Moriarty's masterful plan has succeeded on both fronts."
    "THE END - Political Failure"
    return

label bad_ending_3_sherlock:
    scene bg MoriartyVictory with fade
    "Your attempt to outmaneuver Moriarty's network has backfired spectacularly."
    "The criminal mastermind proved once again why he is your greatest adversary."
    "The blade is gone, his network remains intact, and Mindanao's heritage suffers an irreparable loss."
    "Some puzzles, it seems, are beyond even your legendary abilities to solve."
    "THE END - Moriarty's Triumph"
    return

label moriarty_path:
    #moriarty introduction
    scene bg XUMuseum with fade
    show moriarty_portrait

    "You are Professor James Moriarty, a criminal mastermind orchestrating chaos from the shadows."
    "The Lumad Heritage Blade, a powerful artifact with immense cultural value, is in your possession."
    
    "This theft isn't simply for profit. It's a carefully calculated move to destabilize the region and create political upheaval."
    "Sherlock Holmes is once again hot on your trail, but you know the game isn't over yet."

    #Initial Strategy Choice
    "Choose your initial strategy for the artifact"
    menu:
        "Release it to the public, creating cultural tensions.":
            $ initial_strategy = 1
        "Hide it in a temporary location, away from Sherlock's eyes.":
            $ initial_strategy = 2
        "Sell it to the highest bidder, maximizing its value.":
            $ initial_strategy = 3

    #First Major Strategic Stage: Initial Artifact Placement
    if initial_strategy == 1:
        scene bg AnnounceArtifact with fade
        hide moriarty_portrait
        "The artifact is much more than a simple treasure; its significance is far-reaching."
        menu:
            "Release sensitive cultural information":
                $ cultural_choice = 1
                scene bg SensitiveInformation with fade                
            "Manipulate political leaders":
                $ cultural_choice = 2
                scene bg PoliticalLeaders with fade                
            "Involve international interests":
                $ cultural_choice = 3
                scene bg InternationalInterests with fade

        if cultural_choice == 1:
                "By releasing the blade to the public, cultural tensions in Mindanao escalate."
                "The local factions clash, weakening the region's stability."
                "Your manipulation of the media and local leaders solidifies your control, but the unrest continues to simmer."
                "As the unrest grows, you find yourself at the center of a storm, with factions vying for your support."
                "You must carefully navigate these alliances to maintain your influence and avoid becoming a target yourself."
        elif cultural_choice == 2:
                "Certain political leaders would pay handsomely to keep this artifact hidden."
                "Blackmail and manipulation lead to significant power shifts."
                "Your alliances and strategic destabilization efforts pay off, but rival factions remain a threat."
                "With new power dynamics in play, you must constantly outmaneuver rivals who seek to undermine your position."
                "The political landscape is volatile, and one misstep could unravel all your carefully laid plans."
        elif cultural_choice == 3:
            "Foreign governments take an interest in the blade's value."
            "You fuel international tensions to distract Sherlock from your true agenda."
            "Your secret deals and misinformation campaigns succeed, but the international spotlight remains a concern."
            "As global powers turn their attention to the region, you must ensure your operations remain hidden."
            "The stakes are higher than ever, and any exposure could lead to catastrophic consequences for your schemes."

        call random_encounter("Moriarty") from _call_random_encounter_6
        if _return:
            "You successfully defended yourself during the encounter."

    elif initial_strategy == 2:
        scene bg MoriartyRunning with fade
        hide moriarty_portrait
        "A temporary holding location must be chosen with care. The artifact must remain hidden from prying eyes."
        menu:
            "Hide during the festival":
                $ hiding_choice = 1
                scene bg HidingFestival with fade
            "Use multiple safehouses":
                $ hiding_choice = 2
                scene bg HidingSafehouse with fade
            "Blend with festival logistics":
                $ hiding_choice = 3
                scene bg HidingLogistics with fade

        if hiding_choice == 1:
            "The festival grounds offer excellent cover for a hidden compartment."
            "No one will suspect the dagger is in plain view amidst the chaos of the event."
        elif hiding_choice == 2:
            "Moving the artifact from one safehouse to another keeps Sherlock in the dark."
            "By the time he figures out one location, the blade has already vanished."
        elif hiding_choice == 3:
            "Blending the artifact within the festival logistics makes tracking nearly impossible."
            "The constant movement and large crowds hide its true location."
        
        call random_encounter("Moriarty") from _call_random_encounter_7
        if _return:
            "You successfully defended yourself during the encounter."

    elif initial_strategy == 3:
        "The right buyer is crucial to maximizing the value of the artifact, but the timing must be perfect."
        menu:
            "Sell to private collectors":
                $ buyer_choice = 1
                scene bg PrivateCollectors with fade
            "Negotiate with political players":
                $ buyer_choice = 2
                scene bg Negotiate with fade
            "Auction in black market":
                $ buyer_choice = 3
                scene bg BlackMarket with fade

        if buyer_choice == 1:
            "The sale to private collectors is successful."
            "The collectors' satisfaction ensures the artifact's safety, but their demands for exclusivity remain a challenge."
            "You must carefully manage their expectations to maintain their trust and avoid any potential leaks."

        elif buyer_choice == 2:
            "Negotiations with political players succeed."
            "The political players' influence secures the artifact's safety, but their ongoing demands require careful management."
            "You find yourself entangled in a web of political intrigue, where every decision could have far-reaching consequences."

        elif buyer_choice == 3:
            "The auction in the black market attracts Sherlock's attention."
            "The auction's success brings significant profit, but the increased scrutiny from Sherlock poses a constant threat."
            "You must stay one step ahead, using every resource at your disposal to keep your operations hidden from his watchful eyes."
        
        call random_encounter("Moriarty") from _call_random_encounter_8
        if _return:
            "You successfully defended yourself during the encounter."
        
    #Mid Stage: Realizing Sherlock's Investigations
    scene bg SherlockInvestigate with fade
    "As Sherlock begins his investigation, you know he is closing in on the artifact."
    "But his focus on the blade will blind him to the larger scheme you've set in motion."

    menu:
        "Use misdirection and false clues":
            $ manipulation_choice = 1
            jump moriarty_misdirection
        "Create strategic distractions":
            $ manipulation_choice = 2
            jump moriarty_distraction
        "Manipulate information flow":
            $ manipulation_choice = 3
            jump moriarty_leak

    return

    #Path 1: Misdirection through false clues
label moriarty_misdirection:
    scene bg MoriartyMischievous with fade
    "Professor Moriarty carefully weaves a web of deception. Sherlock Holmes, brilliant as he is, will follow the carefully laid plan."
    
    call random_encounter("Moriarty") from _call_random_encounter_18
    if _return:
        "You eliminate a potential informant who could expose your plan."
    
    menu:
        "Plant subtle clues to consume Sherlock's analytical mind":
            $ misdirection_path = 1
            scene bg MoriartyMisdirection with fade
            
            call random_encounter("Moriarty") from _call_random_encounter_19
            if _return:
                "You deal with an overly curious detective."
            
        "Create a complex network of misdirections":
            $ misdirection_path = 2
            scene bg MoriartyMisdirection with fade
            
            call random_encounter("Moriarty") from _call_random_encounter_20
            if _return:
                "You silence a loose end in your network."
            
        "Craft an elegant misdirection worthy of Holmes":
            $ misdirection_path = 3
            scene bg MoriartyMisdirection with fade
            
            call random_encounter("Moriarty") from _call_random_encounter_21
            if _return:
                "You overcome a rival criminal who tried to interfere."

    if misdirection_path == 1:
        "Holmes' brilliant mind spins endlessly chasing carefully constructed phantoms. The auction proceeds unnoticed."
        jump bad_ending_1
    elif misdirection_path == 2:
        "Holmes sees through the first layer, but he's already trapped within the labyrinth. Victory approaches."
        jump bad_ending_2
    elif misdirection_path == 3:
        "The plan works perfectly. Holmes is completely consumed, his brilliant mind becoming his greatest weakness."
        jump good_ending
    

    
#Path 2: Strategic Distraction
label moriarty_distraction:
    scene bg MoriartyMischievous with fade
    "Moriarty prepares his masterful distraction. Each element is calculated to redirect Holmes' razor-sharp focus."
    
    call random_encounter("Moriarty") from _call_random_encounter_22
    if _return:
        "You defeat someone who discovered your distraction plan."
    
    menu:
        "Create a compelling spectacle":
            $ distraction_path = 1
            scene bg MoriartyDistraction with fade
            
            call random_encounter("Moriarty") from _call_random_encounter_23
            if _return:
                "You handle an unexpected police patrol."
            
        "Introduce strategic uncertainty":
            $ distraction_path = 2
            scene bg MoriartyDistraction with fade
            
            call random_encounter("Moriarty") from _call_random_encounter_24
            if _return:
                "You eliminate a potential witness."
            
        "Design an intellectual challenge":
            $ distraction_path = 3
            scene bg MoriartyDistraction with fade
            
            call random_encounter("Moriarty") from _call_random_encounter_25
            if _return:
                "You overcome a rival intellectual who saw through your plan."

    if distraction_path == 1:
        "The distraction proves effective, momentarily blinding Holmes to Moriarty's true intentions."
        jump bad_ending_1
    elif distraction_path == 2:
        "The seeds of doubt take root. Uncertainty proves more effective than any physical restraint."
        jump bad_ending_2
    elif distraction_path == 3:
        "The plan succeeds perfectly. While Holmes unravels the intricate distraction, the true prize slips away."
        jump good_ending


    
#Path 3: Information Manipulation
label moriarty_leak:
    scene bg MoriartyMischievous with fade
    "Moriarty prepares to weaponize information with surgical precision and strategic ruthlessness."
    
    call random_encounter("Moriarty") from _call_random_encounter_26
    if _return:
        "You deal with someone who intercepted your leaked information."
    
    menu:
        "Release tantalizing information":
            $ leak_path = 1
            scene bg MoriartyLeak with fade
            
            call random_encounter("Moriarty") from _call_random_encounter_27
            if _return:
                "You silence a journalist who got too close to the truth."
            
        "Create a misleading source":
            $ leak_path = 2
            scene bg MoriartyLeak with fade
            
            call random_encounter("Moriarty") from _call_random_encounter_28
            if _return:
                "You defeat an agent who discovered your false source."
            
        "Plant a deliberate 'mistake'":
            $ leak_path = 3
            scene bg MoriartyLeak with fade
            
            call random_encounter("Moriarty") from _call_random_encounter_29
            if _return:
                "You overcome someone who noticed the intentional mistake."

    if leak_path == 1:
        "The information spreads rapidly, consuming Holmes' attention while Moriarty works unobserved."
        jump bad_ending_1
    elif leak_path == 2:
        "Holmes begins to see the manipulation, but the plan is already well underway."
        jump bad_ending_2
    elif leak_path == 3:
        "The strategy proves flawless. While Holmes traces the leak, the auction concludes without interference."
        jump good_ending
    


#moriarty_path endings
label bad_ending_1:
    scene bg MoriartyAngry with fade
    "Despite Moriarty's efforts, unforeseen circumstances force his plans into disarray."
    "Holmes closes in as the region's unrest reaches a boiling point."
    "Your attempts to outmaneuver Holmes have failed, leaving Moriarty's plans in ruins."
    "The chaos Moriarty sought to create has fizzled out, leaving him powerless in its wake."
    "THE END - Unrest Quelled"
    return

label bad_ending_2:
    scene bg MoriartyAbandon with fade
    "Holmes' relentless pursuit forces Moriarty to abandon his plans."
    "As the detective closes the case, the political instability wanes, and Moriarty's influence diminishes."
    "The genius criminal is left to watch his empire of schemes crumble before him."
    "THE END - Holmes' Victory"
    return

label good_ending:
    scene bg MoriartyWin with fade
    "Moriarty's manipulation of Holmes succeeds spectacularly."
    "The artifact is sold, and chaos erupts across the region as planned."
    "Unseen and untouchable, Moriarty remains the puppet master, orchestrating chaos from the shadows."
    "His reputation as the ultimate criminal mastermind grows, undeterred by Sherlock Holmes."
    "THE END - Victory for Moriarty"
    return