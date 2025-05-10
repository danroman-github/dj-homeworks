from django.apps import AppConfig


class PhonesConfig(AppConfig):
    name = 'phones'

    def ready(self):
        # Проверяем регистрацию команд
        try:
            from phones.management import registered_commands
            if not registered_commands:
                raise RuntimeError("No commands were registered")
            print("Registered commands:", list(registered_commands.keys()))
        except ImportError as e:
            print(f"Command registration check failed: {e}")
