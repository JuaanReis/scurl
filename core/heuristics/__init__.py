from core.heuristics.html import external_script, favicon_check, form_action, hidden_fields, image_check
from core.heuristics.server import domain_age
from core.heuristics.url import character
from core.heuristics.url import parts
from core.heuristics.html import redirect_check
from core.heuristics.server import rdap_field
from core.heuristics.server.dns_verify import dns_verify
from core.heuristics.server.ssl_verify import ssl_verify
from core.heuristics.html import password_input
from core.heuristics.server import nameserver_diversity
from core.heuristics.url import domain