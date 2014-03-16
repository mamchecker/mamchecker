# -*- coding: utf-8 -*-

'''
EACH DICT MUST CONTAIN AT LEAST ALL AVAILABLE LANGUAGES (see initdb.py and dodo.py)
'''

# >= contents is content
# >= fragments is fragment
kinds = {

    # order must not be changed, because index is used in html files via
    # kinda()
    'de':
    ['Übungen', 'Inhalte', 'Kurse', 'Informelles', 'Zusammenfassungen',
        'Formelles', 'Fragmente', 'Bemerkungen', 'Zitate', 'Definitionen',
        'Theoreme', 'Korollare', 'Lemmas', 'Propositionen', 'Axiome',
        'Vermutungen', 'Behauptungen', 'Identitäten', 'Paradoxien', 'Meta'],

    'en':
    ['problems', 'content', 'courses', 'informal', 'summaries', 'formal',
        'fragments', 'remarks', 'citations', 'definitions', 'theorems',
        'corollaries', 'lemmas', 'propositions', 'axioms', 'conjectures',
        'claims', 'identities', 'paradoxes', 'meta']

}

def make_kind0(lang):
    '''from kind integer to kind string
    '''
    return {k: v for k, v in enumerate(kinds[lang])}

def make_kinda(lang):
    '''from kind string to kind integer
    '''
    return {v: k for k, v in enumerate(kinds[lang])}


CtxStrings = {

    'en': ['School', 'Period', 'Teacher', 'Class', 'Student'],
    'de': ['Schule', 'Periode', 'Lehrer', 'Klasse', 'Student']

}

languages = {'ab': 'Abkhazian',
             'aa': 'Afar',
             'af': 'Afrikaans',
             'sq': 'Albanian',
             'am': 'Amharic',
             'ar': 'Arabic',
             'an': 'Aragonese',
             'hy': 'Armenian',
             'as': 'Assamese',
             'ay': 'Aymara',
             'az': 'Azerbaijani',
             'ba': 'Bashkir',
             'eu': 'Basque',
             'bn': 'Bengali (Bangla)',
             'dz': 'Bhutani',
             'bh': 'Bihari',
             'bi': 'Bislama',
             'br': 'Breton',
             'bg': 'Bulgarian',
             'my': 'Burmese',
             'be': 'Byelorussian (Belarusian)',
             'km': 'Cambodian',
             'ca': 'Catalan',
             'zh': 'Chinese',
             'co': 'Corsican',
             'hr': 'Croatian',
             'cs': 'Czech',
             'da': 'Danish',
             'nl': 'Dutch',
             'en': 'English',
             'eo': 'Esperanto',
             'et': 'Estonian',
             'fo': 'Faeroese',
             'fa': 'Farsi',
             'fj': 'Fiji',
             'fi': 'Finnish',
             'fr': 'French',
             'fy': 'Frisian',
             'gl': 'Galician',
             'gd': 'Gaelic (Scottish)',
             'gv': 'Gaelic (Manx)',
             'ka': 'Georgian',
             'de': 'German',
             'el': 'Greek',
             'kl': 'Greenlandic',
             'gn': 'Guarani',
             'gu': 'Gujarati',
             'ht': 'Haitian Creole',
             'ha': 'Hausa',
             'he': 'Hebrew',
             'hi': 'Hindi',
             'hu': 'Hungarian',
             'is': 'Icelandic',
             'io': 'Ido',
             'id': 'Indonesian',
             'ia': 'Interlingua',
             'ie': 'Interlingue',
             'iu': 'Inuktitut',
             'ik': 'Inupiak',
             'ga': 'Irish',
             'it': 'Italian',
             'ja': 'Japanese',
             'jv': 'Javanese',
             'kn': 'Kannada',
             'ks': 'Kashmiri',
             'kk': 'Kazakh',
             'rw': 'Kinyarwanda (Ruanda)',
             'ky': 'Kirghiz',
             'rn': 'Kirundi (Rundi)',
             'ko': 'Korean',
             'ku': 'Kurdish',
             'lo': 'Laothian',
             'la': 'Latin',
             'lv': 'Latvian (Lettish)',
             'li': 'Limburgish ( Limburger)',
             'ln': 'Lingala',
             'lt': 'Lithuanian',
             'mk': 'Macedonian',
             'mg': 'Malagasy',
             'ms': 'Malay',
             'ml': 'Malayalam',
             'mt': 'Maltese',
             'mi': 'Maori',
             'mr': 'Marathi',
             'mo': 'Moldavian',
             'mn': 'Mongolian',
             'na': 'Nauru',
             'ne': 'Nepali',
             'no': 'Norwegian',
             'oc': 'Occitan',
             'or': 'Oriya',
             'om': 'Oromo (Afaan Oromo)',
             'ps': 'Pashto (Pushto)',
             'pl': 'Polish',
             'pt': 'Portuguese',
             'pa': 'Punjabi',
             'qu': 'Quechua',
             'rm': 'Rhaeto-Romance',
             'ro': 'Romanian',
             'ru': 'Russian',
             'sm': 'Samoan',
             'sg': 'Sangro',
             'sa': 'Sanskrit',
             'sr': 'Serbian',
             'sh': 'Serbo-Croatian',
             'st': 'Sesotho',
             'tn': 'Setswana',
             'sn': 'Shona',
             'ii': 'Sichuan Yi',
             'sd': 'Sindhi',
             'si': 'Sinhalese',
             'ss': 'Siswati',
             'sk': 'Slovak',
             'sl': 'Slovenian',
             'so': 'Somali',
             'es': 'Spanish',
             'su': 'Sundanese',
             'sw': 'Swahili (Kiswahili)',
             'sv': 'Swedish',
             'tl': 'Tagalog',
             'tg': 'Tajik',
             'ta': 'Tamil',
             'tt': 'Tatar',
             'te': 'Telugu',
             'th': 'Thai',
             'bo': 'Tibetan',
             'ti': 'Tigrinya',
             'to': 'Tonga',
             'ts': 'Tsonga',
             'tr': 'Turkish',
             'tk': 'Turkmen',
             'tw': 'Twi',
             'ug': 'Uighur',
             'uk': 'Ukrainian',
             'ur': 'Urdu',
             'uz': 'Uzbek',
             'vi': 'Vietnamese',
             'vo': 'Volapük',
             'wa': 'Wallon',
             'cy': 'Welsh',
             'wo': 'Wolof',
             'xh': 'Xhosa',
             'yi': 'Yiddish',
             'yo': 'Yoruba',
             'zu': 'Zulu'}
