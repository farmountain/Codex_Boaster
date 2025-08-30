def check_access(user, page):
    # Dummy implementation for testing
    if user is None:
        return {
            "access_granted": False,
            "redirect_url": "/login",
            "warning_logged": True
        }
    return {
        "access_granted": True
    }
