
import logging
from typing import List, Optional, Any
from dataclasses import dataclass
import wikitextparser as wtp

logger = logging.getLogger(__name__)


@dataclass
class WOWTemplateItem:
    """Information about a واو template replacement."""
    link: Any  # Wikilink object from wikitextparser
    localization_result: 'LangLinkResult'  # Full localization result object

@dataclass
class WikiLocalizeResult:
    """Result of wiki localization process."""
    localized_content: str
    original_links_replaced: int
    templates_localized: int
    waou_templates_inserted: int
    wow_templates: List[WOWTemplateItem]
    errors: List[str]


@dataclass
class LangLinkResult:
    """Result of language link retrieval."""
    lang: Optional[str] = None
    ar_page: Optional[str] = None
    en_page: Optional[str] = None

    def is_empty(self) -> bool:
        """Check if the result is empty."""
        return (self.lang is None and self.ar_page is None
                and self.en_page is None)


def dummy_function():
    """Dummy function to avoid linting issues."""
    pass


class WikipediaAPI:
    """Interface to Wikipedia APIs using pywikibot."""

    @staticmethod
    def check_arabic_page_exists(page_title: str) -> Optional[str]:
        """
        Check if a page exists on Arabic Wikipedia using pywikibot.
        If it's a redirect, it resolves to the target page.

        Args:
            page_title (str): Page title to check

        Returns:
            Optional[str]: The resolved page title if it exists, None otherwise
        """
        try:
            import pywikibot

            # Create Arabic Wikipedia site
            arabic_site = pywikibot.Site('ar', 'wikipedia')

            # Create page object
            page = pywikibot.Page(arabic_site, page_title)

            # Resolve redirects recursively
            seen_titles = set()
            while page.isRedirectPage():
                if page.title() in seen_titles:
                    logger.warning(
                        f"Circular redirect detected for '{page_title}'")
                    return None  # Return None for circular redirects
                seen_titles.add(page.title())
                page = page.getRedirectTarget()

            if page.exists():
                return page.title().replace('_', ' ')
            return None

        except ImportError:
            logger.warning("pywikibot not available for Arabic page check")
            return False
        except Exception as e:
            logger.error(f"Error checking Arabic page existence: {e}")
            return False

    @staticmethod
    def get_arabic_langlink(en_page_title: str) -> Optional[str]:
        """
        Get the Arabic language link for an English Wikipedia page.

        Args:
            en_page_title (str): English page title

        Returns:
            Optional[str]: Arabic page title if exists, None otherwise
        """
        try:
            import pywikibot

            # Create English Wikipedia site and get page
            english_site = pywikibot.Site('en', 'wikipedia')

            # Clean up the page title
            clean_title = en_page_title.strip()
            if clean_title.startswith('[[') and clean_title.endswith(']]'):
                clean_title = clean_title[2:-2]
            if '|' in clean_title:
                clean_title = clean_title.split('|')

            page = pywikibot.Page(english_site, clean_title)

            # Check if page exists on English Wikipedia
            # Check if page exists on English Wikipedia
            if not page.exists():
                logger.debug(
                    f"Page '{clean_title}' does not exist on EN Wikipedia")
                return None

            # Get langlinks and find Arabic version
            langlinks = page.langlinks()
            for langlink in langlinks:
                if langlink.site.code == 'ar':
                    return langlink.title.replace('_', ' ')

            logger.debug(f"No Arabic langlink found for: {clean_title}")
            return None

        except ImportError:
            logger.warning("pywikibot not available for langlink retrieval")
            return None
        except Exception as e:
            logger.error(
                f"Error getting Arabic langlink for '{en_page_title}': {e}")
            return None

    @staticmethod
    def get_arabic_langlink_detailed(en_page_title: str) -> LangLinkResult:
        """
        Get the Arabic language link for an English Wikipedia page with
        detailed results.

        Args:
            en_page_title (str): English page title

        Returns:
            LangLinkResult: Object with language and page information
                - If Arabic found: {lang='ar', ar_page=arabic_title}
                - If English exists: {lang='en', en_page=english_title}
                - If not found: empty object {}
        """
        try:
            import pywikibot

            # Create English Wikipedia site and get page
            english_site = pywikibot.Site('en', 'wikipedia')

            # Clean up the page title
            clean_title = en_page_title.strip()
            if clean_title.startswith('[[') and clean_title.endswith(']]'):
                clean_title = clean_title[2:-2]
            if '|' in clean_title:
                clean_title = clean_title.split('|')[0]  # Take first part

            page = pywikibot.Page(english_site, clean_title)

            # Check if page exists on English Wikipedia
            if not page.exists():
                logger.debug(
                    f"Page '{clean_title}' does not exist on EN Wikipedia")
                return LangLinkResult()  # Return empty object

            # Get langlinks and find Arabic version
            langlinks = page.langlinks()
            for langlink in langlinks:
                if langlink.site.code == 'ar':
                    return LangLinkResult(
                        lang='ar',
                        ar_page=langlink.title.replace('_', ' ')
                    )

            # No Arabic link found, but English page exists
            logger.debug(f"No Arabic langlink found for: {clean_title}")
            return LangLinkResult(lang='en', en_page=clean_title)

        except ImportError:
            logger.warning("pywikibot not available for langlink retrieval")
            return LangLinkResult()
        except Exception as e:
            logger.error(
                f"Error getting Arabic langlink for '{en_page_title}': {e}")
            return LangLinkResult()


