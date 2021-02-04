from rdflib import Graph

def compare_graphs(a, b, ignore_predicates=[]):
    ps = set(x.toPython() for x in (a - b).predicates())
    if len(ps - set(ignore_predicates)) == 0:
        return 1.0
    return 0.0

def CC_ask_multichoice(type, inputs):
    print("CC: Is the %s one of the following?" % str(type))
    print("(Type an index of the choice or leave blank)")
    for i, inp in enumerate(inputs):
        print("\t%d) %s" % (i, str(inp)))
    resp = input()
    print()

    if resp in [str(x) for x in range(len(inputs))]:
        return int(resp)
    return None

def CC_ask_text(type):
    print("CC: What is the %s?" % str(type))
    resp = input()
    print()
    return resp

def _query_components(onto, graph):
    r = list(graph.query("""
        SELECT ?p WHERE {
            ?s <%s> ?a .
            ?c <%s> ?s .
            ?c <%s>+ ?p .
        }
    """ % (onto['raised_alert'].iri, 
        onto['has_sensor'].iri,
        onto['prev_step'].iri )))
    return [onto.search_one(iri=x[0].toPython()) for x in r]

known_malfunctions = []
def CC_find_malfunction(onto, graph):
    print("===== Start of the interaction =====")

    possible_malfunctions = []
    for state in known_malfunctions:
        g = Graph().parse(data=state['graph'], format='xml')
        if compare_graphs(graph, g, [onto['has_value'].iri]):
            possible_malfunctions.append(state)

    if len(possible_malfunctions) > 0:
        resp = CC_ask_multichoice('malfunction', [
            x['component'].get_name() + '/' + x['desc'] 
            for x in possible_malfunctions
        ])
        if resp is not None:
            return True # malfunction identified

    # Identify the malfunctioned component
    candidate_components = _query_components(onto, graph)
    resp = CC_ask_multichoice('malfunctioned component', [
        x.get_name() for x in candidate_components
    ])
    component = candidate_components[resp]

    # Get the description of malfunction
    desc = CC_ask_text('malfunction')
    
    known_malfunctions.append({
        'component': component,
        'desc': desc,
        'graph': graph.serialize()
    })

    return True