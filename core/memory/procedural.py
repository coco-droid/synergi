import importlib.util

class ProceduralMemory:
    def __init__(self):
        self.procedures = {}

    def add(self, name, script):
        # Ajoute une procédure
        self.procedures[name] = script

    def run(self, name, args):
        # Exécute une procédure par son nom
        if name in self.procedures:
            spec = importlib.util.spec_from_loader(name, loader=None)
            module = importlib.util.module_from_spec(spec)
            exec(self.procedures[name], module.__dict__)
            result = getattr(module, name)(*args)
            return result
        else:
            raise ValueError(f"La procédure {name} n'existe pas.")

    def list(self):
        # Liste toutes les procédures
        return list(self.procedures.keys())

    def delete(self, name):
        # Supprime une procédure
        if name in self.procedures:
            del self.procedures[name]
        else:
            raise ValueError(f"La procédure {name} n'existe pas.")