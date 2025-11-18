#!/usr/bin/env python3
"""Comprehensive fix for all ModalForm callbacks - add JSON parsing in correct location."""

import re

# Read the file
with open('src/endstone_worldedit/builder_menu.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this is a ModalForm on_submit definition
    if 'def on_submit(player: "Player", data: Optional[str]):' in line:
        new_lines.append(line)
        i += 1
        
        # Collect lines until we find where to insert JSON parsing
        # We want to insert it right after the "if data is None" check and return
        found_none_check = False
        found_return_after_none = False
        has_json_parsing = False
        insert_index = None
        temp_lines = []
        
        # Look ahead up to 20 lines
        for j in range(20):
            if i + j >= len(lines):
                break
            
            current_line = lines[i + j]
            
            # Check if this line has JSON parsing
            if 'import json' in current_line or 'json.loads(data)' in current_line:
                has_json_parsing = True
            
            # Check for None check
            if 'if data is None' in current_line:
                found_none_check = True
            
            # Check for return after None check
            if found_none_check and 'return' in current_line:
                found_return_after_none = True
                insert_index = i + j + 1
                break
        
        # Now process the lines
        for j in range(20):
            if i >= len(lines):
                break
            
            current_line = lines[i]
            
            # If we're at the insert point and don't have JSON parsing, add it
            if insert_index is not None and i == insert_index and not has_json_parsing:
                # Get indentation from previous line
                indent_match = re.match(r'(\s+)', lines[i-1])
                if indent_match:
                    indent = indent_match.group(1)
                    new_lines.append('\n')
                    new_lines.append(indent + 'import json\n')
                    new_lines.append(indent + 'values = json.loads(data)\n')
            
            new_lines.append(current_line)
            i += 1
            
            # Stop if we hit another function definition
            if 'def ' in current_line and 'def on_submit' not in current_line:
                break
            
            # Stop if we've gone past the callback
            if i > insert_index + 30 if insert_index else i > len(lines):
                break
    else:
        new_lines.append(line)
        i += 1

# Write back
with open('src/endstone_worldedit/builder_menu.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Applied comprehensive fixes!")

