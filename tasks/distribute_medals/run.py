import pywikibot
import wikitextparser as wtp

from data import list_of_distribute_medals
from module import SendTemplate, SignatureScanner, SignaturePage


def get_user_name(signature):
    try:
        parsed = wtp.parse(signature)
        link = parsed.wikilinks[0]
        namespace, user_name = link.title.split(":")
        return user_name
    except Exception as e:
        print(f"An error occurred while processing get_user_name def with {signature}: {e}")
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
        for page_data in list_of_distribute_medals:
            try:
                print("start get " + str(page_data['number']))
                # # Create a SendTemplate object with the page data
                obj = SendTemplate(input_dict=page_data, signature_list=signatures)
                # Send the template to the user
                obj.send()
            except Exception as e:
                print(f"An error occurred while processing : {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
