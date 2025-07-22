import pygame
import secrets
import string
import sys
import pyperclip  # Para copiar al portapapeles

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO = 800
ALTO = 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Generador de Contraseñas Seguras")

# Colores (esquema moderno)
FONDO = (20, 20, 30)
FONDO_SECUNDARIO = (30, 30, 45)
PURPURA = (102, 126, 234)
PURPURA_OSCURO = (118, 75, 162)
BLANCO = (255, 255, 255)
GRIS_CLARO = (200, 200, 200)
GRIS = (150, 150, 150)
VERDE = (76, 175, 80)
ROJO = (244, 67, 54)
AMARILLO = (255, 193, 7)

# Fuentes
fuente_titulo = pygame.font.Font(None, 60)
fuente_grande = pygame.font.Font(None, 36)
fuente_mediana = pygame.font.Font(None, 28)
fuente_pequena = pygame.font.Font(None, 24)
fuente_password = pygame.font.Font("C:/Windows/Fonts/consola.ttf", 20) if sys.platform == "win32" else pygame.font.Font(None, 20)

# Clase para manejar botones
class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.color_actual = color_base
        self.hover = False
        self.animacion = 0
        
    def dibujar(self, superficie):
        # Efecto de animación
        if self.hover:
            self.animacion = min(self.animacion + 0.1, 1)
        else:
            self.animacion = max(self.animacion - 0.1, 0)
            
        # Dibujar sombra
        sombra_rect = self.rect.copy()
        sombra_rect.x += 5
        sombra_rect.y += 5
        pygame.draw.rect(superficie, (10, 10, 20), sombra_rect, border_radius=10)
        
        # Interpolar color
        r = self.color_base[0] + (self.color_hover[0] - self.color_base[0]) * self.animacion
        g = self.color_base[1] + (self.color_hover[1] - self.color_base[1]) * self.animacion
        b = self.color_base[2] + (self.color_hover[2] - self.color_base[2]) * self.animacion
        self.color_actual = (int(r), int(g), int(b))
        
        # Dibujar botón con esquinas redondeadas
        pygame.draw.rect(superficie, self.color_actual, self.rect, border_radius=10)
        
        # Dibujar texto
        texto_render = fuente_mediana.render(self.texto, True, BLANCO)
        texto_rect = texto_render.get_rect(center=self.rect.center)
        superficie.blit(texto_render, texto_rect)
        
    def verificar_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)
        
    def es_presionado(self, pos):
        return self.rect.collidepoint(pos)

# Clase para checkboxes
class Checkbox:
    def __init__(self, x, y, texto, activo=True):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.texto = texto
        self.activo = activo
        self.hover = False
        
    def dibujar(self, superficie):
        # Dibujar caja
        color = PURPURA if self.hover else GRIS_CLARO
        pygame.draw.rect(superficie, color, self.rect, 2, border_radius=3)
        
        # Si está activo, dibujar checkmark
        if self.activo:
            pygame.draw.rect(superficie, PURPURA, 
                           (self.rect.x + 4, self.rect.y + 4, 12, 12), 
                           border_radius=2)
        
        # Dibujar texto
        texto_render = fuente_pequena.render(self.texto, True, BLANCO)
        superficie.blit(texto_render, (self.rect.x + 30, self.rect.y))
        
    def verificar_hover(self, pos):
        self.hover = self.rect.collidepoint(pos)
        
    def toggle(self, pos):
        if self.rect.collidepoint(pos):
            self.activo = not self.activo
            return True
        return False

# Clase para el slider
class Slider:
    def __init__(self, x, y, ancho, min_val, max_val, valor_inicial):
        self.rect = pygame.Rect(x, y, ancho, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.valor = valor_inicial
        self.arrastrando = False
        self.handle_rect = pygame.Rect(0, y - 5, 20, 20)
        self.actualizar_handle()
        
    def actualizar_handle(self):
        # Calcular posición del handle basado en el valor
        porcentaje = (self.valor - self.min_val) / (self.max_val - self.min_val)
        self.handle_rect.centerx = self.rect.x + porcentaje * self.rect.width
        
    def dibujar(self, superficie):
        # Dibujar línea de fondo
        pygame.draw.rect(superficie, GRIS, self.rect, border_radius=5)
        
        # Dibujar línea de progreso
        progreso_rect = self.rect.copy()
        progreso_rect.width = self.handle_rect.centerx - self.rect.x
        pygame.draw.rect(superficie, PURPURA, progreso_rect, border_radius=5)
        
        # Dibujar handle
        color = PURPURA_OSCURO if self.arrastrando else PURPURA
        pygame.draw.circle(superficie, color, self.handle_rect.center, 10)
        pygame.draw.circle(superficie, BLANCO, self.handle_rect.center, 5)
        
        # Dibujar valor
        texto_valor = fuente_mediana.render(str(self.valor), True, BLANCO)
        superficie.blit(texto_valor, (self.rect.x + self.rect.width + 20, self.rect.y - 8))
        
    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(evento.pos):
                self.arrastrando = True
        elif evento.type == pygame.MOUSEBUTTONUP:
            self.arrastrando = False
        elif evento.type == pygame.MOUSEMOTION and self.arrastrando:
            # Actualizar valor basado en la posición del mouse
            nuevo_x = max(self.rect.x, min(evento.pos[0], self.rect.x + self.rect.width))
            porcentaje = (nuevo_x - self.rect.x) / self.rect.width
            self.valor = int(self.min_val + porcentaje * (self.max_val - self.min_val))
            self.actualizar_handle()

# Función para generar contraseña
def generar_contrasena_segura(longitud, usar_mayusculas, usar_minusculas, usar_numeros, usar_simbolos):
    # Caracteres disponibles
    caracteres = ""
    password = []
    
    if usar_mayusculas:
        letras_mayusculas = ''.join(c for c in string.ascii_uppercase if c not in 'IO')
        caracteres += letras_mayusculas
        password.append(secrets.choice(letras_mayusculas))
        
    if usar_minusculas:
        letras_minusculas = ''.join(c for c in string.ascii_lowercase if c not in 'lo')
        caracteres += letras_minusculas
        password.append(secrets.choice(letras_minusculas))
        
    if usar_numeros:
        numeros = ''.join(c for c in string.digits if c not in '01')
        caracteres += numeros
        password.append(secrets.choice(numeros))
        
    if usar_simbolos:
        simbolos = '!@#$%^&*()-_=+[]{};:,.<>?/'
        caracteres += simbolos
        password.append(secrets.choice(simbolos))
    
    if not caracteres:
        return "¡Selecciona al menos un tipo de carácter!"
    
    # Completar el resto
    while len(password) < longitud:
        password.append(secrets.choice(caracteres))
    
    # Mezclar
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)

