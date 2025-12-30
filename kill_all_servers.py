"""
Script pour arrêter tous les serveurs Django qui tournent
"""
import subprocess
import re

# Récupérer tous les processus qui écoutent sur le port 8000
result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
lines = result.stdout.split('\n')

pids = set()
for line in lines:
    if ':8000' in line and 'LISTENING' in line:
        # Extraire le PID (dernier élément de la ligne)
        parts = line.split()
        if parts:
            pid = parts[-1]
            if pid.isdigit():
                pids.add(pid)

print(f"Processus trouvés écoutant sur le port 8000: {len(pids)}")
for pid in pids:
    print(f"  - PID: {pid}")
    try:
        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
        print(f"    ✓ Arrêté")
    except Exception as e:
        print(f"    ✗ Erreur: {e}")

print("\nTous les serveurs ont été arrêtés!")
print("Vous pouvez maintenant redémarrer avec: python manage.py runserver")
