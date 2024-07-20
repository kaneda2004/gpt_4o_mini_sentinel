import os
import tiktoken

def count_tokens(file_path, encoding_name="cl100k_base"):
    """Count tokens in a file using the specified encoding."""
    encoding = tiktoken.get_encoding(encoding_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return len(encoding.encode(content))

def main():
    directory = "downloaded_resources"
    results = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            token_count = count_tokens(file_path)
            results.append((token_count, filename))

    # Sort results by token count in descending order
    results.sort(reverse=True)

    # Print results
    for token_count, filename in results:
        print(f"{token_count} tokens - {filename}")

if __name__ == "__main__":
    main()

