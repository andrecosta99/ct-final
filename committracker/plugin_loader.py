from importlib import import_module
import pkgutil

# Function to dynamically load plugin functions from a specified directory
def load_plugins():
    plugins = {}
    # Iterates through modules in the 'committracker/plugins' directory
    for _, name, _ in pkgutil.iter_modules(['committracker/plugins']):
        if name != '__init__':  # Exclude __init__.py from being considered as a plugin
            module = import_module(f'committracker.plugins.{name}')  # Dynamically import the plugin module
            function_name = f'display_{name}'  # Convention for the plugin's main function
            try:
                # Attempt to fetch the plugin function by its convention name
                plugins[name] = getattr(module, function_name)
            except AttributeError as e:
                # Handles the case where the expected function is not found in the module
                print(f"Aviso: {e}")
    return plugins  # Returns a dictionary of plugin names mapped to their functions