class WikiLocalizer:
    """
    Localizes wiki links and templates within a given wikitext.
    """

    def localize_content(self, content: str) -> WikiLocalizeResult:
        """
        Localizes wiki links and templates in the provided wikitext content.

        Args:
            content (str): The wikitext content to localize.

        Returns:
            WikiLocalizeResult: The result of the localization process.
        """
        localized_content = content
        original_links_replaced = 0
        templates_localized = 0
        waou_templates_inserted = 0
        wow_templates = []
        errors = []
        

        parsed_content = wtp.parse(content)

        # Localize wikilinks
        for link in parsed_content.wikilinks:
            original_target = link.target
            localization_result = (self
                                  ._localize_wikilink(original_target, errors))
            if not localization_result.is_empty():
                # Use the localized page based on language
                if localization_result.lang == 'ar' and localization_result.ar_page:
                    if localization_result.ar_page != original_target:
                        link.target = localization_result.ar_page
                        original_links_replaced += 1
                elif (localization_result.lang == 'en'  and localization_result.en_page):
                    # Use واو template for English pages without Arabic equivalent
                    wow_templates.append(WOWTemplateItem(
                        link=link,
                        localization_result=localization_result
                    ))

        # Localize templates
        # for template in parsed_content.templates:
        #     original_name = template.name
        #     localized_name, is_waou = \
        #         self._localize_template(original_name, errors)
        #     if localized_name != original_name:
        #         template.name = localized_name
        #         templates_localized += 1
        #         if is_waou:
        #             waou_templates_inserted += 1

        localized_content = parsed_content.string

        # Handle WOW templates after link localization
        for wow_template in wow_templates:
            en_page = wow_template.localization_result.en_page
            ar_text = wow_template.link.text
            temp_template = f"{{{{وإو|{ar_text}|{en_page}}}}}"
            localized_content = localized_content.replace(wow_template.link.string, temp_template)

        return WikiLocalizeResult(
            localized_content=localized_content,
            original_links_replaced=original_links_replaced,
            templates_localized=templates_localized,
            waou_templates_inserted=waou_templates_inserted,
            wow_templates=wow_templates,
            errors=errors
        )

    def _localize_wikilink(self, target: str, errors: List[str]) -> LangLinkResult:
        """
        Localizes a single wikilink target.

        Returns:
            LangLinkResult: Object with lang and page info
                - If Arabic page found: {lang='ar', ar_page=arabic_title}
                - If English exists: {lang='en', en_page=target}
                - If not found: empty object {}
        """
        # 1. Check in ar wiki directly first
        arabic_page_title = WikipediaAPI.check_arabic_page_exists(target)
        if arabic_page_title:
            return LangLinkResult(lang='ar', ar_page=arabic_page_title)

        # 2. Check in en wiki with detailed results
        langlink_result = WikipediaAPI.get_arabic_langlink_detailed(target)
        if not langlink_result.is_empty():
            return langlink_result

        # If not found, return empty result
        return LangLinkResult()

    def _localize_template(self, template_name: str, errors: List[str]) \
            -> (str, bool):
        """
        Localizes a single template name.
        Returns (localized_name, is_waou_template)
        """
        is_waou = False
        # 1. Check in ar wiki, use if found (and resolved)
        arabic_template_page_title = \
            WikipediaAPI.check_arabic_page_exists(template_name)
        if arabic_template_page_title:
            return arabic_template_page_title, is_waou

        # 2. Check in en wiki with detailed results
        langlink_result = (WikipediaAPI
                          .get_arabic_langlink_detailed(template_name))
        if not langlink_result.is_empty():
            if langlink_result.lang == 'ar' and langlink_result.ar_page:
                return langlink_result.ar_page, is_waou
            elif langlink_result.lang == 'en' and langlink_result.en_page:
                return langlink_result.en_page, is_waou

        # If not found in en wiki, use واو template
        is_waou = True
        return f"واو|{template_name}", is_waou