# Comparativa · reconocimiento manual frente al agente · Kiwi.com

- **Trabajo manual:** `mapa.md` y `cuaderno.md` (Parte 1).
- **Agente:** ejecución entregada del 2026-11-06 (`agente/informe.md`, `agente/traza.jsonl` y `agente/traza.log`), con 9 herramientas.
- **Ejecuciones de apoyo:** otras dos ejecuciones del mismo día, citadas como ejemplo de fallos: la ejecución 1 (misma orden) y la del punto 2.5 (con `booking.com` y `cars.kiwi.com`). Sus trazas no se entregan; los fragmentos usados se copian aquí.

Cada afirmación del informe del agente se ha comprobado contra el campo `resultado` de `traza.jsonl`, que guarda la salida completa de cada herramienta.

---

## 1. Comparación (punto 3.1)

### 1.1 Por tipo de dato

| Dato | Lo encontré yo | Lo encontró el agente | ¿Coincide? | Observaciones |
|---|---|---|---|---|
| Fecha de alta y caducidad del dominio | 1994-11-23; caducidad 2034 en el registro y 2036 en el registrador (#001, #002) | 1994-11-23; caducidad 2034-05-21 | Sí | El agente solo usó RDAP, así que no vio la discrepancia entre registro y registrador |
| Registrador | MarkMonitor (IANA 292) (#001, #002) | «292 (Google Domains)» | **No** | Error de interpretación (ver E1) |
| Titular | Kiwi.com s.r.o., República Checa (Netcraft, #007) | No aparece | No | El WHOIS está redactado y el agente no tenía otra fuente |
| Servidores DNS | 4 × `ns-cloud-c*.googledomains.com` (Google Cloud DNS) | Los mismos 4 | Sí | El agente lo llama «Google Domains» (ver E2) |
| Registros A de `kiwi.com` | 4 IP de Fastly (#005) | Las mismas 4 IP | Sí | |
| Correo (MX) | Google Workspace, 5 MX (#006) | Los mismos 5 MX con sus prioridades | Sí | |
| SPF | `include:tmp-spf.kiwi.com ~all` | El mismo | Sí | |
| DMARC | `p=reject; sp=reject` (#007) | No consultado | No | Omisión (ver O1) |
| DNSSEC | Sin firmar según ICANN; habilitado según Netcraft (#002, #007) | No consultado | No | Omisión (ver O1) |
| Verificaciones TXT | ~14 servicios (#005, #006) | 15 servicios, incluido OSSRH (Sonatype) | Sí | El agente añade OSSRH, que yo no anoté |
| Subdominios en alcance | 281 (crt.sh, #004) | 281 | Sí | Pero el agente solo vio 138 nombres (ver O5) |
| Entornos de prueba | `jira-test`, `confluence-test`, `gdpr-data-sandbox`, `fe.staging`, `research`, `mcp-ui-dev` (#004) | Cita `jira`, `confluence` y `automation-dev` | Parcial | Tenía `jira-test` y `gdpr-data-sandbox` en la salida de crt.sh y no los destacó (ver O6) |
| Hosts fuera de Fastly | `bloomreach-api` (Google Cloud), `email.*` (Mailgun), `cars.*` (CloudFront) (#003, #013) | Ninguno | No | Solo resolvió 6 hosts conocidos (ver O2) |
| Infraestructura de las IP | Fastly AS54113, EE. UU., origen oculto (#005, #013) | Lo mismo, con los 4 prefijos /22 | Sí | |
| Servicios expuestos | Puertos 80 y 443, Varnish (#010) | Puertos 80 y 443, Varnish y Nginx (F5) en 5 hosts | Sí | El agente consultó 5 hosts; yo, 2 IP |
| Cabeceras de la web principal | HSTS, CSP con `unsafe-inline` y `unsafe-eval` (#010) | Lo mismo, y además la ausencia de `x-frame-options` | Sí | |
| Backend de `tequila-api` | No lo encontré | `server: uvicorn` (Python/ASGI) | — | Acierto del agente que yo no tenía |
| Cabeceras de `tequila` y `auth.skypicker` | No las miré | `tequila`: sin CSP, con `x-frame-options: SAMEORIGIN`; `auth`: CSP estricta | — | Acierto del agente |
| robots.txt | Rutas vetadas: `/api`, `/logstash`, `/invoices`… (#008) | 7 user-agents, 1309 rutas vetadas, 3 sitemaps | Sí | El agente da números exactos; yo destaqué las rutas internas |
| security.txt | Contact, Policy, Hiring y Bug Bounty (#008) | Los mismos 4 campos | Sí | |
| Patrón de correo | `nombre.apellido@kiwi.com`, 256 correos (Hunter.io, #012) | No determinado; 1 buzón genérico (`contact@support.kiwi.com`) | No | Omisión por fuente pobre (ver O4) |
| Documentos públicos (dorks) | PDF de términos y condiciones en `public-documents` (#011) | No hay herramienta de dorks; la Wayback Machine falló (503) | No | Omisión por falta de herramienta (ver O3) |
| Hosts con certificados de terceros | `hotels`, `securebooking` y `hotels-tracker` (#004, aviso en el mapa) | No los señala | No | En la ejecución del 2.5 incluso presenta `hotels.kiwi.com` como subdominio de Kiwi (ver E3) |

### 1.2 Resumen con números

| Medida | Yo (manual) | Agente (ejecución entregada) |
|---|---|---|
| Técnicas obligatorias cubiertas | 8 de 8 | 7 de 8 (no tiene Google dorks) |
| Fuentes consultadas | 13: who.is, ICANN, DNSDumpster, crt.sh, nslookup.io, bgp.he.net, Netcraft, Shodan, urlscan, Google, Yandex, Hunter.io, robots/security.txt | 9 herramientas, 31 llamadas |
| Subdominios en alcance | 281 | 281 (solo vio 138 nombres) |
| Hosts resueltos y analizados | 13 filas en el mapa, con 3 infraestructuras distintas | 7 hosts, todos en Fastly |
| Datos que coinciden | — | 13 de los 23 datos de la tabla 1.1 |
| Datos que solo encontró el agente | — | 3 (uvicorn en `tequila-api`, cabeceras de `tequila` y `auth`, OSSRH) |
| Datos que solo encontré yo | 9 | — |
| Errores e invenciones en el informe | — | 2 errores y 1 invención (sección 2) |
| Tiempo | Unas 3,5 horas de reconocimiento en 3 sesiones (#001 a #013), sin contar el alcance ni el mapa | 245 segundos (unos 4 minutos) |
| Coste | Ninguno (servicios gratuitos) | 60.199 tokens de entrada y 5.790 de salida (IA del aula, sin importe en euros) |
| Coste de las 4 ejecuciones del día | — | 228.515 tokens de entrada y 22.869 de salida |

---

## 2. Los fallos del agente (punto 3.2)

### Omisiones

| # | Fallo | Ejemplo de la traza | Por qué |
|---|---|---|---|
| O1 | No consultó DMARC ni DNSSEC | En las 31 llamadas no hay ninguna a `_dmarc.kiwi.com` ni sobre DNSSEC | `dns_registros` podía pedir el TXT de `_dmarc.kiwi.com`, pero el modelo no lo pensó. Ni el prompt ni la descripción de la herramienta lo mencionan |
| O2 | No encontró los hosts fuera de Fastly (`bloomreach-api`, `email.*`) | Solo resolvió `www`, `jobs`, `tequila`, `tequila-api`, `api.tequila` y `auth.skypicker` (líneas 17-28 de `traza.log`), los mismos nombres que aparecen en `scope.txt` | Resolvió los hosts que ya conocía por el prompt en lugar de elegirlos de la lista de crt.sh |
| O3 | No buscó documentos públicos | No existe herramienta de dorks; `wayback_urls` devolvió dos veces `ERROR: … HTTP Error 503` (líneas 53-54 y 63-64) | Falta de herramienta: Google no permite consultas automatizadas sin clave de pago |
| O4 | No dedujo el patrón de correo | `correos` → `1 correos de kiwi.com: 1 genéricos y 0 de personas` (línea 56) | Fuente pobre: theHarvester con buscadores gratuitos frente a los 256 correos de Hunter.io |
| O5 | Solo vio la mitad de los subdominios | La salida de `subdominios_crtsh` termina en `jobs.kiwi.c [... recortado: 3148 caracteres más]`: el modelo recibió 138 de los 281 nombres, por orden alfabético hasta la «j» | Diseño de la herramienta: `recortar()` corta a 3.000 caracteres. Todo lo que empieza por k-z (`mcp-ui-dev`, `public-documents`, `research`, `tequila`…) no le llegó |
| O6 | No destacó los entornos de prueba | `jira-test`, `confluence-test` y `gdpr-data-sandbox` estaban en la parte de la salida de crt.sh que sí recibió, pero el informe solo cita `jira`, `confluence` y `automation-dev` | Interpretación: el prompt pide datos, no priorizar qué es interesante para la fase activa |

### Errores

| # | Fallo | Ejemplo de la traza | Por qué |
|---|---|---|---|
| E1 | Registrador: «292 (Google Domains)» | `whois_dominio` devolvió `Entidad (registrar): 292` (línea 4; completa en `traza.jsonl`). 292 es el identificador IANA de **MarkMonitor** (#002 del cuaderno) | El modelo mezcló el número con los NS (`googledomains.com`) que venían justo debajo. La herramienta dio un dato ambiguo, porque el WHOIS por el puerto 43 falló y se usó RDAP, que solo trae el número |
| E2 | «DNS gestionado por Google Domains» | El SOA dice `cloud-dns-hostmaster.google.com` (línea 62): es **Google Cloud DNS** | Deducción por el nombre de los NS, sin contrastar con el SOA que él mismo pidió |
| E3 | Presenta como de Kiwi hosts de terceros | Informe del 2.5: «Otros: … hotels.kiwi.com, …» | En el trabajo manual vi que `hotels` usa certificados de otras empresas (#004). El agente no mira los certificados, solo los nombres |
| E4 | Caracteres en chino en el informe | Resumen, punto 2: «Google Workspace (MX指向 aspmx.l.google.com)» («MX apunta a») | Fallo de generación del modelo; no viene de ninguna herramienta |

### Invenciones

| # | Fallo | Ejemplo de la traza | Por qué |
|---|---|---|---|
| I1 | `hackerone.kiwi.com (implícito por Bug Bounty)` en la lista de subdominios | El nombre no aparece en la salida de `subdominios_crtsh` (comprobado en `traza.jsonl`) | El modelo lo dedujo de que existe un programa en HackerOne, aunque el prompt dice «si no tienes una herramienta que respalde un dato, no lo incluyas». Él mismo lo marca como «implícito» |
| I2 | En el 2.5, «BLOQUEADO en todas las herramientas» para `booking.com` y `cars.kiwi.com` | La traza muestra solo 2 herramientas por dominio: `whois_dominio` y `dns_registros` (líneas 5-14) | Exageración: generaliza a partir de dos bloqueos |
| I3 | «pqc: Post-Quantum Cryptography habilitado» | `servicios_expuestos` solo devolvió la etiqueta `pqc` | La explicación viene del conocimiento del modelo, no de la herramienta. Probablemente es cierta, pero no está respaldada |

### Intentos fuera de alcance

| # | Objetivo | Ejemplo de la traza | Reacción |
|---|---|---|---|
| F1 | `skypicker.com` (raíz, no autorizada) | Ejecución entregada: `subdominios_crtsh({"dominio": "skypicker.com"}) [BLOQUEADO]` (línea 15) | Una sola llamada; luego siguió con `kiwi.com` |
| F2 | `skypicker.com` en la ejecución 1 | 6 llamadas con 4 herramientas: `whois_dominio`, `dns_registros` (A, MX y TXT), `ficheros_expuestos` y `correos` (líneas 57-68) | **Insistió por otros caminos**, pese a que el prompt dice «no insistas ni lo intentes por otro camino». El scope-guard las bloqueó todas |
| F3 | `booking.com` y `cars.kiwi.com` (punto 2.5) | `whois_dominio` y `dns_registros` con cada uno, los 4 BLOQUEADO (líneas 5-14) | Probó una segunda herramienta con cada uno y después paró |

---

## 3. Reflexión (punto 3.3)

### ¿Qué hizo mejor el agente y qué hice mejor yo?

El agente fue mucho más rápido: unos 4 minutos frente a unas 3,5 horas. Además, fue más sistemático con los hosts que eligió: miró las cabeceras de 5 hosts y encontró cosas que yo no busqué, como el `server: uvicorn` de `tequila-api` (un backend en Python) o que `tequila.kiwi.com` no tiene CSP. También es muy constante citando la herramienta de cada dato, que es justo lo que pide el prompt.

Yo fui mejor en todo lo que exige **contrastar e interpretar**. Comparé fuentes (who.is frente a ICANN, Netcraft frente a ICANN para DNSSEC), saqué el titular real con Netcraft, encontré los hosts que se salen de Fastly (`bloomreach-api` en Google Cloud, `email.*` en Mailgun) y detecté que `hotels` usa certificados de terceros. Y, sobre todo, prioricé: mis puntos de interés (entornos de prueba, rutas internas de robots.txt, tequila) son una propuesta para la fase activa. El informe del agente es una lista de datos, no un plan.

### ¿Por qué falló donde falló?

Casi ningún fallo es "culpa del modelo" en abstracto; la mayoría tienen una causa concreta:

- **Faltaba una herramienta o una fuente:** dorks (O3), patrón de correo (O4) y titular (sin Netcraft). Con Hunter.io y una clave, el agente habría encontrado el patrón.
- **El diseño de mis herramientas le limitó:** el recorte a 3.000 caracteres hizo que viera solo 138 de 281 subdominios (O5). Para crt.sh hace falta otra estrategia: devolver el recuento y los nombres *interesantes* (test, dev, staging, admin) en lugar de los primeros por orden alfabético.
- **El prompt era ambiguo o incompleto:** no dice que la raíz `skypicker.com` está excluida (solo la lista), así que el modelo la deduce de `*.skypicker.com` y la intenta en todas las ejecuciones (F1-F3). Tampoco pide DMARC ni DNSSEC (O1), ni priorizar para la fase activa (O6).
- **El modelo interpretó mal una salida:** el registrador «292» (E1) es un dato ambiguo que el modelo completó con lo que tenía al lado. La herramienta debería devolver el nombre del registrador y no solo su identificador.
- **El modelo no obedece del todo al prompt:** pese a «no insistas», en la ejecución 1 intentó `skypicker.com` con 4 herramientas (F2), y pese a «no incluyas datos sin respaldo», añadió `hackerone.kiwi.com` (I1). El scope-guard es lo que realmente impide salirse del alcance; el prompt solo lo reduce.

### ¿Me fiaría del informe del agente sin revisarlo?

No. Me sirve como **primer barrido rápido**: en 4 minutos da una base correcta en DNS, infraestructura, cabeceras y ficheros expuestos, y alguna pista que yo no tenía. Pero en un solo informe hay un error en un dato básico (el registrador), una invención (`hackerone.kiwi.com`) y una omisión grave (medio listado de subdominios) que el propio informe no avisa: dice «281 subdominios» como si los hubiera visto todos.

Lo que comprobaría siempre:

1. **Cada dato contra la traza**, no contra el informe: que el valor aparezca en el `resultado` de la herramienta citada.
2. **Las salidas recortadas** (`[... recortado …]`), porque el modelo trabaja con lo que ve, no con lo que existe.
3. **Los nombres y la propiedad de los activos**: quién es el registrador, de quién son las IP y si un subdominio es de verdad de la empresa o de un tercero, antes de tocarlo en la fase activa.
4. **Los bloqueos de la traza**: si el agente intentó salir del alcance y por cuántos caminos.
5. **Lo que no aparece**: si una técnica no tiene herramienta o una fuente falló, el informe no lo destaca. Hay que contrastarlo con la lista de técnicas obligatorias.
