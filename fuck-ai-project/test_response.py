from learning_system import LearningSystem

ls = LearningSystem()
# seed a couple of dynamic responses for testing
ls.learned_responses['dynamic_responses'].append({'input':'how are you doing today','response':'I am doing great, thanks! How about you?'})
ls.learned_responses['dynamic_responses'].append({'input':'tell me a joke','response':'Why did the chicken cross the road? To get to the other side!'})

print('TEST1 ->', ls.get_learned_response('how are you?'))
print('TEST2 ->', ls.get_learned_response('can you tell me a joke'))
print('TEST3 ->', ls.get_learned_response('what is your name'))
