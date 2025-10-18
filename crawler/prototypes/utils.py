import urllib


def is_valid_url(url) -> bool:
    """Check if the given URL is valid."""
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_url_domain(url: str) -> str:
    """Extract the domain from a given URL."""
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url.netloc
