import fileinput
import json
from pprint import pprint

def process_input():
  lines = []
  relations = []
  attributes = {}
  data = []
  s = len(lines)
  reading_data = False

  for line in fileinput.input():

    if line[0] != '%':
      line = line.rstrip()
      if len(line):
        #raw data
        lines.append(line)

        # Process input
        if line.startswith('@relation'):
          relations.append(line.split()[1])
        elif line.startswith('@attribute'):
          attribute_values = line.replace('{', "").replace('}', "").replace(',', "").split()[1:]
          attribute = str(attribute_values.pop(0))
          attributes[attribute] = attribute_values
        elif line.startswith('@data'):
          reading_data = True
        if reading_data:
          line = line.split(',')
          data.append(line)


  data = data[1:]
  #pprint(lines)
  pprint(relations)
  pprint(attributes)
  pprint(data)

def main():
  process_input()

  pass

if __name__ == '__main__':
  main()