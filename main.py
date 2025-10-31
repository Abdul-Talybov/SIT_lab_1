# main.py
from repository import PackageRepository
from manager import PackageManager
from commands import InstallCommand, RemoveCommand, UpdateCommand, ListCommand, UndoCommand

repo = PackageRepository()
repo.add_package("C", "1.0", [])
repo.add_package("B", "1.0", ["C==1.0"])
repo.add_package("A", "1.0", ["B==1.0"])
repo.add_package("C", "2.0", [])
repo.add_package("B", "2.0", ["C==2.0"])
repo.add_package("A", "2.0", ["B==2.0"])
repo.add_package("D", "1.0", ["C==1.0"])
repo.add_package("E", "1.0", ["C==2.0"])

pm = PackageManager(repo)

print("=== Установка A==1.0 ===")
InstallCommand(pm, "A==1.0").execute()  # C=1.0 → B=1.0 → A=1.0

print("\n=== Установка D==1.0 ===")
InstallCommand(pm, "D==1.0").execute()  # C=1.0

print("\n=== Попытка E==1.0 (конфликт) ===")
InstallCommand(pm, "E==1.0").execute()  # ТРЕБУЕТ C==2.0 → КОНФЛИКТ!

print("\n=== Список ===")
ListCommand(pm).execute()

print("\n=== Обновление A до 2.0 ===")
UpdateCommand(pm, "A==2.0").execute()  # Нужно C=2.0 → конфликт?

print("\n=== Удаление D ===")
RemoveCommand(pm, "D").execute()

print("\n=== Повторное обновление A ===")
UpdateCommand(pm, "A==2.0").execute()  # Теперь можно!

print("\n=== Дерево зависимостей ===")
pm.show_tree()

print("\n=== Отмена последней команды ===")
UndoCommand(pm).execute()
pm.show_tree()
