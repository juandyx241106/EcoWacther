#!/usr/bin/env python
"""Script para inicializar las bases de datos."""

if __name__ == "__main__":
    from database.usuarios import init_db as init_usuarios
    from database.db import init_db as init_ecowatcher
    
    init_usuarios()
    print("✓ Base de datos usuarios.db creada")
    
    init_ecowatcher()
    print("✓ Base de datos EcoWatcher.db creada")
