from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# Set up proxy server details
proxy_host = "127.0.0.1"
proxy_port = 8080

# Configure Firefox options to use the proxy
firefox_options = Options()
firefox_options.set_preference("network.proxy.type", 1)
firefox_options.set_preference("network.proxy.http", proxy_host)
firefox_options.set_preference("network.proxy.http_port", proxy_port)
firefox_options.set_preference("network.proxy.ssl", proxy_host)
firefox_options.set_preference("network.proxy.ssl_port", proxy_port)
firefox_options.set_preference("network.proxy.ftp", proxy_host)
firefox_options.set_preference("network.proxy.ftp_port", proxy_port)
firefox_options.set_preference("network.proxy.socks", proxy_host)
firefox_options.set_preference("network.proxy.socks_port", proxy_port)
firefox_options.set_preference("network.proxy.no_proxies_on", "")

# Initialize the WebDriver
driver = webdriver.Firefox(options=firefox_options)

# Open a website to test the proxy
driver.get("http://www.example.com")

# ...existing code...

# Close the WebDriver
driver.quit()
