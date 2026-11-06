

# Informe de Reconocimiento Pasivo: kiwi.com

## 1. Registro del Dominio

| Campo | Valor | Fuente |
|-------|-------|--------|
| Dominio | KIWI.COM | `whois_dominio` |
| Fecha de alta | 1994-11-23 | `whois_dominio` |
| Fecha de caducidad | 2034-05-21 | `whois_dominio` |
| Última modificación | 2026-03-11 | `whois_dominio` |
| Registrador | 292 (Google Domains) | `whois_dominio` |
| Nameservers | ns-cloud-c1.googledomains.com, ns-cloud-c2.googledomains.com, ns-cloud-c3.googledomains.com, ns-cloud-c4.googledomains.com | `whois_dominio` |
| Estado | client/server delete/transfer/update prohibited | `whois_dominio` |

## 2. Registros DNS

### A Records (kiwi.com)
| IP | Fuente |
|----|--------|
| 151.101.131.42 | `dns_registros` |
| 151.101.3.42 | `dns_registros` |
| 151.101.67.42 | `dns_registros` |
| 151.101.195.42 | `dns_registros` |

### MX Records
| Prioridad | Servidor | Fuente |
|-----------|----------|--------|
| 1 | aspmx.l.google.com | `dns_registros` |
| 5 | alt1.aspmx.l.google.com | `dns_registros` |
| 5 | alt2.aspmx.l.google.com | `dns_registros` |
| 10 | alt3.aspmx.l.google.com | `dns_registros` |
| 10 | alt4.aspmx.l.google.com | `dns_registros` |

### NS Records
| Servidor | Fuente |
|----------|--------|
| ns-cloud-c1.googledomains.com | `dns_registros` |
| ns-cloud-c2.googledomains.com | `dns_registros` |
| ns-cloud-c3.googledomains.com | `dns_registros` |
| ns-cloud-c4.googledomains.com | `dns_registros` |

### SOA Record
- Primary NS: ns-cloud-c1.googledomains.com
- Admin email: cloud-dns-hostmaster.google.com
- Serial: 1, Refresh: 21600, Retry: 3600, Expire: 259200, TTL mínimo: 300
- Fuente: `dns_registros`

### TXT Records (destacados)
| Registro | Fuente |
|----------|--------|
| `v=spf1 include:tmp-spf.kiwi.com ~all` | `dns_registros` |
| `google-site-verification=8WuGnhoXGME8b34bkWUqln7IPg9ucU3JpeZFJvi4WVg` (+ 10 más) | `dns_registros` |
| `openai-domain-verification=dv-E5LLSHr2yJRP5MeHRlaLLWgd` | `dns_registros` |
| `anthropic-domain-verification-9nr900=LbK3SJq5FI635Wk2tWVNtLel4` | `dns_registros` |
| `atlassian-domain-verification=O9726H3xXjF1zfR1MTE7tbdkryQaI8XPMCmKVVemRwgZpXEoYrOLliFQ/ibdKyHu` | `dns_registros` |
| `mixpanel-domain-verify=29bb57fe-cb98-4303-973a-3e4129155e08` | `dns_registros` |
| `docusign=18596426-6b5b-4624-8d08-ec81dc1fe2fb` | `dns_registros` |
| `facebook-domain-verification=pk4sjaa3xnhejgwe755uyfue1fw2ms` | `dns_registros` |
| `MS=ms94610270` (Microsoft) | `dns_registros` |
| `OSSRH-84018` (Sonatype) | `dns_registros` |
| `cursor-domain-verification-rasqd2=4MhfjN2WFKKIWRSdfdoWGknud` | `dns_registros` |
| `miro-verification=e2124d181e4f29c9f66fd84e0099a2a4e61a2ecb` | `dns_registros` |
| `notion-domain-verification=ywgBxKWtBVKkkPQE8cFCdNHSr4eryF6Ief0G1FJdMoF` | `dns_registros` |
| `northpass-domain-verification=a67d03b1dcc2e0ea289c709f329549e3` | `dns_registros` |
| `mailru-verification: a75f36299595e00a` | `dns_registros` |

## 3. Subdominios (crt.sh)

- **281 subdominios** en alcance autorizado para `kiwi.com`
- Fuente: `subdominios_crtsh`

Subdominios notables dentro del alcance:
- `www.kiwi.com`, `jobs.kiwi.com`, `tequila.kiwi.com`, `tequila-api.kiwi.com`, `api.tequila.kiwi.com`
- `app.kiwi.com`, `assets.kiwi.com`, `docs.kiwi.com`, `graphql.kiwi.com`
- `automation.kiwi.com`, `automation-dev.kiwi.com`
- `jira.kiwi.com`, `confluence.kiwi.com`
- `hackerone.kiwi.com` (implícito por Bug Bounty)
- Múltiples subdominios de partners aéreos (airasia.kiwi.com, flyafrijet.kiwi.com, etc.)
- Subdominios de automatización: `ancillaries.automation.kiwi.com`, `check-in.automation.kiwi.com`

- **skypicker.com**: BLOQUEADO (fuera del alcance como dominio raíz)
- **auth.skypicker.com**: Dentro del alcance (resuelve correctamente)

## 4. Infraestructura IP

Todos los hosts principales resuelven a las mismas 4 IPs detrás de **Fastly CDN**:

| IP | ASN | Organización | País | Tipo | Fuente |
|----|-----|-------------|------|------|--------|
| 151.101.131.42 | AS54113 | Fastly, Inc. | US | CDN/WAF | `infraestructura_ip` |
| 151.101.195.42 | AS54113 | Fastly, Inc. | US | CDN/WAF | `infraestructura_ip` |
| 151.101.3.42 | AS54113 | Fastly, Inc. | US | CDN/WAF | `infraestructura_ip` |
| 151.101.67.42 | AS54113 | Fastly, Inc. | US | CDN/WAF | `infraestructura_ip` |

