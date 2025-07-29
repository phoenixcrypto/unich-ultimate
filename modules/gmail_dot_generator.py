from colorama import Fore, Style, init
init(autoreset=True)

def generate_gmail_dot_variants(username):
    """
    Generate all possible Gmail dot trick variants for a given username (before @).
    Gmail ignores dots in the username, so all variants reach the same inbox.
    """
    results = []
    n = len(username) - 1
    max_val = 1 << n
    for i in range(max_val):
        variant = ''
        for j in range(n):
            variant += username[j]
            if i & (1 << j):
                variant += '.'
        variant += username[n]
        results.append(variant + "@gmail.com")
    return results

def save_gmail_variants_to_accounts(username, password, output_file="data/accounts.txt"):
    """
    Save all generated Gmail variants with the given password to the accounts file.
    """
    variants = generate_gmail_dot_variants(username)
    with open(output_file, "a", encoding="utf-8") as f:
        for email in variants:
            f.write(f"{email}:{password}\n")
    print(Fore.GREEN + Style.BRIGHT + "\n" + "="*44)
    print(Fore.GREEN + Style.BRIGHT + f"✅ {len(variants)} emails have been saved to '{output_file}'")
    print(Fore.GREEN + Style.BRIGHT + "="*44 + "\n")

if __name__ == "__main__":
    print("\n❌ Running this file directly is considered fraudulent!\nPlease run the main script using: python main.py\n")
    exit(1) 