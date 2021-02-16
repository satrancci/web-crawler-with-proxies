from bs4 import BeautifulSoup

TEST_PAGE = "1362215.html"

class Parser:
   def __init__(self, f):
      self._soup = BeautifulSoup(f, "html.parser")

   def parse(self):
        price = self._soup.find("meta",  property="og:price:amount")
        return (True, price.get("content")) if price else (False, 0)


if __name__ == "__main__":
   with open(TEST_PAGE) as f:
    parser = Parser(f)
    print(parser.parse())