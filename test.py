from util import generate_dataset
from qoda import QODA

if __name__ == "__main__":

    X = generate_dataset(3, 1, 0)
    outliers = QODA(X, 0.1)
    print("Outliers: " + str(outliers))