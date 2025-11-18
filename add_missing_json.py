#!/usr/bin/env python3
"""Add JSON parsing to callbacks that are missing it."""

import re

# Read the file
with open('src/endstone_worldedit/builder_menu.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all on_submit functions and check if they have JSON parsing
# Pattern: find on_submit, check next 10 lines for "import json", if not found and "values[" is used, add it

lines = content.split('\n')
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    new_lines.append(line)
    
    # Check if this is an on_submit definition
    if 'def on_submit(player: "Player", data: Optional[str]):' in line:
        # Look ahead to see if there's JSON parsing and where values is first used
        has_json = False
        first_values_line = -1
        none_check_return_line = -1
        
        for j in range(1, min(30, len(lines) - i)):
            check_line = lines[i + j]
            if 'import json' in check_line:
                has_json = True
                break
            if 'values[' in check_line or 'len(values)' in check_line:
                first_values_line = i + j
                break
            if 'if data is None' in check_line:
                # Find the return after this
                for k in range(j + 1, min(j + 5, len(lines) - i)):
                    if 'return' in lines[i + k]:
                        none_check_return_line = i + k
                        break
        
        # If no JSON parsing but values is used, add it after the None check
        if not has_json and first_values_line > 0 and none_check_return_line > 0:
            # Add the next lines until we reach the return line
            for j in range(1, none_check_return_line - i + 1):
                new_lines.append(lines[i + j])
            
            # Add JSON parsing
            indent_match = re.match(r'(\s+)', lines[none_check_return_line])
            if indent_match:
                indent = indent_match.group(1)
                new_lines.append('')
                new_lines.append(indent + 'import json')
                new_lines.append(indent + 'values = json.loads(data)')
            
            # Skip to after the return line
            i = none_check_return_line + 1
            continue
    
    i += 1

# Write back
with open('src/endstone_worldedit/builder_menu.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("Added missing JSON parsing!")

