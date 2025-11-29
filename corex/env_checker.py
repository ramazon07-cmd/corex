"""
Cross-Platform Environment Checker for CoreX
"""

import os
import sys
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


class EnvironmentChecker:
    """Checks and fixes environment issues for CoreX"""
    
    def __init__(self):
        self.os_name = platform.system().lower()
        self.arch = platform.machine()
        
    def check_python_version(self) -> Tuple[bool, str]:
        """Check if Python version is compatible"""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            return True, f"Python {version.major}.{version.minor}.{version.micro}"
        else:
            return False, f"Python {version.major}.{version.minor}.{version.micro} (minimum required: 3.8)"
    
    def check_required_tools(self) -> Dict[str, Tuple[bool, str]]:
        """Check if required tools are installed"""
        tools = {
            "python": "python3 --version",
            "pip": "pip --version",
            "git": "git --version",
            "node": "node --version",
            "npm": "npm --version",
        }
        
        results = {}
        for tool, command in tools.items():
            try:
                result = subprocess.run(
                    command.split(), 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                if result.returncode == 0:
                    results[tool] = (True, result.stdout.strip())
                else:
                    results[tool] = (False, "Not found")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                results[tool] = (False, "Not found")
                
        return results
    
    def check_docker(self) -> Tuple[bool, str]:
        """Check if Docker is installed and running"""
        try:
            # Check if Docker is installed
            result = subprocess.run(
                ["docker", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode != 0:
                return False, "Docker not installed"
                
            version = result.stdout.strip()
            
            # Check if Docker daemon is running
            result = subprocess.run(
                ["docker", "info"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                return True, f"{version} (daemon running)"
            else:
                return True, f"{version} (daemon not running)"
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False, "Docker not installed"
    
    def check_package_managers(self) -> Dict[str, Tuple[bool, str]]:
        """Check package managers based on OS"""
        managers = {}
        
        if self.os_name == "darwin":  # macOS
            try:
                result = subprocess.run(
                    ["brew", "--version"], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                if result.returncode == 0:
                    managers["brew"] = (True, result.stdout.strip())
                else:
                    managers["brew"] = (False, "Homebrew not found")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                managers["brew"] = (False, "Homebrew not found")
                
        elif self.os_name == "windows":
            try:
                result = subprocess.run(
                    ["choco", "--version"], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                if result.returncode == 0:
                    managers["choco"] = (True, f"Chocolatey {result.stdout.strip()}")
                else:
                    managers["choco"] = (False, "Chocolatey not found")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                managers["choco"] = (False, "Chocolatey not found")
                
        elif self.os_name == "linux":
            # Check common Linux package managers
            linux_managers = {
                "apt": "apt --version",
                "yum": "yum --version",
                "dnf": "dnf --version",
                "pacman": "pacman --version"
            }
            
            for manager, command in linux_managers.items():
                try:
                    result = subprocess.run(
                        command.split(), 
                        capture_output=True, 
                        text=True, 
                        timeout=10
                    )
                    if result.returncode == 0:
                        managers[manager] = (True, result.stdout.split('\n')[0])
                        break
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    continue
                    
            if not managers:
                managers["package_manager"] = (False, "No package manager found")
                
        return managers
    
    def generate_report(self) -> Dict:
        """Generate environment health report"""
        report = {
            "os": f"{self.os_name} ({self.arch})",
            "python": self.check_python_version(),
            "tools": self.check_required_tools(),
            "docker": self.check_docker(),
            "package_managers": self.check_package_managers()
        }
        
        return report
    
    def suggest_fixes(self, report: Dict) -> List[str]:
        """Suggest fixes for environment issues"""
        fixes = []
        
        # Check Python version
        if not report["python"][0]:
            fixes.append("Upgrade Python to version 3.8 or higher")
            
        # Check required tools
        missing_tools = [tool for tool, (installed, _) in report["tools"].items() if not installed]
        if missing_tools:
            if self.os_name == "darwin":
                fixes.append(f"Install missing tools: {', '.join(missing_tools)} (use 'brew install {' '.join(missing_tools)}')")
            elif self.os_name == "windows":
                fixes.append(f"Install missing tools: {', '.join(missing_tools)} (use 'choco install {' '.join(missing_tools)}')")
            elif self.os_name == "linux":
                # Find available package manager
                pkg_manager = None
                for manager, (installed, _) in report["package_managers"].items():
                    if installed:
                        pkg_manager = manager
                        break
                        
                if pkg_manager:
                    fixes.append(f"Install missing tools: {', '.join(missing_tools)} (use '{pkg_manager} install {' '.join(missing_tools)}')")
                else:
                    fixes.append(f"Install missing tools: {', '.join(missing_tools)}")
                    
        # Check Docker
        if not report["docker"][0]:
            fixes.append("Install Docker Desktop for your OS")
            
        # Check package managers
        missing_managers = [manager for manager, (installed, _) in report["package_managers"].items() if not installed]
        if missing_managers and self.os_name == "darwin":
            fixes.append("Install Homebrew: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
        elif missing_managers and self.os_name == "windows":
            fixes.append("Install Chocolatey: https://chocolatey.org/install")
            
        return fixes


def main():
    """Main entry point for environment checker"""
    checker = EnvironmentChecker()
    report = checker.generate_report()
    
    print("=== CoreX Environment Check ===")
    print(f"Operating System: {report['os']}")
    print(f"Python: {'✅' if report['python'][0] else '❌'} {report['python'][1]}")
    
    print("\nRequired Tools:")
    for tool, (installed, version) in report["tools"].items():
        status = "✅" if installed else "❌"
        print(f"  {status} {tool}: {version}")
        
    print(f"\nDocker: {'✅' if report['docker'][0] else '❌'} {report['docker'][1]}")
    
    print("\nPackage Managers:")
    for manager, (installed, version) in report["package_managers"].items():
        status = "✅" if installed else "❌"
        print(f"  {status} {manager}: {version}")
        
    # Suggest fixes
    fixes = checker.suggest_fixes(report)
    if fixes:
        print("\n🔧 Suggested Fixes:")
        for i, fix in enumerate(fixes, 1):
            print(f"  {i}. {fix}")
    else:
        print("\n✅ Environment is ready for CoreX!")
        
    # Exit with error code if critical issues found
    critical_issues = not report["python"][0] or not report["tools"]["python"][0]
    sys.exit(1 if critical_issues else 0)


if __name__ == "__main__":
    main()