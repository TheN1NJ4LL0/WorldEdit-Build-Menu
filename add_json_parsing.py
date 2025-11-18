#!/usr/bin/env python3
"""Add JSON parsing to all ModalForm callbacks that don't have it yet."""

import re

# Read the file
with open('src/endstone_worldedit/builder_menu.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    
    # Check if this is a ModalForm on_submit definition
    if 'def on_submit(player: "Player", data: Optional[str]):' in line:
        i += 1
        if i < len(lines):
            # Next line should be the None check
            next_line = lines[i]
            new_lines.append(next_line)
            i += 1
            
            if i < len(lines):
                # Next should be the return or callback
                return_line = lines[i]
                new_lines.append(return_line)
                i += 1
                
                # Check if 'return' is in the previous line
                if 'return' in return_line:
                    # Check if next line already has 'import json'
                    if i < len(lines) and 'import json' not in lines[i]:
                        # Get indentation from the 'if' line
                        indent_match = re.match(r'(\s+)', next_line)
                        if indent_match:
                            indent = indent_match.group(1)
                            # Add JSON parsing
                            new_lines.append('\n')
                            new_lines.append(indent + 'import json\n')
                            new_lines.append(indent + 'values = json.loads(data)\n')
                    continue
    else:
        i += 1

# Write back
with open('src/endstone_worldedit/builder_menu.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Added JSON parsing to all ModalForm callbacks!")

