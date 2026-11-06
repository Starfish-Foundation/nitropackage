from rich.prompt import Prompt

import os
def handle_cli(prompt_str="-> ", default_cmd="mineploit-install"):
    raw_input = Prompt.ask(prompt_str, default=default_cmd).strip()
    parts = raw_input.split()
    
    if not parts:
        return "", []
        
    return parts[0], parts[1:]