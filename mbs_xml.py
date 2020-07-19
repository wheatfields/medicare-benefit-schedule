# -*- coding: utf-8 -*-
"""
Created on Thu May 28 08:32:55 2020

@author: adamw
"""

import pandas as pd
import xml.etree.ElementTree as et

# Definitions of columns can be found here
# http://www.mbsonline.gov.au/internet/mbsonline/publishing.nsf/Content/DD1EE844DE6A60D0CA257CD0000A4485/$File/MOMS%20XML%20FIELD%20Descriptions%20Nov%202017.pdf
df_cols = ["MBS_XML - this initial column is used if there are multiple nodes",
            "ItemNum",
            "SubItemNum",
            "ItemStartDate",
            "ItemEndDate",
            "Category",
            "Group",
            "SubGroup",
            "SubHeading",
            "ItemType",
            "FeeType",
            "ProviderType",
            "NewItem",
            "ItemChange",
            "AnaesChange",
            "DescriptorChange",
            "FeeChange",
            "EMSNChange",
            "EMSNCap",
            "BenefitType",
            "BenefitStartDate",
            "FeeStartDate",
            "ScheduleFee",
            "Benefit75",
            "Benefit85",
            "Benefit100",
            "Basic Units",
            "EMSNStartDate",
            "EMSNEndDate",
            "EMSNFixedCapAmount",
            "EMSNPercentageCap",
            "EMSNMaximumCap",
            "EMSNDescription",
            "EMSNChangeDate",
            "DerivedFeeStartDate",
            "DerivedFee",
            "Anaes",
            "DescriptionStartDate",
            "Description",
            "QFEStartDate",
            "QFEEndDate"]


def parse_XML(xml_file, df_cols): 
    """Parse the input XML file and store the result in a pandas 
    DataFrame with the given columns. 
    
    The first element of df_cols is supposed to be the identifier 
    variable, which is an attribute of each node element in the 
    XML data; other features will be parsed from the text content 
    of each sub-element. 
    """
    
    xtree = et.parse(xml_file)
    xroot = xtree.getroot()
    rows = []
    
    for node in xroot: 
        res = []
        res.append(node.attrib.get(df_cols[0]))
        for x in df_cols[1:]: 
            if node.find(x) is not None:
              res.append(node.find(x).text)
            else:
                res.append(None)

        rows.append({df_cols[i]: res[i] 
                     for i, _ in enumerate(df_cols)})
    
    out_df = pd.DataFrame(rows, columns=df_cols)
        
    return out_df


mbs_df = parse_XML(r"C:\Users\adamw\Downloads\mbs.xml", df_cols)

mbs_df = mbs_df.drop('MBS_XML - this initial column is used if there are multiple nodes', axis = 1)



pathology = mbs_df[mbs_df.Group.isin(['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P10', 'P11',  'P12', 'P13'])]

mental_health = mbs_df[mbs_df.Group == 'M7']

short = mbs_df[mbs_df.ItemNum == '36']

