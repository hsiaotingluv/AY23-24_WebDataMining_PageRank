import os
import re
import pickle
import glob

def construct_index():
    """
    Method to construct the indexing of all title

        Returns:
            title_to_id_dict dictionary with key as title and value as index, i.e. {"title": 1}
    """
    title = ""
    id = 0
    is_redirect_page = False
    title_to_id_dict = {}  # {"title": 1}

    for file_name in glob.glob("data/enwiki-20220901-pages-articles-multistream*.xml*"):
        with open(file_name, encoding="utf8") as origin_file:
            for line in origin_file:
                # get the title
                match_title = re.search(r"<title>([^:]*)<\/title>", line)
                if match_title:
                    title = match_title.group(1)

                # check if is redirect page
                if re.search(r"<redirect title=", line):
                    is_redirect_page = True

                # find a new page (end)
                if re.search(r"<\/page>", line):
                    if not is_redirect_page and title:
                        title_to_id_dict[title] = id
                        id += 1
                    title = ""
                    is_redirect_page = False

    print("Index constructed!")
    return title_to_id_dict


def construct_map(title_to_id_dict):
    """
    Method to construct and write into output file the mapping of all index to title, and the mapping of index to all outlink index

        Parameters:
                title_to_id_dict: a dictionary, e.g. {"title": 1}
    """
    title = ""
    id = 0
    MAX_SIZE = 100000
    block_id = 1
    is_redirect_page = False
    outlinks_id = []
    id_to_title_dict = {}  # {1: "title"}
    id_to_outlinks_id_dict = {}  # {1: [2, 3, 4]}

    for file_name in glob.glob("data/enwiki-20220901-pages-articles-multistream*.xml*"):
        with open(file_name, encoding="utf8") as origin_file:
            for line in origin_file:
                # find a new page (end)
                if re.search(r"<\/page>", line):
                    if not is_redirect_page and title:
                        id_to_title_dict[id] = title
                        id_to_outlinks_id_dict[id] = outlinks_id
                        id += 1
                        
                    title = ""
                    outlinks_id = []
                    is_redirect_page = False

                # get the title from the title
                match_title = re.search(r"<title>([^:]*)<\/title>", line)
                if match_title:
                    title = match_title.group(1)

                # check if is redirect page
                if re.search(r"<redirect title=", line):
                    is_redirect_page = True

                # get the outlinks from the page
                wiki_outlinks = re.findall(r'\[\[[^:\[\]]*\]\]', line)
                _out = []
                for link_title in wiki_outlinks:
                    link_title = link_title[2:-2]  # remove [[...]]
                    pos = link_title.find("|")
                    # extract title name until '|' 
                    if pos != -1:
                        link_title = link_title[: pos]
                    if link_title == "":
                        continue
                    # capitalise first letter
                    link_title = link_title[0].upper() + link_title[1: ]
                    # only save outlinks_id that exist in title_to_id_dict
                    if link_title in title_to_id_dict:
                        _out.append(title_to_id_dict[link_title])
                outlinks_id.extend(_out)

                # store avg MAX_SIZE items
                if id != 0 and id % MAX_SIZE == 0:
                    write_block(block_id, id_to_title_dict, id_to_outlinks_id_dict)
                    block_id += 1
                    id_to_title_dict = {}
                    id_to_outlinks_id_dict = {}

    if id % MAX_SIZE != 0:
        write_block(block_id, id_to_title_dict, id_to_outlinks_id_dict)

    print("Map constructed!")


# Stores every MAX_SIZE pieces
def write_block(block_id, id_to_title_dict, id_to_outlinks_id_dict):
    """
    Method to write content into file
    
        Parameters:
            block_id: an integer 
            id_to_title_dict: a dictionary, e.g. {1: "title"}
            id_to_outlinks_id_dict: a dictionary, e.g. {1: [2, 3, 4]}
    """
    # Create the 'block' directory if it does not exist
    if not os.path.exists('block'):
        os.makedirs('block')

    with open(f"block/id_to_title_block_{block_id}.pkl", 'wb') as file_title:
        pickle.dump(id_to_title_dict, file_title)
        print(f"{block_id} blocks of id_to_title_dict saved!")

    with open(f"block/id_to_outlinks_id_block_{block_id}.pkl", "wb") as file_outlinks_id:
        pickle.dump(id_to_outlinks_id_dict, file_outlinks_id)
        print(f"{block_id} blocks of id_to_outlinks_id_dict saved!")

title_to_id_dict = construct_index()
construct_map(title_to_id_dict)
