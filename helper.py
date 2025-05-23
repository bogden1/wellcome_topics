from jsonpath_ng.ext import parse as json_parse
from collections import Counter
import re

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

#return Markdown-formatted list of titles and the label identified by the jsonpath
#assumes that the entity identified by the jsonpath will have both 'label' and 'id' properties
def dump_labels(jsonl_list, jsonpath, entity_name, emphasis_re = ''):
  searcher = json_parse(jsonpath)
  output = []
  for work in jsonl_list:
    labelled_things = searcher.find(work)
    output.append(f'* {work["title"]} (id: {work["id"]}) [**{len(labelled_things)}** {entity_name}]')
    for labelled_thing in labelled_things:
      label, id = (labelled_thing.value["label"], labelled_thing.value["id"]);
      x = f'{label} (id: {id})'
      if emphasis_re and re.match(emphasis_re, label):
        output.append(f'  * **{x}**')
      else:
        output.append(f'  *   {x}')
  return output

#return the subset of jsonl_list that has an id in work_ids
def works_by_ids(jsonl_list, work_ids):
  return list(filter(lambda x: x['id'] in work_ids, jsonl_list))
