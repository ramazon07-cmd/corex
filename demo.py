#!/usr/bin/env python3
"""
CoreX Demo Script

This script demonstrates the key features of CoreX by creating a sample project.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add the corex package to the path
sys.path.insert(0, str(Path(__file__).parent))

from corex.generators import generate_project, generate_app
from corex.utils import print_success, print_error, print_info, print_warning


def demo_corex():
    """Demonstrate CoreX functionality"""
    print_info("🚀 CoreX Demo - Django Scaffolding Framework")
    print_info("=" * 50)
    
    # Create a temporary directory for the demo
    with tempfile.TemporaryDirectory() as temp_dir:
        demo_path = Path(temp_dir) / "corex_demo"
        demo_path.mkdir()
        
        print_info("📁 Created demo directory")
        
        # Demo 1: Create a Django project
        print_info("\n1️⃣ Creating Django project with JWT auth and Tailwind UI...")
        project_name = "demo_project"
        project_path = demo_path / project_name
        
        success = generate_project(
            project_path=project_path,
            project_name=project_name,
            auth="jwt",
            ui="tailwind",
            database="sqlite",
            docker=True,
            api=True
        )
        
        if success:
            print_success(f"✅ Project '{project_name}' created successfully!")
            
            # Show project structure
            print_info("\n📂 Project structure:")
            for item in project_path.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(project_path)
                    print_info(f"   📄 {rel_path}")
                elif item.is_dir() and not any(part.startswith('.') for part in item.parts):
                    rel_path = item.relative_to(project_path)
                    print_info(f"   📁 {rel_path}/")
        else:
            print_error("❌ Failed to create project")
            return False
        
        # Demo 2: Create a blog app
        print_info("\n2️⃣ Creating blog app...")
        app_name = "blog"
        app_path = project_path / app_name
        
        success = generate_app(
            project_root=project_path,
            app_name=app_name,
            app_type="blog",
            auth="jwt",
            ui="tailwind",
            seed=True,
            api=True
        )
        
        if success:
            print_success(f"✅ Blog app created successfully!")
        else:
            print_warning("⚠️  Blog app creation had issues")
        
        # Demo 3: Show generated files
        print_info("\n3️⃣ Generated files overview:")
        
        # Check key files
        key_files = [
            "manage.py",
            f"{project_name}/settings.py",
            f"{project_name}/urls.py",
            "pyproject.toml",
            "Dockerfile",
            "docker-compose.yml",
            f"{app_name}/models.py",
            f"{app_name}/views.py",
            f"{app_name}/urls.py",
            f"{app_name}/admin.py",
        ]
        
        for file_path in key_files:
            full_path = project_path / file_path
            if full_path.exists():
                print_success(f"   ✅ {file_path}")
            else:
                print_warning(f"   ⚠️  {file_path} (not found)")
        
        # Demo 4: Show configuration
        print_info("\n4️⃣ Project configuration:")
        
        # Read settings to show what was configured
        settings_file = project_path / f"{project_name}/settings.py"
        if settings_file.exists():
            content = settings_file.read_text()
            
            configs = {
                "JWT Authentication": "rest_framework_simplejwt" in content,
                "Tailwind UI": "tailwind" in content.lower(),
                "DRF API": "rest_framework" in content,
                "PostgreSQL": "postgresql" in content,
                "CORS Headers": "corsheaders" in content,
            }
            
            for config, enabled in configs.items():
                status = "✅ Enabled" if enabled else "❌ Disabled"
                print_info(f"   {config}: {status}")
        
        # Demo 5: Show next steps
        print_info("\n5️⃣ Next steps:")
        print_info("   📝 cd demo_project")
        print_info("   📝 poetry install")
        print_info("   📝 python3 manage.py migrate")
        print_info("   📝 python3 manage.py createsuperuser")
        print_info("   📝 python3 manage.py runserver")
        print_info("   📝 Visit http://localhost:8000")
        
        print_success("\n🎉 CoreX demo completed successfully!")
        print_info(f"📁 Demo project created at: {project_path}")
        
        return True


if __name__ == "__main__":
    try:
        success = demo_corex()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_info("\n👋 Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"💥 Demo failed with error: {e}")
        sys.exit(1)
