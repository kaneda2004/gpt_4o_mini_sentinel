import os
import tiktoken
from openai import OpenAI
from urllib.parse import urlparse
from grabber import download_site_resources
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.style import Style

console = Console()

def count_tokens(file_path, encoding_name="cl100k_base"):
    """Count tokens in a file using the specified encoding."""
    encoding = tiktoken.get_encoding(encoding_name)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return len(encoding.encode(content)), content

def get_file_type(filename):
    """Get the file type based on the file extension."""
    _, extension = os.path.splitext(filename)
    return extension[1:] if extension else "unknown"

def save_report(content, filename, file_type, directory_name):
    """Save the report as a markdown file in the 'sites/directory_name/reports' directory."""
    reports_dir = os.path.join("sites", directory_name, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    base_filename = os.path.splitext(filename)[0]
    report_filename = os.path.join(reports_dir, f"{base_filename}_{file_type}_report.md")
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(content)
    console.print(f"[green]Report saved as {report_filename}[/green]")

def get_directory_name(url):
    """Extract directory name from URL using the new naming convention."""
    parsed_url = urlparse(url)
    domain_parts = parsed_url.netloc.split('.')
    path = parsed_url.path.strip('/').replace('/', '_')
    
    if len(domain_parts) > 2:
        subdomain = domain_parts[:-2]
        domain = domain_parts[-2]
        tld = domain_parts[-1]
        directory_name = f"{'_'.join(subdomain)}_{domain}_{tld}"
    else:
        domain = domain_parts[0]
        tld = domain_parts[1] if len(domain_parts) > 1 else ""
        directory_name = f"{domain}_{tld}"
    
    if path:
        directory_name += f"_{path}"
    
    return directory_name

def list_directories(path):
    """List directories in the given path."""
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

def list_files(path):
    """List files in the given path."""
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def analyze_file(file_path, file_type):
    """Analyze the file using OpenAI API."""
    _, file_content = count_tokens(file_path)
    
    MODEL = "gpt-4o-mini"
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>"))

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": """You are an expert cybersecurity analyst specializing in web application security. 
            Your task is to analyze the provided file content and identify actual security vulnerabilities (only report on issues that are actually present in the file - if there are none found, report that there are none found), 
            focusing on but not limited to:

            1. Cross-Site Scripting (XSS)
            2. SQL Injection
            3. Cross-Site Request Forgery (CSRF)
            4. Insecure Direct Object References
            5. Security Misconfigurations
            6. Sensitive Data Exposure
            7. Broken Authentication and Session Management
            8. Using Components with Known Vulnerabilities
            9. Unvalidated Redirects and Forwards
            10. Insecure Deserialization
            11. Improperly stored secrets (API keys, passwords, etc.)
            12. Other common web application vulnerabilities
            13. Personally Identifiable information (PII) exposure - email addresses, names and phone numbers, and more

            For each vulnerability found, provide:
            - A brief description of the vulnerability
            - The specific line(s) or section(s) where the vulnerability is present
            - A severity rating (Low, Medium, High, Critical)
            - An example of how an attacker might exploit it (to prove criticality to management)
            - A suggestion for remediation

            Format your response as a structured report that can be easily presented to management."""},
            {"role": "user", "content": f"Analyze the following {file_type} file content for security vulnerabilities:\n\n{file_content}"}
        ]
    )

    return completion.choices[0].message.content

def display_logo():
    logo = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║   ██████╗ ██████╗ ████████╗   ██╗  ██╗ ██████╗    ███╗   ███╗██╗███╗   ██╗██╗║
    ║  ██╔════╝ ██╔══██╗╚══██╔══╝   ██║  ██║██╔═══██╗   ████╗ ████║██║████╗  ██║██║║
    ║  ██║  ███╗██████╔╝   ██║█████╗███████║██║   ██║   ██╔████╔██║██║██╔██╗ ██║██║║
    ║  ██║   ██║██╔═══╝    ██║╚════╝╚════██║██║   ██║   ██║╚██╔╝██║██║██║╚██╗██║██║║
    ║  ╚██████╔╝██║        ██║           ██║╚██████╔╝   ██║ ╚═╝ ██║██║██║ ╚████║██║║
    ║   ╚═════╝ ╚═╝        ╚═╝           ╚═╝ ╚═════╝    ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝║
    ║                                                                              ║
    ║   ███████╗███████╗███╗   ██╗████████╗██╗███╗   ██╗███████╗██╗                ║
    ║   ██╔════╝██╔════╝████╗  ██║╚══██╔══╝██║████╗  ██║██╔════╝██║                ║
    ║   ███████╗█████╗  ██╔██╗ ██║   ██║   ██║██╔██╗ ██║█████╗  ██║                ║
    ║   ╚════██║██╔══╝  ██║╚██╗██║   ██║   ██║██║╚██╗██║██╔══╝  ██║                ║
    ║   ███████║███████╗██║ ╚████║   ██║   ██║██║ ╚████║███████╗███████╗           ║
    ║   ╚══════╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝           ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """

    console.print(Panel(logo, style="bold magenta"))

def main():
    sites_dir = "sites"
    os.makedirs(sites_dir, exist_ok=True)

    display_logo()

    while True:
        choice = console.input(Panel("Enter the website URL to fetch files from or 'r' to resume a session: ", style="cyan"))
        
        if choice.strip().lower() == 'r':
            directories = list_directories(sites_dir)
            if not directories:
                console.print("[red]No existing sessions found.[/red]")
                continue
            
            table = Table(title="Available Sessions")
            table.add_column("Number", style="cyan", no_wrap=True)
            table.add_column("Session Name", style="magenta")
            
            for i, dir_name in enumerate(directories, 1):
                table.add_row(str(i), dir_name)
            
            console.print(table)
            
            selection = console.input(Panel("Select a session number: ", style="cyan"))
            try:
                selection = int(selection)
                if 1 <= selection <= len(directories):
                    directory_name = directories[selection-1]
                    current_dir = os.path.join(sites_dir, directory_name)
                else:
                    console.print("[red]Invalid selection.[/red]")
                    continue
            except ValueError:
                console.print("[red]Invalid input. Please enter a number.[/red]")
                continue
        else:
            target_url = choice
            if not target_url.startswith(('http://', 'https://')):
                target_url = 'https://' + target_url
            directory_name = get_directory_name(target_url)
            current_dir = os.path.join(sites_dir, directory_name)
            
            try:
                with console.status("[bold green]Downloading resources...[/bold green]"):
                    download_site_resources(target_url, current_dir)
            except Exception as e:
                console.print(f"[red]An error occurred while downloading resources: {e}[/red]")
                continue

        while True:
            files = list_files(current_dir)
            results = []

            for filename in files:
                file_path = os.path.join(current_dir, filename)
                token_count, _ = count_tokens(file_path)
                results.append((token_count, filename))

            results.sort(reverse=True)

            table = Table(title="Available Files")
            table.add_column("Number", style="cyan", no_wrap=True)
            table.add_column("Token Count", style="magenta", justify="right")
            table.add_column("Filename", style="green")

            for i, (token_count, filename) in enumerate(results, 1):
                table.add_row(str(i), str(token_count), filename)

            console.print(table)

            selection = console.input(Panel("Select a file number to audit, 'b' to go back, 'n' for new URL, or 'q' to quit: ", style="cyan"))
            
            if selection.strip().lower() == 'b':
                break
            elif selection.strip().lower() == 'n':
                break
            elif selection.strip().lower() == 'q':
                return
            
            try:
                selection = int(selection)
                if 1 <= selection <= len(results):
                    selected_file = os.path.join(current_dir, results[selection-1][1])
                    selected_filename = results[selection-1][1]
                    file_type = get_file_type(selected_filename)

                    with console.status("[bold green]Analyzing file...[/bold green]"):
                        analysis_result = analyze_file(selected_file, file_type)
                    
                    console.print("\n[bold]Assistant's Analysis:[/bold]")
                    console.print(Panel(analysis_result, expand=False))
                    save_report(analysis_result, selected_filename, file_type, directory_name)

                    next_action = console.input(Panel("Enter 'c' to continue, 'b' to go back, 'n' for new URL, or 'q' to quit: ", style="cyan"))
                    if next_action.strip().lower() == 'c':
                        continue
                    elif next_action.strip().lower() == 'b':
                        break
                    elif next_action.strip().lower() == 'n':
                        break
                    elif next_action.strip().lower() == 'q':
                        return
                else:
                    console.print("[red]Invalid selection.[/red]")
            except ValueError:
                console.print("[red]Invalid input. Please enter a number or a valid option.[/red]")

        if selection.strip().lower() == 'n' or next_action.strip().lower() == 'n':
            continue
        elif selection.strip().lower() == 'q' or next_action.strip().lower() == 'q':
            return

if __name__ == "__main__":
    main()
