"""
Publish stage for publishing Arabic templates to Wikipedia.
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class PublishResult:
    """Result of a publish operation."""
    success: bool
    page_title: str
    edit_summary: str
    revision_id: Optional[int] = None
    errors: list = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.metadata is None:
            self.metadata = {}


def publish_arabic_template(translated_data: Dict[str, Any],
                           arabic_page_title: str,
                           edit_summary: str = "تحديث قالب السيرة الذاتية باستخدام InfoboxSync") -> PublishResult:
    """
    Publish an Arabic Wikipedia template to the specified page.

    Args:
        translated_data (Dict[str, Any]): Data from previous stages including 'arabic_template'
        arabic_page_title (str): Title of the Arabic Wikipedia page to publish to
        edit_summary (str): Edit summary for the Wikipedia edit

    Returns:
        PublishResult: Result of the publish operation
    """
    logger.info(f"Starting publish operation for page: {arabic_page_title}")

    try:
        # Check if arabic_template exists in the data
        if 'arabic_template' not in translated_data:
            error_msg = "No arabic_template found in translated_data"
            logger.error(error_msg)
            return PublishResult(
                success=False,
                page_title=arabic_page_title,
                edit_summary=edit_summary,
                errors=[error_msg]
            )

        template_text = translated_data['arabic_template']
        if not template_text or not template_text.strip():
            error_msg = "Arabic template is empty or invalid"
            logger.error(error_msg)
            return PublishResult(
                success=False,
                page_title=arabic_page_title,
                edit_summary=edit_summary,
                errors=[error_msg]
            )

        # Import pywikibot
        try:
            import pywikibot
        except ImportError:
            error_msg = "pywikibot is required for publishing. Install with: pip install pywikibot"
            logger.error(error_msg)
            return PublishResult(
                success=False,
                page_title=arabic_page_title,
                edit_summary=edit_summary,
                errors=[error_msg]
            )

        # Initialize Arabic Wikipedia site
        try:
            site = pywikibot.Site('ar', 'wikipedia')
            logger.info("Connected to Arabic Wikipedia")
        except Exception as e:
            error_msg = f"Failed to connect to Arabic Wikipedia: {e}"
            logger.error(error_msg)
            return PublishResult(
                success=False,
                page_title=arabic_page_title,
                edit_summary=edit_summary,
                errors=[error_msg]
            )

        # Create page object
        try:
            page = pywikibot.Page(site, arabic_page_title)
            logger.info(f"Created page object for: {arabic_page_title}")
        except Exception as e:
            error_msg = f"Failed to create page object: {e}"
            logger.error(error_msg)
            return PublishResult(
                success=False,
                page_title=arabic_page_title,
                edit_summary=edit_summary,
                errors=[error_msg]
            )

        # Check if page exists
        if not page.exists():
            error_msg = f"Page '{arabic_page_title}' does not exist on Arabic Wikipedia"
            logger.error(error_msg)
            return PublishResult(
                success=False,
                page_title=arabic_page_title,
                edit_summary=edit_summary,
                errors=[error_msg]
            )

        # Get current page content
        try:
            current_content = page.text
            logger.info(f"Retrieved current page content (length: {len(current_content)})")
        except Exception as e:
            error_msg = f"Failed to retrieve current page content: {e}"
            logger.error(error_msg)
            return PublishResult(
                success=False,
                page_title=arabic_page_title,
                edit_summary=edit_summary,
                errors=[error_msg]
            )

        # Smart template insertion/replacement using wikitextparser
        try:
            import wikitextparser as wtp

            # Parse the current page content
            parsed_content = wtp.parse(current_content)

            # Find existing infobox templates
            existing_infoboxes = []
            for template in parsed_content.templates:
                template_name = template.name.strip()
                # Check for common Arabic infobox template names
                if any(infobox_name in template_name.lower() for infobox_name in [
                    'صندوق', 'infobox', 'سيرة', 'biography', 'person', 'football'
                ]):
                    existing_infoboxes.append(template)

            if existing_infoboxes:
                # Remove existing infoboxes
                logger.info(f"Found {len(existing_infoboxes)} existing infobox(es), removing them")
                for infobox in existing_infoboxes:
                    # Remove the template from the parsed content
                    infobox.string = ''

                # Clean up empty lines around removed templates
                new_content = str(parsed_content)
                new_content = '\n'.join(line for line in new_content.split('\n') if line.strip() or line == '')

                # Insert new template at the beginning
                final_content = template_text + '\n\n' + new_content.strip()
                logger.info("Replaced existing infobox with new template")
            else:
                # No existing infobox, add template at the beginning
                final_content = template_text + '\n\n' + current_content.strip()
                logger.info("Added new template at the beginning of the page")

            # Set the final content
            page.text = final_content
            logger.info(f"Set new page content (length: {len(final_content)})")

            # Save the page
            page.save(summary=edit_summary, minor=False)
            revision_id = page.latest_revision_id

            logger.info(f"Successfully published template to: {arabic_page_title}")
            logger.info(f"Revision ID: {revision_id}")

            return PublishResult(
                success=True,
                page_title=arabic_page_title,
                edit_summary=edit_summary,
                revision_id=revision_id,
                metadata={
                    'template_length': len(template_text),
                    'site': 'ar.wikipedia.org',
                    'published_at': page.editTime().isoformat() if hasattr(page, 'editTime') else None
                }
            )

        except Exception as e:
            error_msg = f"Failed to save page: {e}"
            logger.error(error_msg)
            return PublishResult(
                success=False,
                page_title=arabic_page_title,
                edit_summary=edit_summary,
                errors=[error_msg]
            )

    except Exception as e:
        error_msg = f"Unexpected error during publish operation: {e}"
        logger.error(error_msg)
        return PublishResult(
            success=False,
            page_title=arabic_page_title,
            edit_summary=edit_summary,
            errors=[error_msg]
        )


def publish_data(translated_data: Dict[str, Any],
                arabic_page_title: str,
                edit_summary: str = "تحديث قالب السيرة الذاتية باستخدام InfoboxSync") -> PublishResult:
    """
    Convenience function to publish translated data to Arabic Wikipedia.

    Args:
        translated_data (Dict[str, Any]): Translated data with arabic_template
        arabic_page_title (str): Arabic page title to publish to
        edit_summary (str): Edit summary for the edit

    Returns:
        PublishResult: Publish operation result
    """
    return publish_arabic_template(translated_data, arabic_page_title, edit_summary)


def validate_publish_data(translated_data: Dict[str, Any], arabic_page_title: str) -> Dict[str, Any]:
    """
    Validate data before publishing.

    Args:
        translated_data (Dict[str, Any]): Data to validate
        arabic_page_title (str): Target page title

    Returns:
        Dict with validation results
    """
    errors = []
    warnings = []

    # Check arabic_template
    if 'arabic_template' not in translated_data:
        errors.append("Missing arabic_template in translated_data")
    elif not translated_data['arabic_template'] or not translated_data['arabic_template'].strip():
        errors.append("arabic_template is empty")
    elif not translated_data['arabic_template'].startswith('{{'):
        warnings.append("Template doesn't start with '{{' - may not be a valid wiki template")

    # Check arabic_page_title
    if not arabic_page_title or not arabic_page_title.strip():
        errors.append("Arabic page title is empty")
    elif len(arabic_page_title) > 255:
        errors.append("Arabic page title is too long (>255 characters)")

    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'arabic_page_title': arabic_page_title,
        'has_template': 'arabic_template' in translated_data
    }