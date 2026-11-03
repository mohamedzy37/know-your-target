# Mapa de superficie · Kiwi.com

## 1. Resumen

Kiwi.com s.r.o. (#007) es una agencia de viajes en línea con sede en Brno (República Checa), fundada en 2012 y con entre 501 y 1000 empleados (#012). Ofrece su plataforma con marcas blancas para otras empresas (#003, `alcance.md`).

Lo que más destaca:
- Casi todo lo comprobado (`www`, `jobs`, `images`, `tequila` y los hosts de marca) resuelve a las mismas 4 IP de Fastly. Son las IP del CDN y no las del servidor real de Kiwi, que no se ha obtenido; no hay ningún origen expuesto directamente (#005, #013).
- El único host en alcance fuera de Fastly es `bloomreach-api.kiwi.com`, en Google Cloud tras un balanceador (#010, #013).
- Hay nombres de entornos de prueba y de desarrollo en los certificados, y rutas internas en el `robots.txt` (#004, #008).
- Los correos siguen el patrón `nombre.apellido@kiwi.com` según Hunter (#012).

## 2. Dominios y subdominios

IP de Fastly: 151.101.3.42, 151.101.67.42, 151.101.131.42 y 151.101.195.42 (AS54113). Son las IP del CDN, detrás del cual se oculta Kiwi: la IP real de su servidor no la conocemos. La tabla recoge los hosts cuya IP se ha visto en el cuaderno y los de interés; el resto de los 281 hosts en alcance está en crt.sh (#004).

| Subdominio | IP | En alcance | Para qué sirve |
|---|---|---|---|
| `kiwi.com` (raíz) | Las 4 de Fastly (#005) | Sí (línea `kiwi.com` de `scope.txt`, solo consultas pasivas) | Dominio principal |
| `www.kiwi.com` | Las 4 de Fastly (#013) | Sí | Web principal de reservas |
| `jobs.kiwi.com` | Las 4 de Fastly (#013) | Sí | Página de empleo (#011) |
| `images.kiwi.com` | Las 4 de Fastly (#013) | Sí | Imágenes que carga la web (#010) |
| `tequila.kiwi.com` | Las 4 de Fastly (#013) | Sí | Plataforma B2B para socios (`alcance.md`) |
| `bloomreach-api.kiwi.com` | 34.117.1.154 (Google Cloud, AS396982) | Sí | API de Bloomreach, de personalización de marketing (#010, #013) |
| `confluence.kiwi.com` | Fastly | Sí | Wiki de Atlassian; resuelve en público (#003, #013) |
| `mcp-ui-dev.kiwi.com` | No resuelve desde fuera | Sí | Entorno de desarrollo visto en certificados (#004, #013) |
| `fe-cloudrun.kiwi.com` | No resuelve; hay comodín `*.fe-cloudrun.kiwi.com` | Sí | Probablemente un front en Google Cloud Run (#013) |
| `craviation`, `elitetravel`, `emetebe`, `bergamolynk`, `beta-balkan`, `bluebirdairways` (`.kiwi.com`) | Fastly (#003) | Sí | Versiones de marca de la web (el programa las llama así) |
| `email.kiwi.com`, `email.code.kiwi.com` | 34.102.239.211 (Google Cloud, certificado de mailgun.org) | **No** (`email*kiwi.com`, `*code.kiwi.com`) | Correo transaccional de Mailgun, tercero (#013) |
| `code.kiwi.com` | Fastly | **No** (`*code.kiwi.com`) | Blog técnico alojado en Medium (`alcance.md`) |
| `cars.kiwi.com` | CloudFront (Amazon) | **No** (`*cars.kiwi.com`) | Alquiler de coches de un tercero (#003) |

En total hay 31 hosts fuera de alcance (#004); en la tabla están los que se han analizado.

**Aviso para la fase activa:** `hotels`, `securebooking` y `hotels-tracker` (`.kiwi.com`) están en alcance según `scope.txt`, porque ningún patrón de exclusión los cubre, pero usan certificados de terceros (#004). Parecen de terceros, así que hay que confirmarlo con el programa antes de tocarlos.

## 3. Infraestructura y servicios

**Registro y DNS**
- Dominio creado el 23/11/1994, registrador MarkMonitor, con bloqueos de borrado, transferencia y modificación; titular oculto (solo se ve Central Bohemia, CZ) (#001, #002).
- DNS en Google Cloud DNS (`ns-cloud-c1` a `c4.googledomains.com`), DNSSEC sin firmar según ICANN (#002) y habilitado según Netcraft (#007); sin confirmar.
- Correo en Google Workspace (5 MX). SPF con `include:tmp-spf.kiwi.com ~all` (#005, #006) y DMARC con `p=reject` (#007).
- Registros TXT de verificación de unos 14 servicios, entre ellos Google, Atlassian, Notion, Microsoft, DocuSign y OpenAI (#005, #006).

**Alojamiento y CDN**
- Fastly (AS54113, EE. UU.): 4 IP del CDN, no del servidor real de Kiwi, cuya IP no conocemos; solo puertos 80 y 443 abiertos, Varnish, certificado genérico de Fastly cuando se consulta por IP (#005, #010).
- Google Cloud: `bloomreach-api` (balanceador, solo puerto 80 con una redirección) (#010).
- Amazon: CloudFront en `cars.*`, que está fuera de alcance (#003).

**Web**
- Varnish como acelerador, HTTP/2 y HTTP/3, TLS 1.3, HSTS, y CSP con `unsafe-inline` y `unsafe-eval` (#007, #010, #012).
- Certificados `*.kiwi.com` de Certainly (válido hasta el 26/11/2026) (#007).
- Terceros en la web: Forter, Google Tag Manager y Analytics, iPerceptions (#010).
- Tecnologías según Hunter (estimación de un tercero): AWS y Google Cloud, Go, Python y Rust, PostgreSQL y Redis (#012).

**Archivos públicos**
- `security.txt`: contacto `security@kiwi.com`, política del programa de HackerOne; sin fecha de caducidad ni clave PGP (#008).
- `robots.txt`: permite a los rastreadores de IA y veta cuentas, reservas, pagos y varias rutas internas (#008).

**Cruce de fuentes**
- Registrador y servidores de nombres coinciden en who.is, ICANN, bgp.he.net y Netcraft (#001, #002, #006, #007).
- Las IP de Fastly coinciden en DNSDumpster, nslookup.io, bgp.he.net, Netcraft, urlscan y Shodan (#003, #005, #006, #007, #010). El CSV del programa habla de Cloudflare, pero ninguna fuente pasiva lo confirma (#003).
- DNSSEC: Netcraft lo marca como habilitado (#007) y ICANN lo da sin firmar (#002). Las dos fuentes no coinciden, así que queda sin confirmar.
- Shodan por texto (`kiwi.com`) solo devolvió terceros, así que se descartó y se consultó por IP (#009, #010).

## 4. Correos y personas

- **Patrón corporativo:** `nombre.apellido@kiwi.com` según Hunter; el dork de Google no dio resultados que lo confirmen (#012).
- **Volumen:** 256 correos indexados en Hunter: 225 de personas, 21 de cargos directivos y 31 genéricos (#012).
- **Contacto de seguridad:** `security@kiwi.com`, publicado en `security.txt` y en la política del programa (#008).
- **DMARC:** los informes van a `dmarc-rua@mailkit.com`, un servicio de terceros (#007).
- **Organización:** Kiwi.com s.r.o., República Checa (#007). Por los registros TXT de verificación, la empresa usa servicios como Atlassian, Notion, Miro, DocuSign, OpenAI, Anthropic, Cursor y Mixpanel (#005, #006).
- **Personas:** no se anotan nombres ni se contacta con nadie. El programa prohíbe la ingeniería social contra empleados y contratistas (`alcance.md`).

## 5. Puntos de interés

Lo que investigaría primero, en este orden. Ordeno por probabilidad de encontrar algo y por impacto: los entornos de prueba son lo más probable y pueden exponer datos personales; las rutas de `robots.txt` son más baratas de comprobar, pero de impacto incierto; tequila exige cuenta y más preparación.

1. **Entornos de prueba y desarrollo.** `jira-test`, `confluence-test`, `gdpr-data-sandbox`, `fe.staging`, `research`, `mcp-ui-dev` y `fe-cloudrun` aparecen en certificados (#004, #013). Los entornos de prueba suelen tener menos controles que producción. `gdpr-data-sandbox` apunta a datos personales, y `confluence.kiwi.com`, que resuelve en público, es la pieza visible de Atlassian (#013). Lo primero sería ver cuáles responden, sin autenticarse y sin tocar datos.
2. **Rutas internas en `robots.txt`.** `/logstash`, `/wadeep`, `/invoices`, `/api` y `/flights_no_cache` no son rutas de una web pública normal (#008). Los nombres sugieren logs, facturas y servicios internos, y `/invoices` apunta a datos de clientes. Se miraría solo si responden, con un máximo de 2 peticiones por segundo y sin acceder a datos de clientes.
3. **`tequila.kiwi.com` y su API.** Es la plataforma B2B con cuentas de socios, más `tequila-api` y `api.tequila` como backend (`alcance.md`, #013). Una API con cuentas de empresas es donde suelen aparecer fallos de control de acceso. El programa excluye las filtraciones de datos entre miembros de una misma empresa de tequila (`alcance.md`) y las pruebas deberían hacerse con una cuenta propia de `@wearehackerone.com`.
