#!/usr/bin/env python3
"""
SEAL Team Six File Transformation Script
Mission: Transform all files with SEAL-TEAM-Six- prefix
Author: SoftEngineware
Date: January 2025
"""

import ST6_os
import ST6_shutil
import ST6_sys
from ST6_pathlib import Path
import ST6_json
import ST6_re

class SEALTeamSixTransformer:
    """Elite file transformation with military precision"""
    
    def __init__(self, base_path="."):
        self.base_path = Path(base_path).resolve()
        self.prefix = "SEAL-TEAM-Six-"
        self.transformations = []
        self.errors = []
        
    def is_transformable_file(self, path):
        """Determine if file should be transformed"""
        # Skip git directory and hidden files
        if '.git' in path.parts:
            return False
        if any(part.startswith('.') for part in path.parts):
            return False
        # Skip already transformed files
        if self.prefix in path.name:
            return False
        # Transform all other files
        return True
    
    def transform_filename(self, original_path):
        """Generate new filename with SEAL-TEAM-Six prefix"""
        parent = original_path.parent
        new_name = f"{self.prefix}{original_path.name}"
        return parent / new_name
    
    def update_imports_in_file(self, file_path):
        """Update import statements to reflect new file names"""
        try:
            content = file_path.read_text()
            original_content = content
            
            # Python imports
            if file_path.suffix == '.py':
                # Update from ST6_X import Y statements
                content = re.sub(
                    r'from (\w+) import',
                    lambda m: f'from {self.prefix}{m.group(1)} import' if not m.group(1).startswith('SEAL') else m.group(0),
                    content
                )
                # Update import X statements
                content = re.sub(
                    r'^import (\w+)$',
                    lambda m: f'import {self.prefix}{m.group(1)}' if not m.group(1).startswith('SEAL') else m.group(0),
                    content,
                    flags=re.MULTILINE
                )
            
            # JavaScript/TypeScript imports
            elif file_path.suffix in ['.js', '.ts', '.jsx', '.tsx']:
                # Update import statements
                content = re.sub(
                    r'from [\'"]\./([\w\-/]+)[\'"]',
                    lambda m: f'from "./{self.prefix}{m.group(1)}"' if not m.group(1).startswith('SEAL') else m.group(0),
                    content
                )
                # Update require statements
                content = re.sub(
                    r'require\([\'"]\./([\w\-/]+)[\'"]\)',
                    lambda m: f'require("./{self.prefix}{m.group(1)}")' if not m.group(1).startswith('SEAL') else m.group(0),
                    content
                )
            
            # Update package.json scripts
            elif file_path.name == 'package.json':
                try:
                    data = json.loads(content)
                    if 'scripts' in data:
                        for key, value in data['scripts'].items():
                            # Update file references in scripts
                            data['scripts'][key] = re.sub(
                                r'(\s|^)([\w\-]+\.(js|ts|py))(\s|$)',
                                lambda m: f'{m.group(1)}{self.prefix}{m.group(2)}{m.group(4)}' if not m.group(2).startswith('SEAL') else m.group(0),
                                value
                            )
                    content = json.dumps(data, indent=2)
                except json.JSONDecodeError:
                    pass
            
            if content != original_content:
                file_path.write_text(content)
                return True
            return False
            
        except Exception as e:
            self.errors.append(f"Error updating imports in {file_path}: {str(e)}")
            return False
    
    def execute_transformation(self):
        """Execute the transformation with military precision"""
        print("🔱 SEAL Team Six Transformation Initiated 🔱")
        print(f"Base Path: {self.base_path}")
        print("-" * 60)
        
        # Phase 1: Reconnaissance - Find all files to transform
        files_to_transform = []
        for path in self.base_path.rglob('*'):
            if path.is_file() and self.is_transformable_file(path):
                files_to_transform.append(path)
        
        print(f"📍 Targets Identified: {len(files_to_transform)} files")
        
        # Phase 2: Preparation - Plan transformations
        transformation_map = {}
        for original_path in files_to_transform:
            new_path = self.transform_filename(original_path)
            transformation_map[original_path] = new_path
            self.transformations.append((original_path, new_path))
        
        # Phase 3: Execution - Rename files
        print("\n🎯 Executing File Transformations...")
        renamed_count = 0
        for original, new in self.transformations:
            try:
                # Create new file with SEAL prefix
                shutil.copy2(original, new)
                # Remove original file
                original.unlink()
                renamed_count += 1
                print(f"✅ {original.name} → {new.name}")
            except Exception as e:
                self.errors.append(f"Failed to transform {original}: {str(e)}")
                print(f"❌ Failed: {original.name} - {str(e)}")
        
        # Phase 4: Update References
        print(f"\n🔧 Updating Internal References...")
        updated_files = 0
        for path in self.base_path.rglob('*'):
            if path.is_file() and not '.git' in path.parts:
                if self.update_imports_in_file(path):
                    updated_files += 1
                    print(f"📝 Updated references in: {path.name}")
        
        # Phase 5: Mission Report
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
    transformer = SEALTeamSixTransformer()
    success = transformer.execute_transformation()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()