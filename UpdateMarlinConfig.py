from os.path import exists
import re

#exampledir = f'C:\Firmware\skrv3\Configurations\config\examples\Creality\Ender-3\BigTreeTech SKR Mini E3 3.0'


# 3 Plugins: PlatformIO IDE, Auto Build Marlin, C/C++
# Optional Plugin: Python, Compare Folders
# Download: https://marlinfw.org/meta/download/
# Unzip Marlin-2.1.2.1.zip -> C:\Firmware\skrv3_main\Marlin-2.1.2.1
# Move C:\Firmware\skrv3_main\Marlin-2.1.2.1\Marlin-2.1.2.1 to C:\Firmware\skrv3_main\Marlin-2.1.2.1
# Rename Marlin-2.1.2.1 to Marlin
#
# Unzip Configurations-release-2.1.2.1.zip -> C:\Firmware\skrv3_main\Configurations-release-2.1.2.1
# cd C:\Firmware\skrv3_main\Configurations-release-2.1.2.1\Configurations-release-2.1.2.1\config\examples\Creality\Ender-3\BigTreeTech SKR Mini E3 3.0
# copy all 4 files to C:\Firmware\skrv3_main\Marlin\Marlin
#
# In Visual Studio Code -> File -> Open Folder -> C:\Firmware\skrv3_main\Marlin     (YES, Outer Marlin folder)
# Do Test Build (Auto Build Marlin)
# NOTE: if it fails, delete C:\Firmware\skrv3_main\Marlin\.pio and try again
#
# Modify MARLIN/Marlin/Configuration.h
#   --- BR/CR Touch ---
#   //#define Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN                    Make sure it commented out - This is for BLTouch connected to Z Endstop
#   #define USE_PROBE_FOR_Z_HOMING                                  Uncomment
#   #define BLTOUCH                                                 Uncomment
#   #define NOZZLE_TO_PROBE_OFFSET { -40, -10, -1.85 }              Set for Creality Sprite Pro
#   #define AUTO_BED_LEVELING_BILINEAR                              Uncomment
#   //#define MESH_BED_LEVELING                                     Comment out
#   #define Z_SAFE_HOMING                                           Uncomment
#   #define EEPROM_INIT_NOW                                         Uncomment   - clear eeprom on first boot
#   //#define MIN_SOFTWARE_ENDSTOP_Z                                Comment out - allows you to set z-offset below 0
#   --- Optional ---
#   #define X_BED_SIZE 235
#   #define Y_BED_SIZE 235
#   #define GRID_MAX_POINTS_X 3                                     Under EITHER(AUTO_BED_LEVELING_LINEAR, AUTO_BED_LEVELING_BILINEAR)
#   #define PROBING_MARGIN 40                                       Don't probe too close to the edge of the bed
# Modify MARLIN/Marlin/Configuration_adv.h
#   #define PROBE_OFFSET_WIZARD                                     Uncomment
#   #define SHOW_PROGRESS_PERCENT                                   Add under "#if HAS_MARLINUI_U8GLIB || IS_DWIN_MARLINUI", use to be SHOW_SD_PERCENT
#   #define SHOW_REMAINING_TIME                                     Uncomment
#   #define ROTATE_PROGRESS_DISPLAY                                 (Optional) Add this after last command to rotate between them
#
#   #define DIAG_JUMPERS_REMOVED                                    Add this to the top of Configuration.h file to suppress jumper warnings
#
#   --- BTT Smart Filament Runout Sensor ---
#   Modify MARLIN/Marlin/Configuration.h
#       #define FILAMENT_RUNOUT_SENSOR
#       #define FILAMENT_RUNOUT_DISTANCE_MM 7
#       #define FILAMENT_MOTION_SENSOR
#       #define NOZZLE_PARK_FEATURE                                 Make sure this is uncommented
#   Modify MARLIN/Marlin/Configuration_adv.h
#       #define ADVANCED_PAUSE_FEATURE                              Make sure this is uncommented
#       #define FILAMENT_CHANGE_UNLOAD_LENGTH 100
#   Modify /MARLIN/Marlin/src/pins/stm32f1/pins_BTT_SKR_MINI_E3_common.h        (stm32f1 is the chip on the board)
#       #define FIL_RUNOUT_PIN   PC15  // E0-STOP                   We are using the E0-STOP port
#
#  TIP: in Configuration_adv.h make sure HOST_ACTION_COMMANDS and HOST_PROMPT_SUPPORT are uncommented so Octoprint can handle filament runout
#
#
#   --- Normal Runout Sensor ---
#   Modify MARLIN/Marlin/Configuration.h
#       #define FILAMENT_RUNOUT_SENSOR
#       #define FIL_RUNOUT_STATE     LOW                            Low is the default, use this to reverse if necessary
#       #define FILAMENT_RUNOUT_SCRIPT "M600"                       * This only seems necessary for PRUSA
                        # M119 should report filament: open, when filament is out
                        # M119 should report filament: TRIGGERED, when filement is avaliable
                        # if that is backwards, set #define FIL_RUNOUT_STATE  HIGH
