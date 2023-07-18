```bash
git clone https://github.com/chroma-core/chroma
cd chroma && docker-compose up -d --build
```

``` python
import os
from config import InitConfig
from main import OpenSourceApp

chromadb_host = "localhost"
chromadb_port = 8000

config = InitConfig(host=chromadb_host, port=chromadb_port)
elon_bot = OpenSourceApp(config)

elon_bot.add_local("pdf", "/Users/muhammedashique/Downloads/manual.pdf")
elon_bot.query("How to protect the alloy wheel ?")

```