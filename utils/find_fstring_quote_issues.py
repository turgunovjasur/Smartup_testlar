import os
import re

# F-string ichida [" yoki [" kabilarni izlaymiz
fstring_error_pattern = re.compile(r'f".*?\{.*?\[".*?"\].*?\}.*?"')

def find_test_function(lines, error_line_index):
    # Yuqoriga qarab yurib, test funksiyani topamiz
    for i in range(error_line_index, -1, -1):
        line = lines[i].strip()
        if line.startswith("def test_"):
            return line
    return "Unknown test function"

def scan_file(file_path):
    issues_found = False
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        if 'f"' in line and fstring_error_pattern.search(line):
            func_name = find_test_function(lines, idx)
            print(f"❌ Issue in {file_path}, line {idx+1}:")
            print(f"   → {func_name}")
            print(f"   → {line.strip()}")
            print()
            issues_found = True

    return issues_found

def scan_directory(path):
    print("🔍 Scanning for f-string quote issues...\n")
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(root, file)
                scan_file(full_path)

    print("✅ Scan complete.")

if __name__ == '__main__':
    scan_directory('tests')  # tests/ papkasini tekshiradi
