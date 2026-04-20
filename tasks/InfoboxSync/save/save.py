import logging
import json
import os

logger = logging.getLogger(__name__)


def save_data(translated_data: dict, output_dir: str = 'output') -> str:
    """
    Save the translated data to a file.

    Args:
        translated_data (dict): The translated data from the translate stage.
        output_dir (str): Directory to save the data (default: 'output').

    Returns:
        str: Path to the saved file.
    """
    logger.info(f"Starting data save to {output_dir}")
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Generate filename based on page title
        title = translated_data.get('page_title', 'unknown')
        filename = f"{title.replace(' ', '_').lower()}.json"
        filepath = os.path.join(output_dir, filename)

        # Save data as JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Successfully saved data to: {filepath}")
        return filepath
    except Exception as e:
        logger.error(f"Error saving data: {e}")
        raise