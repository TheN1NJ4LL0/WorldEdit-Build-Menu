#!/usr/bin/env python3
"""Fix ModalForm callback signatures to use str instead of list and add JSON parsing."""

import re

# Read the file
with open('src/endstone_worldedit/builder_menu.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0

while i < len(lines):
    line = lines[i]

    # Check if this is a ModalForm on_submit definition
    if 'def on_submit(player: "Player", data: Optional[list]):' in line:
        # Replace list with str
        line = line.replace('Optional[list]', 'Optional[str]')
        new_lines.append(line)
        i += 1

        # Next line should be the None check
        if i < len(lines) and 'if data is None' in lines[i]:
            new_lines.append(lines[i])  # Add the None check line
            i += 1

            # Next should be the return or callback
            if i < len(lines):
                new_lines.append(lines[i])  # Add the return/callback line
                i += 1

                # Check if next line is 'return' - if so, add JSON parsing after it
                if i < len(lines) and 'return' in lines[i-1]:
                    # Get indentation from the 'if' line
                    indent_match = re.match(r'(\s+)', lines[i-2])
                    if indent_match:
                        indent = indent_match.group(1)
                        # Add JSON parsing
                        new_lines.append('\n')
                        new_lines.append(indent + 'import json\n')
                        new_lines.append(indent + 'values = json.loads(data)\n')
                    continue
    else:
        new_lines.append(line)
        i += 1

# Now replace all data[index] with values[index]
content = ''.join(new_lines)
content = re.sub(r'\bdata\[(\d+)\]', r'values[\1]', content)

# Write back
with open('src/endstone_worldedit/builder_menu.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed ModalForm callback signatures and added JSON parsing!")

