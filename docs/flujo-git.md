# Flujo de trabajo Git

## Ramas

- `main`: versión estable y demostrable.
- `feature/mvp-padron`: desarrollo actual del MVP.
- `feature/<tema>`: cambios aislados para importación, telefonía, pagos o permisos.
- `release/<version>`: preparación de una versión candidata cuando el MVP esté validado.
- `hotfix/<tema>`: correcciones urgentes sobre una versión estable.

## Regla de trabajo

1. Cada bloque funcional se desarrolla en una rama `feature/<tema>`.
2. Se valida con Docker, API y pantalla.
3. Se revisa el diff y se documentan las decisiones.
4. Se integra a `main` mediante pull request cuando el área confirme el comportamiento.
5. No se incorporan archivos operativos, Excel originales ni datos reales al repositorio.

Mientras se trabaja en este entorno, los cambios permanecen en `feature/mvp-padron`. No se hacen commits ni merges automáticos.