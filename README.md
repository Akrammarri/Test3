# Sarfraz Safe (Open-Source Replacement)

This is a safe, open-source replacement for the original binary module.
It simulates a backend that your card-checking client can call.

## Quick Start

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run mock API:
```
python mock_api.py
```

3. In another terminal, point your client to local server:
```
export BASE_URL=http://127.0.0.1:5000
python stripe_cvv_api.py
```

## License
MIT License
