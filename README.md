# Prueba Técnica QA - Suite de Automatización

Este proyecto implementa una suite completa de pruebas automatizadas para 4 aplicaciones web públicas:

- JSONPlaceholder
- ReqRes
- The Internet - Herokuapp
- Swagger Petstore

Cumple con los requisitos de pruebas API, E2E, performance para la prueba desarrollador QA Jhon Urueña.


### JSONPlaceholder API
[https://jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com)

- CRUD completo en `/posts`: GET, POST, PUT, DELETE
- Validación de datos: Tipos (`int`, `str`), campos requeridos
- Relaciones:
  - `/posts/{id}/comments` → Verifica que los comentarios pertenezcan al post
  - `/users/{id}/posts` → Verifica que los posts pertenezcan al usuario
- Casos negativos:
  - IDs inexistentes → `GET /posts/999999` → 404
  - Payloads inválidos → `POST` con campos null
  - Métodos no permitidos → `PUT /posts` → 404 o 405
- Performance básica: 10 requests a `/posts` con tiempo promedio < 2 segundos

**Particularidades observadas**
- El endpoint `DELETE /posts/{id}` devuelve 200 o 204, pero no elimina realmente el recurso. Al hacer `GET` después, el post sigue disponible. Esto es esperado, ya que JSONPlaceholder es una API de prueba sin estado persistente.

### ReqRes API
[https://reqres.in/api](https://reqres.in/api)

- Autenticación:
  - `POST /api/login` → Login exitoso y fallido
  - `POST /api/register` → Registro exitoso
- Gestión de usuarios:
  - CRUD completo en `/api/users`
  - Paginación: `GET /api/users?page=2` → Validación de `page`, `per_page`, `total_pages`
- Rate limiting: 50 requests consecutivas a `/api/users` sin errores

**Particularidades observadas**
- Requiere API Key: Aunque no está bien documentado, ReqRes ahora exige el encabezado:
  ```
  x-api-key: reqres-free-v1
  ```
  Sin este header, responde con `401 Missing API key`.
- Login solo funciona con credenciales predefinidas, como:
  ```json
  {
    "email": "eve.holt@reqres.in",
    "password": "123456"
  }
  ```
- No es posible hacer login con un correo registrado en `POST /api/register`, ya que el registro es solo una simulación.
- El token devuelto en login/register es ficticio y no permite autenticación real en otros endpoints.

### The Internet - Herokuapp
[https://the-internet.herokuapp.com/](https://the-internet.herokuapp.com/)

Pruebas E2E con Selenium WebDriver

Casos críticos automatizados:
- Login completo: `/login` → Validación de mensaje y sesión
- Upload de archivo: `/upload` → Subida y verificación de "File Uploaded!"
- Elementos dinámicos: `/dynamic_loading/2` → Espera explícita a contenido asíncrono
- Interacciones complejas: `/drag_and_drop` → Arrastrar y soltar con ActionChains
- Alertas de JavaScript: `/javascript_alerts` → Aceptar, cancelar, enviar texto

### Pruebas de Performance con k6

**Herramienta:** k6

**Escenarios implementados:**
- JSONPlaceholder: 100 usuarios concurrentes durante 2 minutos en `/posts`
- ReqRes: 50 usuarios simultáneos en `/api/users`
- Swagger Petstore: ~200 requests/minuto en `/pet/1`

**Métricas capturadas:**
- Tiempo de respuesta promedio y p95
- Throughput (rps)
- Tasa de errores
- Umbrales definidos para validar éxito

## Tecnologías Usadas
- Python 3.10+
- pytest: Framework de pruebas
- requests: Cliente HTTP para pruebas de API
- Selenium WebDriver: Automatización de navegador
- webdriver-manager: Gestión automática de ChromeDriver
- k6: Pruebas de performance
- JavaScript: Scripts de k6
- Docker: Contenerización (próximamente)

## Cómo Ejecutar

Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/prueba-dev-qa.git
cd prueba-tecnica-qa
```

Instala dependencias:
```bash
pip install pytest requests selenium webdriver-manager
```

Ejecuta las pruebas:

**Pruebas de API - JSONPlaceholder**
```cmd
python -m pytest api-tests\jsonplaceholder\test_posts.py -v
```

**Pruebas de API - ReqRes**
```cmd
python -m pytest api-tests\reqres\test_users.py -v
```

**Pruebas E2E - The Internet**
```cmd
python -m pytest e2e_tests\the_internet\tests\test_login.py -v
python -m pytest e2e_tests\the_internet\tests\test_upload.py -v
python -m pytest e2e_tests\the_internet\tests\test_dynamic_loading.py -v
python -m pytest e2e_tests\the_internet\tests\test_drag_and_drop.py -v
python -m pytest e2e_tests\the_internet\tests\test_javascript_alerts.py -v
```

**Pruebas de Performance - k6**
```bash
k6 run performance-tests/jsonplaceholder/script.js
k6 run performance-tests/reqres/script.js
k6 run performance-tests/petstore/script.js
```
