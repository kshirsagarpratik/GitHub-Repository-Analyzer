import understand
import json


def elist(udb):
    """
    This function creates a list of all the entities by uniquename
    @param udb:
    @return: List of all the entities in the understand database
    """
    try:
        list = []
        for ent in sorted(udb.ents(" ~unused"), key=lambda ent: ent.uniquename()):
            # for pref in methods_interfaces.refs("callby variable parameter ~local"):
            list.append(ent.uniquename())
        return list
    except Exception as e:
        print("Unexpected Error occured while creating list.")


def largelist(oldlist, newlist):
    """
    This function compare the size of two lists and returns the larger and smaller lists
    @param oldlist:
    @param newlist:
    @return:
    """
    try:
        if len(oldlist) > len(newlist):
            larger = oldlist
            smaller = newlist
            NB = False
        else:
            larger = newlist
            smaller = oldlist
        return (larger, smaller)
    except Exception as e:
        print("Unexpected error occured while comparing old and new lists of Entities.")


def getentitylist(entities, udb):
    """

    @param entities: list of entity uniquenames
    @param udb: the understand database
    @return: dictionary with the entity kind(method/variable) as key and number of times this entity is present in the list
    """
    entities_list = []

    ent_dict = {}
    for e in entities:
        kind = udb.lookup_uniquename(e).kindname()
        if kind in ent_dict:
            ent_dict[kind] += 1
        else:
            ent_dict.update({kind: 1})

    for key in ent_dict:
        entities_list.append({'entity_kind': key, 'frequency': ent_dict[key]})

    return entities_list


def getmodifiedmethods(new_methods, old_methods):
    """
    This function compares the two lists of methods and returns the methods whose parameters were modified as a json string
    @param new_methods: list of methods in the newer version of code
    @param old_methods: list of methods in the older version of code
    @return:
    """
    data = {'frequency': 0}
    for key in old_methods.keys():
        if key in new_methods:
            if old_methods[key].parameters() != new_methods[key].parameters():
                # print(key, old_methods[key].parameters(), new_methods[key].parameters())
                old_params = old_methods[key].refs('Define', 'Parameter')
                new_params = new_methods[key].refs('Define', 'Parameter')
                # print(len(old_params), len(new_params))
                if data['frequency'] == 0:
                    data['method'] = key
                    data['old_params'] = []
                    data['new_params'] = []
                    for param in old_params:
                        data['old_params'].append({'name': param.ent().name(), 'type': param.ent().type()})
                    for param in new_params:
                        data['new_params'].append({'name': param.ent().name(), 'type': param.ent().type()})
                data['frequency'] += 1
    return data


def generatejson(new_udb_path, old_udb_path):
    """
    This function generated the json object for the entities added, removed and modified in two version of the code
    @param new_udb_path: path to the udb file pointing to the newer version of the code
    @param old_udb_path: path to the udb file pointing to the older version of the code
    @return: the json object with the addition, deletions and modifications due to the patch
    """
    olddb = understand.open(old_udb_path)
    newdb = understand.open(new_udb_path)

    NB = True

    oldlist = elist(olddb)
    newlist = elist(newdb)

    larger, smaller = largelist(oldlist, newlist)
    # print(len(larger), len(smaller))
    # print(len(larger[0]), len(smaller[0]))
    # print(larger[1078], larger[1078]) #need to access indiviudal string list.
    exclusive_large = (set(larger) - set(smaller))
    exclusive_small = (set(smaller) - set(larger))

    if NB == True:
        added_entities = exclusive_large
        removed_entities = exclusive_small
    else:
        added_entities = exclusive_small
        removed_entities = exclusive_large

    added_entities_list = getentitylist(added_entities, newdb)
    removed_entities_list = getentitylist(removed_entities, olddb)

    old_methods_dict = dict((x.longname(), x) for x in olddb.ents("function,method,procedure ~unknown ~unresolved"))
    new_methods_dict = dict((x.longname(), x) for x in newdb.ents("function,method,procedure ~unknown ~unresolved"))

    modified_ent = getmodifiedmethods(new_methods_dict, old_methods_dict)

    print(added_entities_list)
    print(removed_entities_list)
    print(modified_ent)

    json_data = {'added': added_entities_list, 'removed': removed_entities_list, 'modified': modified_ent}

    olddb.close()
    newdb.close()

    return json.dumps(json_data)