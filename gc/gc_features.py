import gc
import tracemalloc

tracemalloc.start()
# feature 1:
# enable/disbale periodically auto gc.collect() 
gc.disable()
print("Is GC enabled?", gc.isenabled())  # False

gc.enable()
print("Is GC enabled?", gc.isenabled())  # True



# feature 2:
class MyClass:
    def __del__(self):
        print("Object deleted.")

# Create an object and delete the reference
obj = MyClass()
obj = None
# obj auto free by python memory manager
print(f"{gc.collect()} object collected") # therefore is colelcted 0 objects


# feature 3:
# Create a circular reference
obj = MyClass()
obj.self_ref = obj  # Circular reference
obj = None  # or del obj
# Trigger GC to clean up circular references, here gc is usefull
print(f"{gc.collect()} object collected")


# feature 4:
gc.set_debug(gc.DEBUG_LEAK)  # Enable leak detection debug mode
obj = MyClass()
del obj
# Trigger collection and observe debug logs
print(f"{gc.collect()} object collected")
gc.set_debug(0)  # Disable debug mode




# feature 5:
print("Current thresholds:", gc.get_threshold())
# Set custom thresholds
gc.set_threshold(700, 10, 10)
print("Updated thresholds:", gc.get_threshold())
