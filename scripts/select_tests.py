import subprocess
import sys

base = sys.argv[1] if len(sys.argv) > 1 else "HEAD~1"
head = sys.argv[2] if len(sys.argv) > 2 else "HEAD"

result = subprocess.run(
    ["git", "diff", "--name-only", base, head],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print("Git comparison failed. Running all tests.")
    changed_files = []
else:
    changed_files = result.stdout.splitlines()

print("Changed files:", changed_files)

test_mapping = {
    "src/cart.py": "tests/test_cart.py",
    "src/inventory.py": "tests/test_inventory.py",
    "src/pricing.py": "tests/test_pricing.py",
}

selected_tests = {
    test_mapping[file]
    for file in changed_files
    if file in test_mapping
}

if not selected_tests:
    selected_tests = set(test_mapping.values())

print("Selected tests:")

for test in sorted(selected_tests):
    print(test)

print("\nRunning selected tests...")

sys.exit(subprocess.run(
    [sys.executable, "-m", "pytest", "-v", *sorted(selected_tests)]
).returncode)
