"""Flask extensions shared across the application."""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Rate limiting - initialized without app, will be init_app'd later
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
)
