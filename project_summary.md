# Project Summary: mdata

**Goal**: A lightweight CLI tool (`mdata`) to fetch data from the Massive API, optimized for ephemeral Google Colab sessions.

## 1. Repository
- **URL**: [https://github.com/richy1996/mdata](https://github.com/richy1996/mdata)
- **Status**: Public (Safe because no secrets are in code).
- **Structure**:
    - `mdata/`: Source code (`cli.py`, `client.py`, `config.py`)
    - `setup.py`: Package configuration.

## 2. Key Features
- **Security**: Uses **Google Colab Secrets** (`MASSIVE_API_KEY`).
- **Smart Tickers**: Automatically prepends `I:` to indices (e.g., `SPX` -> `I:SPX`).
- **Output**: Saves directly to **Parquet** for easy pandas loading.
- **Flexible CLI**: Supports both positional args and flags.

## 3. Usage Cheat Sheet (Colab)

### A. Environment Setup (Run Once per Session)
Links the Colab Secret to a local config file for the CLI to see.
```python
import mdata
mdata.auth_colab()
```

### B. Installation
```python
!uv pip install massive
!uv pip install git+https://github.com/richy1996/mdata.git
# To update: !uv pip install --force-reinstall git+...
```

### C. Fetching Data
**Positional Style:**
```python
!mdata spx 20260115 20260115
```

**Flag Style:**
```python
!mdata -t spx -s 20260115 -e 20260115 -r minute -d my_data_folder
```

### D. Loading Data
```python
import pandas as pd
df = pd.read_parquet("SPX_20260115_20260115_d.parquet")
```
