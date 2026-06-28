def bullet_list(items):
    """Convert a list of strings to markdown bullet list."""
    return "\n".join(f"- {item}" for item in items)