# Función para evaluar fortaleza
def evaluar_fortaleza(password):
    puntos = 0
    
    if len(password) >= 12:
        puntos += 25
    elif len(password) >= 8:
        puntos += 15
        
    if any(c.isupper() for c in password):
        puntos += 20
    if any(c.islower() for c in password):
        puntos += 20
    if any(c.isdigit() for c in password):
        puntos += 20
    if any(c in '!@#$%^&*()-_=+[]{};:,.<>?/' for c in password):
        puntos += 15
        
    if puntos >= 80:
        return "Muy Fuerte", VERDE
    elif puntos >= 60:
        return "Fuerte", (139, 195, 74)
    elif puntos >= 40:
        return "Media", AMARILLO
    else:
        return "Débil", ROJO

# Función para dibujar gradiente
def dibujar_gradiente(superficie, color1, color2, rect):
    for i in range(rect.height):
        r = color1[0] + (color2[0] - color1[0]) * i / rect.height
        g = color1[1] + (color2[1] - color1[1]) * i / rect.height
        b = color1[2] + (color2[2] - color1[2]) * i / rect.height
        pygame.draw.line(superficie, (int(r), int(g), int(b)), 
                        (rect.x, rect.y + i), (rect.x + rect.width, rect.y + i))

# Crear elementos de UI
boton_generar = Boton(300, 450, 200, 50, "Generar", PURPURA, PURPURA_OSCURO)
boton_copiar = Boton(550, 300, 120, 40, "Copiar", (76, 175, 80), (69, 160, 73))

checkbox_mayusculas = Checkbox(200, 250, "Mayúsculas (A-Z)", True)
checkbox_minusculas = Checkbox(200, 280, "Minúsculas (a-z)", True)
checkbox_numeros = Checkbox(450, 250, "Números (0-9)", True)
checkbox_simbolos = Checkbox(450, 280, "Símbolos (!@#$%)", True)

slider_longitud = Slider(200, 180, 400, 8, 128, 20)

# Variables del juego
reloj = pygame.time.Clock()
ejecutando = True
password_actual = ""
mensaje_copiado = False
tiempo_mensaje = 0
particulas = []

# Clase para efectos de partículas
class Particula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = secrets.choice([-2, -1, 0, 1, 2])
        self.vy = secrets.choice([-3, -2, -1])
        self.vida = 30
        
    def actualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.vida -= 1
        
    def dibujar(self, superficie):
        if self.vida > 0:
            alpha = self.vida / 30
            color = (102, 126, 234, int(255 * alpha))
            pygame.draw.circle(superficie, PURPURA, (int(self.x), int(self.y)), 3)

