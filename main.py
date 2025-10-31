from manager import *
if __name__ == "__main__":
    # Создание структуры пакетов
    core = PackageGroup("Core")
    core.add(Package("LibA"))
    core.add(Package("LibB"))

    app = PackageGroup("AppSuite")
    app.add(core)
    app.add(Package("UI"))
    app.add(Package("CLI"))

    # Менеджер и команды
    manager = PackageManager()

    manager.execute_command(DisplayCommand(app))
    manager.execute_command(InstallCommand(app))
    manager.execute_command(UpdateCommand(Package("UI")))
    manager.execute_command(RemoveCommand(core))