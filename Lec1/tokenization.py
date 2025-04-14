import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")
print("Vocab size", encoder.n_vocab)
encode = encoder.encode("Hello my name is kartek")
print(encode) #[13225, 922, 1308, 382, 6490, 21437]

decode = encoder.decode(encode)
print(decode) # Hello my name is kartek