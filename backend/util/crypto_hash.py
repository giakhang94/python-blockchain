import hashlib
import json


def crypto_hash(*arguments):
    """
    Return a Sha-256 hash of the given data.
    """
    # stringified_data = json.dumps(data)

    stringify_arguments = sorted(map(lambda data: json.dumps(data),arguments))
    joined_data = ''.join(stringify_arguments)
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"crypto_hash('one', 'two', 'three'): {crypto_hash(123, [{"taO": 123}], False)}")

# a = "hello"
# print(a.encode('utf-8'))
# print(hashlib.sha256(a.encode('utf-8')))
# print(hashlib.sha256(a.encode('utf-8')).hexdigest())

if __name__ == "__main__":
    main()