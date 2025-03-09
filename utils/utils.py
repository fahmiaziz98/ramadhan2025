import logging


def convert_to_markdown(data):
    result = ""
    for entry in data["entries"]:
        result += f"**ID:** {entry['id']}\n\n"

        # Access data inside 'fields'
        for field, value in entry['fields'].items():
            result += f"**{field.capitalize()}:** {value}\n\n"

        # Add metadata if present
        if 'metadata' in entry and entry['metadata']:
            result += "**Metadata:**\n"
            for meta_key, meta_value in entry['metadata'].items():
                result += f"- **{meta_key.capitalize()}**: {meta_value}\n"

        result += "\n" + "-" * 50 + "\n\n"
    return result


def setup_logger(level=logging.INFO):
    """ 
    Function to set up a logger with a standard format.

    Args:
        level (int): Logging level, default is logging.INFO.
    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    
    
    ch = logging.StreamHandler()
    ch.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(ch)
    
    return logger