import requests
from .hash import customHash

def shuffleSort(key_value_pairs, nodesMetadata, shuffle_sorted_pairs, NodeID):
    NodesCounter = len(nodesMetadata)
    for item in key_value_pairs:
        node_number = (customHash(item[0]) % NodesCounter) + 1

        if node_number == NodeID:
            if item[0] in shuffle_sorted_pairs:
                shuffle_sorted_pairs[item[0]].add(item[1])
            else:
                shuffle_sorted_pairs[item[0]] = {item[1]}
        else:
            try:
                ip_address = nodesMetadata[str(node_number)][0]
                port_no = nodesMetadata[str(node_number)][1]

                url = f'http://{ip_address}:{port_no}/api/childNode/{node_number}/getPairs'
                
                data = {"key": item[0], "value": item[1]}
                response = requests.post(url = url, json=data)

                if response.status_code == 200:
                        print(f'{item} sent to {node_number}\n')
                else:
                    print(f"Failed to send {item} to {node_number}. Status code: {response.status_code}")
            except Exception as e:
                print(f"Failed to send {item} to Node {node_number}: {e}")

    
