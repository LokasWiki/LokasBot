import wikitextparser as wtp

from core.utils.helpers import prepare_str

template_name = "أرشفة آلية"


def read_archive_template(page_text, archive_template_name):
    # Parse the page text using the wikitextparser library
    parsed = wtp.parse(page_text)

    # Set default values for template type and value
    template_type = 'section'
    template_value = 10

    # Loop over all templates in the parsed page text
    for template in parsed.templates:
        # Check if the current template is the archive template we are looking for
        if prepare_str(template.name) == prepare_str(archive_template_name):
            try:
                # Attempt to parse the template type string from the first argument of the template
                template_type_str = prepare_str(template.arguments[0].value)
                if template_type_str == prepare_str('حجم'):
                    template_type = 'size'
                elif template_type_str == prepare_str('قسم'):
                    template_type = 'section'
            except:
                # If an error occurs while parsing the template type, skip this block and use the default value
                pass
            try:
                # Attempt to parse the template value integer from the second argument of the template
                template_value_str = template.arguments[1].value
                template_value = int(template_value_str)
            except:
                # If an error occurs while parsing the template value, skip this block and use the default value
                pass

    # Return the template type and value
    return template_type, template_value
