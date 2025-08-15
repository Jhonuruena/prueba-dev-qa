# Prueba Técnica QA - Suite de Automatización Completa

Este repositorio contiene una suite completa de pruebas automatizadas para múltiples APIs y aplicaciones web públicas, completamente dockerizada y lista para ejecutarse como parte de prueba tecnica de Jhon Urueña para el cargo de Desarrollador QA 

## Aplicaciones bajo prueba

- JSONPlaceholder API: https://jsonplaceholder.typicode.com/
- ReqRes API: https://reqres.in/
- The Internet (Herokuapp): https://the-internet.herokuapp.com/
- Swagger Petstore: https://petstore.swagger.io/

---

## Cobertura de Pruebas

### JSONPlaceholder API
- CRUD completo en `/posts`: GET, POST, PUT, DELETE
- Validación de datos: tipos (`int`, `str`) y campos requeridos
- Relaciones:
  - `/posts/{id}/comments` → Verifica que los comentarios pertenezcan al post
  - `/users/{id}/posts` → Verifica que los posts pertenezcan al usuario
- Casos negativos:
  - IDs inexistentes → `GET /posts/999999` → 404
  - Payloads inválidos → `POST` con campos `null`
  - Métodos no permitidos → `PUT /posts` → 404 o 405
- Performance básica: 10 requests a `/posts` con tiempo promedio menor a 2 segundos

**Particularidades observadas**
- `DELETE /posts/{id}` devuelve 200 o 204, pero no elimina realmente el recurso; un `GET` posterior sigue devolviendo el post. Esto es esperado porque JSONPlaceholder es una API de prueba sin estado persistente.
- `GET` con IDs muy altos (por ejemplo 999999) devuelve 404; en versiones anteriores podía devolver 200 con `{}`.

### ReqRes API
- Autenticación:
  - `POST /api/login` → Login exitoso y fallido
  - `POST /api/register` → Registro exitoso
- Gestión de usuarios:
  - CRUD completo en `/api/users`
  - Paginación: `GET /api/users?page=2` → Validación de `page`, `per_page`, `total_pages`
- Rate limiting: 50 requests consecutivas a `/api/users` sin errores

**Particularidades observadas**
- Requiere API Key en el encabezado:
  ```
  x-api-key: reqres-free-v1
  ```
  Sin este header responde con `401 Missing API key`.
- Login funcional solo con credenciales predefinidas, por ejemplo:
  ```json
  {
    "email": "eve.holt@reqres.in",
    "password": "123456"
  }
  ```
- No es posible autenticar con el correo registrado mediante `POST /api/register` porque el registro es una simulación.
- El token devuelto por login/register es ficticio y no sirve para autenticación real en otros endpoints.

### The Internet (Herokuapp) — Pruebas E2E con Selenium WebDriver
- Autenticación: `/login` (usuario `tomsmith`, password `SuperSecretPassword!`)
- Elementos dinámicos: `/dynamic_loading/1` y `/dynamic_loading/2`
- Carga/descarga de archivos: `/upload` y `/download`
- Interacciones complejas: `/drag_and_drop` (ActionChains)
- Alertas de JavaScript: `/javascript_alerts` (aceptar, cancelar, enviar texto)

**Casos críticos automatizados**
- Login completo con validación de mensajes y sesión
- Upload de archivo y verificación del resultado
- Manejo de elementos que aparecen/desaparecen dinámicamente
- Interacciones de arrastrar y soltar

### Swagger Petstore
- Pruebas de endpoints de `pets` para validación funcional y escenarios de carga.

---

## Pruebas de Performance (k6)
- JSONPlaceholder: 100 usuarios concurrentes durante 2 minutos contra `/posts`
- ReqRes API: 50 usuarios simultáneos contra `/api/users`
- Swagger Petstore: aproximadamente 200 requests por minuto contra `/pet/1`

**Métricas capturadas**
- Tiempo de respuesta promedio y p95
- Throughput (request por segundo)
- Tasa de errores
- Umbrales para validar éxito y detectar puntos de quiebre

---

## Setup y Entrega

### Repositorio GitHub
Código con commits descriptivos y estructura clara.

### Dockerización
Todo se ejecuta con:
```bash
docker-compose up -d --build
```
Este comando construye imágenes, levanta contenedores en segundo plano e instala dependencias. Los contenedores quedan corriendo para ejecutar pruebas manualmente si se requiere.

---


## Cómo ejecutar la suite de pruebas

### Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/prueba-dev-qa.git
cd prueba-dev-qa
```

### Levantar los contenedores
```bash
docker-compose up -d --build
```

### Ejecutar las pruebas

**Pruebas de API**
```bash
# JSONPlaceholder (GET, POST, PUT, DELETE)
docker-compose exec api-tests python -m pytest api-tests/jsonplaceholder/test_posts.py -v

# ReqRes (login, usuarios)
docker-compose exec api-tests python -m pytest api-tests/reqres/test_users.py -v
```

**Pruebas E2E (The Internet)**
```bash
# Todas las pruebas E2E
docker-compose exec e2e-tests python -m pytest /app/e2e_tests/the_internet/tests/ -v

# Prueba específica
docker-compose exec e2e-tests python -m pytest /app/e2e_tests/the_internet/tests/test_login.py -v
```

**Pruebas de Performance (k6)**
```bash
# JSONPlaceholder
docker-compose exec performance-tests k6 run performance-tests/jsonplaceholder/script.js

# ReqRes
docker-compose exec performance-tests k6 run performance-tests/reqres/script.js

# Petstore
docker-compose exec performance-tests k6 run performance-tests/petstore/script.js
```

### Detener todo
```bash
docker-compose down
```

---

## Estructura del proyecto
```
prueba-dev-qa/
├── api-tests/
│   ├── jsonplaceholder/
│   └── reqres/
├── e2e_tests/
│   └── the_internet/
│       ├── pages/
│       ├── utils/
│       └── tests/
├── performance-tests/
│   ├── jsonplaceholder/
│   ├── reqres/
│   └── petstore/               
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.e2e
└── requirements.txt
```

---

## Tecnologías utilizadas
- Python 3.10+
- pytest
- requests
- Selenium WebDriver
- webdriver-manager
- k6
- JavaScript (scripts k6)
- Docker y Docker Compose
- seleniarm/standalone-chromium

---

## Notas técnicas
- Todas las pruebas corren en modo headless dentro de contenedores.
- El contenedor `e2e-tests` usa una imagen oficial de Selenium para evitar incompatibilidades encontradas por navegador y driver de navegador.
- En pruebas E2E las rutas de archivos se construyen con `os.path.join` para compatibilidad en Docker en la prueba especifica de subir el archivo.
- Se usa entorno virtual (venv) para evitar conflictos con PEP 668.

---

## Entregables completos
- Suite de pruebas API, E2E y Performance
- Dockerización completa
- Documentación técnica en README
- Commits descriptivos


---

## Créditos
Proyecto creado por Jhon Fisgerald Urueña Prieto, con una mano extra de la IA para documentar, organizar ideas y descubrir tecnologías nuevas.