# Bucle principal
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        slider_longitud.manejar_evento(evento)
        
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if boton_generar.es_presionado(evento.pos):
                password_actual = generar_contrasena_segura(
                    slider_longitud.valor,
                    checkbox_mayusculas.activo,
                    checkbox_minusculas.activo,
                    checkbox_numeros.activo,
                    checkbox_simbolos.activo
                )
                # Crear partículas para efecto visual
                for _ in range(20):
                    particulas.append(Particula(ANCHO//2, 400))
                    
            elif boton_copiar.es_presionado(evento.pos) and password_actual and "Selecciona" not in password_actual:
                try:
                    pyperclip.copy(password_actual)
                    mensaje_copiado = True
                    tiempo_mensaje = 60
                except:
                    pass
                    
            checkbox_mayusculas.toggle(evento.pos)
            checkbox_minusculas.toggle(evento.pos)
            checkbox_numeros.toggle(evento.pos)
            checkbox_simbolos.toggle(evento.pos)
    
    # Actualizar
    pos_mouse = pygame.mouse.get_pos()
    boton_generar.verificar_hover(pos_mouse)
    boton_copiar.verificar_hover(pos_mouse)
    checkbox_mayusculas.verificar_hover(pos_mouse)
    checkbox_minusculas.verificar_hover(pos_mouse)
    checkbox_numeros.verificar_hover(pos_mouse)
    checkbox_simbolos.verificar_hover(pos_mouse)
    
    # Actualizar partículas
    particulas = [p for p in particulas if p.vida > 0]
    for p in particulas:
        p.actualizar()
    
    if tiempo_mensaje > 0:
        tiempo_mensaje -= 1
    
    # Dibujar
    ventana.fill(FONDO)
    
    # Dibujar fondo con gradiente
    dibujar_gradiente(ventana, FONDO, FONDO_SECUNDARIO, pygame.Rect(0, 0, ANCHO, ALTO))
    
    # Título con efecto
    titulo = fuente_titulo.render("Generador de Contraseñas", True, BLANCO)
    titulo_rect = titulo.get_rect(center=(ANCHO//2, 60))
    ventana.blit(titulo, titulo_rect)
    
    # Subtítulo
    subtitulo = fuente_pequena.render("Crea contraseñas únicas y seguras", True, GRIS_CLARO)
    subtitulo_rect = subtitulo.get_rect(center=(ANCHO//2, 100))
    ventana.blit(subtitulo, subtitulo_rect)
    
    # Label para longitud
    label_longitud = fuente_mediana.render("Longitud:", True, BLANCO)
    ventana.blit(label_longitud, (100, 175))
    
    # Dibujar slider
    slider_longitud.dibujar(ventana)
    
    # Label para opciones
    label_opciones = fuente_mediana.render("Incluir:", True, BLANCO)
    ventana.blit(label_opciones, (100, 220))
    
    # Dibujar checkboxes
    checkbox_mayusculas.dibujar(ventana)
    checkbox_minusculas.dibujar(ventana)
    checkbox_numeros.dibujar(ventana)
    checkbox_simbolos.dibujar(ventana)
    
    # Área de contraseña
    password_rect = pygame.Rect(100, 340, 600, 60)
    pygame.draw.rect(ventana, FONDO_SECUNDARIO, password_rect, border_radius=10)
    pygame.draw.rect(ventana, PURPURA if password_actual else GRIS, password_rect, 2, border_radius=10)
    
    if password_actual:
        # Mostrar contraseña con scroll si es muy larga
        if len(password_actual) > 40:
            password_mostrar = password_actual[:40] + "..."
        else:
            password_mostrar = password_actual
            
        password_render = fuente_password.render(password_mostrar, True, BLANCO)
        password_render_rect = password_render.get_rect(center=password_rect.center)
        ventana.blit(password_render, password_render_rect)
        
        # Mostrar fortaleza
        if "Selecciona" not in password_actual:
            fortaleza, color_fortaleza = evaluar_fortaleza(password_actual)
            fortaleza_texto = fuente_pequena.render(f"Fortaleza: {fortaleza}", True, color_fortaleza)
            ventana.blit(fortaleza_texto, (100, 410))
            
            # Barra de fortaleza
            barra_rect = pygame.Rect(250, 415, 200, 10)
            pygame.draw.rect(ventana, GRIS, barra_rect, border_radius=5)
            
            # Calcular ancho de la barra según fortaleza
            if fortaleza == "Muy Fuerte":
                ancho = 200
            elif fortaleza == "Fuerte":
                ancho = 150
            elif fortaleza == "Media":
                ancho = 100
            else:
                ancho = 50
                
            barra_llena = pygame.Rect(250, 415, ancho, 10)
            pygame.draw.rect(ventana, color_fortaleza, barra_llena, border_radius=5)
    else:
        hint_text = fuente_pequena.render("Haz clic en 'Generar' para crear una contraseña", True, GRIS)
        hint_rect = hint_text.get_rect(center=password_rect.center)
        ventana.blit(hint_text, hint_rect)
    
    # Dibujar botones
    boton_generar.dibujar(ventana)
    if password_actual and "Selecciona" not in password_actual:
        boton_copiar.dibujar(ventana)
    
    # Mensaje de copiado
    if mensaje_copiado and tiempo_mensaje > 0:
        alpha = min(255, tiempo_mensaje * 8)
        mensaje = fuente_mediana.render("¡Copiado al portapapeles!", True, VERDE)
        mensaje_rect = mensaje.get_rect(center=(ANCHO//2, 520))
        mensaje.set_alpha(alpha)
        ventana.blit(mensaje, mensaje_rect)
    
    # Dibujar partículas
    for p in particulas:
        p.dibujar(ventana)
    
    # Footer
    footer = fuente_pequena.render("💡 Usa contraseñas únicas para cada cuenta", True, GRIS)
    footer_rect = footer.get_rect(center=(ANCHO//2, ALTO - 30))
    ventana.blit(footer, footer_rect)
    
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()