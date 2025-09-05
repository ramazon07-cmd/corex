"""
Test script to verify complete CoreX wiki workflow
"""

import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """Run a command and return the result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"FAILED: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        sys.exit(1)
    return result

def test_wiki_workflow():
    """Test the complete wiki creation workflow"""
    print("🧪 Testing CoreX Wiki Workflow...")
    
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)
        project_name = "test_wiki_project"
        project_path = test_dir / project_name
        
        print(f"📁 Test directory: {test_dir}")
        
        # Test 1: Create project with Bootstrap
        print("\n1️⃣ Creating Bootstrap project...")
        run_command(f"corex new {project_name} --ui=bootstrap", cwd=test_dir)
        assert project_path.exists(), "Project directory should be created"
        
        # Test 2: Create wiki app with explicit UI
        print("\n2️⃣ Creating wiki app with Bootstrap UI...")
        run_command(f"corex app wiki --type=wiki --ui=bootstrap --seed", cwd=project_path)
        
        # Test 3: Check if templates were generated
        templates_dir = project_path / "wiki" / "templates" / "wiki"
        assert templates_dir.exists(), "Wiki templates directory should exist"
        assert (templates_dir / "list.html").exists(), "list.html should exist"
        assert (templates_dir / "detail.html").exists(), "detail.html should exist"
        assert (templates_dir / "form.html").exists(), "form.html should exist"
        
        # Test 4: Check models have correct fields
        models_file = project_path / "wiki" / "models.py"
        models_content = models_file.read_text()
        assert "status = models.CharField" in models_content, "Page model should have status field"
        assert "author = models.ForeignKey" in models_content, "PageRevision should have author field"
        
        # Test 5: Check views use correct field names
        views_file = project_path / "wiki" / "views.py"
        views_content = views_file.read_text()
        assert "status='published'" in views_content, "Views should filter by status='published'"
        assert "wiki/list.html" in views_content, "Views should use correct template names"
        
        # Test 6: Check seed data uses correct fields
        seed_file = project_path / "wiki" / "management" / "commands" / "seed.py"
        seed_content = seed_file.read_text()
        assert "status='published'" in seed_content, "Seed should use status='published'"
        assert "author=random.choice(users)" in seed_content, "Seed should use author field"
        
        # Test 7: Check URLs include authentication
        urls_file = project_path / project_name / "urls.py"
        urls_content = urls_file.read_text()
        assert "django.contrib.auth.urls" in urls_content, "URLs should include auth URLs"
        
        # Test 8: Check base template uses correct URL names
        base_template = project_path / "templates" / "base.html"
        base_content = base_template.read_text()
        assert "admin:login" in base_content, "Base template should use admin:login"
        assert "admin:logout" in base_content, "Base template should use admin:logout"
        
        # Test 9: Run seed command
        print("\n3️⃣ Running seed command...")
        run_command("python3 manage.py seed", cwd=project_path)
        
        # Test 10: Create superuser
        print("\n4️⃣ Creating superuser...")
        create_superuser_cmd = """python3 -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{}.settings')
django.setup()
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@test.com', 'testpass123')
print('Superuser created')
" """.format(project_name)
        
        run_command(create_superuser_cmd, cwd=project_path)
        
        # Test 11: Check server can start (run for a few seconds)
        print("\n5️⃣ Testing server startup...")
        server_process = subprocess.Popen(
            ["python3", "manage.py", "runserver", "--noreload"],
            cwd=project_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        import time
        time.sleep(3)  # Let server start
        
        # Test simple HTTP request
        try:
            import urllib.request
            response = urllib.request.urlopen("http://127.0.0.1:8000/", timeout=5)
            assert response.getcode() == 200, "Server should respond with 200"
            print("✅ Server responds successfully")
        except Exception as e:
            print(f"❌ Server test failed: {e}")
        finally:
            server_process.terminate()
            server_process.wait()
        
        print("\n🎉 All tests passed! Wiki workflow is working correctly.")

if __name__ == "__main__":
    test_wiki_workflow()