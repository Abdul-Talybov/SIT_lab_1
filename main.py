from repository import PackageRepository
from manager import PackageManager
from commands import InstallCommand, RemoveCommand, UpdateCommand, ListCommand


if __name__ == "__main__":
    print("=== Создаём репозиторий пакетов ===")
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

    print("\n=== Установка A==1.0 ===")
    InstallCommand(pm, "A==1.0").execute()
    pm.show_tree()

    print("\n=== Установка D==1.0 ===")
    InstallCommand(pm, "D==1.0").execute()

    print("\n=== Попытка установки E==1.0 (конфликт) ===")
    InstallCommand(pm, "E==1.0").execute()

    print("\n=== Состояние пакетов ===")
    ListCommand(pm).execute()

    print("\n=== Обновление A до 2.0 (конфликт) ===")
    UpdateCommand(pm, "A==2.0").execute()

    print("\n=== Удаляем D, затем обновляем A ===")
    RemoveCommand(pm, "D").execute()
    UpdateCommand(pm, "A==2.0").execute()

    print("\n=== Итоговое дерево ===")
    pm.show_tree()

