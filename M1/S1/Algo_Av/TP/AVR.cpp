#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
using namespace std;

struct Node {
    int key;
    Node* left;
    Node* right;
    int height;   // used for AVL

    Node(int k) : key(k), left(nullptr), right(nullptr), height(1) {}
};

// ---------- Height helpers ----------
int getHeight(Node* n) {
    return n ? n->height : 0;
}

void updateHeight(Node* n) {
    if (!n) return;
    int hl = getHeight(n->left);
    int hr = getHeight(n->right);
    n->height = 1 + (hl > hr ? hl : hr);
}

// ---------- Simple BST (ABR) insertion (no balancing) ----------
Node* insertBST(Node* root, int key) {
    if (!root) return new Node(key);
    if (key < root->key)
        root->left = insertBST(root->left, key);
    else if (key > root->key)
        root->right = insertBST(root->right, key);
    // ignore duplicates
    return root;
}

// ---------- Print tree sideways (just to visualize) ----------
void printTree(Node* root, int space = 0, int indent = 5) {
    if (!root) return;
    space += indent;
    printTree(root->right, space, indent);
    cout << endl;
    for (int i = indent; i < space; i++) cout << ' ';
    cout << root->key;
    printTree(root->left, space, indent);
}

// ---------- In-order traversal : fills a vector ----------
void inorder(Node* root, vector<int>& vals) {
    if (!root) return;
    inorder(root->left, vals);
    vals.push_back(root->key);
    inorder(root->right, vals);
}

// ---------- Build AVL from sorted vector ----------
Node* buildAVLFromSorted(const vector<int>& vals, int l, int r) {
    if (l > r) return nullptr;
    int mid = (l + r) / 2;
    Node* root = new Node(vals[mid]);
    root->left  = buildAVLFromSorted(vals, l, mid - 1);
    root->right = buildAVLFromSorted(vals, mid + 1, r);
    updateHeight(root);
    return root;
}

// ---------- Convert ABR -> AVL (using a vector) ----------
Node* convertABRtoAVL(Node* abrRoot) {
    vector<int> vals;
    inorder(abrRoot, vals); // sorted keys in a vector
    return buildAVLFromSorted(vals, 0, (int)vals.size() - 1);
}

// ---------- Free memory ----------
void freeTree(Node* root) {
    if (!root) return;
    freeTree(root->left);
    freeTree(root->right);
    delete root;
}

int main() {
    srand((unsigned)time(nullptr));

    int n = 10; // number of random nodes
    Node* abrRoot = nullptr;

    cout << "Random values inserted in ABR (BST):\n";
    for (int i = 0; i < n; ++i) {
        int x = rand() % 100; // 0..99
        cout << x << " ";
        abrRoot = insertBST(abrRoot, x);
    }
    cout << "\n\nABR (BST) structure:\n";
    printTree(abrRoot);
    cout << "\n\n";

    // --- Convert ABR to AVL ---
    Node* avlRoot = convertABRtoAVL(abrRoot);

    cout << "AVL tree structure (balanced):\n";
    printTree(avlRoot);
    cout << "\n\n";

    // --- RESULT IN VECTOR (vecteur) ---
    vector<int> result;
    inorder(avlRoot, result);   // in-order of AVL into vector

    cout << "Result vector (in-order traversal of AVL):\n[ ";
    for (int v : result) {
        cout << v << " ";
    }
    cout << "]\n";

    // clean up
    freeTree(abrRoot);
    freeTree(avlRoot);

    return 0;
}
