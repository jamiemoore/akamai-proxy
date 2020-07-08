# akamai-proxy
Proxy Akamai Production Requests to Staging



## Overview

Sometimes when connecting systems together it remains important to use the production Akamai urls but actually use the Akamai staging environment by only changing the proxy configuration, such as when doing mobile development.



## Installation

* Install mitmproxy

  ```
  brew install mitmproxy
  ```

* Download the akamai-proxy plugin

  ```
  curl https://raw.githubusercontent.com/jamiemoore/akamai-proxy/master/akamai-proxy.py -O
  ```

  

## Usage

* Determine your staging url

  ```
  dig PRODUCTIONHOSTNAME | grep -m 1 -oE '[a-z.]+edgekey.net' | sed 's/edgekey/edgekey-staging/'
  ```

* Run mitmdump using the plugin, configure your production and staging hostname

  ```
  mitmdump  --no-http2 --ssl-insecure -v --set production="PRODUCTIONHOSTNAME" --set staging="STAGINGHOSTNAME" -s akamai-proxy.py
  ```

* Leave that running and open another window

* Configure your application/ browser to use a proxy, here is an example for the cli

  ```
  export ALL_PROXY=localhost:8080
  ```

* Confirm you are accessing the staging system using the production url

  ```
  curl -LIX GET 'YOURPRODUCTIONURL' | grep X-Akamai
  X-Akamai-Staging: ESSL
  ```

