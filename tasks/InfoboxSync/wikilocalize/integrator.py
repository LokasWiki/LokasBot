"""
Integration functions for embedding wiki localization into the InfoboxSync pipeline.
"""

import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from tasks.InfoboxSync.wikilocalize.wikilocalize import WikiLocalizeResult, WikiLocalizer

logger = logging.getLogger(__name__)


@dataclass
class LocalizationProcessingResult:
    """Result of localization processing in the pipeline."""
    success: bool
    localized_data: Dict[str, Any]
    localization_info: WikiLocalizeResult
    processing_time: float
    errors: list = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []


def process_construct_to_publish(
    construct_result: Dict[str, Any],
    enable_local_link_replacement: bool = True,
    enable_template_localization: bool = True
) -> LocalizationProcessingResult:
    """
    Process data from construct stage through wiki localization for publishing.

    This function sits between construct and publish stages, taking the
    constructed Arabic template and localizing any English wiki links
    and templates to their Arabic equivalents.

    Args:
        construct_result (Dict[str, Any]): Data from construct stage containing 'arabic_template'
        enable_local_link_replacement (bool): Whether to replace English wiki links with Arabic
        enable_template_localization (bool): Whether to localize template names

    Returns:
        LocalizationProcessingResult: Processed data ready for publishing
    """
    import time
    start_time = time.time()

    logger.info("Starting wiki localization processing")

    try:
        # Check if we have the required input
        if 'arabic_template' not in construct_result:
            error_msg = "No arabic_template found in construct_result"
            logger.error(error_msg)
            return LocalizationProcessingResult(
                success=False,
                localized_data=construct_result,
                localization_info=WikiLocalizeResult(
                    localized_content="",
                    original_links_replaced=0,
                    templates_localized=0,
                    waou_templates_inserted=0,
                    errors=[error_msg]
                ),
                processing_time=time.time() - start_time,
                errors=[error_msg]
            )

        arabic_content = construct_result['arabic_template']
        if not arabic_content or not arabic_content.strip():
            error_msg = "Arabic template is empty"
            logger.error(error_msg)
            return LocalizationProcessingResult(
                success=False,
                localized_data=construct_result,
                localization_info=WikiLocalizeResult(
                    localized_content=arabic_content,
                    original_links_replaced=0,
                    templates_localized=0,
                    waou_templates_inserted=0,
                    errors=[error_msg]
                ),
                processing_time=time.time() - start_time,
                errors=[error_msg]
            )

        # Initialize localizer
        localizer = WikiLocalizer()

        # Perform localization if enabled
        if enable_local_link_replacement or enable_template_localization:
            localization_result = localizer.localize_content(arabic_content)

            # Update the construct result with localized content
            localized_data = construct_result.copy()
            localized_data['arabic_template'] = localization_result.localized_content
            localized_data['localization_metadata'] = {
                'links_replaced': localization_result.original_links_replaced,
                'templates_localized': localization_result.templates_localized,
                'waou_templates_inserted': localization_result.waou_templates_inserted,
                'localization_errors': localization_result.errors
            }

            processing_time = time.time() - start_time

            logger.info("Wiki localization completed successfully")
            logger.info(f"- Links replaced: {localization_result.original_links_replaced}")
            logger.info(f"- Templates localized: {localization_result.templates_localized}")
            logger.info(f"- واو templates inserted: {localization_result.waou_templates_inserted}")

            if localization_result.errors:
                logger.warning(f"Localization errors: {localization_result.errors}")

            return LocalizationProcessingResult(
                success=len(localization_result.errors) == 0,
                localized_data=localized_data,
                localization_info=localization_result,
                processing_time=processing_time
            )
        else:
            # Localization disabled, just pass through
            logger.info("Wiki localization disabled, passing through data unchanged")
            return LocalizationProcessingResult(
                success=True,
                localized_data=construct_result,
                localization_info=WikiLocalizeResult(
                    localized_content=arabic_content,
                    original_links_replaced=0,
                    templates_localized=0,
                    waou_templates_inserted=0,
                    errors=[]
                ),
                processing_time=time.time() - start_time
            )

    except Exception as e:
        error_msg = f"Unexpected error during localization processing: {e}"
        logger.error(error_msg)
        processing_time = time.time() - start_time

        return LocalizationProcessingResult(
            success=False,
            localized_data=construct_result,
            localization_info=WikiLocalizeResult(
                localized_content=construct_result.get('arabic_template', ''),
                original_links_replaced=0,
                templates_localized=0,
                waou_templates_inserted=0,
                errors=[error_msg]
            ),
            processing_time=processing_time,
            errors=[error_msg]
        )


def get_localization_statistics(localization_result: WikiLocalizeResult) -> Dict[str, Any]:
    """
    Extract useful statistics from localization results for reporting.

    Args:
        localization_result (WikiLocalizeResult): Localization result

    Returns:
        Dict[str, Any]: Statistics dictionary
    """
    return {
        'total_links_processed': localization_result.original_links_replaced + localization_result.waou_templates_inserted,
        'links_successfully_replaced': localization_result.original_links_replaced,
        'waou_fallback_templates': localization_result.waou_templates_inserted,
        'templates_localized': localization_result.templates_localized,
        'localization_errors': len(localization_result.errors),
        'success_rate': 'High' if not localization_result.errors else 'Medium' if localization_result.original_links_replaced > 0 else 'Low'
    }