# -*- coding: utf-8 -*-

make_kind0 = lambda lang: {k: v for k, v in enumerate(kinds[lang])}
make_kinda = lambda lang: {v: k for k, v in enumerate(kinds[lang])}

# >= contents is content
# >= fragments is fragment

kinds = {

    # order must not be changed, because index is used in html files via
    # kinda()
    'de':
    ['Übungen', 'Inhalte', 'Kurse', 'Informelles', 'Zusammenfassungen', 'Formelles', 'Fragmente',
     'Bemerkungen', 'Zitate', 'Definitionen', 'Theoreme', 'Korollare', 'Lemmas',
     'Propositionen', 'Axiome', 'Vermutungen', 'Behauptungen', 'Identitäten', 'Paradoxien', 'Meta'],

    'en':
    ['problems', 'content', 'courses', 'informal', 'summaries', 'formal', 'fragments',
     'remarks', 'citations', 'definitions', 'theorems', 'corollaries', 'lemmas',
     'propositions', 'axioms', 'conjectures', 'claims', 'identities', 'paradoxes', 'meta']

}

CtxStrings = {

    'en': ['School', 'Period', 'Teacher', 'Class', 'Student'],
    'de': ['Schule', 'Periode', 'Lehrer', 'Klasse', 'Student']

}

Error = {
    'en': 'Error',
    'de': 'Fehler'
}
