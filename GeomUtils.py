# Helper for looping over multiple geometries 
# and extracting dimensions from VGM-saved ROOT-format geometry
# Raymond Tsang, Feb 8, 2017

import csv
import itertools
import ROOT

def GetListOfGeometries(geomtext):
  lines = [s.strip() for s in geomtext.split('\n') if s.strip() != '']
  keys = []
  values = {}
  for line in lines:
    line = line.split('#')[0]       # Remove comments
    key = line.split(' ')[0]   # Name of variables
    value_csv = ' '.join([s for s in line.split(' ')[1:] if s.strip() != ''])  # Remove key
    value = list(csv.reader([value_csv], delimiter=','))[0]

    if key == "LinkDimensions":
      keys.append(value)
    else:
      values[key] = value

  # Add non-linked keys
  for k in values.keys():
    if len([1 for a in keys if k in a]) == 0: keys.append([k]) 
  flat_keys = [item for sublist in keys for item in sublist]

  # Calculate "Product" of lists of tuples, then flatten it.
  linked = []
  for k in keys:
    linked.append(zip(*[values[a] for a in k]))
  geom_list = [[item for sublist in a for item in sublist] for a in list(itertools.product(*linked))]

  # Reformat into list of "geom" objects (dicts) for easy looping
  geoms = []
  label = 1   # geoms are labelled simply by an incrementing number.
  for g in geom_list:
    geom = {}
    for a,b in zip(flat_keys,g):
      geom[a] = b
    geom['_label'] = 'Geometry'+str(label)
    label += 1
    geoms.append(geom)

  return geoms
    
def SubstituteDimensions(model,geom):
  if geom == None: return model
  for k in geom.keys():
    if k != '_label': model = model.replace('['+k+']',geom[k])
  return model

def ExtractLXeDimensions(fn):

    # Deduce from geometry in input root file
    
    # Load geometry saved by VGM
    f = ROOT.TFile(fn,'r')
    geom = f.Get('nEXOGeometry')
    
    # Deduce active volume center from inner cryostat offset
    geom.CdTop()
    nodeids = [0,0,0,0,0,1] # need a more robust way! 
    for i in nodeids:
      geom.CdDown(i)
    activeCenter = [geom.GetCurrentNode().GetMatrix().GetTranslation()[i]*10 for i in range(3)]
    #print 'Active LXe center',activeCenter
    
    # Deduce active volume radius from field ring inner radius
    fieldRingShape = geom.GetVolume('/nEXO/TPCInternals/FieldRing').GetShape()
    # field ring = (mid + inner) + outer. So inner = fieldring->left->right.
    innerRing = fieldRingShape.GetBoolNode().GetLeftShape().GetBoolNode().GetRightShape()
    activeR = (innerRing.GetR() - innerRing.GetRmax()) * 10
    #print 'ActiveR = %.2f mm' % activeR
    
    # Deduce active volume lower Z from cathode position and thickness
    geom.CdTop()
    cathodeShape = geom.GetVolume('/nEXO/TPCInternals/Cathode').GetShape()
    cathodeThickness = 2*cathodeShape.GetDz() * 10
    nodeids = [0,0,0,0,0,1,0,8,0,130] # need a more robust way! 
    for i in nodeids:
      geom.CdDown(i)
    cathodePosition = geom.GetCurrentNode().GetMatrix().GetTranslation()
    cathodeZ = cathodePosition[2] * 10
    activeZneg = cathodeZ + cathodeThickness/2.
    #print 'ActiveZ- = %.2f mm' % activeZneg
    
    # Deduce active volume upper Z from anode position and thickness
    geom.CdTop()
    anodeShape = geom.GetVolume('/nEXO/TPCInternals/Anode').GetShape()
    anodeThickness = 2*anodeShape.GetDZ() *10 
    nodeids = [0,0,0,0,0,1,0,8,0,25] # need a more robust way! 
    for i in nodeids:
      geom.CdDown(i)
    anodePosition = geom.GetCurrentNode().GetMatrix().GetTranslation()
    anodeZ = anodePosition[2] * 10
    activeZpos = anodeZ - anodeThickness/2.
    #print 'ActiveZ+ = %.2f mm' % activeZpos

    ans = {
      'LXeCenterX': activeCenter[0],
      'LXeCenterY': activeCenter[1],
      'LXeCenterZ': activeCenter[2],
      'ActiveLXeRadius': activeR,
      'ActiveLXeMinAxial': activeZneg,
      'ActiveLXeMaxAxial': activeZpos,
      'FidVolRadius': activeR - 5,
      'FidVolMinAxial': activeZneg + 15,
      'FidVolMaxAxial': activeZpos - 15,
    }

    print('Extracted LXe Dimensions',ans)

    return ans
