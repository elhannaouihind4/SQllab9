import subprocess
import datetime

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"dump_universite_{ts}.sql"
subprocess.run([
    "mysqldump", "-u", "root", "-pVotreMdp", 
    "--routines", "--triggers", "universite",
    "-r", filename
])
print("Backup saved to", filename)