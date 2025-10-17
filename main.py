from repository import PackageRepository
from manager import PackageManager
from commands import InstallCommand, RemoveCommand, UpdateCommand, ListCommand

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

InstallCommand(pm, "A==1.0").execute()
InstallCommand(pm, "D==1.0").execute()
InstallCommand(pm, "E==1.0").execute()  # конфликт

ListCommand(pm).execute()

UpdateCommand(pm, "A==2.0").execute()

RemoveCommand(pm, "D").execute()
UpdateCommand(pm, "A==2.0").execute()

pm.show_tree()