import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')

print("vocab size : ", encoder.n_vocab)

text = "The cat sat on the mat"

tokens = encoder.encode(text)

print("tokens", tokens) # tokens [976, 9059, 10139, 402, 290, 2450]

my_tokens = [976, 9059, 10139, 402, 290, 2450]

print(encoder.decode(my_tokens))