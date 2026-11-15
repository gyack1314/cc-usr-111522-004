from .model import Period,row_period

def snapshot_at(store,name,time):
    return [row for row in store.scan(name) if row_period(row).contains(time)]

def clip(store,name,start,end):
    requested=Period(start,end);output=[]
    for row in store.scan(name):
        period=row_period(row).intersection(requested)
        if period:output.append({**row,'start':period.start,'end':period.end})
    return output

def overlap_pairs(store,left,right):
    rs=list(store.scan(right));output=[]
    for l in store.scan(left):
        for r in rs:
            common=row_period(l).intersection(row_period(r))
            if l['key'] is not None and l['key']==r['key'] and common:
                output.append({'left':l['row_id'],'right':r['row_id'],'start':common.start,'end':common.end,'multiplicity':l['multiplicity']*r['multiplicity']})
    return output

def describe(store):return {'at_5':snapshot_at(store,'enrollment',5),'overlaps':overlap_pairs(store,'enrollment','teaching')}
