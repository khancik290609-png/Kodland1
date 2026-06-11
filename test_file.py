f = open('kodland_file.txt', "w", encoding="utf-8")
f.write("Что нибудь")
f.close()

f = open('kodland_file.txt', "r", encoding="utf-8")
print(f.read())
f.close()

with open('kodland_file.txt', 'r', encoding='utf-8') as f:
    print(f.read())