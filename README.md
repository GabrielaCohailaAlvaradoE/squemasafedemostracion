# SchemaSafe NoSQL · GitHub Action

Revisa en **solo lectura** el riesgo de un cambio de esquema en MongoDB, CouchDB o Cassandra y lo publica como comentario en el pull request. Si el riesgo es **CRÍTICO**, abre o actualiza una issue.

- **Sin tokens que crear:** usa el `GITHUB_TOKEN` que GitHub genera solo en cada ejecución.
- **Sin cuentas ni servidores:** instala el CLI [`schemasafe` de PyPI](https://pypi.org/project/schemasafe/) y analiza datos sintéticos (procedencia `fixture`).
- **Nunca escribe en una base de datos.**

## Probarlo en 3 pasos

1. Pulsa **Use this template → Create a new repository** (o haz *fork* y activa Actions en la pestaña *Actions*).
2. En tu copia, edita `schema-change.json` en una rama nueva, por ejemplo cambia `"operation"` a `"remove_field"`, y abre un **pull request dentro de tu copia**.
3. En un minuto aparece el comentario de SchemaSafe en el PR. Con `remove_field` el riesgo es CRÍTICO y además se abre una issue.

> Un PR que viene de un *fork* hacia otro repositorio recibe un token de solo lectura y no puede comentar. Abre el PR dentro de tu propia copia.

## Usarlo en tu repositorio

```yaml
name: SchemaSafe
on:
  pull_request:
    paths: ["schema-change.json"]
permissions:
  contents: read
  pull-requests: write
  issues: write
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: GabrielaCohailaAlvaradoE/schemasafe-action@v1
```

`schema-change.json`:

```json
{ "engine": "mongodb", "resource": "demo", "operation": "change_type", "field": "edad", "target_type": "string" }
```

## Entradas

| Entrada | Por defecto | Uso |
| --- | --- | --- |
| `change-file` | `schema-change.json` | Archivo con el cambio propuesto |
| `engine`, `resource`, `operation`, `field`, `target-type` | del archivo | Reemplazan los valores del archivo |
| `pr-number` | el PR del evento | PR donde comentar |
| `github-token` | `GITHUB_TOKEN` automático | No hace falta cambiarlo |
| `dry-run` | `false` | `true` muestra el comentario en el log sin publicarlo |
| `schemasafe-version` | `0.2.0` | Versión del CLI en PyPI |

Operaciones probadas con el CLI 0.2.0: `remove_field` (CRÍTICO), `change_type` con `target_type` (ALTO), `require_field` (MEDIO), `add_index` y `remove_index` (BAJO). Las operaciones que necesitan parámetros extra, como `rename_field`, todavía no se pueden indicar desde el CLI.

## Parte de SchemaSafe NoSQL

Proyecto de Base de Datos II (SI-783), Universidad Privada de Tacna. Las otras integraciones:

- Extensión de VS Code: [Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=SchemaSafeNoSQL.schemasafe-vscode).
- CLI y webhook firmado: [PyPI](https://pypi.org/project/schemasafe/).
- Aplicación web de demostración: <https://schemasafe-frontend-demo.pages.dev>.
