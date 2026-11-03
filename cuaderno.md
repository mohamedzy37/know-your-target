# Cuaderno de trabajo · Know Your Target · Kiwi.com

- **Objetivo:** Kiwi.com · https://hackerone.com/kiwicom · alcance en `alcance.md` y `scope.txt`
- **Inicio:** 29/10/2026
- **Entorno:** Mozilla Firefox sobre Windows 11. Todas las consultas se hacen desde el navegador, sin instalar herramientas locales; por eso no uso `dig`, `subfinder` ni `theHarvester` y los sustituyo por servicios en línea equivalentes: `dig` → nslookup.io y bgp.he.net; `subfinder` → crt.sh y DNSDumpster; `theHarvester` → Hunter.io. La comprobación con Yandex (#011) se hizo en Opera. Resto de servicios usados: who.is, ICANN Lookup, Netcraft, Shodan, urlscan.io y Google (dorks). Si se usa alguna herramienta local, su versión se anota en la entrada correspondiente.
- **Regla de trabajo:** solo técnicas pasivas. Antes de cada acción compruebo el objetivo contra `scope.txt`. Las peticiones directas, si las hay, solo van a hosts en alcance, a un ritmo muy inferior a 2 por segundo.

## Convención

Cada acción es una entrada numerada (#001, #002...) con las cinco anotaciones: cuándo · objetivo (y si está en alcance) · qué hice · qué salió · siguiente paso. El mapa cita estos números para que cada dato sea trazable.

Plantilla:

```
#NNN · AAAA-MM-DD HH:MM (hora local) · objetivo: dominio (en alcance / fuera de alcance)
$ comando exacto
-> resumen de lo que salió
siguiente: qué hago después y por qué
```

---

## Registro

```
#000 · 2026-10-29 20:08 (hora local) · objetivo: hackerone.com/kiwicom (el programa; no es un host)
$ web: https://hackerone.com/kiwicom (política y alcance estructurado; descarga del CSV scopes_for_kiwicom_at_2026-10-29_19_08_21_UTC.csv)
-> Programa público y con recompensas: 9 activos en alcance y 23 exclusiones de terceros. Resultado: alcance.md y scope.txt
siguiente: reconocimiento pasivo del raíz kiwi.com, empezando por el whois para saber quién es el titular antes de mirar el DNS
```

```
#001 · 2026-11-02 10:53 · objetivo: kiwi.com (en alcance; raíz de *.kiwi.com, consulta a registro, sin tráfico al objetivo)
$ web: https://who.is/whois/kiwi.com
-> Registrador MarkMonitor (corporativo); creado 23/11/1994, actualizado 11/03/2026, caduca 21/05/2036; NS: ns-cloud-c1..c4.googledomains.com (Google Cloud DNS); titular oculto por privacidad (solo visible región Central Bohemia, CZ); estados de bloqueo de borrado, transferencia y modificación (protección contra secuestro); IP resuelta por who.is: 151.101.195.42. Datos en caché de who.is del 24/10/2026
siguiente: contrastar con lookup.icann.org; contrastar la IP con nslookup.io en el paso de DNS
```

```
#002 · 2026-11-02 10:54 · objetivo: kiwi.com (en alcance; raíz de *.kiwi.com, consulta RDAP a registro, sin tráfico al objetivo)
$ web: https://lookup.icann.org/en/lookup (búsqueda: kiwi.com; ICANN consulta el RDAP de Verisign y de MarkMonitor)
-> Coincide con #001: registrador Markmonitor Inc. (IANA 292), creado 1994-11-23, actualizado 2026-03-11, 4 NS ns-cloud-c1..c4.googledomains.com, 6 estados de bloqueo (client y server: delete, transfer, update), titular y contactos redactados (solo región Central Bohemia, CZ; contacto por formulario de MarkMonitor). Novedades: DNSSEC sin firmar; caducidad en el registro 2034-05-21 frente a caducidad en el registrador 2036-05-21 (who.is mostraba 2036); ID de dominio 902033_DOMAIN_COM-VRSN. Marca temporal de los datos RDAP: 2026-11-02T09:49:17Z
siguiente: registros DNS (DNSDumpster): el whois solo da el titular y los NS, falta ver a qué IP apunta y qué subdominios hay
```

```
#003 · 2026-11-02 11:04 · objetivo: kiwi.com (en alcance)
$ web: dnsdumpster.com → kiwi.com
-> 196 registros (50 visibles). Hosting: Fastly (casi todo), Google Cloud (3), CloudFront (cars). MX: Google Workspace. NS: ns-cloud-c1..c4 (= whois). SPF: include:tmp-spf.kiwi.com ~all. TXT: verificaciones de 14 servicios (Google, Atlassian, Notion, Microsoft...). 4 fuera de alcance (cars.*, code.*, email.code.*, email.*). El CSV del programa cita Cloudflare y no Fastly
siguiente: saber cuántos subdominios hay
```

```
#004 · 2026-11-02 11:24 · objetivo: kiwi.com (en alcance)
$ web: https://crt.sh/?q=kiwi.com&exclude=expired&group=none (CSV, vigentes)
$ web: https://crt.sh/?q=kiwi.com&group=none (CSV, con caducados)
-> 80 certificados vigentes y 4523 con caducados: 313 hosts concretos y 26 comodines. 48 de los 50 hosts de DNSDumpster salen aquí; los 2 que no salen son dp.kiwi.com y eastmidlandsairport.kiwi.com (los dos en Fastly, 151.101.195.42). En alcance (*.kiwi.com): 281 hosts. Fuera de alcance: 31 (email.* 11, parking.* 3, cars.*, citi-sign.*, code.*, coupons.*, learn.* 2 cada uno, experiences, kiwistore, link, packages, rooms, status, vacation). No cubierto: payments-kiwi.com (otro dominio). hotels, securebooking y hotels-tracker usan certificados de terceros (hotelix.co.il, vio.com). De interés: jira-test, confluence-test, gdpr-data-sandbox, fe.staging, research, mcp-ui-dev
siguiente: ver dónde está de verdad el servidor y compararlo con who.is
```

```
#005 · 2026-11-03 08:15 · objetivo: kiwi.com (en alcance)
$ web: https://www.nslookup.io/domains/kiwi.com/dns-records/ (respuesta del DNS de Cloudflare)
-> 4 registros A: 151.101.131.42, 151.101.3.42, 151.101.195.42 y 151.101.67.42 (revalidación 1 h); sin AAAA ni CNAME. Son las mismas 4 IP de Fastly (ASN 54113) vistas en DNSDumpster, y una es la de who.is (151.101.195.42). Frente a who.is: titular en CZ, DNS en Google Cloud DNS y web en Fastly (ASN de EE. UU.); el servidor real queda oculto tras el CDN. TXT: mismas verificaciones que DNSDumpster (Google x12, Atlassian x2, OpenAI x2, Facebook, DocuSign, Microsoft, Miro, Mixpanel, Notion, Mail.ru)
siguiente: contrastar con otra fuente (bgp.he.net)
```

```
#006 · 2026-11-03 08:19 · objetivo: kiwi.com (en alcance)
$ web: https://bgp.he.net/dns/kiwi.com
-> SOA: NS primario ns-cloud-c1.googledomains.com (coincide con whois), serial 1 y TTL mínimo 300 (valores típicos de Google Cloud DNS). MX: los 5 de Google Workspace con las mismas prioridades que DNSDumpster (aspmx 1, alt1 y alt2 5, alt3 y alt4 10). TXT idénticos a DNSDumpster y nslookup.io (SPF include:tmp-spf.kiwi.com ~all y verificaciones de Google, Atlassian, Microsoft, Facebook, DocuSign, OpenAI, Notion, Mail.ru, Northpass, Cursor y Anthropic); Northpass, Cursor y Anthropic no estaban en las capturas de nslookup.io
siguiente: huella tecnológica (Netcraft): con la IP y los NS ya contrastados, falta saber qué software y qué certificado usa el sitio
```

```
#007 · 2026-11-03 08:52 · objetivo: kiwi.com (en alcance)
$ web: https://sitereport.netcraft.com/?url=https://kiwi.com
-> Hosting: Fastly (EE. UU., AS54113), IP 151.101.67.42 (otra de las 4 de #005), sin IPv6. NS ns-cloud-c1 y registrador MarkMonitor (= whois). Organización: Kiwi.com s.r.o., República Checa (el whois la ocultaba). DNSSEC habilitado. Visto por primera vez en julio de 2016; ranking 380989. Tecnología: Varnish (acelerador HTTP), JavaScript y CSP; sin rastreadores conocidos. TLS: certificado *.kiwi.com de Certainly R1 válido del 27/10 al 26/11/2026, TLS 1.3 con HTTP/2, sin SSLv3 ni Heartbleed. Correo: SPF `include:tmp-spf.kiwi.com ~all` (= #005) y DMARC `p=reject; sp=reject` con informes a dmarc-rua@mailkit.com
siguiente: ficheros expuestos (robots.txt y security.txt) en www.kiwi.com: Netcraft ya dio la tecnología, falta ver qué rutas anuncia el propio sitio y si publica un contacto de seguridad
```

```
#008 · 2026-11-03 09:01 · objetivo: www.kiwi.com (en alcance)
$ web: https://www.kiwi.com/robots.txt
$ web: https://www.kiwi.com/.well-known/security.txt
-> robots.txt: permite expresamente a GPTBot, ChatGPT-User, OAI-SearchBot, PerplexityBot, ClaudeBot y Applebot; al resto les veta (en unas 60 variantes por idioma) /account, /booking, /manage, /payment, /trips, /user, /wishlist y otras, y rutas sin idioma como /api, /invoices, /locations, /logstash, /wadeep, /flights_no_cache, /aggregation_flights, /stream_updates y /additional_action; las rutas sin idioma (/api, /logstash, /wadeep, /invoices, /flights_no_cache...) no parecen de una web pública y sugieren servicios internos; 3 sitemaps (principal, stories y help). security.txt: Contact security@kiwi.com (= política de HackerOne), Policy www.kiwi.com/us/pages/security, Hiring y Bug Bounty hackerone.com/kiwicom; sin Expires ni clave PGP
siguiente: servicios expuestos (Shodan): comprobar si alguna IP enseña algo más que los puertos 80 y 443; las rutas /api y /logstash sugieren servicios internos
```

```
#009 · 2026-11-03 09:10 · objetivo: kiwi.com (en alcance)
$ web: https://www.shodan.io/search?query=kiwi.com
-> 6 resultados y ninguno es de Kiwi (todos terceros, fuera de alcance): 4 de Strapi en Vultr (India, uno con certificado de api.targettours.online), 1 en Aliyun (China) que redirige a qifeng-kiwi.com y 1 IP de UnitedHealth/Optum (EE. UU.) con respuesta de Varnish que redirige a 8648511.kiwi.com. La búsqueda por texto coincide con cualquier respuesta que contenga "kiwi.com"
siguiente: consultar por IP (151.101.195.42 y 34.117.1.154), porque la búsqueda por texto solo devolvió terceros
```

```
#010 · 2026-11-03 17:40 · objetivo: IP de Fastly y Google Cloud (151.101.195.42 y 34.117.1.154), que no están en scope.txt, y www.kiwi.com (en alcance); consulta a Shodan y urlscan; el escaneo de urlscan lo lancé yo y supone una sola visita a www.kiwi.com, host en alcance
$ web: urlscan.io/result/01a1a248-2c2e-74fa-9853-1b6579c26338/ · shodan.io/host/151.101.195.42 · shodan.io/host/34.117.1.154
-> Las dos IP son de terceros y no enseñan nada de Kiwi. 151.101.195.42: Fastly (AS54113), solo puertos 80 y 443, Varnish, errores 500/421 y certificado genérico de Fastly. 34.117.1.154: Google Cloud (AS396982), solo puerto 80 con un 302. urlscan: la home contacta con images.kiwi.com y loglady.kiwi.com, que no salían en crt.sh ni DNSDumpster. Terceros: Forter, Google Tag Manager/Analytics, iPerceptions. CSP con 'unsafe-inline' y 'unsafe-eval'
siguiente: Google dorks sobre hosts en alcance
```

```
#011 · 2026-11-03 18:33 · objetivo: hosts en alcance de *.kiwi.com (consulta a Google y Yandex, sin tráfico a Kiwi)
$ google: site:kiwi.com -site:www.kiwi.com
$ google: site:kiwi.com filetype:pdf
$ google: site:kiwi.com filetype:xlsx OR filetype:docx OR filetype:csv
$ google: site:kiwi.com filetype:log OR filetype:env OR filetype:sql OR filetype:bak
$ google: site:kiwi.com inurl:admin OR inurl:login
$ google: site:kiwi.com inurl:api OR inurl:swagger OR inurl:graphql
$ yandex: site:kiwi.com filetype:pdf (segunda comprobación, 20:40)
-> Google: solo dieron resultados las dos primeras consultas; las otras 4 no devolvieron nada (`ext:pdf` no funcionó, `filetype:pdf` sí). Subdominios indexados: media, jobs (/locations, /teams, /about-us), getapp (/acsms, ficha de la app en Google Play) y public-documents. Todos en alcance y ya vistos en crt.sh, salvo getapp. PDF públicos: 3 versiones de Terms & Conditions (13, 17 y 30 páginas) en public-documents.kiwi.com y el PDF del índice de precios de Navidad en www.kiwi.com. Yandex confirma los PDF de public-documents y añade 4: una plantilla de certificado médico (images.kiwi.com/general/), la guía de marca (images.kiwi.com/content-media/), el aviso de denuncias en inglés y checo (public-documents.kiwi.com/legal/whistleblowing) y un PDF enlazado desde media.kiwi.com. Por los fragmentos, son documentos legales o de marketing, sin datos internos ni personales; no se abrió ninguno
siguiente: correos (Hunter.io): los dorks no mostraron documentos internos ni correos, y falta el patrón de correo corporativo
```

```
#012 · 2026-11-03 18:47 · objetivo: kiwi.com (en alcance; consulta a Hunter.io, sin contacto con nadie)
$ web: https://hunter.io/discover?domains[]=kiwi.com&last_ai_query=kiwi.com (pestañas Email addresses y Technologies)
-> 256 correos indexados: 225 de personas, 21 de cargos directivos y 31 genéricos. Patrón corporativo: nombre.apellido@kiwi.com (el dork `"@kiwi.com" -site:kiwi.com` en Google no devolvió ningún resultado, así que de momento solo lo confirma Hunter.io). No se anotan nombres. Empresa: 501-1000 empleados, sede en Brno (República Checa), fundada en 2012. Tecnologías: AWS y Google Cloud, Go, Python y Rust, PostgreSQL y Redis, HTTP/3, Varnish, HSTS y PayPal. Con #007 y #010 coincide en Varnish, HSTS y Google Cloud
siguiente: opcional (resolver las IP de los subdominios y whois de la IP) y escribir mapa.md
```

```
#013 · 2026-11-03 19:13 · objetivo: jobs, images, tequila, fe-cloudrun y mcp-ui-dev .kiwi.com (en alcance por *.kiwi.com; consulta DNS a fuentes públicas)
$ web: https://bgp.he.net/dns/jobs.kiwi.com
$ web: https://www.nslookup.io/domains/<host>/dns-records/ (images, tequila, fe-cloudrun y mcp-ui-dev)
$ web: dnsdumpster.com → kiwi.com (revisión de los hosts de Google Cloud)
-> jobs, images y tequila resuelven a las mismas 4 IP de Fastly que www (151.101.3.42, .67.42, .131.42 y .195.42; AS54113): están detrás del CDN y no hay ningún origen expuesto. fe-cloudrun y mcp-ui-dev no resuelven desde fuera. El nombre fe-cloudrun sale en un certificado como comodín de subdominios (*.fe-cloudrun.kiwi.com), probablemente Google Cloud Run. Los 3 hosts de Google Cloud de #003: bloomreach-api (34.117.1.154, en alcance) y email.kiwi.com y email.code.kiwi.com (34.102.239.211, certificado de mailgun.org, fuera de alcance); el resto de hosts vistos (code, confluence, craviation, elitetravel, emetebe, bergamolynk, beta-balkan, bluebirdairways) van por Fastly
siguiente: escribir mapa.md
```

