import uuid



def gen_uid(length):
    #generate a random alphanumeric string
    return str(uuid.uuid4()).replace('-', '')[:length]


