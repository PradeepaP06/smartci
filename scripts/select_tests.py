
import subprocess
import sys

# Get changed files from Git
base = sys.argv[1] if len(sys.argv) > 1 else "HEAD~1"
head = sys.argv[2] if len(sys.argv) > 2 else "HEAD"

result = subprocess.run(
    ["git", "diff", "--name-only", base, head],
    capture_output=True,
    text=True,
    check=True
)

changed_files = result.stdout.splitlines()

# Map source files to their test files
test_mapping = {
    "src/cart.py": "tests/test_cart.py",
    "src/inventory.py": "tests/test_inventory.py",
    "src/pricing.py": "tests/test_pricing.py",
}

selected_tests = set()

for file in changed_files:
    if file in test_mapping:
        selected_tests.add(test_mapping[file])

# Run all tests if no specific test was selected
if not selected_tests:
    selected_tests = {
        "tests/test_cart.py",
        "tests/test_inventory.py",
        "tests/test_pricing.py",
    }

print("Changed files:", changed_files)
print("Selected tests:")

for test in sorted(selected_tests):
    print(test)
