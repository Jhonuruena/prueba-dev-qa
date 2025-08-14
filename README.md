# Prueba Técnica QA - Suite de Automatización

Este proyecto implementa una suite de pruebas automatizadas para las APIs públicas **JSONPlaceholder** y **ReqRes**, (Pendiente continuar con el resto de la Suite) cumpliendo con los requisitos de validación, relaciones, casos negativos, performance y buenas prácticas.

## Cobertura de Pruebas

### JSONPlaceholder API

**URL:** [https://jsonplaceholder.typicode.com](https://jsonplaceholder.typicode.com)

- CRUD completo en `/posts`: `GET`, `POST`, `PUT`, `DELETE`
- Validación de datos: Tipos (`int`, `str`), campos requeridos
- Relaciones:
  - `/posts/{id}/comments` → Verifica que los comentarios pertenezcan al post
  - `/users/{id}/posts` → Verifica que los posts pertenezcan al usuario
- Casos negativos:
  - IDs inexistentes → `GET /posts/999999` → 404
  - Payloads inválidos → `POST` con campos null
  - Métodos no permitidos → `PUT /posts` → 404 o 405
- Performance básica: 10 requests a `/posts` con tiempo promedio < 2 segundos

**Particularidades observadas:**

- El endpoint `DELETE /posts/{id}` devuelve 200 o 204, pero no elimina realmente el recurso. Al hacer `GET` después, el post sigue disponible. Esto es esperado, ya que JSONPlaceholder es una API de prueba sin estado persistente.
- `GET` con IDs muy altos (ej: 999999) ahora devuelve 404, no 200 con `{}` como en versiones anteriores.

### ReqRes API

**URL:** [https://reqres.in/api](https://reqres.in/api)

- Autenticación:
  - `POST /api/login` → Login exitoso y fallido
  - `POST /api/register` → Registro exitoso
- Gestión de usuarios:
  - CRUD completo en `/api/users`
  - Paginación: `GET /api/users?page=2` → Validación de `page`, `per_page`, `total_pages`
- Rate limiting: 50 requests consecutivas a `/api/users` sin errores

**Particularidades observadas:**

- Requiere API Key: Aunque no está bien documentado, ReqRes ahora exige el encabezado:

```
x-api-key: reqres-free-v1
```

Sin este header, responde con 401 Missing API key.

- Login solo funciona con credenciales predefinidas:

```json
{
  "email": "eve.holt@reqres.in",
  "password": "123456"
}
```

- No es posible hacer login con un correo registrado en `POST /api/register`, ya que el registro es solo una simulación.
- El token devuelto en login/register es ficticio y no permite autenticación real en otros endpoints.

## Tecnologías Usadas

- Python 3.10+
- `pytest` (Framework de pruebas)
- `requests` (Cliente HTTP para pruebas de API)
- `time` (Medición de tiempos de respuesta)

## Cómo Ejecutar

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/prueba-tecnica-qa.git
cd prueba-tecnica-qa
```

2. Instalar dependencias:

```bash
pip install pytest requests
```

3. Ejecutar las pruebas:

- Pruebas de JSONPlaceholder:

```bash
python -m pytest api-tests/jsonplaceholder/test_posts.py -v
```

- Pruebas de ReqRes:

```bash
python -m pytest api-tests/reqres/test_users.py -v
```

