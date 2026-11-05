"""Універсальний скрипт порівняльного аналізу структури проектів."""

import os
import sys


def scan_directory(path: str, prefix: str = '') -> list[str]:
    """Рекурсивно сканує каталог та повертає дерево файлів."""
    tree = []
    ignore_items = {'__pycache__', '.git', '.vs', 'venv', '.venv', 'db.sqlite3', '.pytest_cache'}
    ignore_extensions = {'.pyc', '.pyo'}

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        return tree

    filtered_entries = []
    for entry in entries:
        if entry in ignore_items:
            continue
        ext = os.path.splitext(entry)[1]
        if ext in ignore_extensions:
            continue
        filtered_entries.append(entry)

    count = len(filtered_entries)
    for index, entry in enumerate(filtered_entries):
        full_path = os.path.join(path, entry)
        is_last = (index == count - 1)
        connector = "└── " if is_last else "├── "

        if os.path.isdir(full_path):
            tree.append(f"{prefix}{connector}{entry}/")
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree.extend(scan_directory(full_path, new_prefix))
        else:
            tree.append(f"{prefix}{connector}{entry}")

    return tree


def analyze_project(path: str) -> dict:
    """Аналізує проект та збирає статистику."""
    stats = {
        'py_files': 0,
        'html_files': 0,
        'css_files': 0,
        'total_size': 0,
        'directories': 0,
    }

    ignore_items = {'__pycache__', '.git', '.vs', 'venv', '.venv', 'db.sqlite3', '.pytest_cache'}

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ignore_items]
        stats['directories'] += len(dirs)

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in {'.pyc', '.pyo'} or file == 'db.sqlite3':
                continue

            file_path = os.path.join(root, file)
            try:
                stats['total_size'] += os.path.getsize(file_path)
            except OSError:
                pass

            if ext == '.py':
                stats['py_files'] += 1
            elif ext == '.html':
                stats['html_files'] += 1
            elif ext == '.css':
                stats['css_files'] += 1

    return stats


def compare_projects(proj1_path: str, proj2_path: str):
    """Порівнює два проекти та виводить таблицю відмінностей."""
    name1 = os.path.basename(os.path.abspath(proj1_path))
    name2 = os.path.basename(os.path.abspath(proj2_path))

    print("=" * 60)
    print("ПОРІВНЯННЯ СТРУКТУРИ ПРОЕКТІВ")
    print("=" * 60)

    
    print(f"\n--- Проєкт 1: {name1} ({proj1_path}) ---")
    tree1 = scan_directory(proj1_path)
    for line in tree1:
        print(line)
    stats1 = analyze_project(proj1_path)

    
    print(f"\n--- Проєкт 2: {name2} ({proj2_path}) ---")
    tree2 = scan_directory(proj2_path)
    for line in tree2:
        print(line)
    stats2 = analyze_project(proj2_path)

    print("\n" + "=" * 60)
    print("ПОРІВНЯЛЬНА ТАБЛИЦЯ ХАРАКТЕРИСТИК")
    print("=" * 60)
    print(f"{'Характеристика':<25} | {name1[:12]:<12} | {name2[:12]:<12}")
    print("-" * 55)
    print(f"{'Файли .py':<25} | {stats1['py_files']:<12} | {stats2['py_files']:<12}")
    print(f"{'Файли .html':<25} | {stats1['html_files']:<12} | {stats2['html_files']:<12}")
    print(f"{'Файли .css':<25} | {stats1['css_files']:<12} | {stats2['css_files']:<12}")
    print(f"{'Каталоги':<25} | {stats1['directories']:<12} | {stats2['directories']:<12}")
    print(f"{'Загальний розмір (байт)':<25} | {stats1['total_size']:<12} | {stats2['total_size']:<12}")
    print("-" * 55)


def main():
    
    if len(sys.argv) == 3:
        path1, path2 = sys.argv[1], sys.argv[2]
    else:
        
        print("Вкажіть шляхи до папок проєктів (відносні або абсолютні):")
        path1 = input("Шлях до Django-проєкту (наприклад, ../pr5_2_1_2_2): ").strip()
        path2 = input("Шлях до Flask-проєкту (наприклад, .): ").strip()

    if not os.path.isdir(path1):
        print(f"Помилка: Папку '{path1}' не знайдено.")
        return

    if not os.path.isdir(path2):
        print(f"Помилка: Папку '{path2}' не знайдено.")
        return

    compare_projects(path1, path2)


if __name__ == "__main__":
    main()
