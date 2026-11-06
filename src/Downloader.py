import sys
import subprocess
from pathlib import Path
import requests
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.panel import Panel

console = Console()

ORDERLIST_URL = "https://raw.githubusercontent.com/Starfish-Foundation/mineploit_packages/refs/heads/main/orderlist.json"
BASE_RAW_URL = "https://raw.githubusercontent.com/Starfish-Foundation/mineploit_packages/refs/heads/main/"

# Mapowanie rozszerzeń na polecenia interpretera/kompilatora
RUNTIMERS = {
    ".py": {"cmd": [sys.executable], "name": "Python"},
    ".js": {"cmd": ["node"], "name": "Node.js", "dep_handler": "npm install"},
    ".ts": {"cmd": ["npx", "ts-node"], "name": "TypeScript"},
    ".sh": {"cmd": ["bash"], "name": "Bash"},
    ".rb": {"cmd": ["ruby"], "name": "Ruby"},
    ".go": {"cmd": ["go", "run"], "name": "Go"},
    ".lua": {"cmd": ["lua"], "name": "Lua"}, # or luajit
}

def handle_dependencies(file_path: Path, runtime_info: dict):
    """Automatyczna obsługa zależności zależna od języka"""
    parent_dir = file_path.parent
    
    # Python: requirements.txt
    req_file = parent_dir / "requirements.txt"
    if runtime_info["name"] == "Python" and req_file.exists():
        console.print(f"[cyan]Wykryto requirements.txt, instalowanie zależności...[/cyan]")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_file)], check=True)
        
    # Node.js: package.json / npm install
    elif runtime_info["name"] == "Node.js" and (parent_dir / "package.json").exists():
        console.print(f"[cyan]Wykryto package.json, uruchamianie npm install...[/cyan]")
        subprocess.run(["npm", "install"], cwd=parent_dir, check=True)

def load_and_run_package(package_name: str):
    console.print(f"[bold cyan]>[/bold cyan] Pobieranie listy pakietów z repozytorium...")
    
    try:
        response = requests.get(ORDERLIST_URL)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        console.print(f"[bold red]Błąd pobierania orderlist.json:[/bold red] {e}")
        return

    # Szukanie pakietu w orderlist
    script_path = None
    for item in data.get("orderlist", []):
        if package_name in item:
            script_path = item[package_name]
            break

    if not script_path:
        console.print(f"[bold yellow]Nie znaleziono pakietu dla parametru:[/bold yellow] {package_name}")
        return

    console.print(f"[green]✔ Znaleziono pakiet:[/green] {package_name} -> [italic]{script_path}[/italic]")

    script_url = BASE_RAW_URL + script_path
    
    local_dir = Path("packages")
    local_dir.mkdir(exist_ok=True)
    
    file_name = Path(script_path).name
    local_file_path = local_dir / file_name
    file_ext = local_file_path.suffix.lower()

    # Weryfikacja obsługi rozszerzenia
    if file_ext not in RUNTIMERS:
        console.print(f"[bold red]Nieobsługiwane rozszerzenie pliku:[/bold red] {file_ext}")
        return

    runtime = RUNTIMERS[file_ext]

    # Pobieranie pliku z paskiem postępu Rich
    console.print(f"[cyan]Pobieranie pliku z {script_url} ({runtime['name']})...[/cyan]")
    try:
        with requests.get(script_url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
                console=console
            ) as progress:
                task = progress.add_task(f"[green]Pobieranie {file_name}", total=total_size)
                with open(local_file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
                            
        console.print(f"[bold green]✔ Pomyślnie pobrano plik do:[/bold green] {local_file_path}")
        
    except Exception as e:
        console.print(f"[bold red]Błąd podczas pobierania pliku:[/bold red] {e}")
        return

    # Obsługa zależności
    try:
        handle_dependencies(local_file_path, runtime)
    except Exception as e:
        console.print(f"[bold yellow]Ostrzeżenie: Problem z instalacją zależności:[/bold yellow] {e}")

    # Uruchomienie skryptu we właściwym środowisku
    console.print(Panel(f"[bold yellow]Uruchamianie przez {runtime['name']}:[/bold yellow] {local_file_path}", border_style="yellow"))
    try:
        run_command = runtime["cmd"] + [str(local_file_path)]
        subprocess.run(run_command, check=True)
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Program zakończył działanie z błędem (kod powrotu: {e.returncode})[/bold red]")
    except FileNotFoundError:
        console.print(f"[bold red]Błąd: Nie znaleziono interpretera dla {runtime['name']} w systemie![/bold red]")
    except Exception as e:
        console.print(f"[bold red]Nie udało się uruchomić programu:[/bold red] {e}")

if __name__ == "__main__":
    load_and_run_package("@qol/end_portal_finder")