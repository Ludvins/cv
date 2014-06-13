#!/usr/bin/env python3
#
# Generates LaTeX, markdown, and plaintext copies of my CV.
#
# Brandon Amos <http://bamos.io>
# 2013.12.28

import re
import yaml

from bibtexparser.customization import *
from bibtexparser.bparser import BibTexParser
from datetime import date
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("tmpl"))

f = open("cv.yaml", 'r')
yaml_contents = yaml.load(f)
f.close()

def latexToMd(s):
  if isinstance(s,str):
    s = s.replace(r'\\', '\n\n')
    s = s.replace(r'\it', '')
    s = s.replace('--', '-')
    s = s.replace('``', '"')
    s = s.replace("''", '"')
    s = s.replace(r"\LaTeX", "LaTeX")
    s = s.replace(r"\#", "#")
    s = s.replace(r"\&", "&")
    s = re.sub(r'\\[hv]space\*?\{[^}]*\}', '', s)
    s = s.replace(r"*", "\*")
    s = re.sub(r'\{ *\\bf *([^\}]*)\}', r'**\1**', s)
    s = re.sub('\{([^\}]*)\}', r'\1', s)
  elif isinstance(s,dict):
    for k,v in s.items():
      s[k] = latexToMd(v)
  elif isinstance(s,list):
    for idx, item in enumerate(s):
      s[idx] = latexToMd(item)
  return s

def get_bibtex_md(p, pub_types):
  def get_author_str(authors):
    a_len = len(authors)
    if a_len == 1:
      author_str = authors[0]
    elif a_len == 2:
      author_str = authors[0] + " and " + authors[1]
    else:
      author_str = ""
      for i in range(a_len):
        author_str += authors[i]
        if i < a_len-1: author_str += ", "
        if i == a_len-2: author_str += "and "
    return author_str

  for item in p:
    new_auth_list = []
    for auth in item['author']:
      new_auth = auth.split(", ")
      new_auth = new_auth[1][0] + ". " + new_auth[0]
      new_auth_list.append(new_auth)
    item['author'] = new_auth_list

  contents = []
  gidx = 1
  for t in pub_types:
    type_content = {}
    type_content['title'] = t[1]
    filtered = filter(lambda x: x['type'] == t[0], p)
    details = ""
    for item in filtered:
      author_str = get_author_str(item['author'])
      if t[0] == "inproceedings":
        details += "[" + str(gidx) + "] " + \
          author_str + ", \"" + item['title'] + ",\" in <em>" + \
          item['booktitle'] + "</em>, " + item['year'] + "<br><br>\n"
      elif t[0] == "article":
        details += "[" + str(gidx) + "] " + \
          author_str + ", \"" + item['title'] + ",\" <em>" + \
          item['journal'] + "</em>, " + item['year'] + "<br><br>\n"
      else:
        print(t)
        raise Exception()
      gidx += 1
    type_content['details'] = details
    contents.append(type_content)

  return contents

def generate(ext):
  body = ""
  for section in yaml_contents['order']:
    if ext == "md":
      contents = latexToMd(yaml_contents[section[0]])
      name = latexToMd(section[1].title())
    elif ext == "tex":
      contents = yaml_contents[section[0]]
      name = section[1].title()

    if name == 'Publications' and ext == "md":
      with open(contents, 'r') as f:
        p = BibTexParser(f.read(), author).get_entry_list()
        pub_types = [
          ('inproceedings', 'Conference Proceedings'),
          ('article', 'Articles')
        ]
        contents = get_bibtex_md(p, pub_types)

    body += env.get_template("cv-section.tmpl." + ext).render(
      name = name,
      contents = contents
    )

  f_cv = open("gen/cv." + ext, 'w')
  f_cv.write(env.get_template("cv.tmpl." + ext).render(
    name = yaml_contents['name'],
    pdf = yaml_contents['pdf'],
    src = yaml_contents['src'],
    phone = yaml_contents['phone'],
    email = yaml_contents['email'],
    email_recaptcha = yaml_contents['email_recaptcha'],
    url = yaml_contents['url'],
    body = body,
    today = date.today().strftime("%B %d, %Y")
  ))
  f_cv.close()

generate("tex")
generate("md")
