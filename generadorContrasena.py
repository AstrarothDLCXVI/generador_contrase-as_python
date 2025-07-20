import secrets
import string

def generar_contrasena_segura(longitud=20):
    # Caracteres que usaremos, excluyendo los ambiguos
    letras_mayusculas = ''.join(c for c in string.ascii_uppercase if c not in 'IO')
    letras_minusculas = ''.join(c for c in string.ascii_lowercase if c not in 'lo')
    numeros = ''.join(c for c in string.digits if c not in '01')
    simbolos = '!@#$%^&*()-_=+[]{};:,.<>?/'

    # Combinamos todos los caracteres
    caracteres = letras_mayusculas + letras_minusculas + numeros + simbolos

    # Aseguramos que incluya al menos un carácter de cada tipo
    password = [
        secrets.choice(letras_mayusculas),
        secrets.choice(letras_minusculas),
        secrets.choice(numeros),
        secrets.choice(simbolos),
    ]

    # Completamos el resto de la contraseña
    while len(password) < longitud:
        password.append(secrets.choice(caracteres))

    # Mezclamos para que no siempre estén en el mismo orden
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)

# Ejemplo de uso
if __name__ == "__main__":
    print("Contraseña segura generada:")
    print(generar_contrasena_segura(100))  # Se puede aumentar o disminuir la longitud
