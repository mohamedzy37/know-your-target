"""Herramientas iniciales de reconocimiento. AQUÍ PUEDES AÑADIR LAS TUYAS.

WHOIS (whois.py), DNS y crt.sh ya están implementadas y activas en lanzar.py.
DNS y crt.sh proceden de la solución del profesor (herramientas/recon.py).

Para ampliar: una tarea por función, @protegida, sin shell, con timeout,
salida recortada, errores como texto y resultados filtrados por el alcance.
Importa tu nueva función en lanzar.py y añádela a HERRAMIENTAS.

Ideas: subdominios_subfinder, wayback_urls, correos (theHarvester / hunter.io),
infraestructura_ip, correo_postura (SPF/DMARC/MTA-STS/CAA), urlscan, shodan_host.
"""

import ipaddress
import json
import subprocess
import urllib.parse
import urllib.request

from guard import protegida, filtrar
from whois import recortar

UA = "aap-recon/1.0 (educativo; IES Rafael Alberti)"
TIPOS_DNS = {"A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"}


def _http(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


@protegida(objetivo="dominio")
def dns_registros(dominio: str, tipo: str = "A") -> str:
    """Consulta registros DNS de un dominio. tipo: A, AAAA, MX, NS, TXT, CNAME o SOA.
    Devuelve los valores, uno por línea."""
    tipo = tipo.upper()
    if tipo not in TIPOS_DNS:
        return f"ERROR: tipo DNS no válido ({tipo}). Usa uno de: {', '.join(sorted(TIPOS_DNS))}."
    try:
        r = subprocess.run(["dig", "+short", tipo, dominio],
                           capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        return "ERROR: dig no respondió en 20 segundos."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar dig: {e}")
    if r.returncode != 0:
        return recortar(f"ERROR: dig falló ({r.returncode}): {r.stderr.strip() or 'sin detalles'}")
    salida = recortar(r.stdout.strip())
    return salida or f"Sin registros {tipo} para {dominio}."


@protegida(objetivo="dominio")
def subdominios_crtsh(dominio: str) -> str:
    """Enumera subdominios de un dominio por transparencia de certificados (crt.sh).
    Pasivo: no toca el objetivo. Devuelve solo los subdominios dentro del alcance."""
    url = f"https://crt.sh/?q=%25.{urllib.parse.quote(dominio)}&output=json"
    try:
        datos = json.loads(_http(url, timeout=90))
    except Exception as e:
        return (f"ERROR: crt.sh no respondió ({e}). crt.sh suele ir lento; "
                "puedes reintentar más tarde o añadir otra fuente de subdominios.")
    if not isinstance(datos, list) or any(
        not isinstance(fila, dict) or not isinstance(fila.get("name_value"), str)
        for fila in datos
    ):
        return "ERROR: crt.sh devolvió un formato de certificados inesperado."
    nombres = set()
    for fila in datos:
        for n in str(fila.get("name_value", "")).splitlines():
            n = n.strip().lstrip("*.").lower()
            if n:
                nombres.add(n)
    dentro, fuera = filtrar(sorted(nombres))
    cab = f"{len(dentro)} subdominios en alcance ({fuera} filtrados por estar fuera):\n"
    return recortar(cab + "\n".join(dentro))



@protegida(objetivo="dominio")
def servicios_expuestos(dominio: str) -> str:
    """Puertos, software y vulnerabilidades de las IP de un dominio (Shodan InternetDB, pasivo).
    Puertos, etiquetas y vulnerabilidades conocidas de las IP de un dominio según
    Shodan InternetDB. Pasivo: consulta a Shodan, no al objetivo. Ojo: las IP pueden
    ser de un CDN compartido y no del propio objetivo."""
    try:
        r = subprocess.run(["dig", "+short", "A", dominio],
                           capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired:
        return "ERROR: dig no respondió en 20 segundos."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar dig: {e}")
    ips = []
    for valor in r.stdout.split():
        try:
            ips.append(str(ipaddress.IPv4Address(valor)))
        except ValueError:
            pass  # líneas CNAME u otras que no son IP
    if not ips:
        return f"{dominio} no resuelve a ninguna IPv4."
    lineas = [f"{dominio} resuelve a {len(ips)} IP (se consultan como máximo 5):"]
    for ip in ips[:5]:
        try:
            d = json.loads(_http(f"https://internetdb.shodan.io/{ip}", timeout=20))
        except Exception as e:
            if getattr(e, "code", None) == 404:
                lineas.append(f"{ip}: sin datos en InternetDB")
            else:
                lineas.append(f"{ip}: ERROR al consultar InternetDB ({e})")
            continue
        puertos = ", ".join(str(p) for p in d.get("ports", [])) or "ninguno"
        lineas.append(f"{ip}: puertos {puertos}")
        if d.get("tags"):
            lineas.append(f"  etiquetas: {', '.join(d['tags'])}")
        if d.get("cpes"):
            lineas.append(f"  software: {', '.join(d['cpes'][:10])}")
        if d.get("vulns"):
            lineas.append(f"  vulnerabilidades conocidas: {len(d['vulns'])} "
                          f"(p. ej. {', '.join(d['vulns'][:5])})")
        dentro, fuera = filtrar(sorted(d.get("hostnames", [])))
        if dentro:
            lineas.append(f"  hostnames en alcance: {', '.join(dentro[:10])}")
        if fuera:
            lineas.append(f"  ({fuera} hostnames filtrados por estar fuera de alcance)")
    return recortar("\n".join(lineas))


@protegida(objetivo="dominio")
def ficheros_expuestos(dominio: str) -> str:
    """Rutas vetadas de robots.txt, sitemaps y contacto de security.txt de un dominio (2 peticiones).
    Lee robots.txt y /.well-known/security.txt de un dominio. Devuelve las rutas
    que el dueño veta a los buscadores, los sitemaps y los campos de security.txt.
    Hace solo 2 peticiones al objetivo, con una pausa entre ellas."""
    import time  # pausa entre peticiones (límite de 2 por segundo del programa)
    lineas = []

    # --- robots.txt ---
    try:
        robots = _http(f"https://{dominio}/robots.txt", timeout=20)
    except Exception as e:
        if getattr(e, "code", None) == 404:
            lineas.append("robots.txt: no existe (404)")
        else:
            lineas.append(f"robots.txt: ERROR al descargarlo ({e})")
        robots = ""
    if robots:
        agentes, vetadas, sitemaps = set(), set(), []
        for linea in robots.splitlines():
            l = linea.split("#", 1)[0].strip()
            if ":" not in l:
                continue
            clave, valor = (p.strip() for p in l.split(":", 1))
            clave = clave.lower()
            if clave == "user-agent":
                agentes.add(valor)
            elif clave == "disallow" and valor:
                vetadas.add(valor)
            elif clave == "sitemap":
                sitemaps.append(valor)
        lineas.append(f"robots.txt: {len(agentes)} user-agents, {len(vetadas)} rutas vetadas")
        if vetadas:
            muestra = sorted(vetadas)[:40]
            lineas.append("  rutas vetadas (máx. 40): " + ", ".join(muestra))
        hosts = sorted({urllib.parse.urlparse(s).hostname or "" for s in sitemaps} - {""})
        dentro, fuera = filtrar(hosts)
        for s in sitemaps:
            if urllib.parse.urlparse(s).hostname in dentro:
                lineas.append(f"  sitemap: {s}")
        if fuera:
            lineas.append(f"  ({fuera} hosts de sitemaps filtrados por estar fuera de alcance)")

    time.sleep(0.6)

    # --- security.txt ---
    try:
        sec = _http(f"https://{dominio}/.well-known/security.txt", timeout=20)
    except Exception as e:
        if getattr(e, "code", None) == 404:
            lineas.append("security.txt: no existe (404)")
        else:
            lineas.append(f"security.txt: ERROR al descargarlo ({e})")
        sec = ""
    if sec:
        if "<html" in sec.lower():
            lineas.append("security.txt: la URL devuelve una página HTML, no un security.txt")
        else:
            campos = [l.strip() for l in sec.splitlines()
                      if l.strip() and not l.strip().startswith("#")]
            lineas.append(f"security.txt: {len(campos)} campos")
            lineas.extend(f"  {c}" for c in campos[:20])

    return recortar("\n".join(lineas))


# ===================== Más herramientas =====================
import re

_CDN = ("fastly", "cloudflare", "akamai", "amazon", "cloudfront", "google",
        "microsoft", "azure", "incapsula", "imperva", "sucuri", "edgecast", "stackpath")


def _dig(*args: str) -> list:
    """dig +short sin shell y con timeout. Devuelve las líneas; lanza excepción si falla."""
    r = subprocess.run(["dig", "+short", *args], capture_output=True, text=True, timeout=20)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200] or f"dig devolvió {r.returncode}")
    return [l.strip().strip('"') for l in r.stdout.splitlines() if l.strip()]


def _ipv4(dominio: str) -> list:
    ips = []
    for v in _dig("A", dominio):
        try:
            ips.append(str(ipaddress.IPv4Address(v)))
        except ValueError:
            pass
    return ips


@protegida(objetivo="dominio")
def infraestructura_ip(dominio: str) -> str:
    """Dueño de las IP de un dominio (ASN, organización, país) y si están tras un CDN o WAF.
    Resuelve un dominio y dice de quién son sus IP (ASN, organización, prefijo y país,
    vía DNS de Team Cymru). Indica si parece CDN/WAF o servidor expuesto. Pasivo."""
    try:
        ips = _ipv4(dominio)
    except subprocess.TimeoutExpired:
        return "ERROR: dig no respondió en 20 segundos."
    except Exception as e:
        return recortar(f"ERROR: no se pudo resolver {dominio}: {e}")
    if not ips:
        return f"{dominio} no resuelve a ninguna IPv4."
    lineas = [f"{dominio} resuelve a {len(ips)} IP (se analizan como máximo 5):"]
    for ip in ips[:5]:
        try:
            inverso = ".".join(reversed(ip.split(".")))
            origen = _dig("TXT", f"{inverso}.origin.asn.cymru.com")
            if not origen:
                lineas.append(f"{ip}: sin datos de ASN")
                continue
            asn, prefijo, pais = [p.strip() for p in origen[0].split("|")[:3]]
            asn = asn.split()[0]
            info = _dig("TXT", f"AS{asn}.asn.cymru.com")
            org = info[0].split("|")[-1].strip() if info else "desconocida"
        except Exception as e:
            lineas.append(f"{ip}: ERROR al consultar el ASN ({e})")
            continue
        if any(c in org.lower() for c in _CDN):
            tipo = "CDN/WAF o nube: el servidor de origen queda oculto"
        else:
            tipo = "posible servidor propio o hosting directo"
        lineas.append(f"{ip}: AS{asn} {org} · prefijo {prefijo} · país {pais} · {tipo}")
    return recortar("\n".join(lineas))


_CABECERAS = ("server", "via", "x-served-by", "x-cache", "x-powered-by", "x-aspnet-version",
              "x-generator", "cf-ray", "x-amz-cf-id", "strict-transport-security",
              "content-security-policy", "x-frame-options", "set-cookie")


@protegida(objetivo="dominio")
def huella_tecnologica(dominio: str) -> str:
    """Servidor, CDN y cabeceras de seguridad de la web de un dominio (1 petición HTTP).
    Huella tecnológica de la web de un dominio por sus cabeceras HTTP: servidor, CDN,
    caché, frameworks y cabeceras de seguridad. Hace 1 sola petición."""
    req = urllib.request.Request(f"https://{dominio}/", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            estado, final, cab = r.status, r.geturl(), r.headers
    except urllib.error.HTTPError as e:
        estado, final, cab = e.code, e.geturl(), e.headers
    except Exception as e:
        return recortar(f"ERROR: no se pudo conectar con https://{dominio}/ ({e})")
    host_final = urllib.parse.urlparse(final).hostname or dominio
    dentro, _ = filtrar([host_final])
    if not dentro:
        return f"{dominio} redirige a {host_final}, fuera de alcance: no se muestran sus datos."
    lineas = [f"https://{dominio}/ -> HTTP {estado}, URL final {final}"]
    for nombre in _CABECERAS:
        for v in (cab.get_all(nombre) or [])[:3]:
            if nombre == "set-cookie":
                v = v.split("=", 1)[0] + "=(valor oculto)"
            lineas.append(f"  {nombre}: {v[:200]}")
    faltan = [c for c in ("strict-transport-security", "content-security-policy",
                          "x-frame-options") if not cab.get(c)]
    if faltan:
        lineas.append("  cabeceras de seguridad ausentes: " + ", ".join(faltan))
    return recortar("\n".join(lineas))


_INTERES = re.compile(
    r"\.(pdf|docx?|xlsx?|csv|sql|bak|old|env|log|zip|tar|gz|json|xml|conf|cfg|ini|txt)(\?|$)"
    r"|admin|login|api|swagger|graphql|internal|backup|debug|test|staging|dev", re.I)


@protegida(objetivo="dominio")
def wayback_urls(dominio: str) -> str:
    """Documentos y rutas de interés archivados de un dominio en la Wayback Machine (pasivo).
    URL históricas de un dominio en la Wayback Machine (archive.org). Destaca
    documentos, ficheros de configuración y rutas de interés. Pasivo."""
    url = ("https://web.archive.org/cdx/search/cdx?url=" + urllib.parse.quote(dominio)
           + "/*&output=json&fl=original&collapse=urlkey&limit=2000")
    try:
        datos = json.loads(_http(url, timeout=90) or "[]")
    except Exception as e:
        return recortar(f"ERROR: la Wayback Machine no respondió ({e}). Reintenta más tarde.")
    urls = [fila[0] for fila in datos[1:] if fila]  # la fila 0 es la cabecera
    if not urls:
        return f"La Wayback Machine no tiene URL archivadas de {dominio}."
    hosts = sorted({urllib.parse.urlparse(u).hostname or "" for u in urls} - {""})
    dentro, fuera = filtrar(hosts)
    permitidos = set(dentro)
    urls = [u for u in urls if urllib.parse.urlparse(u).hostname in permitidos]
    interes = [u for u in urls if _INTERES.search(u)]
    lineas = [f"{len(urls)} URL archivadas en alcance ({fuera} hosts filtrados por estar "
              f"fuera); {len(interes)} de interés (máx. 40):"]
    lineas += interes[:40]
    return recortar("\n".join(lineas))


_GENERICOS = {"info", "contact", "contacto", "security", "support", "help", "press", "media",
              "jobs", "careers", "hr", "privacy", "legal", "dpo", "abuse", "admin", "sales",
              "partners", "marketing", "noreply", "no-reply", "hello", "team", "office"}


@protegida(objetivo="dominio")
def correos(dominio: str) -> str:
    """Patrón de correo corporativo y buzones genéricos de un dominio (theHarvester, pasivo).
    Busca correos del dominio con theHarvester (fuentes pasivas) y deduce el patrón
    corporativo. Por privacidad no devuelve correos de personas: solo el patrón,
    los recuentos y los buzones genéricos (security@, press@...)."""
    try:
        r = subprocess.run(["theHarvester", "-d", dominio, "-b", "duckduckgo,yahoo,baidu",
                            "-l", "200"], capture_output=True, text=True, timeout=240)
    except subprocess.TimeoutExpired:
        return "ERROR: theHarvester no terminó en 4 minutos."
    except OSError as e:
        return recortar(f"ERROR: no se pudo ejecutar theHarvester: {e}")
    texto = (r.stdout + "\n" + r.stderr).lower()
    patron = r"[a-z0-9._%+-]+@(?:[a-z0-9-]+\.)*" + re.escape(dominio.lower())
    encontrados = set(re.findall(patron, texto))
    if not encontrados:
        detalle = r.stderr.strip()[:200] if r.returncode else ""
        return recortar(f"theHarvester no encontró correos de {dominio}. {detalle}")
    tipos = {"nombre.apellido": 0, "una sola palabra": 0, "otros": 0}
    genericos = []
    for c in sorted(encontrados):
        local = c.split("@", 1)[0]
        if local in _GENERICOS:
            genericos.append(c)
        elif re.fullmatch(r"[a-z]+\.[a-z]+", local):
            tipos["nombre.apellido"] += 1
        elif re.fullmatch(r"[a-z]+", local):
            tipos["una sola palabra"] += 1
        else:
            tipos["otros"] += 1
    personales = sum(tipos.values())
    lineas = [f"{len(encontrados)} correos de {dominio}: {len(genericos)} genéricos y "
              f"{personales} de personas (no se muestran)."]
    if personales:
        mayor = max(tipos, key=tipos.get)
        lineas.append(f"Patrón más probable: {mayor}@{dominio} ({tipos[mayor]} de {personales}).")
        lineas.append("Reparto: " + ", ".join(f"{k}: {v}" for k, v in tipos.items()))
    if genericos:
        lineas.append("Buzones genéricos: " + ", ".join(genericos[:20]))
    return recortar("\n".join(lineas))
