#!/usr/bin/env python3
"""Fix form API calls to use add_control instead of add_input/add_toggle/add_dropdown."""

import re

# Read the file
with open('src/endstone_worldedit/builder_menu.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []

for line in lines:
    original_line = line

    # Replace add_input with add_control(TextInput(...))
    if 'form.add_input(' in line:
        # Find the closing paren for add_input
        line = line.replace('form.add_input(', 'form.add_control(TextInput(')
        # Add extra closing paren before the newline
        line = line.rstrip('\n')
        if line.endswith(')'):
            line = line + ')\n'
        else:
            line = line + '\n'

    # Replace add_toggle with add_control(Toggle(...))
    elif 'form.add_toggle(' in line:
        line = line.replace('form.add_toggle(', 'form.add_control(Toggle(')
        line = line.rstrip('\n')
        if line.endswith(')'):
            line = line + ')\n'
        else:
            line = line + '\n'

    # Replace add_dropdown with add_control(Dropdown(...))
    elif 'form.add_dropdown(' in line:
        line = line.replace('form.add_dropdown(', 'form.add_control(Dropdown(')
        line = line.rstrip('\n')
        if line.endswith(')'):
            line = line + ')\n'
        else:
            line = line + '\n'

    new_lines.append(line)

# Write back
with open('src/endstone_worldedit/builder_menu.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed form API calls!")

