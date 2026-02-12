from learning_system import LearningSystem

ls = LearningSystem()

print('Adding word "computer" with translations...')
res = ls.add_word_with_translations('computer', target_languages=['spanish','french'])
print('Result:', res)

print('\nEnriching "computer" from Wikipedia...')
defn = ls.enrich_word_from_wikipedia('computer')
print('Definition (truncated):', (defn or '')[:200])

print('\nVocabulary entry:')
print(ls.vocabulary['words'].get('computer'))
