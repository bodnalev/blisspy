from blisspy import canonical_form_from_edge_list

def test_quick():
    Vnr = 5
    Vout = [0, 1, 2, 3, 4]
    Vin = [1, 2, 3, 4, 0]
    labels = []
    partition = [[0, 1, 2], [3, 4]]
    certificate = True
    
    result = canonical_form_from_edge_list(
        Vnr, Vout, Vin, labels=labels, partition=partition,
        certificate=certificate
    )

    canonical_edges, relabeling = result
    assert(canonical_edges==[(2, 0, 0), (2, 1, 0), (4, 1, 0), (4, 3, 0), (3, 0, 0)])
    assert(relabeling=={0: 0, 1: 2, 2: 1, 3: 4, 4: 3})
    print("Success!")


if __name__ == "__main__":
    test_quick()