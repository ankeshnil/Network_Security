import re
import socket
import urllib.parse
import whois
import requests
from datetime import datetime
from networksecurity.exception.excetion import NetworkException
import sys
import os

def extract_features(url: str) -> dict:

    # ── helpers ──────────────────────────────────────────────
    def get_domain(url):
        try:
            return urllib.parse.urlparse(url).netloc
        except Exception as e:
            raise NetworkException(e, sys) from e

    def get_scheme(url):
        try:
            return urllib.parse.urlparse(url).scheme
        except Exception as e:
            raise NetworkException(e, sys) from e

    domain = get_domain(url)
    scheme = get_scheme(url)

    # ── 1. having_IP_Address ─────────────────────────────────
    # -1 = has IP, 1 = has domain name
    ip_pattern = re.compile(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|2[0-4]\d|25[0-5])'
        r'|'
        r'(0x[0-9a-fA-F]{1,2}\.){3}(0x[0-9a-fA-F]{1,2})'
    )
    having_IP_Address = -1 if ip_pattern.search(url) else 1

    # ── 2. URL_Length ─────────────────────────────────────────
    # 1 = short (<54), 0 = medium (54–75), -1 = long (>75)
    url_len = len(url)
    if url_len < 54:
        URL_Length = 1
    elif url_len <= 75:
        URL_Length = 0
    else:
        URL_Length = -1
        

    # ── 3. Shortining_Service ─────────────────────────────────
    # -1 = uses shortening service, 1 = does not
    shorteners = r'bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|is\.gd|cli\.gs|' \
                 r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|' \
                 r'su\.pr|twurl\.nl|snipurl\.com|short\.to|BudURL\.com|' \
                 r'ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|' \
                 r'loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|' \
                 r'om\.ly|to\.ly|bit\.do|lnkd\.in|db\.tt|qr\.ae|adf\.ly|' \
                 r'bitly\.com|cur\.lv|ity\.im|q\.gs|po\.st|bc\.vc|twitthis\.com|' \
                 r'u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|prettylinkpro\.com|' \
                 r'scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|' \
                 r'v\.gd|link\.zip\.net'
    Shortining_Service = -1 if re.search(shorteners, url) else 1
    

    # ── 4. having_At_Symbol ───────────────────────────────────
    # -1 = has @, 1 = does not
    having_At_Symbol = -1 if "@" in url else 1

    # ── 5. double_slash_redirecting ───────────────────────────
    # position of "//" after the scheme — if found beyond position 7, suspicious
    # -1 = suspicious redirect, 1 = normal
    pos = url.rfind('//')
    double_slash_redirecting = -1 if pos > 7 else 1

    # ── 6. Prefix_Suffix ──────────────────────────────────────
    # -1 = hyphen in domain, 1 = no hyphen
    Prefix_Suffix = -1 if "-" in domain else 1

    # ── 7. having_Sub_Domain ─────────────────────────────────
    # count dots in domain: 1 dot = 1, 2 dots = 0, 3+ dots = -1
    dot_count = domain.count(".")
    if dot_count == 1:
        having_Sub_Domain = 1
    elif dot_count == 2:
        having_Sub_Domain = 0
    else:
        having_Sub_Domain = -1

    # ── 8. SSLfinal_State ─────────────────────────────────────
    # 1 = HTTPS with valid cert, 0 = HTTPS no cert check, -1 = HTTP
    if scheme == "https":
        try:
            requests.get(url, timeout=3, verify=True)
            SSLfinal_State = 1
        except:
            SSLfinal_State = 0
    else:
        SSLfinal_State = -1

    # ── 9. Domain_registeration_length ───────────────────────
    # 1 = registered > 1 year, -1 = < 1 year or unknown
    try:
        w = whois.whois(domain)
        exp = w.expiration_date
        if isinstance(exp, list):
            exp = exp[0]
        remaining = (exp - datetime.now()).days
        Domain_registeration_length = 1 if remaining > 365 else -1
    except:
        Domain_registeration_length = -1

    # ── 10. Favicon ───────────────────────────────────────────
    # 1 = favicon loaded from same domain, -1 = external domain
    # (simplified: assume same domain if we can't check)
    Favicon = 1

    # ── 11. port ──────────────────────────────────────────────
    # 1 = standard port, -1 = non-standard port present in URL
    parsed_port = urllib.parse.urlparse(url).port
    standard_ports = [80, 443, None]
    port = 1 if parsed_port in standard_ports else -1

    # ── 12. HTTPS_token ───────────────────────────────────────
    # -1 = "https" appears in the domain name itself (fake), 1 = normal
    HTTPS_token = -1 if "https" in domain.lower() else 1

    # ── 13. Request_URL ───────────────────────────────────────
    # % of external objects loaded (images, scripts) from other domains
    # simplified: 1 = safe, -1 = suspicious (we default to 1 without full HTML parse)
    Request_URL = 1

    # ── 14. URL_of_Anchor ─────────────────────────────────────
    # % of anchor tags pointing outside — simplified default
    URL_of_Anchor = 1

    # ── 15. Links_in_tags ─────────────────────────────────────
    # meta/script/link tags with external links — simplified default
    Links_in_tags = 1

    # ── 16. SFH (Server Form Handler) ────────────────────────
    # 0 = empty/about:blank, -1 = external domain, 1 = same domain
    SFH = 0

    # ── 17. Submitting_to_email ───────────────────────────────
    # -1 = form submits to email (mailto:), 1 = does not
    Submitting_to_email = -1 if "mailto:" in url else 1

    # ── 18. Abnormal_URL ──────────────────────────────────────
    # -1 = host name not in URL (abnormal), 1 = normal
    try:
        Abnormal_URL = 1 if domain in url else -1
    except:
        Abnormal_URL = -1

    # ── 19. Redirect ──────────────────────────────────────────
    # 0 = <=1 redirect, 1 = >1 redirect
    try:
        r = requests.get(url, timeout=3, allow_redirects=True)
        Redirect = 0 if len(r.history) <= 1 else 1
    except:
        Redirect = 0

    # ── 20. on_mouseover ──────────────────────────────────────
    # 1 = status bar not changed, -1 = changed (simplified default)
    on_mouseover = 1

    # ── 21. RightClick ────────────────────────────────────────
    # 1 = right click enabled, -1 = disabled (simplified default)
    RightClick = 1

    # ── 22. popUpWidnow ───────────────────────────────────────
    # 1 = no popup, -1 = has popup (simplified default)
    popUpWidnow = 1

    # ── 23. Iframe ────────────────────────────────────────────
    # 1 = no iframe, -1 = has invisible iframe (simplified default)
    Iframe = 1

    # ── 24. age_of_domain ─────────────────────────────────────
    # 1 = domain age > 6 months, -1 = < 6 months or unknown
    try:
        w = whois.whois(domain)
        created = w.creation_date
        if isinstance(created, list):
            created = created[0]
        age_months = (datetime.now() - created).days / 30
        age_of_domain = 1 if age_months >= 6 else -1
    except:
        age_of_domain = -1

    # ── 25. DNSRecord ─────────────────────────────────────────
    # 1 = DNS record found, -1 = not found
    try:
        socket.gethostbyname(domain)
        DNSRecord = 1
    except:
        DNSRecord = -1

    # ── 26. web_traffic ───────────────────────────────────────
    # Alexa rank: 1 = top 100k, 0 = > 100k, -1 = not ranked
    # (Alexa is discontinued — default to 0 / unknown)
    web_traffic = 0

    # ── 27. Page_Rank ─────────────────────────────────────────
    # 1 = page rank > 0.2, -1 = low/zero (simplified default)
    Page_Rank = -1

    # ── 28. Google_Index ──────────────────────────────────────
    # 1 = indexed by Google, -1 = not indexed (simplified default)
    Google_Index = 1

    # ── 29. Links_pointing_to_page ────────────────────────────
    # 1 = many backlinks, 0 = few, -1 = none (simplified default)
    Links_pointing_to_page = 0

    # ── 30. Statistical_report ────────────────────────────────
    # -1 = URL in phishing reports, 1 = not reported (simplified default)
    Statistical_report = 1

    # ── return in exact column order ─────────────────────────
    return {
        "having_IP_Address":          having_IP_Address,
        "URL_Length":                  URL_Length,
        "Shortining_Service":          Shortining_Service,
        "having_At_Symbol":            having_At_Symbol,
        "double_slash_redirecting":    double_slash_redirecting,
        "Prefix_Suffix":               Prefix_Suffix,
        "having_Sub_Domain":           having_Sub_Domain,
        "SSLfinal_State":              SSLfinal_State,
        "Domain_registeration_length": Domain_registeration_length,
        "Favicon":                     Favicon,
        "port":                        port,
        "HTTPS_token":                 HTTPS_token,
        "Request_URL":                 Request_URL,
        "URL_of_Anchor":               URL_of_Anchor,
        "Links_in_tags":               Links_in_tags,
        "SFH":                         SFH,
        "Submitting_to_email":         Submitting_to_email,
        "Abnormal_URL":                Abnormal_URL,
        "Redirect":                    Redirect,
        "on_mouseover":                on_mouseover,
        "RightClick":                  RightClick,
        "popUpWidnow":                 popUpWidnow,
        "Iframe":                      Iframe,
        "age_of_domain":               age_of_domain,
        "DNSRecord":                   DNSRecord,
        "web_traffic":                 web_traffic,
        "Page_Rank":                   Page_Rank,
        "Google_Index":                Google_Index,
        "Links_pointing_to_page":      Links_pointing_to_page,
        "Statistical_report":          Statistical_report,
    }