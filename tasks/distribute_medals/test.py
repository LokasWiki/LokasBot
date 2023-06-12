import logging

import pywikibot
import wikitextparser as wtp

from module import SendTemplate, SignatureScanner, SignaturePage


def get_user_name(signature):
    try:
        parsed = wtp.parse(signature)
        link = parsed.wikilinks[0]
        namespace, user_name = link.title.split(":")
        return user_name
    except Exception as e:
        print(f"An error occurred while processing get_user_name def with {signature}: {e}")
        logging.exception(e)
        return None


def main(*args: str) -> int:
    site = pywikibot.Site()
    # signaturePage
    page = SignaturePage(site)
    page.title = "ويكيبيديا:توزيع أوسمة/تواقيع"
    #  get list of signatures
    scanner = SignatureScanner()
    scanner.pattern = r"\*(?P<signature>.*?)(?=\*|$)"
    scanner.scan(page.get_page_text())
    if scanner.have_requests:
        signatures = []
        for request in scanner.requests:
            signatures.append({
                'signature': request['signature'],
                'user_name': get_user_name(request['signature'])
            })
        for page_data in [
            {
                "number": 150000,
                "query": """select 'Dr-Taher' as 'actor_name', 150000 as 'sum_yc', 150000 as 'sum_tc' from actor limit 1""",
                "template_stub": "{{وسام تعديلات|NUMBER|-- SIGNATURE  {{safesubst:#وقت:G:i، j F Y}}  (ت ع م)|USERNAME}}"
            },
        ]:
            try:
                print("start get " + str(page_data['number']))
                # # Create a SendTemplate object with the page data
                obj = SendTemplate(input_dict=page_data, signature_list=signatures)
                # Send the template to the user
                obj.send()
            except Exception as e:
                print(f"An error occurred while processing : {e}")
                logging.exception(e)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
