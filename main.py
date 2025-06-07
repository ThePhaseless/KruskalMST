# Implementacja struktury zbiorów rozłącznych (Disjoint Set Union)
# do efektywnego wykrywania cykli.
class DSU:
    def __init__(self, n):
        # Każdy wierzchołek jest na początku swoim własnym rodzicem.
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, i):
        """Znajduje reprezentanta zbioru, do którego należy element i."""
        if self.parent[i] == i:
            return i
        # Kompresja ścieżki dla optymalizacji.
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """Łączy zbiory zawierające elementy i oraz j."""
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Unia według rangi dla zbalansowania drzewa.
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False


def kruskal(graph, num_vertices):
    """Główna funkcja implementująca algorytm Kruskala."""
    mst = []
    total_weight = 0

    # Krok 1: Posortuj wszystkie krawędzie według wagi w porządku rosnącym.
    # Krawędź jest reprezentowana jako (waga, wierzchołek_początkowy, wierzchołek_końcowy)
    graph.sort()

    dsu = DSU(num_vertices)

    # Krok 2: Przechodź przez posortowane krawędzie.
    for weight, u, v in graph:
        # Krok 3: Jeśli dodanie krawędzi nie tworzy cyklu, dodaj ją do MST.
        if dsu.union(u, v):
            mst.append((u, v, weight))
            total_weight += weight

    return mst, total_weight


# --- Główna część programu ---
if __name__ == "__main__":
    try:
        # Wprowadzanie danych o grafie
        num_vertices = int(input("Podaj liczbę wierzchołków w grafie: "))
        num_edges = int(input("Podaj liczbę krawędzi w grafie: "))

        graph_edges = []
        print("Podaj dane dla każdej krawędzi w formacie 'u v w'")
        print("(wierzchołek_początkowy wierzchołek_końcowy waga)")
        print(f"Wierzchołki numeruj od 0 do {num_vertices - 1}.")

        for i in range(num_edges):
            while True:
                try:
                    u, v, w = map(int, input(f"Krawędź {i + 1}: ").split())
                    if u < 0 or u >= num_vertices or v < 0 or v >= num_vertices:
                        print(
                            f"Błąd: numery wierzchołków muszą być w zakresie od 0 do {num_vertices - 1}."
                        )
                        continue
                    graph_edges.append((w, u, v))
                    break
                except ValueError:
                    print(
                        "Błąd: nieprawidłowy format. Podaj trzy liczby oddzielone spacją."
                    )

        # Wykonanie algorytmu Kruskala
        minimum_spanning_tree, total_weight = kruskal(graph_edges, num_vertices)

        # Wyświetlenie wyników
        print("\n--- Minimalne Drzewo Rozpinające (MST) ---")
        if not minimum_spanning_tree or len(minimum_spanning_tree) < num_vertices - 1:
            print("Graf jest niespójny. Nie można utworzyć MST.")
        else:
            print("Krawędzie w MST (u, v, waga):")
            for u, v, weight in minimum_spanning_tree:
                print(f"({u}, {v}, {weight})")
            print(f"\nCałkowita waga MST: {total_weight}")

    except ValueError:
        print("Błąd: Wprowadzono nieprawidłową wartość. Oczekiwano liczby całkowitej.")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
