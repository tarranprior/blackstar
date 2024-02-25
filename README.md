# Blackstar
An asynchronous and lightweight open-source intelligence tool which searches for usernames across common social networking platforms.

```
                          ______  _              _                            
             ,d8         (____  \| |            | |           _               
          ,d888" ,d       ____)  ) | _____  ____| |  _  ___ _| |_ _____  ____ 
      888888888,d88      |  __  (| |(____ |/ ___) |_/ )/___|_   _|____ |/ ___)
 =888888888888888K       | |__)  ) |/ ___ ( (___|  _ (|___ | | |_/ ___ | |    
      888888888"Y88      |______/ \_)_____|\____)_| \_|___/   \__)_____|_|    
          "Y888, "Y      
             "Y8         An open-source intelligence tool for blazing-fast
                         username enumeration.
```

## Disclaimer
This tool was made for educational purposes only.

## Prerequisites
* Python
* [Poetry](https://python-poetry.org/docs) (or the [pip](https://pypi.org/project/pip/) package management tool.)

## Installation
1. Clone the repository:
```bash
git clone https://github.com/tarranprior/blackstar
```

2. Change the directory:
```bash
cd blackstar
```

3. Install the dependencies:
```bash
# Install using Poetry:
poetry install

# Install using pip:
pip install -r requirements.txt
```

## Usage
```bash
blackstar.py [-h] [-u USERNAME] [-t TIMEOUT] [--show-all]
```

### Results.json - Example
```json
{
    "parameters": {
        "username": "example",
        "date": "01/01/2001 00:00:00",
        "total_sites": 100,
        "search_duration": "3.02s"
    },
    "results": [
        {
            "site": "9GAG",
            "url": "https://9gag.com/u/example",
            "response_status": "200 OK",
            "success": true
        },
        {
            "site": "About.me",
            "url": "https://about.me/example",
            "response_status": "404 Not Found",
            "success": false
        },
        {
            "site": "AskFM",
            "url": "https://ask.fm/example",
            "response_status": "200 OK",
            "success": true
        },
    ]
}
```

## License
This project is licensed under the [MIT](https://github.com/tarranprior/blackstar/blob/main/LICENSE) License.