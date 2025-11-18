#!/usr/bin/env python3
"""Fix all ModalForm callbacks - add JSON parsing where missing, remove duplicates."""

import re

# Read the file
with open('src/endstone_worldedit/builder_menu.py', 'r', encoding='utf-8') as f:
    content = f.read()

# First, remove duplicate import json / values = json.loads(data) pairs
content = re.sub(
    r'(\s+import json\s+values = json.loads\(data\)\s+)(\s+import json\s+values = json.loads\(data\)\s+)',
    r'\1',
    content
)

# Now find all on_submit functions and ensure they have JSON parsing
lines = content.split('\n')
new_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Check if this is a ModalForm on_submit definition
    if 'def on_submit(player: "Player", data: Optional[str]):' in line:
        new_lines.append(line)
        i += 1
        
        # Collect lines until we find one that uses 'values'
        temp_lines = []
        has_json_parsing = False
        found_values_usage = False
        
        while i < len(lines) and not found_values_usage:
            current = lines[i]
            temp_lines.append(current)
            
            if 'import json' in current:
                has_json_parsing = True
            
            if 'values[' in current or 'len(values)' in current:
                found_values_usage = True
                
                # If we found values usage but no JSON parsing, insert it before this line
                if not has_json_parsing:
                    # Get indentation
                    indent_match = re.match(r'(\s+)', current)
                    if indent_match:
                        indent = indent_match.group(1)
                        # Insert JSON parsing before the last line
                        temp_lines.insert(-1, '\n')
                        temp_lines.insert(-1, indent + 'import json\n')
                        temp_lines.insert(-1, indent + 'values = json.loads(data)\n')
            
            i += 1
            
            # Stop if we hit another function definition
            if 'def ' in current and 'def on_submit' not in current:
                break
        
        new_lines.extend(temp_lines)
    else:
        new_lines.append(line)
        i += 1

# Write back
with open('src/endstone_worldedit/builder_menu.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_lines))

print("Fixed all ModalForm callbacks!")

