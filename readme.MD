# gpt-4o-mini SENTINEL

<pre>
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
</pre>


## Overview

This tool combines website resource grabbing, token counting, and AI-powered security auditing to assist in thorough web security analysis. It leverages the power of OpenAI's GPT models to perform in-depth security assessments of web applications.

The main components of GPT-4O-Mini SENTINEL include:

1. Website Resource Grabber: Automatically downloads files from a specified website for analysis.
2. Token Counter: Counts tokens in the downloaded files, preparing them for AI analysis.
3. AI-Powered Security Auditor: Utilizes the GPT-4O-Mini model to analyze files for potential vulnerabilities.

The security auditor is designed to identify a wide range of vulnerabilities, including but not limited to:

- Cross-Site Scripting (XSS)
- SQL Injection
- Cross-Site Request Forgery (CSRF)
- Insecure Direct Object References
- Security Misconfigurations
- Sensitive Data Exposure
- Broken Authentication and Session Management
- Use of Components with Known Vulnerabilities
- Unvalidated Redirects and Forwards
- Insecure Deserialization
- Improperly stored secrets (API keys, passwords, etc.)
- Personally Identifiable Information (PII) exposure

For each identified vulnerability, the tool provides:
- A brief description
- The specific location in the code
- A severity rating
- An example of potential exploitation
- Suggestions for remediation

This approach allows for a thorough security assessment, providing valuable insights for both developers and security professionals.


## Workflow

``` mermaid
graph TD
    A[Start] --> B{User Input}
    B -->|Enter URL| C[grabber.py]
    B -->|Resume Session| D[List Existing Sessions]
    C --> E[Download Resources]
    E --> F[Save Files]
    F --> G[Display File List]
    D --> G
    G --> H{User Selection}
    H -->|Select File| I[auditor.py]
    H -->|Back| B
    H -->|New URL| B
    H -->|Quit| Z[End]
    I --> J[Count Tokens]
    J --> K[Analyze File with gpt-4o-mini]
    K --> L[Generate Security Report]
    L --> M[Display Analysis]
    M --> N[Save Report]
    N --> O{Next Action}
    O -->|Continue| G
    O -->|Back| B
    O -->|New URL| B
    O -->|Quit| Z
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/kaneda2004/gpt-4o-mini-sentinel.git
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

Run the main script:

```
python auditor.py
```

Follow the on-screen prompts to navigate through the tool's functions.

## License

This project is licensed under the MIT License.

## Acknowledgments

- OpenAI for providing the GPT models used in this tool.
- Contributors and maintainers of the libraries used in this project.

Note: This tool is for educational and research purposes. Use responsibly and in compliance with applicable laws and regulations. (We're not responsible for your shenanigans. Use responsibly.)