#
# Clean and Build
# Copy to micro-SD card and reboot 3d printer, if successful the file will be renamed from firmware.bin to FIRMWARE.CUR
# Remember to add G29 code to Ultimaker Cura to run ABL before prints
#
# Additional Note:
#   Modify MARLIN/Marlin/Configuration_adv.h
#   #define NO_SD_DETECT                                            Allow you to init / refresh the SD card
#   #define SD_DETECT_STATE HIGH                                    Reverse the detection of the SD card


exampledir = f'C:\Firmware\skrv3_main\Configurations-release-2.1.2.1\Configurations-release-2.1.2.1\config\examples\Creality\Ender-3\BigTreeTech SKR Mini E3 3.0'
outputdir = f'C:\Firmware\skrv3_main\Marlin\Marlin'

if __name__ == '__main__':
    print()
    print('0. Default Hotend')
    print('1. Creality Sprite Extruder Pro')
    while True:
        hotend = input('Enter your Hotend type(0-1): ')
        if hotend == "0":
            hotend = 0
            print('  \033[48;5;57m\033[38;5;15m Default Hot End \033[0m')
            break
        elif hotend == "1":
            hotend = 1
            print('  \033[48;5;57m\033[38;5;15m Creality Sprite Extruder Pro \033[0m')
            break
    if hotend == 1:
        print()
        while True:
            zoff = input('Enter your Z-Offset(-10.0 to 10.0): ')
            if re.search('^-?[0-9][0-9]?\.[0-9]+$|^[0-9][0-9]?$', zoff):
                zoff = float(f'{float(zoff):.2f}')
                if zoff > -10.001 and zoff < 10.001:
                    print(f'  \033[48;5;57m\033[38;5;15m {zoff:.2f} is your Z-Offset \033[0m')
                    break
    print()
    print('0. No Run Out Sensor')
    print('1. Normal Run Out Sensor')
    print('2. Smart Run Out Sensor')
    while True:
        runout = input('Enter your Run Out Sensor Type(0-2): ')
        if runout == "0":
            runout = 0
            print('  \033[48;5;57m\033[38;5;15m No Run Out Sensor \033[0m')
            break
        elif runout == "1":
            runout = 1
            print('  \033[48;5;57m\033[38;5;15m Normal Run Out Sensor \033[0m')
            break
        elif runout == "2":
            runout = 2
            print('  \033[48;5;57m\033[38;5;15m Smart Run Out Sensor \033[0m')
            break
    print()
    while True:
        touch = input("Are you using BLTOUCH  or CRTOUCH(Y/N): ")
        if touch.strip().upper() == "Y":
            touch = True
            print('  \033[48;5;57m\033[38;5;15m BLTOUCH/CRTOUCH Selected \033[0m')
            break
        elif touch.strip().upper() == "N":
            touch = False
            print('  \033[48;5;57m\033[38;5;15m No ABL device \033[0m')
            break
    if touch:
        print()
        while True:
            gridpoints = input('Enter Touch Max Grid Points(1-7): ')
            if gridpoints.isnumeric() and int(gridpoints)>0 and int(gridpoints)<8:
                gridpoints = int(gridpoints)
                print(f'  \033[48;5;57m\033[38;5;15m {gridpoints} Grid points selected ({gridpoints * gridpoints} total) \033[0m')
                break
    print()

    if exists(f'{exampledir}\\Configuration.h'):
        with open(f'{exampledir}\\Configuration.h', encoding='utf8') as file:
            conf = file.read().splitlines()

    if exists(f'{exampledir}\\Configuration_adv.h'):
        with open(f'{exampledir}\\Configuration_adv.h', encoding='utf8') as file:
            advconf = file.read().splitlines()

    #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    print('\033[32mConfiguration.h\033[0m')
    target = False
    for i, line in enumerate(conf):
        if re.search(r'\bHEATER_0_MAXTEMP\b', line) and hotend == 1:                                                                         # Set Temp to 275°C ( 300°C - 15°C )
            #print(f'\033[33m{line}\033[0m')
            #conf[i] = "#define HEATER_0_MAXTEMP 295  // JEREMY default: 275 (250°C)"
            print(conf[i])
        elif re.search(r'define \bHOTEND_OVERSHOOT\b', line) and hotend == 1:
            # print(f'\033[33m{line}\033[0m')
            #conf[i] = "#define HOTEND_OVERSHOOT 5   // (°C) Forbid temperatures over MAXTEMP - OVERSHOOT"
            print(conf[i])
        #elif re.search(r'define \bX_BED_SIZE\b', line):
            #print(f'\033[33m{line}\033[0m')
            #conf[i] = "#define X_BED_SIZE 235 // JEREMY default: 235"
            #print(conf[i])
        #elif re.search(r'define \bY_BED_SIZE\b', line):
            #print(f'\033[33m{line}\033[0m')
            #conf[i] = "#define Y_BED_SIZE 235 // JEREMY default: 235"
            #print(conf[i])
        elif re.search(r'define \bFILAMENT_RUNOUT_SENSOR\b', line) and runout>0:                                                            # Enable Runout Sensor
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "#define FILAMENT_RUNOUT_SENSOR // JEREMY - Enable Runout Sensor"
            print(conf[i])
        elif re.search(r'define NUM_RUNOUT_SENSORS', line) and runout>0:
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "  #define NUM_RUNOUT_SENSORS   1  // JEREMY - set to 1, then update pins_BTT_SKR_MINI_E3_common.h"
            # /MARLIN/Marlin/src/pins/stm32f1/pins_BTT_SKR_MINI_E3_common.h
            print(conf[i])
        elif re.search(r'define \bFILAMENT_RUNOUT_DISTANCE_MM\b', line) and runout == 2:                                                    # Needed only with Smart Run Out Sensor
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "  #define FILAMENT_RUNOUT_DISTANCE_MM 7 // JEREMY set smart sensor length"
            print(conf[i])
        elif re.search(r'define \bFILAMENT_MOTION_SENSOR\b', line) and runout == 2:                                                         # Needed only with Smart Run Out Sensor
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "    #define FILAMENT_MOTION_SENSOR // JEREMY enable motion sensor"
            print(conf[i])
        elif re.search(r'define \bGRID_MAX_POINTS_X\b [0-9]+', line) and touch and target:
            # Unified Bed Leveling Max 15, Mesh Bed leveling Max 7
            #print(f'\033[33m{line}\033[0m')
            conf[i] = f"  #define GRID_MAX_POINTS_X {gridpoints}   // JEREMY default - 5, max 7"
            print(conf[i])
        elif re.search(r'define \bNOZZLE_PARK_FEATURE\b', line) and runout>0:
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "#define NOZZLE_PARK_FEATURE // JEREMY make sure this exists"
            print(conf[i])
        #elif re.search(r'define \bNOZZLE_PARK', line):
            #print(f'\033[33m{line}\033[0m')
        elif re.search(r'define \bZ_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN\b', line) and touch:
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "//#define Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN"
            print(conf[i])
        elif re.search(r'define \bUSE_PROBE_FOR_Z_HOMING\b', line) and touch:
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "#define USE_PROBE_FOR_Z_HOMING"
            print(conf[i])
        elif re.search(r'define \bBLTOUCH\b', line) and touch:
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "#define BLTOUCH"
            print(conf[i])
        elif re.search(r'define \bNOZZLE_TO_PROBE_OFFSET\b', line) and not re.search(r'\bExample\b|set with', line) and hotend == 1 and touch:      # Set offset from nozzle to touch
            #print(f'\033[33m{line}\033[0m')
            conf[i] = f'#define NOZZLE_TO_PROBE_OFFSET {{ -36.5, -40, {zoff:.2f} }}  // JEREMY'
            print(conf[i])
        elif re.search(r'define \bAUTO_BED_LEVELING_BILINEAR\b', line) and touch:
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "#define AUTO_BED_LEVELING_BILINEAR"
            print(conf[i])
        elif re.search(r'define \bMESH_BED_LEVELING\b', line) and touch:
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "//#define MESH_BED_LEVELING"
            print(conf[i])
        elif re.search(r'define \bZ_SAFE_HOMING\b', line) and touch:
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "#define Z_SAFE_HOMING"
            print(conf[i])
        elif re.search(r'define \bEEPROM_INIT_NOW\b', line):
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "#define EEPROM_INIT_NOW"
            print(conf[i])
        elif re.search(r'define \bMIN_SOFTWARE_ENDSTOP_Z\b', line):
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "//#define MIN_SOFTWARE_ENDSTOP_Z"
            print(conf[i])
        elif re.search(r'define \bPROBING_MARGIN\b', line) and hotend == 1:
            #print(f'\033[33m{line}\033[0m')
            conf[i] = "#define PROBING_MARGIN 40  // JEREMY stops head from hitting edges when probing"
            print(conf[i])
        elif re.search(r'define \bDEFAULT_AXIS_STEPS_PER_UNIT\b', line) and hotend == 1:
            # print(f'\033[33m{line}\033[0m')
            conf[i] = "#define DEFAULT_AXIS_STEPS_PER_UNIT   { 80, 80, 400, 424.9 } // JEREMY Default: { 80, 80, 400, 93 }"
            print(conf[i])
        elif re.search(r'define \bSWITCHING_TOOLHEAD_RETRACT_MM\b', line) and hotend == 1:
            # print(f'\033[33m{line}\033[0m')
            conf[i] = "#define SWITCHING_TOOLHEAD_RETRACT_MM         0.8  // (mm)   Retract after priming length"
            print(conf[i])
        elif re.search(r'define \bFIL_RUNOUT_ENABLED_DEFAULT\b', line) and runout>0:
            # print(f'\033[33m{line}\033[0m')
            conf[i] = "#define FIL_RUNOUT_ENABLED_DEFAULT true  // Enable the sensor on startup. Override with M412 followed by M500.  JEREMY"
            print(conf[i])
        elif re.search(r'#(el)?if .*\bAUTO_BED_LEVELING_BILINEAR\b', line): target = True
        elif re.search(r'#(el)?if .*\bAUTO_BED_LEVELING_UBL\b', line): target = False
        elif re.search(r'#(el)?if .*\bMESH_BED_LEVELING\b', line): target = False


    print()
    print('\033[32mConfiguration_adv.h\033[0m')
    for i, line in enumerate(advconf):
        if re.search(r'define \bADVANCED_PAUSE_FEATURE\b',line) and runout>0:
            #print(f'\033[33m{line}\033[0m')
            advconf[i] = "#define ADVANCED_PAUSE_FEATURE   // JEREMY - make sure it is enabled"
            print(advconf[i])
        elif re.search(r'define \bPAUSE_PARK_RETRACT_FEEDRATE\b',line) and hotend == 1:
            #print(f'\033[33m{line}\033[0m')
            advconf[i] = "  #define PAUSE_PARK_RETRACT_FEEDRATE      424.9  // (mm/s) Initial retract feedrate.  JEREMY Default: 60"
            print(advconf[i])
        elif re.search(r'define \bFILAMENT_CHANGE_UNLOAD_LENGTH\b', line):
            #print(f'\033[33m{line}\033[0m')
            advconf[i] = "  #define FILAMENT_CHANGE_UNLOAD_LENGTH 100"
            print(advconf[i])
        elif re.search(r'define \bPAUSE_PARK_RETRACT_LENGTH\b',line) and hotend == 1:
            #print(f'\033[33m{line}\033[0m')
            advconf[i] = "  #define PAUSE_PARK_RETRACT_LENGTH          0.8  // (mm) Initial retract. JEREMY Default: 2"
            print(advconf[i])
        elif re.search(r'define \bPROBE_OFFSET_WIZARD\b', line) and touch:
            #print(f'\033[33m{line}\033[0m')
            advconf[i] = "#define PROBE_OFFSET_WIZARD"
            print(advconf[i])
        elif re.search(r'define \bSHOW_PROGRESS_PERCENT\b', line):
            #print(f'\033[33m{line}\033[0m')
            advconf[i] = "#define SHOW_PROGRESS_PERCENT"
            print(advconf[i])
        elif re.search(r'define \bSHOW_REMAINING_TIME\b', line):
            #print(f'\033[33m{line}\033[0m')
            advconf[i] = "#define SHOW_REMAINING_TIME"
            print(advconf[i])
        #elif re.search(r'define \bNO_SD_DETECT\b', line):
            #print(f'\033[33m{line}\033[0m')
            #advconf[i] = "#define NO_SD_DETECT   // JEREMY Allow you to init / refresh the SD card"
            #print(advconf[i])
        #elif re.search(r'define \bSD_DETECT_STATE\b', line):
            #print(f'\033[33m{line}\033[0m')
            #       advconf[i] = "#define SD_DETECT_STATE HIGH"
            #print(advconf[i])

    conf.insert(0, '#define DIAG_JUMPERS_REMOVED')

with open(f'{outputdir}/Configuration.h', 'w', encoding='utf8') as writer:
    for line in conf:
        writer.write(line + "\n")

with open(f'{outputdir}/Configuration_adv.h', 'w', encoding='utf8') as writer:
    for line in advconf:
        writer.write(line + "\n")

