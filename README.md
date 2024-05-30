# akamai-proxy

Proxy Akamai Production Requests to Staging

## Overview

Sometimes when connecting systems together it remains important to use the production Akamai urls but actually use the Akamai staging environment by only changing the proxy configuration, such as when doing mobile development.

## Installation

- Install mitmproxy

  ```
  brew install mitmproxy
  ```

- Download the akamai-proxy plugin

  ```
  curl https://raw.githubusercontent.com/jamiemoore/akamai-proxy/master/akamai-proxy.py -O
  ```

## Usage

- Determine your staging url, this works with the default naming standard.

  ```
  dig PRODUCTIONHOSTNAME | grep -m 1 -oE '[a-z.]+edgekey.net' | sed 's/edgekey/edgekey-staging/'
  ```

- Modify the config.ini to reflect your production and staging environments

- Run mitmdump using the script plugin

  ```
  mitmdump -s akamai-proxy.py
  ```

- Leave that running and open another window

- Configure your application/ browser to use a proxy, here is an example for the cli

  ```
  export ALL_PROXY=localhost:8080
  ```

- Confirm you are accessing the staging system using the production url

  ```
  curl -LIX GET 'YOURPRODUCTIONURL' | grep X-Akamai
  X-Akamai-Staging: ESSL
  ```

- You can use the SwitchyOmegaProxy chrome extension too for interactive sessions
- May need to trust the mitmproxy cert or use the insecure setting

## Development notes

- Don't allow local config.ini changes to be detected by git after adding to .gitignore

  ```
  git update-index --no-assume-unchanged config.ini
  git update-index --assume-unchanged config.ini
  ```

* Example command to create a new config file if you have the akamai cli installed.
```
 echo "[environments]" > config.ini; akamai property-manager leh -g XXXXXX -c V-XXXXXX | jq -r '.[] | (.domainPrefix) + " = " + (.domainPrefix + ".edgekey-staging.net")' >> config.ini
 ```