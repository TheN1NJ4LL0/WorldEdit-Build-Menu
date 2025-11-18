#!/usr/bin/env python3
"""Final comprehensive fix for all ModalForm callbacks."""

import re

# Read the file
with open('src/endstone_worldedit/builder_menu.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to match ModalForm on_submit functions
# We need to:
# 1. Ensure JSON parsing is AFTER the None check
# 2. Remove extra blank lines
# 3. Ensure values is used instead of data for array access

# Replace pattern: on_submit with misplaced JSON parsing
pattern = r'(def on_submit\(player: "Player", data: Optional\[str\]\):)\s*\n\s*\n\s*import json\s*\n\s*values = json\.loads\(data\)\s*\n\s*(if data is None)'

replacement = r'\1\n            \2'

content = re.sub(pattern, replacement, content)

# Now add JSON parsing after None checks that don't have it
# Pattern: None check followed by return, then code that uses values without JSON parsing
pattern2 = r'(if data is None[^\n]*\n[^\n]*return\n)\s*(if [^\n]*values\[)'

replacement2 = r'\1\n            import json\n            values = json.loads(data)\n            \2'

content = re.sub(pattern2, replacement2, content)

# Also handle cases where values is used directly after None check
pattern3 = r'(if data is None[^\n]*\n[^\n]*return\n)\s*([a-z_]+ = values\[)'

replacement3 = r'\1\n            import json\n            values = json.loads(data)\n            \2'

content = re.sub(pattern3, replacement3, content)

# Write back
with open('src/endstone_worldedit/builder_menu.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied final fixes to all ModalForm callbacks!")

