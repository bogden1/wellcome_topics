from jsonpath_ng.ext import parse as json_parse
import re

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
