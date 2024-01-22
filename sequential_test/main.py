import subprocess


# import file1
# import file2
# import file3

# file1.run()

# file2.run()

# file3.run()

# Run each script in sequence
subprocess.run(['python', 'file1.py'])
subprocess.run(['python', 'sequential_test/file2.py'])
subprocess.run(['python', 'sequential_test/file3.py'])