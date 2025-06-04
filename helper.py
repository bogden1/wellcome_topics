from jsonpath_ng.ext import parse as json_parse
from collections import Counter
import requests
import re

def expect_one(a_list):
  length = len(a_list)
  if length == 0:
    raise Exception('List is empty')
  if length > 1:
    raise Exception(f'List has more than one ({length}) entries')
  return a_list[0]

def get(url, params = {}):
  response = requests.get(url, params = params)
  if response.status_code != 200:
    raise Exception(f'HTTP error {response.status_code} getting {url} with {params}')
  return response

def down(number, scale):
  return scale * int(number / scale)

def up(number, scale):
  return down(number, scale) + scale

def list_by_jsonpath(jsonpath, jsonl_list):
  retval = []
  searcher = json_parse(jsonpath)
  for jsonl in jsonl_list:
    retval.extend([x.value for x in searcher.find(jsonl)])
  return retval

#Return a counter keyed on the value of query that matched the elements of jsonl_list
def count(jsonpath, jsonl_list):
  empty = 0
  counter = Counter()
  searcher = json_parse(jsonpath)
  for jsonl in jsonl_list:
    results = searcher.find(jsonl)
    if len(results) == 0:
      empty += 1
    else:
      for result in results: #we should have a list of DatumInContext
                             #this function assumes the value will be hashable, so it does not handle all queries
                             #for example, it will not work if "value" is a dict or a list
        counter[result.value] += 1
  return empty, counter

#Call counter with jsonpath and jsonl_list
#Then report on what was counted, per entry in the jsonl_list and (if different total) per hit
def dumpCount(jsonpath, jsonl_list, min_entry_proportion = 0):
  emptyCount, counter = count(jsonpath, jsonl_list)
  list_total = len(jsonl_list)
  query_total = counter.total()
  below_min = 0
  for k, v in counter.most_common():
    list_proportion = v/list_total
    if list_proportion >= min_entry_proportion:
      output = f'{v:4}/{list_total} entries ({100 * v/list_total:3.0f}%)'
      if list_total != query_total:
        output += f'; {v:4}/{query_total} hits ({100 * v/query_total:3.0f}%)'
      print(output, k)
    else:
      below_min += 1
  if emptyCount > 0 or below_min > 0:
    print() #Space things out if we need to append this stuff
  if emptyCount > 0:
    output = f'{emptyCount:4}/{list_total} entries ({100 * emptyCount/list_total:3.0f}%)'
    if list_total != query_total:
      output += f'; {emptyCount:4}/{query_total} hits ({100 * emptyCount/query_total:3.0f}%)'
    print(output, 'have no value')
  if below_min > 0:
    output = f'{below_min:4}/{list_total} entries ({100 * below_min/list_total:3.0f}%)'
    if list_total != query_total:
      output += f'; {below_min:4}/{query_total} hits ({100 * below_min/query_total:3.0f}%)'
    print(output, f'non-empty results hidden as below minimum entry proportion of {min_entry_proportion * 100:.0f}%')
