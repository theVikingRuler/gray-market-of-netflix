import requests
import re
import os
from bs4 import BeautifulSoup

ALL_REGIONS = [
	{"value":"AF","label":"Afghanistan"},
	{"value":"AX","label":"\u00C5land Islands"},
	{"value":"AL","label":"Albania"},{"value":"DZ","label":"Algeria"},{"value":"AS","label":"American Samoa"},{"value":"AD","label":"Andorra"},{"value":"AO","label":"Angola"},{"value":"AI","label":"Anguilla"},{"value":"AQ","label":"Antarctica"},{"value":"AG","label":"Antigua \u0026 Barbuda"},{"value":"AR","label":"Argentina"},{"value":"AM","label":"Armenia"},{"value":"AW","label":"Aruba"},{"value":"AU","label":"Australia"},{"value":"AT","label":"Austria"},{"value":"AZ","label":"Azerbaijan"},{"value":"BS","label":"Bahamas"},{"value":"BH","label":"Bahrain"},{"value":"BD","label":"Bangladesh"},{"value":"BB","label":"Barbados"},{"value":"BY","label":"Belarus"},{"value":"BE","label":"Belgium"},{"value":"BZ","label":"Belize"},{"value":"BJ","label":"Benin"},{"value":"BM","label":"Bermuda"},{"value":"BT","label":"Bhutan"},{"value":"BO","label":"Bolivia"},{"value":"BA","label":"Bosnia \u0026 Herzegovina"},{"value":"BW","label":"Botswana"},{"value":"BV","label":"Bouvet Island"},{"value":"BR","label":"Brazil"},{"value":"IO","label":"British Indian Ocean Territory"},{"value":"VG","label":"British Virgin Islands"},{"value":"BN","label":"Brunei"},{"value":"BG","label":"Bulgaria"},{"value":"BF","label":"Burkina Faso"},{"value":"BI","label":"Burundi"},{"value":"KH","label":"Cambodia"},{"value":"CM","label":"Cameroon"},{"value":"CA","label":"Canada"},{"value":"CV","label":"Cape Verde"},{"value":"BQ","label":"Caribbean Netherlands"},{"value":"KY","label":"Cayman Islands"},{"value":"CF","label":"Central African Republic"},{"value":"TD","label":"Chad"},{"value":"CL","label":"Chile"},{"value":"CN","label":"China"},{"value":"CX","label":"Christmas Island"},{"value":"CC","label":"Cocos (Keeling) Islands"},{"value":"CO","label":"Colombia"},{"value":"KM","label":"Comoros"},{"value":"CG","label":"Congo - Brazzaville"},{"value":"CD","label":"Congo - Kinshasa"},{"value":"CK","label":"Cook Islands"},{"value":"CR","label":"Costa Rica"},{"value":"CI","label":"C\u00F4te d\u2019Ivoire"},{"value":"HR","label":"Croatia"},{"value":"CU","label":"Cuba"},{"value":"CW","label":"Cura\u00E7ao"},{"value":"CY","label":"Cyprus"},{"value":"CZ","label":"Czechia"},{"value":"DK","label":"Denmark"},{"value":"DJ","label":"Djibouti"},{"value":"DM","label":"Dominica"},{"value":"DO","label":"Dominican Republic"},{"value":"EC","label":"Ecuador"},{"value":"EG","label":"Egypt"},{"value":"SV","label":"El Salvador"},{"value":"GQ","label":"Equatorial Guinea"},{"value":"ER","label":"Eritrea"},{"value":"EE","label":"Estonia"},{"value":"SZ","label":"Eswatini"},{"value":"ET","label":"Ethiopia"},{"value":"FK","label":"Falkland Islands"},{"value":"FO","label":"Faroe Islands"},{"value":"FJ","label":"Fiji"},{"value":"FI","label":"Finland"},{"value":"FR","label":"France"},{"value":"GF","label":"French Guiana"},{"value":"PF","label":"French Polynesia"},{"value":"TF","label":"French Southern Territories"},{"value":"GA","label":"Gabon"},{"value":"GM","label":"Gambia"},{"value":"GE","label":"Georgia"},{"value":"DE","label":"Germany"},{"value":"GH","label":"Ghana"},{"value":"GI","label":"Gibraltar"},{"value":"GR","label":"Greece"},{"value":"GL","label":"Greenland"},{"value":"GD","label":"Grenada"},{"value":"GP","label":"Guadeloupe"},{"value":"GU","label":"Guam"},{"value":"GT","label":"Guatemala"},{"value":"GG","label":"Guernsey"},{"value":"GN","label":"Guinea"},{"value":"GW","label":"Guinea-Bissau"},{"value":"GY","label":"Guyana"},{"value":"HT","label":"Haiti"},{"value":"HM","label":"Heard \u0026 McDonald Islands"},{"value":"HN","label":"Honduras"},{"value":"HK","label":"Hong Kong"},{"value":"HU","label":"Hungary"},{"value":"IS","label":"Iceland"},{"value":"IN","label":"India"},{"value":"ID","label":"Indonesia"},{"value":"IR","label":"Iran"},{"value":"IQ","label":"Iraq"},{"value":"IE","label":"Ireland"},{"value":"IM","label":"Isle of Man"},{"value":"IL","label":"Israel"},{"value":"IT","label":"Italy"},{"value":"JM","label":"Jamaica"},{"value":"JP","label":"Japan"},{"value":"JE","label":"Jersey"},{"value":"JO","label":"Jordan"},{"value":"KZ","label":"Kazakhstan"},{"value":"KE","label":"Kenya"},{"value":"KI","label":"Kiribati"},{"value":"KW","label":"Kuwait"},{"value":"KG","label":"Kyrgyzstan"},{"value":"LA","label":"Laos"},{"value":"LV","label":"Latvia"},{"value":"LB","label":"Lebanon"},{"value":"LS","label":"Lesotho"},{"value":"LR","label":"Liberia"},{"value":"LY","label":"Libya"},{"value":"LI","label":"Liechtenstein"},{"value":"LT","label":"Lithuania"},{"value":"LU","label":"Luxembourg"},{"value":"MO","label":"Macau"},{"value":"MG","label":"Madagascar"},{"value":"MW","label":"Malawi"},{"value":"MY","label":"Malaysia"},{"value":"MV","label":"Maldives"},{"value":"ML","label":"Mali"},{"value":"MT","label":"Malta"},{"value":"MH","label":"Marshall Islands"},{"value":"MQ","label":"Martinique"},{"value":"MR","label":"Mauritania"},{"value":"MU","label":"Mauritius"},{"value":"YT","label":"Mayotte"},{"value":"MX","label":"Mexico"},{"value":"FM","label":"Micronesia"},{"value":"MD","label":"Moldova"},{"value":"MC","label":"Monaco"},{"value":"MN","label":"Mongolia"},{"value":"ME","label":"Montenegro"},{"value":"MS","label":"Montserrat"},{"value":"MA","label":"Morocco"},{"value":"MZ","label":"Mozambique"},{"value":"MM","label":"Myanmar (Burma)"},{"value":"NA","label":"Namibia"},{"value":"NR","label":"Nauru"},{"value":"NP","label":"Nepal"},{"value":"NL","label":"Netherlands"},{"value":"NC","label":"New Caledonia"},{"value":"NZ","label":"New Zealand"},{"value":"NI","label":"Nicaragua"},{"value":"NE","label":"Niger"},{"value":"NG","label":"Nigeria"},{"value":"NU","label":"Niue"},{"value":"NF","label":"Norfolk Island"},{"value":"MP","label":"Northern Mariana Islands"},{"value":"KP","label":"North Korea"},{"value":"MK","label":"North Macedonia"},{"value":"NO","label":"Norway"},{"value":"OM","label":"Oman"},{"value":"PK","label":"Pakistan"},{"value":"PW","label":"Palau"},{"value":"PS","label":"Palestine"},{"value":"PA","label":"Panama"},{"value":"PG","label":"Papua New Guinea"},{"value":"PY","label":"Paraguay"},{"value":"PE","label":"Peru"},{"value":"PH","label":"Philippines"},{"value":"PN","label":"Pitcairn Islands"},{"value":"PL","label":"Poland"},{"value":"PT","label":"Portugal"},{"value":"PR","label":"Puerto Rico"},{"value":"QA","label":"Qatar"},{"value":"RE","label":"R\u00E9union"},{"value":"RO","label":"Romania"},{"value":"RU","label":"Russia"},{"value":"RW","label":"Rwanda"},{"value":"WS","label":"Samoa"},{"value":"SM","label":"San Marino"},{"value":"ST","label":"S\u00E3o Tom\u00E9 \u0026 Pr\u00EDncipe"},{"value":"SA","label":"Saudi Arabia"},{"value":"SN","label":"Senegal"},{"value":"RS","label":"Serbia"},{"value":"SC","label":"Seychelles"},{"value":"SL","label":"Sierra Leone"},{"value":"SG","label":"Singapore"},{"value":"SX","label":"Sint Maarten"},{"value":"SK","label":"Slovakia"},{"value":"SI","label":"Slovenia"},{"value":"SB","label":"Solomon Islands"},{"value":"SO","label":"Somalia"},{"value":"ZA","label":"South Africa"},{"value":"GS","label":"South Georgia \u0026 South Sandwich Islands"},{"value":"KR","label":"South Korea"},{"value":"SS","label":"South Sudan"},{"value":"ES","label":"Spain"},{"value":"LK","label":"Sri Lanka"},{"value":"BL","label":"St. Barth\u00E9lemy"},{"value":"SH","label":"St. Helena"},{"value":"KN","label":"St. Kitts \u0026 Nevis"},{"value":"LC","label":"St. Lucia"},{"value":"MF","label":"St. Martin"},{"value":"PM","label":"St. Pierre \u0026 Miquelon"},{"value":"VC","label":"St. Vincent \u0026 Grenadines"},{"value":"SD","label":"Sudan"},{"value":"SR","label":"Suriname"},{"value":"SJ","label":"Svalbard \u0026 Jan Mayen"},{"value":"SE","label":"Sweden"},{"value":"CH","label":"Switzerland"},{"value":"SY","label":"Syria"},{"value":"TW","label":"Taiwan"},{"value":"TJ","label":"Tajikistan"},{"value":"TZ","label":"Tanzania"},{"value":"TH","label":"Thailand"},{"value":"TL","label":"Timor-Leste"},{"value":"TG","label":"Togo"},{"value":"TK","label":"Tokelau"},{"value":"TO","label":"Tonga"},{"value":"TT","label":"Trinidad and Tobago"},{"value":"TN","label":"Tunisia"},{"value":"TR","label":"T\u00FCrkiye"},{"value":"TM","label":"Turkmenistan"},{"value":"TC","label":"Turks \u0026 Caicos Islands"},{"value":"TV","label":"Tuvalu"},{"value":"UM","label":"U.S. Outlying Islands"},{"value":"VI","label":"U.S. Virgin Islands"},{"value":"UG","label":"Uganda"},{"value":"UA","label":"Ukraine"},{"value":"AE","label":"United Arab Emirates"},{"value":"GB","label":"United Kingdom"},{"value":"US","label":"United States"},{"value":"UY","label":"Uruguay"},{"value":"UZ","label":"Uzbekistan"},{"value":"VU","label":"Vanuatu"},{"value":"VA","label":"Vatican City"},{"value":"VE","label":"Venezuela"},{"value":"VN","label":"Vietnam"},{"value":"WF","label":"Wallis \u0026 Futuna"},{"value":"EH","label":"Western Sahara"},{"value":"YE","label":"Yemen"},{"value":"ZM","label":"Zambia"},
    {"value":"ZW","label":"Zimbabwe"}]
   
