#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path

def process_renpy_file(input_file, output_file):
    """Process a single Ren'Py file into a Python file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract all Python blocks
    python_blocks = []
    current_block = []
    in_python = False
    
    for line in content.split('\n'):
        # Check for Python block start
        if re.match(r'\s*init\s+[-]?\d*\s+python:', line):
            in_python = True
            continue
            
        # Check for other init blocks
        if re.match(r'\s*init\s+[-]?\d*:', line):
            if in_python:
                if current_block:
                    python_blocks.append('\n'.join(current_block))
                    current_block = []
            in_python = False
            continue
            
        if in_python and line.strip():
            # Remove common indentation
            if re.match(r'\s+', line):
                line = re.sub(r'^\s+', '', line)
            current_block.append(line)
    
    # Add last block if exists
    if current_block:
        python_blocks.append('\n'.join(current_block))
    
    # Write processed content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('"""\nAutomatically generated Python file from {}.\n"""\n\n'.format(input_file))
        for block in python_blocks:
            f.write(block)
            f.write('\n\n')

def main():
    # Create output directory
    output_dir = Path('docs/processed_python')
    output_dir.mkdir(exist_ok=True)
    
    # Process all .rpy files in game/scripts and its subdirectories
    scripts_dir = Path('game/scripts')
    for rpy_file in scripts_dir.rglob('*.rpy'):
        # Create corresponding output path
        rel_path = rpy_file.relative_to(scripts_dir)
        output_path = output_dir / rel_path.with_suffix('.py')
        
        # Create necessary subdirectories
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Processing {rpy_file} -> {output_path}")
        process_renpy_file(rpy_file, output_path)

if __name__ == '__main__':
    main() 