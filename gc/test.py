import gc
gc.disable()

class MyClass:
    def __init__(self, name):
        self.name = name
        print(f"Object {self.name} created.")

    def __del__(self):
        print(f"Object {self.name} deleted.")

# Create objects and then remove references
obj1 = MyClass("A")
obj2 = MyClass("B")

# Remove references
obj1 = None
obj2 = None

# Explicitly call garbage collection
collected = gc.collect()

# Output the number of objects collected
print(f"Garbage collector: collected {collected} objects.")



obj = MyClass("new")
obj.self_ref = obj  # Circular reference

# Remove external reference
obj = None

print(gc.garbage)
# Trigger garbage collection
collected = gc.collect()
print(f"Garbage collector: collected {collected} objects.")