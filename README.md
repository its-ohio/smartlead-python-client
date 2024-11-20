# Smartlead Python Client

Python client for interacting with [Smartlead](https://www.smartlead.ai/) platform. 
API documentation can be found [here](https://help.smartlead.ai/API-Documentation-a0d223bdd3154a77b3735497aad9419f).

## Example Usage

```python
import os

from smartlead.client import SmartleadClient


client = SmartleadClient(api_key=os.getenv("SMARTLEAD_API_KEY"))


client.fetch_all_clients()
```
Example output:
```json
[
  {
    "id": 3286, 
    "name": "Tech Pty", 
    "email": "john@tech.com",
    "uuid": "6187b5by-9a55-4ecb-8f91-2ed14005zb57",
    "created_at": "2023-07-12T14:19:49.846Z",
    "user_id": 199,
    "logo": "Tech",
    "logo_url": null,
    "client_permision": {
      "permission": [
        "reply_master_inbox"
      ],
      "retricted_category": []
    }
  }
]
```