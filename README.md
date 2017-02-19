# tiny-pyscaper
Tiny python scrapper using HTMLParser and urllib request for python 3.x.x

#### This sript is simple:

#### How to use the html parser? the html parser implement using HTMLParser class from python and then generate the python etree.

```python
html = "<html><head><title></title></head><body><h1 id="title">test</h1></body></html>"
parser = HTMLParser()
root = parser.feed(html)
parser.close()

# xpath support for etree
# minimal xpath
h1 = root.find("body/h1[@id='title']").text
print(h1)
```

#### only support python xpath etree syntax

| Syntax        | Meaning       |
| ------------- |:-------------:|
| tag      | Selects all child elements with the given tag. For example, spam selects all child elements named spam, and spam/egg selects all grandchildren named egg in all children named spam. |
| *      | Selects all child elements. For example, */egg selects all grandchildren named egg. |
| . | Selects the current node. This is mostly useful at the beginning of the path, to indicate that it’s a relative path. |
| .. | Selects the parent element. Returns None if the path attempts to reach the ancestors of the start element (the element find was called on). |
| // | Selects all subelements, on all levels beneath the current element. For example, .//egg selects all egg elements in the entire tree. |
| [@attrib] | Selects all elements that have the given attribute. |
| [@attrib='value'] | Selects all elements for which the given attribute has the given value. The value cannot contain quotes. |
| [tag] | Selects all elements that have a child named tag. Only immediate children are supported. |
| [tag='text'] | Selects all elements that have a child named tag whose complete text content, including descendants, equals the given text. |
| [position] | Selects all elements that are located at the given position. The position can be either an integer (1 is the first position), the expression last() (for the last position), or a position relative to the last position (e.g. last()-1). |

#### the example script using asosde website to retrieve sidebar menu and request search result api
Usage is simple

```bash
$python asosde.py
```

the script will result sidebar.json and searchResultExample.json
