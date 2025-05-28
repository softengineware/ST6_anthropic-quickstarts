#!/usr/bin/env python3
"""
ST6 (SEAL Team Six) File Transformation Script
Mission: Transform all files with ST6_ prefix
Author: SoftEngineware
Date: January 2025
"""

import ST6_os
import ST6_shutil
import ST6_sys
from ST6_pathlib import Path
import ST6_json
import ST6_re

class ST6Transformer:
    """Elite file transformation with military precision"""
    
    def __init__(self, base_path="."):
        self.base_path = Path(base_path).resolve()
        self.prefix = "ST6_"
        self.transformations = []
        self.errors = []
        
    def is_transformable_file(self, path):
        """Determine if file should be transformed"""
        # Skip git directory and hidden files (except specific ones we want to transform)
        if '.git' in str(path) and path.name != '.gitignore':
            return False
        # Skip already transformed files
        if path.name.startswith(self.prefix):
            return False
        if path.name.startswith('SEAL-TEAM-Six-'):
            return False
        # Skip node_modules and other build directories
        if any(part in ['node_modules', '__pycache__', '.next', 'dist', 'build'] for part in path.parts):
            return False
        # Transform all other files
        return True
    
    def transform_filename(self, original_path):
        """Generate new filename with ST6_ prefix"""
        parent = original_path.parent
        new_name = f"{self.prefix}{original_path.name}"
        return parent / new_name
    
    def update_imports_in_file(self, file_path):
        """Update import statements to reflect new file names"""
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content
            
            # Python imports
            if file_path.suffix == '.py':
                # Update from ST6_X import Y statements
                content = re.sub(
                    r'from ([a-zA-Z_]\w*) import',
                    lambda m: f'from {self.prefix}{m.group(1)} import' if not m.group(1).startswith(('ST6_', 'SEAL')) else m.group(0),
                    content
                )
                # Update import X statements
                content = re.sub(
                    r'^import ([a-zA-Z_]\w*)$',
                    lambda m: f'import {self.prefix}{m.group(1)}' if not m.group(1).startswith(('ST6_', 'SEAL')) else m.group(0),
                    content,
                    flags=re.MULTILINE
                )
            
            # JavaScript/TypeScript imports
            elif file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
                # Update import statements with file extensions
                content = re.sub(
                    r'from [\'"]\./([\w\-/]+)(\.\w+)?[\'"]',
                    lambda m: f'from "./{self.prefix}{m.group(1)}{m.group(2) or ""}"' if not m.group(1).startswith(('ST6_', 'SEAL')) else m.group(0),
                    content
                )
                # Update require statements
                content = re.sub(
                    r'require\([\'"]\./([\w\-/]+)(\.\w+)?[\'"]\)',
                    lambda m: f'require("./{self.prefix}{m.group(1)}{m.group(2) or ""}")' if not m.group(1).startswith(('ST6_', 'SEAL')) else m.group(0),
                    content
                )
            
            # Update package.json scripts and files
            elif file_path.name.endswith('package.json'):
                try:
                    data = json.loads(content)
                    
                    # Update main, types, and other file references
                    for key in ['main', 'types', 'typings', 'module', 'browser']:
                        if key in data and isinstance(data[key], str):
                            if not data[key].startswith(('ST6_', './ST6_')):
                                if data[key].startswith('./'):
                                    data[key] = f'./{self.prefix}{data[key][2:]}'
                                else:
                                    data[key] = f'{self.prefix}{data[key]}'
                    
                    # Update scripts
                    if 'scripts' in data:
                        for key, value in data['scripts'].items():
                            # Update file references in scripts
                            data['scripts'][key] = re.sub(
                                r'(\s|^)([\w\-]+\.(js|ts|py))(\s|$)',
                                lambda m: f'{m.group(1)}{self.prefix}{m.group(2)}{m.group(4)}' if not m.group(2).startswith(('ST6_', 'SEAL')) else m.group(0),
                                value
                            )
                    
                    content = json.dumps(data, indent=2)
                except json.JSONDecodeError:
                    pass
            
            # Update Markdown files
            elif file_path.suffix == '.md':
                # Update relative links to files
                content = re.sub(
                    r'\[([^\]]+)\]\(\./([\w\-/]+)(\.\w+)?\)',
                    lambda m: f'[{m.group(1)}](./{self.prefix}{m.group(2)}{m.group(3) or ""})' if not m.group(2).startswith(('ST6_', 'SEAL')) else m.group(0),
                    content
                )
            
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                return True
            return False
            
        except Exception as e:
            self.errors.append(f"Error updating imports in {file_path}: {str(e)}")
            return False
    
    def execute_transformation(self):
        """Execute the transformation with military precision"""
        print("🔱 ST6 (SEAL Team Six) Transformation Initiated 🔱")
        print(f"Base Path: {self.base_path}")
        print("-" * 60)
        
        # Phase 1: Reconnaissance - Find all files to transform
        files_to_transform = []
        for path in self.base_path.rglob('*'):
            if path.is_file() and self.is_transformable_file(path):
                files_to_transform.append(path)
        
        print(f"📍 Targets Identified: {len(files_to_transform)} files")
        
        # Phase 2: Execution - Rename files
        print("\n🎯 Executing File Transformations...")
        renamed_count = 0
        for original_path in sorted(files_to_transform):
            try:
                new_path = self.transform_filename(original_path)
                # Rename the file
                original_path.rename(new_path)
                renamed_count += 1
                rel_original = original_path.relative_to(self.base_path)
                rel_new = new_path.relative_to(self.base_path)
                print(f"✅ {rel_original} → {rel_new}")
                self.transformations.append((original_path, new_path))
            except Exception as e:
                self.errors.append(f"Failed to transform {original_path}: {str(e)}")
                print(f"❌ Failed: {original_path.name} - {str(e)}")
        
        # Phase 3: Update References
        print(f"\n🔧 Updating Internal References...")
        updated_files = 0
        for path in self.base_path.rglob('*'):
            if path.is_file() and '.git' not in str(path):
                if self.update_imports_in_file(path):
                    updated_files += 1
                    print(f"📝 Updated references in: {path.relative_to(self.base_path)}")
        
        # Phase 4: Mission Report
        print("\n" + "=" * 60)
        print("🎖️  MISSION COMPLETE 🎖️")
        print(f"Files Renamed: {renamed_count}")
        print(f"Files Updated: {updated_files}")
        print(f"Errors: {len(self.errors)}")
        
        if self.errors:
            print("\n⚠️  Error Report:")
            for error in self.errors:
                print(f"  - {error}")
        
        print("\n🔱 Transformation Status: SUCCESS 🔱")
        return renamed_count > 0

def main():
    """Main entry point"""
    transformer = ST6Transformer()
    success = transformer.execute_transformation()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()