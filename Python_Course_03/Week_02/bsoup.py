from bs4 import BeautifulSoup


html_doc = """
<!DOCTYPE html>
<html>
<body>

<h2>Text input fields</h2>

<form>
  <label for="fname">First name:</label><br>
  <input type="text" id="fname" name="fname" value="John"><br>
  <label for="lname">Last name:</label><br>
  <input class="cl1 cl2" type="text" id="lname" name="lname" value="Doe">
</form>
<p>Note that the form itself is not visible.</p>
<p>Also note that the default width of text input fields is 20 characters.</p>
</body>
</html>
"""


soup = BeautifulSoup(html_doc, 'lxml')
#print(soup.prettify())
print(soup.form)
print("contents start\n", soup.form.contents[1],  "\ncontents end\n")
print("children start\n", [tag.name for tag in soup.form.children],  "\nchildren end\n")
print("parent start\n", soup.form.parent.name,  "\nparent end\n")
print("parents start\n", [tag.name for tag in soup.form.parents],  "\nparents end\n")
print("find_parent start\n", soup.label.find_parent().name,  "\nfind_parent end\n")     # родитель с условием
print("find_parents start===========\n", soup.label.find_parents()[0],  "\nfind_parents end\n")     # список родителей с условием

print("find_next_sibling start\n", soup.label.find_next_sibling(type="text").name,  "\nfind_next_sibling end\n")    # сосед с условием
print("find_next_siblings start\n", soup.label.find_next_siblings(type="text"),  "\nfind_next_siblings end\n")      # соседи с условием
print("find_all start\n", soup.form.find_all('input', class_="cl1 cl2", type="text", id="lname", value="Doe"),  "\nfind_all end\n")      # внутри с условием

print("selector start\n", soup.select('input.cl2.cl1'),  "\nselector end\n")      # внутри с условием на классы (в любом порядке)
print("selector start\n", soup.select('input:nth-of-type(1)'),  "\nselector end\n")      # внутри с условием на порядок
print("selector start\n", soup.select('form > input'),  "\nselector end\n")      # внутри с условием на вложенность


import re

print([(i.name, i['type']) for i in soup.find_all(type=re.compile('tex.'))])
print([i for i in soup(['input', 'label'])])
