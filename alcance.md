# Alcance · Kiwi.com

- **Programa:** Kiwi.com Bug Bounty (HackerOne, programa gestionado) · https://hackerone.com/kiwicom
- **Fecha de consulta:** 29/10/2026
- **Estado:** programa público y con recompensas.
- **Fuentes:**
  1. Política del programa (última actualización indicada: 21/08/2025).
  2. CSV de alcance estructurado descargado de HackerOne el 29/10/2026 a las 19:08 UTC (`scopes_for_kiwicom_at_2026-10-29_19_08_21_UTC.csv`).

## 1. Dentro del alcance

| Activo | Tipo | Qué es (según el programa) |
|---|---|---|
| `www.kiwi.com` | URL | Sitio web principal |
| `*.kiwi.com` | Comodín | Versiones de marca del sitio principal. El programa pide reportar solo en `www.kiwi.com` y no duplicar aquí |
| `*.skypicker.com` | Comodín | APIs y herramientas internas |
| `auth.skypicker.com` | URL | API de autenticación usada por `www.kiwi.com` |
| `tequila.kiwi.com` | URL | Plataforma B2B. Su backend pasa por `tequila-api.kiwi.com` y `api.tequila.kiwi.com` |
| `www.kiwi.com/stories` | URL | Revista online, con impacto muy limitado |
| `jobs.kiwi.com` | URL | Página de empleo |
| `com.skypicker.main` | App Android | Objetivo principal |
| `com.skypicker.Skypicker` | App iOS | Objetivo principal |

**Decisión del proyecto sobre `skypicker.com`:** aunque `*.skypicker.com` está en alcance, el reconocimiento se centra en `kiwi.com` porque es la marca y el sitio principal, mientras que `skypicker.com` aloja APIs y herramientas internas. `skypicker.com` se mantiene en `scope.txt` por fidelidad al programa.

**Decisión del proyecto sobre el dominio raíz `kiwi.com`:** el programa lista `www.kiwi.com` y `*.kiwi.com`, pero no `kiwi.com`, y un comodín `*.dominio` no incluye el propio dominio. Lo incluyo en `scope.txt` con un comentario que lo justifica: sobre el raíz solo hago consultas pasivas a registros públicos (whois y DNS), que no tocan al objetivo.

## 2. Fuera del alcance (23 entradas, todas de terceros)

El programa marca como no elegibles los servicios operados por otras empresas bajo dominios de Kiwi.com.

| Patrón | Motivo según el CSV |
|---|---|
| `*cars.kiwi.com` | Operado por rentalcars.com |
| `status.kiwi.com` | Alojado en statuspage.io |
| `*code.kiwi.com` | Alojado en medium.com |
| `*parking.kiwi.com` | Operado por travelcar.com |
| `rooms.kiwi.com` | Operado por Booking.com |
| `retool.skypicker.com` | Operado por Retool |
| `*learn.kiwi.com` | Operado por Northpass |
| `vacation.kiwi.com` | Tercero |
| `*.coupons.kiwi.com` | Gestionado por un tercero |
| `*experiences.kiwi.com` | Gestionado por un tercero |
| `kiwistore.kiwi.com` | Tercero alojado bajo el dominio |
| `*ov.kiwi.com`, `*sg.kiwi.com` | Activos de terceros bajo dominios de Kiwi.com |
| `*._domainkey.kiwi.com`, `*_domainkey.skypicker.com` | Activos de terceros (claves DKIM) |
| `outbound.intercom.kiwi.com` | Activo de tercero |
| `email*kiwi.com`, `email*skypicker.com` | Tercero enlazado bajo el dominio |
| `mail.skypicker.com` | Tercero enlazado bajo el dominio |
| `packages.kiwi.com` | Tercero enlazado bajo el dominio |
| `nyrujhhu3yuk.nest.skypicker.com` | Tercero enlazado bajo el dominio |
| `*citi-sign.kiwi.com` | Tercero enlazado bajo el dominio |
| `link.kiwi.com` | Tercero enlazado bajo el dominio |

## 3. Reglas que afectan a este proyecto

Respuestas a las preguntas del enunciado:

