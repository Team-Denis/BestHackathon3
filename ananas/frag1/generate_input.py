import random

l = [str(random.randint(0, 500)) for _ in range(5000)]

print(" ".join(l))