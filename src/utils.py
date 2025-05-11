import platform
import os
import sys
from pathlib import Path

def notify_done():
    system = platform.system()
    
    try:
        if system == "Windows":
            import winsound
            winsound.Beep(1000, 500)
            print("🔔 Traitement terminé (Windows beep)")

        elif system == "Darwin":  # macOS
            os.system('say "Traitement terminé"')
            print("🔔 Traitement terminé (macOS vocal)")

        elif "microsoft" in platform.uname().release.lower():  # WSL
            print('\a')  # Bip terminal WSL (si activé)
            print("🔔 Traitement terminé (WSL bip)")

        elif system == "Linux":
            if Path("/usr/bin/paplay").exists():
                os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga')
            elif Path("/usr/bin/aplay").exists():
                os.system('aplay /usr/share/sounds/alsa/Front_Center.wav')
            else:
                print('\a')  # Fallback bip terminal
            print("🔔 Traitement terminé (Linux son système)")

        else:
            print('\a')
            print("🔔 Traitement terminé (bip générique)")
    except Exception as e:
        print("⚠️ Impossible de jouer le son :", e)
        print('\a')

