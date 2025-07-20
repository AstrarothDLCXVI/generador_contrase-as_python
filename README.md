# 🔐 Generador de Contraseñas Seguras en Python

Este proyecto es un generador de contraseñas seguras escrito en Python. Utiliza el módulo `secrets` para garantizar una aleatoriedad criptográficamente segura, ideal para proteger cuentas personales, claves API, o sistemas que requieran alta seguridad.

## ✅ Características

- Genera contraseñas seguras y aleatorias.
- Longitud personalizable (por defecto 100 caracteres).
- Incluye:
  - Letras mayúsculas y minúsculas (sin caracteres ambiguos).
  - Números (excluye `0` y `1`).
  - Símbolos especiales seguros.
- Se asegura de incluir al menos un carácter de cada tipo.
- Evita caracteres fácilmente confundibles como: `l`, `I`, `1`, `0`, `O`, etc.

## 📦 Requisitos

Este script no requiere instalar librerías externas. Solo utiliza módulos estándar de Python.

- Python 3.6 o superior

