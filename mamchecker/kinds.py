# -*- coding: utf-8 -*-

make_kind0 = lambda lang:{k:v for k,v in enumerate(kinds[lang])}
make_kinda = lambda lang:{v:k for k,v in enumerate(kinds[lang])}

# >= contents is content
# >= fragments is fragment

kinds = {

#order cannot be changed, because index is used in html files via kinda()
#TODO: is this ok?
'de':
['Übungen', 'Inhalte', 'Kurse', 'Informelles', 'Zusammenfassungen', 'Formelles', 'Fragmente',
'Bemerkungen', 'Zitate', 'Definitionen', 'Theoreme', 'Korollare', 'Lemmas',
'Propositionen', 'Axiome', 'Vermutungen', 'Behauptungen','Meta'],

'en': 
['Problems', 'Content', 'Courses', 'Informal', 'Summaries', 'Formal', 'Fragments',
'Remarks', 'Citations', 'Definitions', 'Theorems', 'Corollaries', 'Lemmas',
'Propositions', 'Axioms', 'Conjectures', 'Claims', 'Identities', 'Paradoxes','Meta']

}

CtxStrings = {

'en': ['School', 'Period', 'Teacher', 'Class', 'Student'],
'de': ['Schule', 'Periode', 'Lehrer', 'Klasse', 'Student']

}

Error = {
'en': 'Error',
'de': 'Fehler'
}