- Los servidores de origen quedan ocultos tras Fastly
- Prefijos: 151.101.0.0/22, 151.101.64.0/22, 151.101.128.0/22, 151.101.192.0/22

## 5. Servicios Expuestos

Todos los hosts principales expuestos:

| Host | Puertos | Etiquetas | Software | Fuente |
|------|---------|-----------|----------|--------|
| kiwi.com | 80, 443 | cdn, pqc | Varnish Cache, Varnish Cache Plus, Nginx (F5) | `servicios_expuestos` |
| www.kiwi.com | 80, 443 | cdn, pqc | Varnish Cache, Varnish Cache Plus, Nginx (F5) | `servicios_expuestos` |
| tequila.kiwi.com | 80, 443 | cdn, pqc | Varnish Cache, Varnish Cache Plus, Nginx (F5) | `servicios_expuestos` |
| tequila-api.kiwi.com | 80, 443 | cdn, pqc | Varnish Cache, Varnish Cache Plus, Nginx (F5) | `servicios_expuestos` |
| auth.skypicker.com | 80, 443 | cdn, pqc | Varnish Cache, Varnish Cache Plus, Nginx (F5) | `servicios_expuestos` |

- **pqc**: Post-Quantum Cryptography habilitado
- No se detectaron vulnerabilidades conocidas en Shodan

## 6. Huella Tecnológica

### kiwi.com / www.kiwi.com
- **HTTP 200**, redirige a `https://www.kiwi.com/en/`
- **Vía**: Google, Varnish
- **Cache**: cache-mad2200131-MAD, cache-toj-leto2350079-TOJ (Fastly edge servers)
- **HSTS**: `max-age=31536000; includeSubDomains`
- **CSP**: `upgrade-insecure-requests; default-src 'self' https://static.kiwi.com; frame-ancestors 'self' kiwi.com *.kiwi.com skypicker.com *.skypicker.com; script-src 'self' 'unsafe-inline' 'unsafe-eval' blob: h...`
- **Cookies**: SKYPICKER_VISITOR_UNIQID, kw_session_id, kw_user_market
- **Ausente**: x-frame-options
- Fuente: `huella_tecnologica`

### tequila.kiwi.com
- **HTTP 200**
- **HSTS**: `max-age=31536000; includeSubDomains`
- **x-frame-options**: SAMEORIGIN
- **Ausente**: content-security-policy
- Fuente: `huella_tecnologica`

### tequila-api.kiwi.com
- **HTTP 404** (API, no web)
- **Server**: uvicorn (servidor ASGI para Python)
- **HSTS**: `max-age=31536000; includeSubDomains`
- **Ausente**: content-security-policy, x-frame-options
- Fuente: `huella_tecnologica`

### auth.skypicker.com
- **HTTP 404** (API de autenticación)
- **CSP**: `upgrade-insecure-requests; block-all-mixed-content; frame-ancestors 'none'`
- **HSTS**: `max-age=31536000; includeSubDomains`
- **Ausente**: x-frame-options
- Fuente: `huella_tecnologica`

## 7. Ficheros Expuestos

### robots.txt
- **7 user-agents** definidos
- **1309 rutas vetadas**
- Rutas vetadas notables: `/account`, `/api`, `/ag/*` (agregador), `/ae/*`, `/ar/*`, `/aggregation_flights`, `/airlines`
- Fuente: `ficheros_expuestos`

### Sitemaps
- `https://www.kiwi.com/sitemap.xml`
- `https://www.kiwi.com/stories/sitemap.xml`
- `https://www.kiwi.com/help/sitemap.xml`
- Fuente: `ficheros_expuestos`

### security.txt
- **Contact**: security@kiwi.com
- **Policy**: https://www.kiwi.com/us/pages/security
- **Hiring**: https://www.kiwi.com/jobs/
- **Bug Bounty**: https://hackerone.com/kiwicom
- Fuente: `ficheros_expuestos`

## 8. Correos Corporativos

| Buzón genérico | Fuente |
|----------------|--------|
| contact@support.kiwi.com | `correos` |

- El patrón de correo corporativo no se pudo determinar (solo 1 correo genérico encontrado, 0 de personas visibles por privacidad)
- Fuente: `correos`

## 9. Wayback Machine

- **No disponible**: Error HTTP 503 (Service Unavailable) en ambas consultas
- Fuente: `wayback_urls`

---

## Resumen de Hallazgos Clave

1. **Infraestructura unificada**: Todos los hosts principales comparten las mismas 4 IPs de Fastly CDN (AS54113)
2. **Correo**: Google Workspace (MX指向 aspmx.l.google.com)
3. **DNS gestionado por Google Domains**
4. **CDN/WAF**: Fastly con Varnish Cache y soporte PQC (Post-Quantum Cryptography)
5. **Seguridad web**: HSTS con includeSubDomains, CSP presente en web principal y auth.skypicker.com
6. **API tequila**: Servida por uvicorn (Python/ASGI), sin CSP ni x-frame-options
7. **Bug Bounty**: Programa activo en HackerOne (hackerone.com/kiwicom)
8. **Ecosistema amplio**: 281 subdominios detectados, incluyendo partners aéreos, servicios de automatización y herramientas internas (Jira, Confluence)
9. **skypicker.com**: El dominio raíz está fuera del alcance, pero auth.skypicker.com sí está incluido y resuelve correctamente