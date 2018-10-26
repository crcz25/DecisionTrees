import fileinput
import json
import math
from pprint import pprint

VALUES = 0
INDEX = 1

class DecisionTreeNode:
  def __init__(self, name, children, ocurrence, level):
    self.name = name
    self.children = children
    self.ocurrence = ocurrence
    self.level = level

  def __str__(self):
    return "  " * self.level + self.name

def process_input():
  lines = []
  relation = None
  attributes = {}
  data = []
  reading_data = False

  for line in fileinput.input():
    
    if line[0] != '%':
      line = line.rstrip()
      if len(line):
        #raw data
        lines.append(line)

        # Process input
        if line.startswith('@relation'):
          #relations.append(line.split()[1])
          pass
        elif line.startswith('@attribute'):
          attribute_values = line.replace('{', "").replace('}', "").replace(',', "").split()[1:]
          attribute = str(attribute_values.pop(0))
          attributes[attribute] = (attribute_values, len(attributes))
          relation = attribute
        elif line.startswith('@data'):
          reading_data = True
        if reading_data:
          line = line.split(',')
          data.append(line)

  return relation, attributes, data[1:]
  
def calculateEntropy(variable, relation, attributes, data):
  counts = {}
  for arc in attributes[variable][VALUES]:
    counts[arc] = dict.fromkeys(attributes[relation][VALUES], 0)
  
  for row in data:
    valueVariable = row[attributes[variable][INDEX]]
    valueRelation = row[attributes[relation][INDEX]]
  
    #print(valueVariable, valueRelation)
    counts[valueVariable][valueRelation] += 1
  
  
  #pprint(counts)
  entropy = 0
  totalD = len(data)
  
  totals = {}
  for keyArc in counts:
    totalKey = 0
    for keyRel in counts[keyArc]:
      totalKey += counts[keyArc][keyRel]
    
    totals[keyArc] = totalKey
    
    if totalKey <= 0:
      continue
    
    arcEntropy = 0
    for keyRel in counts[keyArc]:
      if counts[keyArc][keyRel] > 0:
        d = counts[keyArc][keyRel] / totalKey
        arcEntropy += d * math.log2(d)
        
        
    totalKey /= totalD
    entropy += -(totalKey * arcEntropy)
  
  
  #print("Yeh", counts, totals)
  return (entropy, totals)
  
def generateTree(set_variables, relation, attributes, data):
  
  filteredData = []
  for row in data:
    mustAcept = True
    
    newRow = []
    for v in set_variables:
      #print(row[attributes[v][INDEX]], set_variables[v], set_variables)
      if row[attributes[v][INDEX]] != set_variables[v]:
        mustAcept = False
        break
      
    if not mustAcept:
      continue
    
    filteredData.append(row)
    
  #pprint(filteredData)
  
  unset_variables = [a for a in attributes.keys() if a not in set_variables.keys()]
  unset_variables.remove(relation)
  #print(unset_variables)
  
  entropies = {}
  minEntropy = 1e9 # Infinite value
  minEntropyKey = ""

  for unset_v in sorted(unset_variables):
    entropies[unset_v] = calculateEntropy(unset_v, relation, attributes, filteredData)

    if minEntropy > entropies[unset_v][0]:
      minEntropy = entropies[unset_v][0]
      minEntropyKey = unset_v
      
      
  uniqueRelation = filteredData[0][attributes[relation][INDEX]]
  for row in filteredData:
    if row[attributes[relation][INDEX]] != uniqueRelation:
      uniqueRelation = None
      break
  
  if uniqueRelation != None: # EPSILON
    #pprint(filteredData)
    return [DecisionTreeNode("ANSWER: " + uniqueRelation, None, len(filteredData), len(set_variables))]
  
  totalsArc = entropies[minEntropyKey][1]
  #print("TOTAL", totalsArc)
  #print(len(),minEntropy, minEntropyKey, totalsArc)
  
  ans = []
  for arc in totalsArc:
    if totalsArc[arc] > 0:
      added_variable =  set_variables.copy()
      added_variable[minEntropyKey] = arc
      
      arcName = minEntropyKey + ": " + arc
      children = generateTree(added_variable, relation, attributes, filteredData)
      
      ans.append(DecisionTreeNode(arcName, children, totalsArc[arc], len(set_variables)))
      
  #return {minEntropyKey: ans}
  
  return ans
      
      
def printTree(nodes, attributes):
  if nodes == None:
    return
  
  if len(nodes) == 1:
    print(nodes[0])
  else:
    
    nameVariable = nodes[0].name.split(':')[0]
    
    for value in attributes[nameVariable][VALUES]:
      arcName = nameVariable + ": " + value
      for node in nodes:
        if node.name == arcName:
          print(node)
          printTree(node.children, attributes)
          break

def main():
  relation, attributes, data = process_input()
  #pprint(relation)
  #pprint(attributes)
  #pprint(data)

  tree = generateTree({}, relation, attributes, data)
  
  printTree(tree, attributes)

if __name__ == '__main__':
  main()