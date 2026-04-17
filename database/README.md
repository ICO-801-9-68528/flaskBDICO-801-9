Carpeta para archivos relacionados con la base de datos del proyecto.

Propósito:
- Centralizar volcados (`dumps/`), esquemas y scripts de import/export.

Estructura sugerida:
- `dumps/` — volcados locales (.sql). Este directorio está pensado para no subirse al repositorio.
- `schema.sql` — plantilla o export del esquema (opcional, versionable).

Comandos útiles (MySQL):

Exportar toda la base de datos (volcado):
```bash
mysqldump -u USUARIO -p NOMBRE_BD > database/dumps/backup.sql
```

Importar un volcado:
```bash
mysql -u USUARIO -p NOMBRE_BD < database/dumps/backup.sql
```

Sugerencia: no almacenar credenciales en texto plano; usar variables de entorno o `config.py`.

Nota: la aplicación usa `config.py` para la URI de la base de datos. Ajusta los comandos según `SQLALCHEMY_DATABASE_URI`.