1. **¿Permite herramientas automáticas?** No las prohíbe, pero regula los escaneos con un límite de peticiones. En este proyecto uso herramientas pasivas que consultan fuentes públicas y no al objetivo.
2. **¿Límite de peticiones?** Sí: un retardo de 500 ms entre peticiones a un mismo hostname, es decir, 2 peticiones por segundo como máximo. Mis peticiones directas se limitan a unas pocas consultas puntuales (`robots.txt`, `security.txt`) a hosts en alcance, muy por debajo de ese límite. Este límite se aplicará también al agente de la Parte 2.
3. **¿Prohíbe contactar con empleados?** Prohíbe la ingeniería social contra empleados o contratistas. No contacto con ninguna persona; del reconocimiento de correos solo recojo el patrón corporativo, sin nombres.
4. **¿Requisito de identificación?** No exige cabecera ni *user-agent* concretos. Para registros o inicios de sesión pide un correo `<usuario>@wearehackerone.com`. En esta fase pasiva no creo cuentas ni uso el entorno de reservas de prueba.

Otras reglas relevantes:

- **Prohibido en cualquier circunstancia:** ataques físicos, ingeniería social contra empleados o contratistas y ataques de denegación de servicio o de disponibilidad.
- **Cuentas y datos de clientes:** no se pueden comprometer. No accedo a ninguno.
- **Divulgación:** no se pueden publicar detalles de una vulnerabilidad fuera de HackerOne antes de su aprobación. Este trabajo no reporta ni publica vulnerabilidades.
- **Protección legal (safe harbor):** la actividad conforme a la política se considera autorizada. Me ciño a ella.
- **Tequila:** el programa excluye las filtraciones de datos personales entre miembros de una misma empresa de tequila, y los saltos de autorización dentro de una misma empresa de tequila pueden quedar sin recompensa.
- **Contacto del programa:** security@kiwi.com.
- **Si encuentro algo grave:** no lo exploto ni lo copio. Lo anoto en el cuaderno sin el dato sensible y aviso al profesor. El canal del programa para reportarlo sería HackerOne o security@kiwi.com.

## 4. Fichero `scope.txt`

Cada línea es un objetivo. Una línea normal está en alcance y una línea con `!` está fuera de alcance. Las exclusiones (`!`) prevalecen sobre las inclusiones. Los comentarios empiezan por `#`. La ruta `www.kiwi.com/stories` y las dos apps móviles no son hosts, así que van como comentario en `scope.txt` y siguen apareciendo en la sección 1. El fichero completo está en `scope.txt`:

```
# scope.txt · programa: Kiwi.com (https://hackerone.com/kiwicom) · consultado: 2026-10-29
# Linea normal = en alcance · linea con "!" = fuera de alcance · las exclusiones prevalecen sobre las inclusiones

# --- En alcance: dominios ---
www.kiwi.com
jobs.kiwi.com
tequila.kiwi.com
# (las dos siguientes proceden de la descripcion de tequila.kiwi.com)
tequila-api.kiwi.com
api.tequila.kiwi.com
auth.skypicker.com
*.kiwi.com
*.skypicker.com
# raiz: no listado en el programa; solo consultas pasivas a registros publicos (whois, DNS)
kiwi.com
# www.kiwi.com/stories esta en alcance (ruta, ya cubierta por www.kiwi.com)

# --- En alcance pero no son objetivos de red (apps moviles) ---
# com.skypicker.main (Android)
# com.skypicker.Skypicker (iOS)

# --- Fuera de alcance: terceros ---
!*cars.kiwi.com
!status.kiwi.com
!*code.kiwi.com
!*parking.kiwi.com
!rooms.kiwi.com
!retool.skypicker.com
!*learn.kiwi.com
!vacation.kiwi.com
!*ov.kiwi.com
!*sg.kiwi.com
!*._domainkey.kiwi.com
!outbound.intercom.kiwi.com
!email*skypicker.com
!email*kiwi.com
!*_domainkey.skypicker.com
!mail.skypicker.com
!packages.kiwi.com
!nyrujhhu3yuk.nest.skypicker.com
!*citi-sign.kiwi.com
!*.coupons.kiwi.com
!*experiences.kiwi.com
!kiwistore.kiwi.com
!link.kiwi.com
```
