from bs4 import BeautifulSoup


class Parser:
   def __init__(self, f):
      self._soup = BeautifulSoup(f, "html.parser")

   def parse(self):
        price = self._soup.find("meta",  property="og:price:amount")
        return (True, price.get("content")) if price else (False, 0)


