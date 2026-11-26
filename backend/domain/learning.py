import numpy as np
from sklearn.decomposition import FastICA
from sklearn.preprocessing import StandardScaler

def calculate(data):
    matrix=[r['probes'] for r in data['baseline']]
    train,test=matrix[:-12],matrix[-12:]
    scale=StandardScaler().fit(train)
    model=FastICA(n_components=3, whiten='unit-variance', random_state=24,max_iter=1400,tol=.001)
    model.fit(scale.transform(train))
    detection=np.max(np.abs(model.transform(scale.transform(test))),axis=1)
    query=model.transform(scale.transform([data['target']['probes']]))[0]
    return {'score':round(float(max(abs(query))),4),'cutoff':round(float(np.quantile(detection,.95)),4),
            'components':query.round(4).tolist(),'baseline':len(matrix),'held_out':len(test)}
