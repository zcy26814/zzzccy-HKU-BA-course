tree = {
    0:{'Parent':[],'Child':[1,2],'Note':'Root','Type':'D','CTG':0},
    1:{'Parent':[0],'Child':[3,4],'Note':'Develop_1','Type':'S','Cost':2,'CTG':0},
    2:{'Parent':[0],'Child':[5,6,7],'Note':'Develop_2','Type':'S','Cost':4,'CTG':0},
    3:{'Parent':[1],'Child':[8,9],'Note':'1st_passes','Type':'D','Cost':-5,'Probability':0.5,'CTG':0},
    4:{'Parent':[1],'Child':[10,11],'Note':'1st_fails','Type':'D','Cost':0,'Probability':0.5,'CTG':0},
    5:{'Parent':[2],'Child':[],'Note':'Both_pass','Type':'L','Cost':-10,'Probability':0.4,'CTG':0},
    6:{'Parent':[2],'Child':[],'Note':'One_passes','Type':'L','Cost':-5,'Probability':0.2,'CTG':0},
    7:{'Parent':[2],'Child':[],'Note':'Both_fail','Type':'L','Cost':0,'Probability':0.4,'CTG':0},
    8:{'Parent':[3],'Child':[],'Note':'Give_up_2nd','Type':'L','Cost':0,'CTG':0},
    9:{'Parent':[3],'Child':[12,13],'Note':'Develop_2nd','Type':'S','Cost':2,'CTG':0},
    10:{'Parent':[4],'Child':[],'Note':'Give_up_2nd','Type':'L','Cost':0,'CTG':0},
    11:{'Parent':[4],'Child':[14,15],'Note':'Develop_2nd','Type':'L','Cost':2,'CTG':0},
    12:{'Parent':[9],'Child':[],'Note':'2nd_passes','Type':'L','Cost':-4,'Probability':0.8,'CTG':0},
    13:{'Parent':[9],'Child':[],'Note':'2nd_fails','Type':'L','Cost':0,'Probability':0.2,'CTG':0},
    14:{'Parent':[11],'Child':[],'Note':'2nd_passes','Type':'L','Cost':-4,'Probability':0.2,'CTG':0},
    15:{'Parent':[11],'Child':[],'Note':'2nd_fails','Type':'L','Cost':0,'Probability':0.8,'CTG':0}
    }

def cost_to_go(tree, node):
    if tree[node]['Type']=='L':
        tree[node]['CTG'] = 0
    else:
        if tree[node]['Type']=='D':
            child_CCTG = []
            for i in tree[node]['Child']:
                child_CCTG.append(tree[i]['Cost'] + cost_to_go(tree, i))
            tree[node]['CTG'] = min(child_CCTG)
        else:
            E_CCTG = 0
            for i in tree[node]['Child']:
                E_CCTG = E_CCTG + tree[i]['Probability']*(tree[i]['Cost']+cost_to_go(tree, i))
            tree[node]['CTG'] = E_CCTG
    return tree[node]['CTG']

cost_to_go(tree, 0)
print(tree)