SCRAPED_REGIONS = []

def extract_netflix_pricing(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0"
    }

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    pricing = {}

    # Step 1: find heading that contains "Pricing"
    heading = soup.find(lambda tag: tag.name in ["h3", "h2"] and "Pricing" in tag.text)
    if not heading:
        print("⚠️ No pricing section found.")
        return {}

    # Step 2: get the nearest <ul> or <div> containing list items
    container = heading.find_next(["ul", "div"])
    if not container:
        print("⚠️ No pricing container found.")
        return {}

    # Step 3: find all list-like tags
    for li in container.find_all(["li", "p"], recursive=True):
        text = li.get_text(" ", strip=True)
        # flexible pattern: e.g. "Basic - $3.99/month" or "Basic: $3.99"
        import re
        m = re.search(r"(\b\w+\b)[\s:–-]+([$€₹]\s?\d+(?:\.\d+)?\s*/?\s*\w*)", text)
        if m:
            plan, price = m.groups()
            pricing[plan] = price

    return pricing



os.system("clear")
base_url = 'https://help.netflix.com/en/node/24926/'

file = open("result.txt", "a")

for region in ALL_REGIONS:

    country_code = region['value'].lower()

    if country_code in SCRAPED_REGIONS:
        continue

    target_url = base_url + country_code

    data = extract_netflix_pricing(target_url)

    line_list = [country_code, region['label'], data.get('Mobile', '0'), data.get('Basic', '0'), data.get('Standard', '0'), data.get('Premium', '0')]

    line_str = ','.join(line_list)
    file.write(line_str)

    print('added')
    ALL_REGIONS.append(country_code)

file.close()
