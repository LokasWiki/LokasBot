import logging
from fetch import fetch_wikipedia_data
from parse.parse import parse_data
from map.map import map_data
from translate.translate import translate_data
from construct.build import construct_arabic_template
from publish.publish import publish_data
from save.save import save_data
from wikilocalize.integrator import process_construct_to_publish
# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def run_wikipedia_pipeline(ar_page_title: str, target_lang: str = 'ar',
                          output_dir: str = 'output',
                          template_type: str = 'football_biography') -> str:
    """
    Run the complete Wikipedia infobox sync pipeline.

    Args:
        ar_page_title (str): Arabic Wikipedia page title to sync.
        target_lang (str): Target language for translation (default: 'ar').
        output_dir (str): Directory to save the processed data.
        template_type (str): Type of template to parse and map.

    Returns:
        str: Path to the saved file.
    """
    msg = f"Starting Wikipedia InfoboxSync pipeline for: {ar_page_title}"
    logger.info(msg)

    try:
        # Stage 1: Fetch Wikipedia data
        logger.info("Pipeline stage: Fetch Wikipedia data")
        wiki_data = fetch_wikipedia_data(ar_page_title)

        if not wiki_data['sync_possible']:
            error_msg = wiki_data.get('error', 'Unknown error occurred')
            logger.error(f"Cannot proceed with pipeline: {error_msg}")
            raise ValueError(error_msg)

        # Extract English page content for processing
        en_page_info = wiki_data['english']
        if not en_page_info or not en_page_info.content:
            msg = "No English page content available for processing"
            raise ValueError(msg)

        # Convert page info to dictionary format expected by parse stage
        raw_data = {
            'title': en_page_info.title,
            'content': en_page_info.content,
            'arabic_title': wiki_data['arabic'].title,
            'langlinks': en_page_info.langlinks or {}
        }

        # Stage 2: Parse
        logger.info("Pipeline stage: Parse")
        parsed_data = parse_data(raw_data, template_type)

        # Stage 3: Map
        logger.info("Pipeline stage: Map")
        mapped_data = map_data(parsed_data, template_type)

        # Stage 4: Translate
        logger.info("Pipeline stage: Translate")
        translated_data = translate_data(mapped_data, target_lang)

        # Stage 5: Build Arabic Template
        logger.info("Pipeline stage: Construct Arabic Template")
        build_result = construct_arabic_template(translated_data, template_type)

        if not build_result.success:
            error_msg = f"Template construction failed: {build_result.errors}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Add the constructed template to the translated data for saving
        translated_data['arabic_template'] = build_result.template_text
        translated_data['construct_metadata'] = {
            'template_type': build_result.template_type,
            'field_count': build_result.field_count,
            'builder_name': build_result.metadata.get('builder_name', 'unknown'),
            'template_name': build_result.metadata.get('template_name', 'unknown')
        }
        # Stage 6: Wiki Localization - Localize links and templates to Arabic equivalents
        logger.info("Pipeline stage: Wiki Localization")
        localization_result = process_construct_to_publish(
            translated_data,  # Contains arabic_template from previous step
            enable_local_link_replacement=True,
            enable_template_localization=True
        )

        if not localization_result.success:
            error_msg = f"Wiki localization failed: {localization_result.errors}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Use the localized data for publishing
        translated_data = localization_result.localized_data

        # Add localization metadata to the translated data
        translated_data['localization_metadata'] = {
            'links_replaced': localization_result.localization_info.original_links_replaced,
            'templates_localized': localization_result.localization_info.templates_localized,
            'waou_templates_inserted': localization_result.localization_info.waou_templates_inserted,
            'localization_errors': localization_result.localization_info.errors
        }
        
        # Stage 6: Publish to Arabic Wikipedia
        logger.info("Pipeline stage: Publish to Arabic Wikipedia")
        arabic_page_title = wiki_data['arabic'].title
        edit_summary = f"تحديث قالب السيرة الذاتية باستخدام InfoboxSync - {template_type}"

        publish_result = publish_data(translated_data, arabic_page_title, edit_summary)

        if not publish_result.success:
            error_msg = f"Publishing failed: {publish_result.errors}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Add publish metadata to the translated data
        translated_data['publish_metadata'] = {
            'page_title': publish_result.page_title,
            'edit_summary': publish_result.edit_summary,
            'revision_id': publish_result.revision_id,
            'publish_success': publish_result.success,
            'published_at': publish_result.metadata.get('published_at')
        }

        # Stage 7: Save
        logger.info("Pipeline stage: Save")
        saved_path = save_data(translated_data, output_dir)

        msg = f"Data saved to: {saved_path}"
        logger.info(f"Pipeline completed successfully. {msg}")
        return saved_path

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


def run_pipeline(url: str, target_lang: str = 'ar', output_dir: str = 'output') -> str:
    """
    Legacy function for backward compatibility.
    Now extracts page title from Wikipedia URL and calls new pipeline.
    """
    msg = ("run_pipeline(url) is deprecated. Use "
           "run_wikipedia_pipeline(page_title) instead.")
    logger.warning(msg)

    if 'wikipedia.org' in url and '/wiki/' in url:
        page_title = url.split('/wiki/')[-1].replace('_', ' ')
        return run_wikipedia_pipeline(page_title, target_lang, output_dir)
    else:
        msg = ("URL must be a Wikipedia page URL "
               "(e.g., https://en.wikipedia.org/wiki/Page_Title)")
        raise ValueError(msg)


if __name__ == "__main__":
    # Example usage with Arabic page title
    example_arabic_page = "خير الدين مضوي"  # Football player in Arabic
    try:
        result_path = run_wikipedia_pipeline(example_arabic_page, target_lang='ar')
        print(f"Pipeline result saved to: {result_path}")
    except Exception as e:
        print(f"Pipeline execution failed: {e}")

    # Alternative: Example with English page title (for testing)
    # example_english_page = "Egypt"
    # try:
    #     result_path = run_wikipedia_pipeline(example_english_page)
    #     print(f"Pipeline result saved to: {result_path}")
    # except Exception as e:
    #     print(f"Pipeline execution failed: {e}")